from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='base'),
    path('home/',views.home, name='home'),
    path('home/<uuid:userid>/', views.home, name='home_with_userid'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('product/', views.product, name='product'),
    path('product/<uuid:userid>/', views.product, name='product_with_userid'),
    path('cart/', views.cart, name='cart'),
    path('cart/<uuid:userid>/', views.cart, name='cart_with_userid'),
    path('logout/', views.logout, name='logout'),
    path('profile_view/<uuid:userid>/', views.profile_view, name='profile_view')
]
