from .models import Category

def store_menu(request):
    menu_items = Category.objects.all()

    return {'menu_items':menu_items}