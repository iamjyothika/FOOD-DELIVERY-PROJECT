from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from vendorapp.models import *



# Create your models here.
class UserModel(models.Model):
    email=models.EmailField(max_length=20)
    password=models.CharField(max_length=20)
    phone_no=models.IntegerField()
    def __str__(self):
        return self.email
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'): 
            self.password = make_password(self.password)
        super(UserModel, self).save(*args, **kwargs)


class CartModel(models.Model):
    user=models.ForeignKey(UserModel, on_delete=models.CASCADE)
    product=models.ForeignKey('vendorapp.Product',on_delete=models.CASCADE)
    quantity=models.IntegerField()
    def __str__(self):
        return self.product.name

    
