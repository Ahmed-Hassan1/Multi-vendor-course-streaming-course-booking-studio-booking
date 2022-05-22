from dataclasses import fields
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.core.mail import send_mail
from .models import CustomUser, Customer, Vendor, VendorPayments
from store.models import Product,OrderItem



class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True,max_length=50)
    last_name = forms.CharField(required=True,max_length=50)
    phone_number = forms.CharField(max_length=20)

    class Meta(UserCreationForm.Meta):
        model = CustomUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder':'password'
            })

    def save(self):
        user = super().save(commit=False)
        user.is_customer=True
        user.save()
        customer = Customer.objects.create(customuser=user)
        customer.first_name = self.cleaned_data.get('first_name')
        customer.last_name = self.cleaned_data.get('last_name')
        customer.phone_number = self.cleaned_data.get('phone_number')
        customer.save()
        return customer.customuser

class VendorSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True,max_length=50)
    last_name = forms.CharField(required=True,max_length=50)
    company_name = forms.CharField(required=True,max_length=100)
    phone_number = forms.CharField(max_length=20)

    class Meta(UserCreationForm.Meta):
        model = CustomUser


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder':'password'
            })

    def save(self):
        user = super().save(commit=False)
        user.is_vendor=True
        user.save()
        vendor = Vendor.objects.create(customuser=user)
        vendor.first_name = self.cleaned_data.get('first_name')
        vendor.last_name = self.cleaned_data.get('last_name')
        vendor.company_name = self.cleaned_data.get('company_name')
        vendor.phone_number = self.cleaned_data.get('phone_number')
        vendor.save()
        
        #
        subject = vendor.company_name + ' is a new vendor'
        message = 'Activate the account'
        send_mail(
        subject,
        message,
        'from@Admin.com',
        ['to@example.com']
        )
        return vendor.customuser

class CustomerProfileForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['customuser']


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['vendor','slug']

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['status']


class VendorPaymentsForm(forms.ModelForm):
    class Meta:
        model = VendorPayments
        fields = '__all__'

    def clean_payments(self):
        payments=self.cleaned_data['payments']
        x=self.data['vendor']
        
        orders = OrderItem.objects.all().filter(order__complete=True,product__vendor__customuser__id=x)
        deliveredOrders = orders.filter(status = 'Delivered')
        deliveredSales = 0
        for item in deliveredOrders:
            deliveredSales+=item.price

        vendorPayments = VendorPayments.objects.all().filter(vendor__customuser__id=x)
        totalPayments=0
        for payment in vendorPayments:
            totalPayments+=payment.payments

        total = deliveredSales-totalPayments
        print('payments: ',payments,'  Sales: ',deliveredSales, '  totalPays: ',totalPayments,'  Net:',total)
        if payments > total:
            raise forms.ValidationError('The money is more then the account only has: '+ str(total))
        

        return payments

