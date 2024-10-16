from django.urls import path
from .views import *

urlpatterns = [
    path('add-getcategory/',CategoryView.as_view()),
    path('add-getbanner/',BannerView.as_view()),
    path('update-deletecategory/<int:pk>',CategoryDetailView.as_view()),
    path('update-deletebanner/<int:pk>',BannerDetailView.as_view())



]