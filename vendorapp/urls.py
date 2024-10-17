from django.urls import path
from .views import *



urlpatterns = [
    path('vendor/create/',VendorCreate.as_view()),
    path('login/',VendorLogin.as_view()),
    # path('productadd/',ProductAdd.as_view()),
    path('vendordata/',ProductAdd.as_view()),
    path('product/<int:product_id>',ProductView.as_view())
    
    

    
]
