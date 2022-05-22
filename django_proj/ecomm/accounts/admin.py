from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Customer, Vendor, VendorPayments
from .forms import VendorPaymentsForm
# Register your models here.

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['username','email','age','is_staff']

#     fieldsets = UserAdmin.fieldsets+( (None,{'fields':('age',)}),)
#     add_fieldsets = UserAdmin.add_fieldsets + ( (None,{'fields':('age',)}) )

# admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Vendor)


class VendorPaymentsAdmin(admin.ModelAdmin):
    form = VendorPaymentsForm
    list_display = ['vendor','payments']

admin.site.register(VendorPayments,VendorPaymentsAdmin)