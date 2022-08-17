from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
import json
import datetime
import requests
from decouple import config

from .models import CustomUser, Customer, Vendor
from .forms import *
from store.models import Product, Order, OrderItem,ShippingAddress
from .decorators import *
# Create your views here.

@method_decorator(unauthenticated_user,name='dispatch')
class CustomerSignUpView(CreateView):
    model = CustomUser
    form_class = CustomerSignUpForm
    template_name = 'accounts/customer_signup.html'

    def form_valid(self,form):
        user=form.save()
        #login(self.request,user)
        return redirect('signin')

@method_decorator(unauthenticated_user,name='dispatch')
class VendorSignUpView(CreateView):
    model = CustomUser
    form_class = VendorSignUpForm
    template_name = 'accounts/vendor_signup.html'

    def form_valid(self,form):
        user=form.save()
        #login(self.request,user)
        return redirect('signin')

@unauthenticated_user
def signInView(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        user = authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect(request.GET['next'])
    context={}
    return render(request,'accounts/signin.html')

@login_required(login_url='login')
@allowed_user(roles=['Customer'])
def customerProfileView(request):
    
    context={}
    return render(request,'accounts/customer_profile.html',context)

@login_required(login_url='login')
@allowed_user(roles=['Customer'])
def customerProfileDetailsView(request):

    customer = request.user.customer
    phone_form=CustomUserProfileForm(instance=request.user)
    form = CustomerProfileForm(instance=customer)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        phone_form=CustomUserProfileForm(request.POST,instance=request.user)
        if form.is_valid() and phone_form.is_valid():
            form.save()
            phone_form.save()
            return redirect('customer-profile-details')
    context={'form':form,'phone_form':phone_form}
    return render(request,'accounts/customer_profile_details.html',context)


@login_required(login_url='login')
@allowed_user(roles=['Customer'])
def customerProfileOrdersView(request):
    orders = Order.objects.all().filter(customer=request.user.customer)
    orderItems = OrderItem.objects.all().filter(order__customer=request.user.customer)
    context={'orderItems':orderItems,'orders':orders}
    return render(request,'accounts/customer_profile_orders.html',context)


@login_required(login_url='login')
@allowed_user(roles=['Customer'])
def customerProfileOrdersDetailsView(request,pk):
    order = Order.objects.get(id=pk)
    orderItems = OrderItem.objects.all().filter(order=order)
    context={'orderItems':orderItems,'order':order}
    return render(request,'accounts/customer_profile_orders_details.html',context)


@login_required(login_url='login')
@allowed_user(roles=['Customer'])
def customerProfileAddressView(request):
    addresses = ShippingAddress.objects.all().filter(customer=request.user.customer)
    print(addresses)
    context={'addresses':addresses}
    return render(request,'accounts/customer_profile_address.html',context)

@login_required(login_url='login')
@allowed_user(roles=['Customer'])
def customerProfilePasswordView(request):

    context={}
    return render(request,'accounts/customer_profile_password.html',context)


def signOutView(request):
    logout(request)
    return redirect(request.GET['next'])

@login_required(login_url='login')
@allowed_user(roles=['Vendor'])
def dashboardView(request):
    orders = OrderItem.objects.all().filter(order__complete=True,product__vendor=request.user.vendor)

    recentOrders = orders.order_by('-order__date')[0:5]

    print("Orders: ",orders)
    print("RECENT: ",recentOrders)
    newOrders = orders.filter(status='Processing').count()

    processingOrders = orders.filter(status = 'Processing')
    processingSales = 0
    for item in processingOrders:
        processingSales+=item.price
    context={'recentOrders':recentOrders, 'newOrders':newOrders,'processingSales':processingSales}
    return render(request,'accounts/dashboard.html',context)


@login_required(login_url='login')
@allowed_user(roles=['Vendor'])
def dashboardOrdersView(request):
    orders = OrderItem.objects.all().filter(order__complete=True,product__vendor=request.user.vendor).order_by('-order__date')

    processingOrders = orders.filter(status='Processing').count()
    shippingOrders = orders.filter(status='Shipping').count()
    deliveredOrders = orders.filter(status='Delivered').count()

    context={
        'orders':orders,
        'processingOrders':processingOrders,
        'shippingOrders':shippingOrders,
        'deliveredOrders':deliveredOrders
        }
    return render(request,'accounts/dashboard_orders.html',context)


@login_required(login_url='login')
@allowed_user(roles=['Vendor'])
def dashboardOrderDetailsView(request,pk):
    
    orderitem = OrderItem.objects.get(id=pk)
    shipping = ShippingAddress.objects.filter(order=orderitem.order)
    print(shipping[0].name)

    form = OrderForm(instance = orderitem)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=orderitem)
        print('inside POST')
        if form.is_valid():
            print('is valid')
            form.save()
            return redirect('dashboard-ordersdetails',pk=orderitem.id)

    if request.user.vendor == orderitem.product.vendor:
        context = {'orderitem':orderitem,'form':form,'shipping':shipping[0]}
    else:
        context={}
    return render(request,'accounts/dashboard_orderitemdetails.html',context)


