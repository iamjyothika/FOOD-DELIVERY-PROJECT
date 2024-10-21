from django.contrib import admin
from .models import *
from adminapp.models import *
from vendorapp.models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Banner)
admin.site.register(Product)
admin.site.register(BannerProducts)
