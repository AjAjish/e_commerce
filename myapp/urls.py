from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='base'),
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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)