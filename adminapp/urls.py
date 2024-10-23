from django.urls import path
from .views import *

urlpatterns = [
    path('getadmindata/',getAdminData.as_view()),
    path('adminlogin/',AdminLogin.as_view()),
    path('add-getcategory/',CategoryView.as_view()),
    path('add-getbanner/',BannerCreate.as_view()),
    path('addbanner/',BannerView.as_view()),
    path('update-deletecategory/<int:pk>',CategoryDetailView.as_view()),
    path('update-deletebanner/<int:pk>',BannerDetailView.as_view()),
    path('productlist/',AllProductListView.as_view()),
    path('vendorlist/',AllVendorListView.as_view()),
    path('vendorproductdetail/<int:pk>/',VendorProductDetailView.as_view()),
    path('bannerproducts/<int:pk>/',BannerProductsView.as_view()),
    path('productvariants/',ProductVariantsView.as_view()),
    path('productvariants/<int:pk>',ProductsVariantsByID.as_view()),
    path('mainproducts/<int:pk>',BigViewById.as_view()),
    path('useradd-get/',UsersList.as_view()),
    path('userupdate-delete/',UsersDetail.as_view()),
    
   




]