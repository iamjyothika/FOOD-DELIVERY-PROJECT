from django.urls import path
from .views import *



urlpatterns = [
    path('userregister/',UserRegister.as_view()),
    path('userlogin/',UserLogin.as_view()),
    path('bannersview/',BannersView.as_view()),
    path('allproducts/',ListingProductsView.as_view()),
    path('bannerproducts/',BannerProducts.as_view()),
    path('bigview/',BigViewProducts.as_view()),
    path('addtocart/',CartView.as_view()),
    path('update-deletecart/<int:cart_item_id>',UpdateCartItemView.as_view()),
    path('addwish/',AddWishlist.as_view())
    








]