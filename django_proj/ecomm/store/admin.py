from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
# Register your models here.


class CustomProductAdmin(admin.ModelAdmin):
    list_display=['name','price','vendor','category']
    list_filter=('category','subCategory')


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product,CustomProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CarouselBanner)

