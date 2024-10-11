from django.http import JsonResponse
from django.shortcuts import render,redirect
from shop.form import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json

def home(request):
    products = Product.objects.filter(trending = 1)
    return render(request,"shop/index.html",{"products":products})

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect('/')

def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.load(request)
                product_qty = data.get('product_qty')
                product_id = data.get('pid')
                product_status = Product.objects.get(id=product_id)
                if product_status:
                    if Cart.objects.filter(user=request.user.id,product_id=product_id):
                        return JsonResponse({'status':'Product Is Already in the Cart'}, status=200)
                    else:
                        if product_status.quantity>=product_qty:
                            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                            return JsonResponse({'status':'Product Added to Cart Successfully'}, status=200)
                        else:
                             return JsonResponse({'status':'Product Stock Is Not Available'}, status=200)

                # You can further validate the fields here if necessary
                print(f"Product Quantity: {product_qty}")
                print(f"Product ID: {product_id}")
                print(f"User ID: {request.user.id}")
                # Continue with logic to add product to the cart

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
                return JsonResponse({'status': 'Invalid data format'}, status=400)

            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                return JsonResponse({'status': 'Error processing request'}, status=500)
        else:
            return JsonResponse({'status': 'Login to Add cart'}, status=200)

    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)

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