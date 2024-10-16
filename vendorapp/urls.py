from django.urls import path
from .views import *



urlpatterns = [
    path('vendor/create/',VendorCreate.as_view()),
    path('login/',VendorLogin.as_view())

    
]
