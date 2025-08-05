from django.db import models
import uuid

class User(models.Model):
    userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile/', null=True, blank=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.userid} - {self.email} - {self.password}"

class Product(models.Model):
    productid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50,choices=[
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home_appliances', 'Home Appliances'),
        ('footwear', 'Footwear'),
        ('accessories', 'Accessories'),
    ])
    stock = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.productid} - {self.name} - ${self.price}"

class Cart(models.Model):
    cartid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='in_carts')
    cart_items = models.JSONField(default=dict, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Cart {self.cartid}"

class Order(models.Model):
    orderid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordered_items')
    quantity = models.IntegerField(default=1)
    order_items = models.JSONField(default=dict, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.orderid} - User {self.user.email} - Product {self.product.name} x{self.quantity} "