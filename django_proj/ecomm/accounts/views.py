from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
import json
from .models import CustomUser, Customer, Vendor
from .forms import *
from store.models import Product, Order, OrderItem
# Create your views here.


class CustomerSignUpView(CreateView):
    model = CustomUser
    form_class = CustomerSignUpForm
    template_name = 'accounts/customer_signup.html'

    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        return redirect('home')

class VendorSignUpView(CreateView):
    model = CustomUser
    form_class = VendorSignUpForm
    template_name = 'accounts/vendor_signup.html'

    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        return redirect('home')

def signInView(request):
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
    return render(request,'accounts/signin.html')

def customerProfileView(request):
    customer = request.user.customer
    form = CustomerProfileForm(instance=customer)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer-profile')

    context={'form':form}
    return render(request,'accounts/customer_profile.html',context)

def signOutView(request):

    logout(request)
    return redirect('home')


def dashboardView(request):
    orders = OrderItem.objects.all().filter(product__vendor=request.user.vendor).order_by('-order__date')[0:5]
    context={'orders':orders}
    return render(request,'accounts/dashboard.html',context)

def dashboardOrdersView(request):
    orders = OrderItem.objects.all().filter(product__vendor=request.user.vendor).order_by('-order__date')
    context={'orders':orders}
    return render(request,'accounts/dashboard_orders.html',context)

def dashboardOrderDetailsView(request,pk):
    
    orderitem = OrderItem.objects.get(id=pk)
    form = OrderForm(instance = orderitem)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=orderitem)
        print('inside POST')
        if form.is_valid():
            print('is valid')
            form.save()
            return redirect('dashboard-ordersdetails',pk=orderitem.id)

    if request.user.vendor == orderitem.product.vendor:
        context = {'orderitem':orderitem,'form':form}
    else:
        context={}
    return render(request,'accounts/dashboard_orderitemdetails.html',context)

def dashboardProductsView(request):
    products=[]
    products = Product.objects.filter(vendor=request.user.vendor)

    context={'products':products}
    return render(request,'accounts/dashboard_products.html',context)



def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.save()
            return redirect('dashboard')
    else:
        form = ProductForm()

    context={'form':form}
    return render(request,'accounts/add_product.html',context)




def cartView(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitems = order.orderitem_set.all()
        print(order)
        print(orderitems)
        
    else:
        orderitems=[]
        order = {'get_total_items':0,'get_total_price':0}
    context = {'orderitems':orderitems, 'order':order}
    return render(request,'accounts/cart.html',context)

def checkoutView(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitems = order.orderitem_set.all()
        print(order)
        print(orderitems)
        
    else:
        orderitems=[]
        order = {'get_total_items':0,'get_total_price':0}
    context = {'orderitems':orderitems, 'order':order}
    return render(request,'accounts/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    prodID=data['prodID']
    action=data['action']

    customer = request.user.customer
    product = Product.objects.get(id=prodID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    orderItem.save()
    if action == 'remove':
        orderItem.delete()

    return JsonResponse('Item added', safe=False)