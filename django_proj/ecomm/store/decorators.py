from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):

    def wrapper(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        
        return view_func(request,*args, **kwargs)
    
    return wrapper

def allowed_user(roles=[]):
    def decorator(view_func):
        def wrapper(request,*args, **kwargs):
            print('working',roles)
            group=None
            if request.user.groups.exists():
                group= request.user.groups.all()[0].name
            
            if group in roles:
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponse('Not authorized')

        return wrapper
    
    return decorator