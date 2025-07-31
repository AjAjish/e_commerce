# scripts/load_products.py
import json
from myapp.models import Product
from django.core.files.base import ContentFile

with open('products.json', 'r') as f:
    data = json.load(f)

for item in data:
    product = Product(
        productid=item["productid"],
        name=item["name"],
        description=item["description"],
        price=item["price"],
        category=item["category"],
        stock=item["stock"],
    )
    if item.get("product_image"):
        product.product_image = item["product_image"]  # this assumes it's a valid path or FileField-compatible
    product.save()


# to store json data on model 
# open shell and enter----> exec(open('demo.py').read())