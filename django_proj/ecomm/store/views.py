from multiprocessing import context
from django.shortcuts import render
from .models import Product

# Create your views here.

def homeView(request):
    products = Product.objects.all()
    context={'products':products}
    return render(request,'store/home.html',context)

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