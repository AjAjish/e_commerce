from django.shortcuts import render , redirect
from . models import User

# Create your views here.
def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        conform_password = request.POST.get('password2')

        print(f"Username: {username}, Email: {email}, Password: {password}")
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})
        if password != conform_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        User.objects.create(username=username, email=email, password=password)
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
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Invalid email or password'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
        
    return render(request, 'login.html')

def product(request):
    return render(request, 'product.html')

def cart(request):      
    return render(request, 'cart.html')