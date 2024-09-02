from django.urls import path
from .views import home, register, login_page, logout_page, cart_page,add_to_cart ,favorite,fav_page_main, favviewpage, remove_fav, remove_cart, collections, collection_detail, product_details,add_to_cart_main,fav_page_main

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login_page/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout'),
    path('cart/', cart_page, name='cart'),
    path('addtocart', add_to_cart, name='addtocart'),
    path('favorite/', favorite, name='favorite'),
    path('favviewpage', favviewpage, name='favviewpage'),
    path('remove_fav/<str:fid>', remove_fav, name='remove_fav'),
    path('remove_cart/<str:cid>', remove_cart, name='remove_cart'),
    path('collections/', collections, name='collections'),
    path('collection_detail/<str:cname>/', collection_detail, name='collection_detail'),  # Renamed to avoid conflict
    #  path('product_details/<str:id>/', product_details, name='product_details'),  # Renamed to avoid conflict
    path('product_details/<str:id>/', product_details, name='product_details'),
    path('add_to_cart_main/', add_to_cart_main, name='add_to_cart_main'),
    path('fav_page_main', fav_page_main, name='fav_page_main'),
    # other paths
    
]
