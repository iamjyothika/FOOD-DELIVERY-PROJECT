from django.db import models
from vendorapp.models import *



# Create your models here.



    


class Category(models.Model):
    category_name=models.CharField(max_length=20)
    category_image=models.ImageField(upload_to="categoryimages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.category_name
    

class Banner(models.Model):
    banner_name=models.TextField(max_length=30,null=True) 
    banner_image=models.ImageField(upload_to="bannerimages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.banner_name
    
class BannerProducts(models.Model):
    banner=models.ForeignKey(Banner,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('vendorapp.Product',on_delete=models.CASCADE,null=True) 



