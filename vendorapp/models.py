from django.db import models
from adminapp.models import *
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
class Vendor(models.Model):
    shop_name=models.CharField(max_length=20)
    phone=models.IntegerField()
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=10,null=True)
    logo=models.ImageField(upload_to="logoimages")
    def __str__(self):
        return self.shop_name
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'): 
            self.password = make_password(self.password)
        super(Vendor, self).save(*args, **kwargs)





class Product(models.Model):
    TYPE_CHOICES=[
    ('single','SINGLE'),
    ('variant','VARIANT')
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255)
    category=models.ForeignKey('adminapp.Category',on_delete=models.CASCADE,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description=models.TextField()
    type=models.CharField(max_length=20,choices=TYPE_CHOICES,default="single")
    def __str__(self):
        return self.name
    



class SingleproductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,related_name="single_images")
    image = models.ImageField(upload_to="singleproductimages")
    alt_text = models.CharField(max_length=100, null=True,blank=True)

    class Meta:
        db_table = "single_product_images"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,related_name="variants")
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    attribute=models.CharField(max_length=20)
    description=models.TextField(null=True)
    created_time=models.DateTimeField(auto_now_add=True,null=True)
    salesprice=models.DecimalField(max_digits=10,decimal_places=2,null=True)
    discount=models.DecimalField(max_digits=10,decimal_places=2,null=True)
    
    def __str__(self):
        return self.name

class VariantProductImages(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE,null=True,related_name="variant_images")
    images=models.ImageField(upload_to="variantproductimages")
    alt_text = models.CharField(max_length=100, null=True,blank=True)
    

    class Meta:
        db_table = "variant_product_images"
        









