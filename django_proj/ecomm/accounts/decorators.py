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
            
            if request.user.is_customer and roles[0]=='Customer':
                return view_func(request,*args, **kwargs)
            elif request.user.is_vendor and roles[0]=='Vendor':
                return view_func(request,*args, **kwargs)
            else:
                return redirect('home')

        return wrapper
    
    return decorator