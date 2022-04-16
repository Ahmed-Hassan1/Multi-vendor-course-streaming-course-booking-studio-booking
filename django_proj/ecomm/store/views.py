#Remove excess auth stuff

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Product,CarouselBanner, SubCategory, Category
from .forms import newUserForm
from .decorators import *

# Create your views here.

def homeView(request):
    products = Product.objects.all()
    banners=CarouselBanner.objects.all()
    mainCats=Category.objects.all()
    context={'products':products,'banners':banners,'mainCats':mainCats}

    return render(request,'store/home.html',context)


def instrumentView(request,pk):
    subs=Category.objects.get(name=pk)
    subCats=SubCategory.objects.all().filter(category__name=subs)
    context = {'subCats':subCats}

    return render(request,'store/instruments.html',context)

def subCatView(request,pk):
    subCat=SubCategory.objects.get(name=pk)
    products = Product.objects.filter(subCategory__name=subCat)
    print('Products:')
    print(products)
    context = {'products':products}
    print('SubCat:')
    print(subCat)
    return render(request,'store/subCat.html',context)    

def productView(request,pk):
    product=Product.objects.get(slug=pk)
    context={'product':product}
    return render(request,'store/product.html',context)

@unauthenticated_user
def registerView(request):
    form = newUserForm()
    if request.method == 'POST':
        form = newUserForm(request.POST)
        print(form.error_messages)
        if form.is_valid():
            form.save()
            return redirect('login')

    context={'form':form}
    return render(request,'store/register.html',context)

@unauthenticated_user
def logInView(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            print('SUCCESS')
            return redirect('home')
        print('Fail')
    context={}
    return render(request,'store/login.html',context)

def logOutView(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
@allowed_user(roles=['Vendor'])
def vendorDashboardView(request):

    return render(request,'store/dashboard.html')

def oudView(request):
    if request.GET.get('filter_by')=='HighToLow':
        products = Product.objects.order_by('-price')
        context={'products':products}
        return render(request,'store/ouds.html',context)

    if request.GET.get('filter_by')=='LowToHigh':
        products = Product.objects.order_by('price')
        context={'products':products}
        return render(request,'store/ouds.html',context)
    
    products = Product.objects.all()
    context={'products':products}
    return render(request,'store/ouds.html',context)