@login_required(login_url='login')
@allowed_user(roles=['Vendor'])
def dashboardProductsView(request):
    products=[]
    products = Product.objects.filter(vendor=request.user.vendor)

    context={'products':products}
    return render(request,'accounts/dashboard_products.html',context)


#Modify the product
@login_required(login_url='login')
@allowed_user(roles=['Vendor'])
def dashboardProductsDetailsView(request,pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard-productsdetails',pk=product.id)
    context={'form':form}
    return render(request,'accounts/dashboard_productDetails.html',context)

    
@login_required(login_url='login')
@allowed_user(roles=['Vendor'])
def dashboardProductsDeleteView(request,pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard-products')
    context={'product':product}
    return render(request,'accounts/dashboard_productDelete.html',context)
        


@login_required(login_url='login')
@allowed_user(roles=['Vendor'])
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



@login_required(login_url='login')
@allowed_user(roles=['Vendor'])
def dashboardFinancesView(request):
    #Money in account
    #Money recieved
    #Total sales
    orders = OrderItem.objects.all().filter(order__complete=True,product__vendor=request.user.vendor)

    processingOrders = orders.filter(status = 'Processing')
    processingSales = 0
    for item in processingOrders:
        processingSales+=item.price

    shippingOrders = orders.filter(status = 'Shipping')
    shippingSales = 0
    for item in shippingOrders:
        shippingSales+=item.price

    deliveredOrders = orders.filter(status = 'Delivered')
    deliveredSales = 0
    for item in deliveredOrders:
        deliveredSales+=item.price



    payments= VendorPayments.objects.all().filter(vendor=request.user.vendor)
    totalPayments=0
    for payment in payments:
        totalPayments+=payment.payments

    moneyInAccount = deliveredSales-totalPayments

    context={
        'processingSales':processingSales,
        'deliveredSales':deliveredSales,
        'shippingSales':shippingSales,
        'totalPayments':totalPayments,
        'moneyInAccount':moneyInAccount}
    return render(request,'accounts/dashboard_finances.html',context)



def cartView(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitems = order.orderitem_set.all()
        
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        orderitems=[]
        order = {'get_total_items':0,'get_total_price':0}

        for i in cart:
            product =  Product.objects.get(id=i)
            price = product.price * cart[i]['quantity']
            order['get_total_price']+=price
            order['get_total_items']+=cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'quantity':cart[i]['quantity'],
                'price': price,
            }
            orderitems.append(item)
    
    context = {'orderitems':orderitems, 'order':order}
    return render(request,'accounts/cart.html',context)

def checkoutView(request):
    orderPrice_paymob=0
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitems = order.orderitem_set.all()
        orderPrice_paymob+=order.get_total_price
        
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        orderitems=[]
        order = {'get_total_items':0,'get_total_price':0}

        for i in cart:
            product =  Product.objects.get(id=i)
            price = product.price * cart[i]['quantity']
            order['get_total_price']+=price
            order['get_total_items']+=cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'quantity':cart[i]['quantity'],
                'price': price,
            }
            orderitems.append(item)
        orderPrice_paymob+=order['get_total_price']
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    
    r= requests.post(
        "https://accept.paymob.com/api/auth/tokens",
        json={
            "api_key":config('PayMob_api')
        },
        headers=headers
    )
    first_token = r.json()['token']

    request_items=[]
    orderPrice = 0
    for item in orderitems:
        if type(item) is dict:
            request_items.append(
                {
                    "name": item['product']['name'],
                    "amount_cents": item['price']*100,
                    "description": item['product']['name'],
                    "quantity": item['quantity']
                }
            )
        else:
            request_items.append(
                {
                    "name": item.product.name,
                    "amount_cents": item.price*100,
                    "description": item.product.name,
                    "quantity": item.quantity
                }
            )
    if type(order) is dict:
        orderPrice+=order['get_total_price']
    else:
        orderPrice+=order.get_total_price
    
    r= requests.post("https://accept.paymob.com/api/ecommerce/orders",
    json={
        "auth_token": first_token,
        "delivery_needed": "false",
        "amount_cents": orderPrice_paymob*100,
        "currency": "EGP",
        "items": request_items,
    },
    headers=headers
    )
    order_id = r.json()['id']

    r= requests.post("https://accept.paymob.com/api/acceptance/payment_keys",
    json={
        "auth_token": first_token,
        "delivery_needed": "false",
        "amount_cents": orderPrice*100,
        "expiration": 3600,
        "order_id": order_id,
        "billing_data": {
            "apartment": "NA", 
            "email": "wolfrine97@gmail.com", 
            "floor": "NA", 
            "first_name": "Ahmed", 
            "street": "NA", 
            "building": "NA", 
            "phone_number": "01065584023", 
            "shipping_method": "NA", 
            "postal_code": "NA", 
            "city": "NA", 
            "country": "NA", 
            "last_name": "Mohamed", 
            "state": "NA"
        },
        "currency": "EGP", 
        "integration_id": 92460
    },
    headers=headers
    )
    payment_token = r.json()['token']

    context = {'orderitems':orderitems, 'order':order,'payment_token':payment_token}
    return render(request,'accounts/checkout.html',context)


#process the callback
@csrf_exempt
@require_POST
def callBack(request):
    payload = json.loads(request.body)
    print("PAYLOAD: ",payload)
    response = {
        'pending':payload['obj']['pending'],
        'success':payload['obj']['success']
    }
    return HttpResponse('Recieved callback',response)

def paymentResponse(request):
    paymentStatus = request.GET['success']
    total_price = float(request.GET['amount_cents'])/100
    print("status: ",paymentStatus," price: ",total_price)
    context={'paymentStatus':paymentStatus,'total_price':total_price}
    return render(request,'accounts/paymentResponse.html',context)

def updateItem(request):
    data = json.loads(request.body)
    prodID=data['prodID']
    action=data['action']
    prodQuant=data['prodQuant']

    customer = request.user.customer
    product = Product.objects.get(id=prodID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity= (orderItem.quantity + int(prodQuant))
    elif action == 'remove':
        orderItem.quantity= (orderItem.quantity - 1)

    orderItemPrice=product.price*orderItem.quantity
    orderItem.price = orderItemPrice
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item added', safe=False)


def processOrder(request):
    print('Data: ', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        totalPrice = float(data['userFormData']['total'])
        order.transaction_id = transaction_id

        if totalPrice == order.get_total_price:
            order.complete = True
        #Validate the order before saving it the total price
        order.save()

        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            telephone = customer.phone_number,
            name = customer.first_name +" "+customer.last_name,
            address = data['shippingData']['address'],
            city = data['shippingData']['city'],
            state = data['shippingData']['state'],

        )
    else:
        print('not logged in')
        print('COOKIES: ',request.COOKIES)
        name = data['userFormData']['name']
        email = data['userFormData']['email']

        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        orderitems=[]
        order = {'get_total_items':0,'get_total_price':0}

        for i in cart:
            product =  Product.objects.get(id=i)
            price = product.price * cart[i]['quantity']
            order['get_total_price']+=price
            order['get_total_items']+=cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'quantity':cart[i]['quantity'],
                'price': price,
            }
            orderitems.append(item)

        cookieData = {'orderitems':orderitems, 'order':order}
        items = cookieData['orderitems']

        order = Order.objects.create(
        )

        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            orderItem = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price'],
            )
        
        totalPrice = float(data['userFormData']['total'])
        order.transaction_id = transaction_id

        if totalPrice == order.get_total_price:
            order.complete = True
        order.save()

        ShippingAddress.objects.create(
            order = order,
            telephone=email,
            name = name,
            address = data['shippingData']['address'],
            city = data['shippingData']['city'],
            state = data['shippingData']['state'],

        )



    return JsonResponse('Payment Complete', safe=False)