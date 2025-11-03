from django.http import HttpResponse
from django.shortcuts import redirect,render


def allowed_users(allowed_roles=[]):
    # Define the decorator function
    def decorate(view_func):
        # Define the wrapper function that replaces the original view function
        def wrapper_func(request, *args, **kwargs):
            # Initialize the group variable
            group = None
            
            # Check if the current user belongs to any groups
            if request.user.groups.exists():
                # Get the name of the first group the user belongs to
                group = request.user.groups.all()[0].name
            
            # Check if the user's group is allowed to access the view
            if group in allowed_roles:
                # If the user's group is allowed, call the original view function
                return view_func(request, *args, **kwargs)
            else:
                # If the user's group is not allowed, render a 403 Forbidden page
                return render(request, '403.html', {})
        
        # Return the wrapper function as the replacement for the original view function
        return wrapper_func
    
    # Return the decorator function
    return decorate
 