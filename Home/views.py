from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from.forms import *
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout


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
            new_user=form.save()  # This saves the new user to the database

            group = Group.objects.get(name='Clients')
            new_user.groups.add(group) # This adds user into clients group


             # Extract username and password from the form data
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:  # Check if user authentication is successful
                login(request, user)  # Log in the user
                return redirect('home')  # Redirect to the home page

            messages.success(request, "Your account has been created successfully!")
            return redirect('login')  # Redirect to login page after signup
    else:
        form = SignUpForm()
    
    return render(request, 'client-signup.html', {'form': form})



def agentsignup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_agent = form.save()  # saves new user into the Agent table

        group = Group.objects.get(name='Agents')
        new_agent.groups.add(group) # This adds user into agents group


        # Extract username and password from the form data
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:  # Check if user authentication is successful
                login(request, user)  # Log in the user
                return redirect('agentregistration')  # Redirect to the home page

        
        
        messages.success(request, "Your account has been created successfully!")
        return redirect('agentregistration')  # Redirect to login page after signup
    else:
        form = SignUpForm()
    
    return render(request, 'agent-signup.html', {'form': form})

# def agentsignup(request):
#     return render(request, 'agent-signup.html')

def agentregistration(request):
    if request.method == "POST":
        form = AgentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # saves directly into the Agent table

          

        messages.success(request, "Your registration was successful!")
        return redirect('home')  # redirect to home page
    else:
        form = AgentForm()

    return render(request, 'agent-registration.html', {'form': form})

# def agentregistration(request):
#     return render(request, 'agent-registration.html')

def propertyregistration(request):
    return render(request, 'property-registration.html')


def notfound(request):
    return render(request, '404.html')