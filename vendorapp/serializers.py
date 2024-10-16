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


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'      