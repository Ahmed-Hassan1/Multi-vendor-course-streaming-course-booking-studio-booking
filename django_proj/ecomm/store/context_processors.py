from .models import Category,Order
import json

def store_menu(request):
    menu_items = Category.objects.all()

    return {'menu_items':menu_items}

def cart_badge(request):
    if request.user.is_authenticated and request.user.is_customer:
        try:
            cart_items = Order.objects.get(customer=request.user.customer).get_total_items
        except:
            cart_items=0
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        cart_items=0
        for i in cart:
            cart_items += cart[i]['quantity']
    print("Cart items",cart_items)

    return {'cart_items':cart_items}