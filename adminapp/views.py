from django.shortcuts import render
from .serializers import *
from rest_framework import status
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from vendorapp.models import *
from userapp.models import *
from vendorapp.serializers import *
from userapp.serializers import *
from .serializers import *
from datetime import datetime, timedelta
from django.conf import settings
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.contrib.auth import get_user_model

User = get_user_model()




        


class getAdminData(APIView):
    def get(self,request):
        try :
            admin = User.objects.all()
            serializer = AdminSerializer(admin, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Exception Error   :",e)
            
        


class AdminLogin(APIView):
    def post(self, request):
        try:
            email=request.data.get('email')
            password=request.data.get('password')

            print(f"email  :{email} password  {password}")
            if  email and password is None:
                return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

            
            admin = User.objects.filter(email = email).first()
            if admin and admin.check_password(password):
                expiration_time = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
                admin_token = {
                        'id': admin.pk, 
                        'email': admin.email,
                        'name':admin.username,
                        'exp': expiration_time,
                        'iat': datetime.utcnow() 
                }
                token = jwt.encode(admin_token, settings.SECRET_KEY, algorithm='HS256')
                response = Response({"message": "Login successful","token": token,'name':admin.username}, status=status.HTTP_200_OK)
                return response
            else:
                print("invalid password")
                return Response({'error': 'Invalid Email or Password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            print("Exception Error   :",e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        




    



class CategoryView(APIView):
    def get(self,request):
        try:
            token=request.headers.get("Authorization")
            if not token:
                return Response({'error':'Token is missing'},status=status.HTTP_401_UNAUTHORIZED)
            try:
                token = token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            admin_id = decoded_data.get('id')
            if not admin_id:
                return Response({'error': 'admin ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            admin = User.objects.filter(pk=admin_id).first()
            if not admin:
                return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
            category=Category.objects.all()
            serializer=CategorySerializer(category,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self,request):
        try:
            token=request.headers.get("Authorization")
            if not token:
                return Response({'error':'Token is missing'},status=status.HTTP_401_UNAUTHORIZED)
            try:
                token = token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            admin_id = decoded_data.get('id')
            if not admin_id:
                return Response({'error': 'admin ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            admin = User.objects.filter(pk=admin_id).first()
            if not admin:
                return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer_obj=CategorySerializer(data=request.data)
            if serializer_obj.is_valid():
                serializer_obj.save()
                return Response(serializer_obj.data,status=status.HTTP_201_CREATED)
            return Response(serializer_obj.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CategoryDetailView(APIView):
           
    
    def put(self,request,pk):
        try:
            token=request.headers.get("Authorization")
            if not token:
                return Response({'error':'Token is missing'},status=status.HTTP_401_UNAUTHORIZED)
            try:
                token = token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            admin_id = decoded_data.get('id')
            if not admin_id:
                return Response({'error': 'Admin ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            admin= User.objects.filter(pk=admin_id).first()
            if not admin:
                return Response({'error': 'Vendorad not found'}, status=status.HTTP_404_NOT_FOUND)
            category=Category.objects.get(pk=pk)
            serializer_obj=CategorySerializer(category,data=request.data,partial=True)
            if serializer_obj.is_valid():
                serializer_obj.save()
                return Response(serializer_obj.data,status=status.HTTP_200_OK)
            return Response(serializer_obj.errors,status=status.HTTP_400_BAD_REQUEST) 
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def delete(self,request,pk):
        try:
            token=request.headers.get("Authorization")
            if not token:
                return Response({'error':'Token is missing'},status=status.HTTP_401_UNAUTHORIZED)
            try:
                token = token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            admin_id = decoded_data.get('id')
            if not admin_id:
                return Response({'error': 'Admin ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            admin = User.objects.filter(pk=admin_id).first()
            if not admin:
                return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
            category=Category.objects.get(pk=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)





class BannerCreate(APIView):
    def post(self,request):
        try:
            token=request.headers.get("Authorization")
            if not token:
                return Response({'error':'Token is missing'},status=status.HTTP_401_UNAUTHORIZED)
            try:
                token = token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            admin_id = decoded_data.get('id')
            if not admin_id:
                return Response({'error': 'Admin ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            admin = User.objects.filter(pk=admin_id).first()
            if not admin:
                return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer_obj=BannerSerializer(data=request.data)
            if serializer_obj.is_valid():
                serializer_obj.save()
                return Response(serializer_obj.data,status=status.HTTP_201_CREATED)
            return Response(serializer_obj.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self,request):
        try:
            
            token=request.headers.get("Authorization")
            if not token:
                return Response({'error':'Token is missing'},status=status.HTTP_401_UNAUTHORIZED)
            try:
                token = token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            admin_id = decoded_data.get('id')
            if not admin_id:
                return Response({'error': 'Admin ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            admin = User.objects.filter(pk=admin_id).first()
            if not admin:
                return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

            banner=Banner.objects.all()
            serializer=BannerSerializer(banner,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Banner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

        



        



          
class BannerView(APIView):
    def post(self, request):
        try:
            
            token=request.headers.get("Authorization")
            if not token:
                return Response({'error':'Token is missing'},status=status.HTTP_401_UNAUTHORIZED)
            try:
                token = token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            admin_id = decoded_data.get('id')
            if not admin_id:
                return Response({'error': 'Admin ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            admin = User.objects.filter(pk=admin_id).first()
            if not admin:
                return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
            banner_id = request.data.get('id')
            print(banner_id)
            if banner_id:
                check_banner = Banner.objects.filter(pk=banner_id).first()
                if check_banner:
                    products = request.data.get('products')  # Assuming this is a list of product IDs
                    if not products:  # Check if products are provided
                        return Response({'error': 'No products provided'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    for product_id in products:
                        try:
                            product = Product.objects.get(pk=product_id)  # Ensure product exists
                            BannerProducts.objects.create(banner=check_banner, product=product)  # Save BannerProducts
                        except Product.DoesNotExist:
                            return Response(
                                {'error': f'Product with id {product_id} does not exist'}, 
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    
                    return Response({'message':'Banners added for the required products'},status=status.HTTP_201_CREATED)  # Successful creation of all BannerProducts
                else:
                    return Response({'message':"Banner not found"},status=status.HTTP_404_NOT_FOUND)  # Banner not found
            else:
                return Response({'message':"No banner id is provided"},status=status.HTTP_400_BAD_REQUEST)  # No banner ID provided
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # Internal server error



  
        

class BannerDetailView(APIView):
    def put(self,request,pk):
        try:
            
            token=request.headers.get("Authorization")
            if not token:
                return Response({'error':'Token is missing'},status=status.HTTP_401_UNAUTHORIZED)
            try:
                token = token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            admin_id = decoded_data.get('id')
            if not admin_id:
                return Response({'error': 'Admin ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            admin = User.objects.filter(pk=admin_id).first()
            if not admin:
                return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
            banners=Banner.objects.get(pk=pk)
            bannerserializer=BannerSerializer(banners,data=request.data,partial=True)
            if bannerserializer.is_valid():
                bannerserializer.save()
                return Response(bannerserializer.data,status=status.HTTP_200_OK)
            return Response(bannerserializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Banner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request,pk) :
        try:
             
            token=request.headers.get("Authorization")
            if not token:
                return Response({'error':'Token is missing'},status=status.HTTP_401_UNAUTHORIZED)
            try:
                token = token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            admin_id = decoded_data.get('id')
            if not admin_id:
                return Response({'error': 'Admin ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            admin = User.objects.filter(pk=admin_id).first()
            if not admin:
                return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
            banner_data=Banner.object.get(pk=pk) 
            banner_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Banner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        
class BannerProductsView(APIView):
    
  def get(self, request, pk):
        try:
             
            token=request.headers.get("Authorization")
            if not token:
                return Response({'error':'Token is missing'},status=status.HTTP_401_UNAUTHORIZED)
            try:
                token = token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            admin_id = decoded_data.get('id')
            if not admin_id:
                return Response({'error': 'Admin ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            
            admin = User.objects.filter(pk=admin_id).first()
            if not admin:
                return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
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
        









        

            

class AllProductListView(APIView):
    def get(self,request):
        try:
            product=Product.objects.all()
            serializer=ProductSerializersssssssssss(product,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class AllVendorListView(APIView):
    def get(self,request):
        try:
            vendor=Vendor.objects.all()
            vendor_serializer=VendorSerializer(vendor,many=True)
            return Response(vendor_serializer.data,status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class VendorProductDetailView(APIView):

    def get(self,request,pk):
        try:
            vendor=Vendor.objects.get(pk=pk)
            print(vendor)
            product=Product.objects.filter(vendor=vendor)
            
            product_serializer=ProductSerializersssssssssss(product,many=True)
            return Response(product_serializer.data,status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductVariantsView(APIView):
    def get(self,request):
        try:
            product=ProductVariant.objects.all()
            serializer=ProductVariantSerializers(product,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except ProductVariant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductsVariantsByID(APIView):
    def get(self,request,pk):        #pk=product variant id
        try:
            product=ProductVariant.objects.get(pk=pk)
            serializer=ProductVariantSerializers(product)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except ProductVariant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class BigViewById(APIView):
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
        


class UsersList(APIView):
    def get(self,request):
        try:
            users=UserModel.objects.all()
            user_serializer=UserSerializer(users,many=True)
            return Response(user_serializer.data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except UserModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):
        try:
            user_serializerr=UserSerializer(data=request.data)
            if user_serializerr.is_valid():
                user_serializerr.save()
                return Response(user_serializerr.data,status=status.HTTP_201_CREATED)
            return Response(user_serializerr.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UsersDetail(APIView):
    def patch(self,request,pk):
        try:
            users=UserModel.objects.get(pk=pk)
            userserializerr_obj=UserSerializer(users,data=request.data)
            if userserializerr_obj.is_valid():
                userserializerr_obj.save()
                return Response(userserializerr_obj.data,status=status.HTTP_200_OK)
            return Response(userserializerr_obj.errors,status=status.HTTP_400_BAD_REQUEST) 
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self,request,pk):
        try:
            userrss=UserModel.objects.get(pk=pk)
            userrss.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        

        
            




        

           
               
                
                


        



            
        

        
        




        

        

  
           
          

            
        
        


       


    
       
 