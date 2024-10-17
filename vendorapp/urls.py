from django.urls import path
from .views import *



urlpatterns = [
    path('vendor/create/',VendorCreate.as_view()),
    path('login/',VendorLogin.as_view()),
    # path('productadd/',ProductAdd.as_view()),
    path('vendordata/',ProductAdd.as_view()),
    path('product/<int:product_id>',ProductView.as_view()),
    path('productvariant/<int:pk>',ProductVariantAdd.as_view()),
    path('getproductvariant/<int:product_id>',ProductVariantView.as_view())
    
    

    
]
