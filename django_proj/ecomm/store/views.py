from django.shortcuts import render
import os

from .models import Product,CarouselBanner, SubCategory, Category

# Create your views here.

#use Activate for product and is_activated for vendors in filter to show and hide
def homeView(request):
    products = Product.objects.all().filter(vendor__is_activated=True,activate=True)[:8]
    banners=CarouselBanner.objects.all()
    mainCats=Category.objects.all()
    context={'products':products,'banners':banners,'mainCats':mainCats}
    print(os.environ)
    return render(request,'store/home.html',context)


# new of each category
def newView(request):
    products = Product.objects.all().filter(vendor__is_activated=True,activate=True)[:8]

    context={'products':products}
    return render(request,'store/new_products.html',context)


def instrumentView(request,pk):
    subs=Category.objects.get(name=pk)
    subCats=SubCategory.objects.all().filter(category__name=subs)
    products= Product.objects.filter(category__name=subs)

    context = {'subCats':subCats,'products':products,'subs':subs}

    return render(request,'store/instruments.html',context)

def subCatView(request,pk):
    sorting='ترتيب حسب'
    subCat=SubCategory.objects.get(name=pk)
    subs=subCat.category   
    products = Product.objects.filter(subCategory__name=subCat) 

    if request.GET.get('filter_by')=='HighToLow':
        products = products.order_by('-price')
        sorting='السعر من الاعلى الى الاقل'

    if request.GET.get('filter_by')=='LowToHigh':
        products = products.order_by('price')
        sorting='السعر من الاقل الى الاعلى'

    if request.GET.get('filter_by')=='new':
        sorting='احدث الاضافات'
    
    context = {'products':products,'subs':subs,'subCat':subCat,'sorting':sorting}
    return render(request,'store/subCat.html',context) 

def productView(request,pk):
    product=Product.objects.get(slug=pk)
    subCat = product.subCategory
    subs = product.category
    context={'product':product,'subs':subs,'subCat':subCat}
    return render(request,'store/product.html',context)


def aboutUsView(request):

    return render(request,'store/about_us.html')