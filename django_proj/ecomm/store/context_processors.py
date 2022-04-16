from .models import Category,Order

def store_menu(request):
    menu_items = Category.objects.all()

    return {'menu_items':menu_items}

def cart_badge(request):
    cart_items = Order.objects.get(customer=request.user.customer)
    print(cart_items.get_total_items)

    return {'cart_items':cart_items.get_total_items}