from django.shortcuts import render,redirect
from shop.form import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

def home(request):
    products = Product.objects.filter(trending = 1)
    return render(request,"shop/index.html",{"products":products})

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out successfully")
    return redirect('/')

def login_page(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')

        # Debug the values entered
        print(f"Entered Username: {name}")
        print(f"Entered Password: {pwd}")

        user = authenticate(request, username=name, password=pwd)
        
        if user is not None:
            print(f"Authentication successful for {user}")
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect('/')
        else:
            print("Authentication failed for these credentials")
            messages.error(request, "Invalid Username or Password")
            return redirect('/login')
    return render(request, "shop/login.html")



def register(request):
    form=CustomUserForm()
    if request.method == 'POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration success. You can Login now..!")
            return redirect('/login')
    return render(request,"shop/register.html",{'form':form})

def collections(request):
    category=Category.objects.filter(status=0)
    return render(request,"shop/collections.html",{"category":category})

def collectionsview(request,name):
    if( Category.objects.filter(name=name, status=0)):
        products = Product.objects.filter(category__name=name)
        return render(request,"shop/products/index.html",{"products":products, "category_name":name})
    else:
        messages.warning(request,"No such category found")
        return redirect('collections')

def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products = Product.objects.filter(name=pname, status=0).first()
            return render(request,"shop/products/product_details.html",{"products": products})
        else:
            messages.error(request,"No such product found")
            return redirect('collections')
    else:
        messages.error(request,"No such category found")
        return redirect('collections')