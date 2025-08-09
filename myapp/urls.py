from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='base'),
    path('base/<uuid:userid>/',views.home,name='base_with_userid'),
    path('home/',views.home, name='home'),
    path('home/<uuid:userid>/', views.home, name='home_with_userid'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('product/', views.product_page, name='product'),
    path('product/<uuid:userid>/', views.product_page, name='product_with_userid'),
    path('cart/', views.cart, name='cart'),
    path('cart/<uuid:userid>/', views.cart, name='cart_with_userid'),
    path('logout/', views.logout, name='logout'),
    path('profile_view/<uuid:userid>/', views.profile_view, name='profile_view'),
    path('add_to_cart/<uuid:userid>/<uuid:productid>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<uuid:userid>/<uuid:productid>/', views.remover_from_cart, name='remove_from_cart'),
    path('order/',views.buy_now,name='buy_now'),
    path('buy_all_products/<uuid:userid>/', views.buy_all_products, name='buy_all_products'),
    path('buy_single_product/<uuid:userid>/<uuid:productid>/', views.buy_single_product, name='buy_single_product'),
    path('order_details/<uuid:userid>/', views.list_order_details, name='list_order_details'),
    path('add_product<uuid:userid>/', views.add_product, name='add_product'),
    path('delete_product/<uuid:userid>/<uuid:productid>/', views.delete_product, name='delete_product'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)