from django.http import HttpResponse
from django.shortcuts import redirect,render


def allowed_users(allowed_roles=[]):
    def decorate(view_func):
        
        def wrapper_func(request, *args, **kwargs): # Define the wrapper function that replaces the original view function
            group = None
            
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
    
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, '404.html', {})
        
        return wrapper_func  # Return the wrapper function as the replacement for the original view function
    
    return decorate
 