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
from userapp.models import *
from datetime import datetime, timedelta
from django.conf import settings
import jwt
import random
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string


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


            user = UserModel.objects.filter(email = email).first()

            if  user and user.check_password(password):
                expiration_time = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
                user_token = {
                        'id': user.pk, 
                        'email': user.email,
                        'contact':user.phone_no,
                        'exp': expiration_time,
                        'iat': datetime.utcnow() 
                }
                token = jwt.encode(user_token, settings.SECRET_KEY, algorithm='HS256')
                response = Response({"message": "Login successful","token": token,'name':user.email,'contact':user.phone_no}, status=status.HTTP_200_OK)
                return response
            else :
                print("invalid password")
                return Response({'error': 'Invalid Email or Password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            print("Exception Error   :",e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class BaseTokenView(APIView):
    
    def get_user_from_token(self, request):
        try:
            token=request.headers.get("Authorization")
            if not token:
                return Response({'error':'Token is missing'},status=status.HTTP_401_UNAUTHORIZED)
            try:
                token = token.split(' ')[1]
                decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except (IndexError, ExpiredSignatureError, InvalidTokenError):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
            user_id = decoded_data.get('id')
            if not user_id:
                return Response({'error': 'User ID missing in token'}, status=status.HTTP_400_BAD_REQUEST)
            user = UserModel.objects.filter(pk=user_id).first()
            if not user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            return user, None
        
        except jwt.ExpiredSignatureError:
            return None, Response({"status": "error", "message": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        
        except jwt.InvalidTokenError:
            return None, Response({"status": "error", "message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return None, Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        

import logging

logger = logging.getLogger(__name__)        


class SendOTPView(BaseTokenView):
    def post(self, request):
        try:
            email = request.data.get('email')
            print(email)
            user = UserModel.objects.filter(email=email).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            otp_instance = OTPModel.objects.filter(user=user).first()
            otp = random.randint(100000, 999999)

            if otp_instance:
                otp_instance.otp = otp
                otp_instance.save()
            else:
                OTPModel.objects.create(user=user, otp=otp)

            # Render email template with OTP value
            email_body = render_to_string('otp.html', {'otp': otp})

            # Send email
            send_mail(
                'Your OTP Code',
                '',  # Leave plain text blank if you're only sending HTML
                settings.EMAIL_HOST_USER,  
                [email],  
                fail_silently=False,
                html_message=email_body  # Sending HTML email
            )
            return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in SendOTPView: {e}")
            return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class VerifyOTPView(BaseTokenView):
    def post(self, request):
        try:
            email=request.data.get('email')
            otp=request.data.get('otp')
            if not otp and email :
                return Response({"message": "OTP not found"}, status=status.HTTP_404_NOT_FOUND)


            user = User.objects.filter(email=email).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
            valid_otp = OTPModel.objects.filter(user=user, otp=otp).first()
            if not valid_otp:
                return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "OTP verified"}, status=status.HTTP_200_OK)

                
        except Exception as e:
            print(e)
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ChangePasswordView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')
            user = User.objects.filter(email=email).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
            if new_password != confirm_password :
                return Response({"message": "Password is not match !"}, status=status.HTTP_404_NOT_FOUND)
        
            user.password = make_password(new_password)
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
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
        

class ListingProductsView(BaseTokenView):
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
        



class BannerProducts(BaseTokenView):
    
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
        
class BigViewProducts(BaseTokenView):
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
        


class CartView(BaseTokenView):
    def post(self, request):
        try:
            # Get the authenticated user from the token
            user, error_response = self.get_user_from_token(request)
            if error_response:
                return error_response

            print(f"Authenticated user: {user}")

            # Get product_id and quantity from the request data
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity')

            # Check if both product_id and quantity are provided
            if not product_id or quantity is None:
                return Response({"message": "Product ID and quantity are required."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the product already exists in the user's cart
            existing_cart_item = CartModel.objects.filter(user=user, product_id=product_id).first()
            if existing_cart_item:
                return Response({"message": "This product is already in your cart."}, status=status.HTTP_400_BAD_REQUEST)

            # Prepare data for the serializer
            cart_data = {
                'product_id': product_id,
                'quantity': quantity
            }

            # Initialize the serializer with the data and user context
            serializer = CartModelSerializer(data=cart_data, context={'request': request})
            if serializer.is_valid():
                # Save the cart item with the authenticated user
                serializer.save(user=user)
                return Response({"message": "Product added to cart successfully", "cart_item": serializer.data}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


   
        
class UpdateCartItemView(BaseTokenView):
    def put(self, request, cart_item_id):
        try:
            user, error_response = self.get_user_from_token(request)
            if error_response:
                return error_response

            # Get the existing cart item
            cart_item = CartModel.objects.get(id=cart_item_id, user=user)
            serializer = CartModelSerializer(cart_item, data=request.data, partial=True)  # Allow partial updates
            if serializer.is_valid():
                serializer.save(user=user)  # Save the updated cart item
                return Response({"message": "Cart item updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CartModel.DoesNotExist:
            return Response({"message": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND) 
        

    def delete(self, request,cart_item_id):
        try:
            user, error_response = self.get_user_from_token(request)
            if error_response:
                return error_response

            # The product ID to be removed
            cart_item = CartModel.objects.filter(user=user, pk=cart_item_id).first()

            if not cart_item:
                return Response({"message": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

         
            cart_item.delete()
            return Response({"message": "Product removed from cart successfully."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)           
        

class AddWishlist(BaseTokenView):
    def post(self, request):
        try:
            user, error_response = self.get_user_from_token(request)
            if error_response:
                return error_response
            
            product_id = request.data.get('product_id')
            if not product_id:
                return Response({'error': 'Product ID is missing'}, status=status.HTTP_400_BAD_REQUEST)
            
            wishlist_item, created = WishlistModel.objects.get_or_create(user=user, product_id=product_id)
            
            if created:
                # Use WishlistSerializer to serialize the wishlist item
                serializer = WishlistSerializer(wishlist_item)
                return Response({"message": "Product added to wishlist successfully", "wishlist": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Product is already in your wishlist"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
    

          
         
           
            
       
class Wishlistdetail(BaseTokenView):

    def delete(self,request,wishlist_id):
        
        try:
            user, error_response = self.get_user_from_token(request)
            if error_response:
                return error_response
           
            wishlist_item = WishlistModel.objects.get(user=user, pk=wishlist_id)
            wishlist_item.delete()
            return Response({"message": "Product removed from wishlist"}, status=status.HTTP_204_NO_CONTENT)
        except WishlistModel.DoesNotExist:
            return Response({"error": "Product not found in your wishlist"}, status=status.HTTP_404_NOT_FOUND)





        
            
            
            




        
            


            

    


