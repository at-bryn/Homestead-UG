from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from.forms import *
from django.contrib import messages

def home(request):
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def testimonial(request):
    return render(request, 'testimonial.html')

def property_list(request):
    return render(request, 'property-list.html')

def property_agent(request):
    return render(request, 'property-agent.html')

def property_type(request):
    return render(request, 'property-type.html')

def agentprofile(request):
    return render(request, 'agent-profile.html')

def clientlogin(request):
    return render(request, 'client-login.html')

def clientsignup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the new user to the database
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')  # Redirect to login page after signup
    else:
        form = SignUpForm()
    
    return render(request, 'client-signup.html', {'form': form})




def agentsignup(request):
    return render(request, 'agent-signup.html')

def agentregistration(request):
    return render(request, 'agent-registration.html')

def propertyregistration(request):
    return render(request, 'property-registration.html')


def notfound(request):
    return render(request, '404.html')