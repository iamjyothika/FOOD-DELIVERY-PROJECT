from django.shortcuts import render
from .serializers import *
from rest_framework import status
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password



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

                return Response({'token': '123456'}, status=status.HTTP_200_OK)
            else :
                print("invalid password")
                return Response({'error': 'Invalid Email or Password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            print("Exception Error   :",e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                
                
            
            