from django.shortcuts import render

# Create your views here.
from adminapp.models import *
from vendorapp.models import *
from adminapp.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from datetime import datetime, timedelta
from django.conf import settings
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


class UserRegister(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserLogin(APIView):
    def post(self, request):
       
        try:
            email = request.data.get('email')
            password = request.data.get('password')


            user = user.objects.filter(email = email).first()

            if  user and user.check_password(password):
                expiration_time = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
                vendor_token = {
                        'id': user.pk, 
                        'email': user.email,
                        'contact':user.phone_no,
                        'exp': expiration_time,
                        'iat': datetime.utcnow() 
                }
                token = jwt.encode(vendor_token, settings.SECRET_KEY, algorithm='HS256')
                response = Response({"message": "Login successful","token": token,'name':user.email,'contact':user.phone_no}, status=status.HTTP_200_OK)
                return response
            else :
                print("invalid password")
                return Response({'error': 'Invalid Email or Password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            print("Exception Error   :",e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class BannersView(APIView):
    def get(self, request):
        try:
            banners = Banner.objects.all()
            serializer = BannerSerializer(banners, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Banner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ListingProductsView(APIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class BannerProducts(APIView):
    
  def get(self, request, pk):
        try:
            # Retrieve the banner by primary key
            banner = Banner.objects.get(pk=pk)
            print(f"Banner: {banner}")

            # Fetch all products associated with the banner
            banner_products = BannerProducts.objects.filter(banner=banner)
            
            # Prepare a list to hold serialized product data
            product_data = []

            # Serialize each product associated with the banner
            for banner_product in banner_products:
                product = banner_product.product  # Get the actual product
                product_serializer = ProductSerializersssssssssss(product)  # Serialize the product
                product_data.append(product_serializer.data)  # Append serialized data to the list

            # Return the list of serialized products
            return Response(product_data, status=status.HTTP_200_OK)

        except Banner.DoesNotExist:
            return Response({'error': 'Banner not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        
class BigViewProducts(APIView):
    def get(self,request,pk):
        try:
            prodts=Product.objects.get(pk=pk)
            print(pk)
            print(f"Product: {prodts}")
           
            product_=ProductSerializersssssssssss(prodts)
            return Response(product_.data,status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CartView(APIView):
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
            
            user_id = decoded_data.get('id')
            if not user_id:
                return Response({'error': 'Vendor ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = Vendor.objects.filter(pk=user_id).first()
            if not user:
                return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

            
            serializer = CartModelSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({"message": "Product added to cart successfully", "cart_item": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
            


            

    


