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
    descripton=models.TextField()
    type=models.CharField(max_length=20,choices=TYPE_CHOICES,default="single")
    def __str__(self):
        return self.name