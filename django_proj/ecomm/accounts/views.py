from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm

# Create your views here.


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


def signUpView(request):
    form = CustomUserCreationForm
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(form.error_messages)
        if form.is_valid():
            form.save()
            return redirect('signin')

    context={'form':form}
    return render(request,'accounts/signup.html',context)


def signOutView(request):

    logout(request)
    return redirect('home')