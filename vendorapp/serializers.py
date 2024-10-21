from rest_framework import serializers
from .models import *

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields='__all__'

class VendorLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields=['email','password']

 

class SingleImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=SingleproductImages
        fields='__all__'
class ProductVariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=VariantProductImages
        fields='__all__'        

class ProductSerializer(serializers.ModelSerializer):
    single_images=SingleImageSerializer(many=True,read_only=True)
    variant_images=ProductVariantImageSerializer(many=True,read_only=True)
   
    class Meta:
        model=Product
        fields=['id', 'name', 'category', 'price', 'description', 'type','product_image', 'single_images','variant_images']   



    


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductVariant
        fields=['id','name','price','stock','attribute','description', 
                  'created_time', 'salesprice', 'discount']
        extra_kwargs = {
            'description': {'required': True}, 
            'salesprice': {'required': True},
            'discount': {'required': True},
            'created_time': {'read_only': True},
        }



class ProductVariantSerializers(serializers.ModelSerializer):
    class Meta:
        model=ProductVariant
        fields='__all__'


