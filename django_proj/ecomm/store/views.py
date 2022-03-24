from multiprocessing import context
from unicodedata import category, name
from django.shortcuts import render
from .models import Product,CarouselBanner, SubCategory, Category

# Create your views here.

def homeView(request):
    products = Product.objects.all()
    banners=CarouselBanner.objects.all()
    mainCats=Category.objects.all()
    context={'products':products,'banners':banners,'mainCats':mainCats}
    print(context)
    return render(request,'store/home.html',context)

def instrumentView(request,pk):
    subs=Category.objects.get(name=pk)
    a=SubCategory.objects.all().filter(category__name=subs)
    print(subs)
    print(a)
    return render(request,'store/instruments.html')

    

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