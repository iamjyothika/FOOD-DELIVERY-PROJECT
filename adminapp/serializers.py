from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from vendorapp.serializers import *

User = get_user_model()




class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    
   
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description','type',''] 

class BannerProductsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = BannerProducts
        fields = ['id','banner','product']


class BannerSerializer(serializers.ModelSerializer):
    banner_products = BannerProductsSerializer(many=True, read_only=True)

    class Meta:
        model = Banner
        fields = ['id', 'banner_name', 'banner_image', 'created_at', 'updated_at', 'banner_products']


       





class SingleImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=SingleproductImages
        fields='__all__'



class ProductVariantImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=VariantProductImages
        fields='__all__' 



class ProductVariantSerializers(serializers.ModelSerializer):
    single_images=SingleImageSerializer(many=True,read_only=True)
    variant_images=ProductVariantImageSerializer(many=True,read_only=True)
    class Meta:
        model=ProductVariant
        fields=['id','name','price','stock','attribute','description','created_time','salesprice','discount','single_images','variant_images']

class ProductSerializer(serializers.ModelSerializer):
    
   
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description','type']         



class ProductSerializersssssssssss(serializers.ModelSerializer):
    single_images=SingleImageSerializer(many=True,read_only=True)
    variants=ProductVariantSerializers(many=True,read_only=True)

    class Meta:
        model=Product
        fields=['id', 'name', 'category', 'price', 'description', 'type', 'single_images','variants']  

class Productsss(serializers.ModelSerializer):
    single_images = SingleImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'description', 'type', 'product_image', 'single_images']
        

class ProductVariantSerializerzz(serializers.ModelSerializer):
    variant_images=ProductVariantImageSerializer(many=True,read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'price', 'stock', 'attribute', 'description', 'created_time', 'salesprice', 'discount','variant_images']

  


     


