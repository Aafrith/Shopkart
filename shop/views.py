from django.shortcuts import render
from .models import *
from django.contrib import messages

def home(request):
    return render(request,"shop/index.html")

def register(request):
    return render(request,"shop/register.html")

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

