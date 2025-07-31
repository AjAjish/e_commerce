from django.shortcuts import render , redirect
from django.contrib import messages
from . models import User,Product,Cart


# Create your views here.
def base(request):
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
    products = Product.objects.all()
    return render(request, 'product.html', {'userid': userid,'products': products})

def cart(request,userid=None):
    userid = request.session.get('userid')
    if userid:
        return render(request, 'cart.html', {'userid': userid})
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
            return messages.error(request,"User Not Found.")
        
        user = User.objects.filter(userid=userid).first()
        product = Product.objects.filter(productid=productid).first()
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()
    return redirect('cart')
