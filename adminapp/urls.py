from django.urls import path
from .views import *

urlpatterns = [
    path('getadmindata/',getAdminData.as_view()),
    # path('adminlogin/',AdminLogin.as_view()),
    path('add-getcategory/',CategoryView.as_view()),
    path('addbanner/',BannerCreate.as_view()),
    path('add-getbanner/',BannerView.as_view()),
    path('update-deletecategory/<int:pk>',CategoryDetailView.as_view()),
    path('update-deletebanner/<int:pk>',BannerDetailView.as_view()),
    # path('bannercreate/',BannerCreateAPIView.as_view()),
    path('productlist/',AllProductListView.as_view()),
    path('vendorlist/',AllVendorListView.as_view()),
    path('vendorproductdetail/<int:pk>/',VendorProductDetailView.as_view()),
    # path('bannerproducts/<int:pk>/',BannerProducts.as_view()),




]