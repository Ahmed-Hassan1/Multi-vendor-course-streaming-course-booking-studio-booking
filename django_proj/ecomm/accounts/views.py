from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView

from .models import CustomUser, Customer, Vendor
from .forms import *

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
    print(customer)
    form = CustomerProfileForm(instance=customer)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer-profile')

    context={'form':form}
    return render(request,'accounts/customer_profile.html',context)

# def signUpView(request):
#     form = CustomUserCreationForm
    
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         print(form.error_messages)
#         if form.is_valid():
#             form.save()
#             return redirect('signin')

#     context={'form':form}
#     return render(request,'accounts/signup.html',context)


def signOutView(request):

    logout(request)
    return redirect('home')