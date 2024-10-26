from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from vendorapp.models import *
from django.utils import timezone
from datetime import timedelta



# Create your models here.
class UserModel(models.Model):
    email=models.EmailField(max_length=40)
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


class WishlistModel(models.Model):
    user=models.ForeignKey(UserModel, on_delete=models.CASCADE)
    product=models.ForeignKey('vendorapp.Product',on_delete=models.CASCADE)
    added_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Ensure a user cannot add the same product multiple times to the wishlist

    def __str__(self):
        return f"{self.user} - {self.product.name}"
    
class OTPModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
   

    def is_valid(self):
        # OTP is valid for 15 minutes
        expiration_time = self.created_at + timedelta(minutes=15)
        return timezone.now() <= expiration_time and not self.is_used      


    
