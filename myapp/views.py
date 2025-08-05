from django.shortcuts import render , redirect
from django.contrib import messages
from . models import User,Product,Cart,Order


# Create your views here.
def base(request,userid=None):
    userid = request.session.get('userid')
    if userid:
        return render(request,'base.html',{'userid':userid})
    return render(request, 'base.html')

def home(request, userid=None):
    return render(request, 'home.html', {'userid': userid})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username:
            return render(request, 'register.html', {'username_error': 'Username is required'})
        email = request.POST.get('email')
        if not email:
            return render(request, 'register.html', {'email_error': 'Email is required'})
        password = request.POST.get('password1')
        conform_password = request.POST.get('password2')
        if password != conform_password:
            return render(request, 'register.html', {'password_error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})
        if password != conform_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        User.objects.create(username=username, email=email, password=password)
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Email: {email}, Password: {password}")
        try:
            user = User.objects.get(email=email)
            if user.password == password:  
                userid = str(user.userid)
                request.session['userid'] = userid
                messages.success(request, 'Login successful!')
                return redirect('home_with_userid',userid) 
            else:
                return render(request, 'login.html', {'error': 'Invalid email or password'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
        
    return render(request, 'login.html')

def product_page(request,userid=None):
    userid = request.session.get('userid')
    if userid:
        products = Product.objects.all()
        return render(request, 'product.html', {'userid': userid,'products': products})
    if userid is None:
        products = Product.objects.all()
        render(request, 'product.html', {'userid':None,'products': products})
    return render(request, 'product.html',{'products': products})
    
def cart(request,userid=None):
    userid = request.session.get('userid')
    if userid:
        user = User.objects.get(userid=userid)
        cart_items = Cart.objects.filter(user=user).all()
        return render(request, 'cart.html', {'userid': userid,'cart_items':cart_items})
    return render(request,'cart.html')

def logout(request):
    if 'userid' in request.session:
        del request.session['userid']
        messages.success(request, 'Logout successful!')
    return redirect('home')

def profile_view(request, userid=None):
    if userid is None:
        userid = request.session.get('userid')
    user = User.objects.get(userid=userid)
    if request.method == 'POST':
        profile_pic = request.FILES.get('image')
        if profile_pic:
            user.profile_pic = profile_pic
            user.save()
            messages.success(request, 'Profile picture updated successfully!')
        else:
            messages.error(request, 'Please upload a valid image.')
    return render(request, 'profile_view.html', {'user': user})


def add_to_cart(request, productid, userid=None):
    if request.method == 'POST':
        userid = request.session.get('userid') or userid
        if not userid:
            messages.error(request, "User Not Found.")
            return redirect('product_with_userid', userid=userid)

        try:
            user = User.objects.get(userid=userid)
            product = Product.objects.get(productid=productid)
            cart = Cart.objects.filter(user=user).first()
            if not cart:
                cart = Cart.objects.create(
                    user=user,
                    product=product,
                    cart_items={str(product.productid): {
                        "name":product.name,
                        "product_image": str(product.product_image),
                        "description" :product.description,
                        "price": int(product.price),
                        "quantity": 1
                    }}
                )
            else:
                items = cart.cart_items or {}
                pid = str(product.productid)
                if pid in items:
                    cur_price = int(items[pid]['price'])
                    items[pid]['price'] = cur_price + int(product.price)
                    items[pid]['quantity'] += 1
                else:
                    items[pid] = {
                        "name": product.name,
                        "product_image": str(product.product_image),
                        "description": product.description,
                        "price": int(product.price),
                        "quantity": 1
                    }
                cart.cart_items = items
                cart.save()

            messages.success(request, f"Product {product.name} added to cart.")

        except Exception as e:
            messages.error(request, f"Error adding product to cart: {str(e)}")

    return redirect('product_with_userid', userid=userid)

def buy_now(request):
    return render(request, 'order.html')

def remover_from_cart(request, productid, userid=None):
    if request.method == 'POST':
        userid = request.session.get('userid') or userid
        if not userid:
            messages.error(request, "User Not Found.")
            return redirect('cart_with_userid', userid=userid)

        try:
            user = User.objects.get(userid=userid)
            cart = Cart.objects.filter(user=user).first()
            if cart:
                items = cart.cart_items or {}
                pid = str(productid)
                if pid in items:
                    del items[pid]
                    cart.cart_items = items
                    cart.save()
                    messages.success(request, "Product removed from cart.")
                else:
                    messages.error(request, "Product not found in cart.")
            else:
                messages.error(request, "Cart not found.")

        except Exception as e:
            messages.error(request, f"Error removing product from cart: {str(e)}")

    return redirect('cart_with_userid', userid=userid)

def buy_all_products(request, userid=None):
    if request.method == 'POST':
        userid = request.session.get('userid') or userid
        if not userid:
            messages.error(request, "User Not Found.")
            return redirect('cart_with_userid', userid=userid)

        try:
            user = User.objects.get(userid=userid)
            cart = Cart.objects.filter(user=user).first()
            if cart and cart.cart_items:
                order_items = {}
                total_price = 0

                # Extract product quantities sent from form
                quantities = request.POST.getlist('quantities')  # won't work as-is
                quantities = request.POST.dict()
                quantity_map = {
                    k.split('[')[1].rstrip(']'): int(v)
                    for k, v in quantities.items()
                    if k.startswith('quantities[')
                }

                for productid, item in cart.cart_items.items():
                    product = Product.objects.get(productid=productid)
                    quantity = quantity_map.get(str(productid), 1)
                    price = int(product.price * quantity)

                    order_items[str(product.productid)] = {
                        "name": item['name'],
                        "product_image": item['product_image'],
                        "description": item['description'],
                        "price": price,
                        "quantity": quantity
                    }

                    total_price += price

                Order.objects.create(
                    user=user,
                    product=product,
                    order_items=order_items,
                    quantity=sum(quantity_map.values()),  # total quantity of all products
                )

                cart.cart_items.clear()
                cart.save()
                messages.success(request, "All products purchased successfully.")
            else:
                messages.error(request, "Cart is empty.")

        except Exception as e:
            messages.error(request, f"Error purchasing products: {str(e)}")

    return redirect('cart_with_userid', userid=userid)



def buy_single_product(request, productid, userid=None):
    if request.method == 'POST':
        userid = request.session.get('userid') or userid
        if not userid:
            messages.error(request, "User Not Found.")
            return redirect('product_with_userid', userid=userid)

        try:
            user = User.objects.get(userid=userid)
            product = Product.objects.get(productid=productid)
            cart = Cart.objects.filter(user=user).first()
            quantity = int(request.POST.get('quantity', 1))
            price = int(product.price * quantity)

            Order.objects.create(
                user=user,
                product=product,
                order_items={str(product.productid): {
                    "name": product.name,
                    "product_image": str(product.product_image),
                    "description": product.description,
                    "price": price,
                    "quantity": quantity
                    }
                },
                
            )
            cart.cart_items.clear()
            cart.save()
            messages.success(request, f"Product {product.name} (x{quantity}) purchased successfully.")

        except Exception as e:
            messages.error(request, f"Error purchasing product: {str(e)}")

    return redirect('product_with_userid', userid=userid)

def list_order_details(request,userid=None):
    userid = request.session.get('userid')
    if userid:
        user = User.objects.get(userid=userid)
        orders = Order.objects.filter(user=user).all()
        return render(request, 'order_details.html', {'userid': userid, 'orders': orders})