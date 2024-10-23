from rest_framework import serializers
from .models import *
from adminapp.serializers import *
from vendorapp.serializers import *

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField()
    class Meta:
        model = UserModel
        fields = ['email', 'password', 'phone_no']  # Include necessary fields

    def create(self, validated_data):
        # Hash the password using the model's set_password method
        user = UserModel(
            email=validated_data['email'],
            phone_no=validated_data['phone_no'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Update the user's fields, including password handling
        instance.email = validated_data.get('email', instance.email)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)

        # If password is provided, hash it before saving
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance
    

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'password']  

class BannerSerializer(serializers.ModelSerializer):
    banner_products = BannerProductsSerializer(many=True, read_only=True)

    class Meta:
        model = Banner
        fields = ['id', 'banner_name', 'banner_image', 'created_at', 'updated_at', 'banner_products']  

class ProductSerializer(serializers.ModelSerializer):
    
   
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description','type','product_image']   

class SingleImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=SingleproductImages
        fields='__all__'


class ProductVariantSerializers(serializers.ModelSerializer):
    single_images=SingleImageSerializer(many=True,read_only=True)
    variant_images=ProductVariantImageSerializer(many=True,read_only=True)
    class Meta:
        model=ProductVariant
        fields=['id','name','price','stock','attribute','description','created_time','salesprice','discount','single_images','variant_images']        


class ProductSerializersssssssssss(serializers.ModelSerializer):
    single_images=SingleImageSerializer(many=True,read_only=True)
    variants=ProductVariantSerializers(many=True,read_only=True)

    class Meta:
        model=Product
        fields=['id', 'name', 'category', 'price', 'description', 'type', 'single_images','variants'] 


class CartModelSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Nested Product serializer to show product details
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = CartModel
        fields = ['id', 'user', 'product', 'product_id', 'quantity']

    def create(self, validated_data):
        user = validated_data.get('user')
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        cart_item, created = CartModel.objects.update_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity}
        )
        return cart_item 

class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Nested product details

    class Meta:
        model = WishlistModel
        fields = ['id', 'user', 'product', 'added_date']
        read_only_fields = ['user', 'added_date']                   
