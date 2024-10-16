from django.shortcuts import render
from .serializers import *
from rest_framework import status
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class CategoryView(APIView):
    def get(self,request):
        try:
            category=Category.objects.all()
            serializer=CategorySerializer(category,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self,request):
        try:
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
            category=Category.objects.get(pk=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)






        

        



        



          
class BannerView(APIView):
    def post(self,request):
        try:
            banner_serializer=BannerSerializer(data=request.data)
            if banner_serializer.is_valid():
                banner_serializer.save()
                return Response(banner_serializer.data,status=status.HTTP_201_CREATED)
            return Response(banner_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self,request):
        try:
            banner=Banner.objects.all()
            serializer=BannerSerializer(banner,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Banner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class BannerDetailView(APIView):
    def put(self,request,pk):
        try:
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
            banner_data=Banner.object.get(pk=pk) 
            banner_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Banner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

            

            




    
       
 