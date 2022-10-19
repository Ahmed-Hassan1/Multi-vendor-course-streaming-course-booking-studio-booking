from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import CustomUser, Customer, Vendor, VendorPayments
from .forms import VendorPaymentsForm
# Register your models here.

class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email','first_name','last_name','phone_number','is_staff']

    # fieldsets = UserAdmin.fieldsets+( (None,{'fields':('age',)}),)
    # add_fieldsets = UserAdmin.add_fieldsets + ( (None,{'fields':('age',)}) )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','phone_number'),
        }),
    )
    ordering = ('email',)

admin.site.register(CustomUser,CustomUserAdmin)
#admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Vendor)


class VendorPaymentsAdmin(admin.ModelAdmin):
    form = VendorPaymentsForm
    list_display = ['vendor','payments']
    list_filter=('vendor',)

admin.site.register(VendorPayments,VendorPaymentsAdmin)