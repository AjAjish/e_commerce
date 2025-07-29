from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='base'),
    path('home/',views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('product/', views.product, name='product'),
    path('cart/', views.cart, name='cart')
]
