from django.shortcuts import render
from .serializers import *
from rest_framework import status
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.shortcuts import get_object_or_404


# Create your views here.
class VendorCreate(APIView):
    def post(self, request):
        try:
            serializer = VendorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
class VendorLogin(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')


            vendor = Vendor.objects.filter(email = email).first()

            if  vendor and vendor.check_password(password):
                expiration_time = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
                vendor_token = {
                        'id': vendor.pk, 
                        'email': vendor.email,
                        'name':vendor.shop_name,
                        'exp': expiration_time,
                        'iat': datetime.utcnow() 
                }
                token = jwt.encode(vendor_token, settings.SECRET_KEY, algorithm='HS256')
                response = Response({"message": "Login successful","token": token,'name':vendor.shop_name,'contact':vendor.phone}, status=status.HTTP_200_OK)
                return response
            else :
                print("invalid password")
                return Response({'error': 'Invalid Email or Password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            print("Exception Error   :",e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class ProductAdd(APIView):
    def post(self, request):
        try:
            token = request.headers.get("Authorization")
            if not token:
                return Response({'error': 'Authorization token missing'}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                token = token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            
            vendor_id = decoded_data.get('id')
            if not vendor_id:
                return Response({'error': 'Vendor ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            vendor = Vendor.objects.filter(pk=vendor_id).first()
            if not vendor:
                return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                product = serializer.save(vendor=vendor)

                if product.type == "single":
                    images = request.FILES.getlist('images')  
                    print("images     :",images)

                    for image in images:
                        image_instance = SingleproductImages.objects.create(product=product, image=image)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print("Exception Error:", e)
            return Response({'error': 'An error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class ProductView(APIView):
    def get(self, request, product_id):
        try:
            token=request.headers.get('Authorization')
            if not token:
                return Response({'error': 'Authorization token missing'}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                token = token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            vendor_id = decoded_data.get('id')
            if not vendor_id:
                return Response({'error': 'Vendor ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            vendor = Vendor.objects.filter(pk=vendor_id).first()
            if not vendor:
                return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
            try:
                product = Product.objects.get(pk=product_id,vendor=vendor)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer=ProductSerializer(product)
            return Response(serializer.data,status=status.HTTP_200_OK)
            
        
        
        except Exception as e:
            print("Exception Error:", e)
            return Response({'error': 'An error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProductVariantAdd(APIView):
    def post(self,request,pk):
        try:
            token=request.headers.get("Authorization")
            if not token:
                return Response({'error': 'Authorization token missing'}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                token=token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            vendor_id=decoded_data.get('id')
            if not vendor_id:
                return Response({'error': 'Vendor ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            vendor = Vendor.objects.filter(pk=vendor_id).first()
            if not vendor:
                return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
            

            
            productid=get_object_or_404(Product,pk=pk)
            data=request.data.copy()
            data['product'] = productid.pk
            data['vendor']=vendor.pk

            if productid.type == "variant":
                product_data=ProductVariantSerializers(data=data)
                if product_data.is_valid():
                    product_ =product_data.save()
                    images=request.FILES.getlist('images')
                    for image in images:
                        image_instance = VariantProductImages.objects.create(product_variant=product_, images=image)
                    return Response(product_data.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(product_data.errors, status=status.HTTP_400_BAD_REQUEST)
                
            else :
                return Response({'error': 'Product is not a variant'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print("Exception Error:", e)
            return Response({'error': 'An error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ProductVariantView(APIView):
    def get(self, request, product_variant_id):
        try:
            token=request.headers.get('Authorization')
            if not token:
                return Response({'error': 'Authorization token missing'}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                token = token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            vendor_id = decoded_data.get('id')
            if not vendor_id:
                return Response({'error': 'Vendor ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            vendor = Vendor.objects.filter(pk=vendor_id).first()
            if not vendor:
                return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
        
            product_variant = ProductVariant.objects.filter(pk=product_variant_id).first()
            if not product_variant:
                    return Response({'error': 'Product variant not found'}, status=status.HTTP_404_NOT_FOUND)

            variant_serializer = ProductVariantSerializer(product_variant)
            return Response(variant_serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                
  

                
                 



                
            



            

        



        

            
          
















                
            
            