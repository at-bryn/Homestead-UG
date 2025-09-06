from django.shortcuts import render,get_object_or_404
from .models import *
from django.shortcuts import redirect
from.forms import *
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q


def home(request):
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def testimonial(request):
    return render(request, 'testimonial.html')

# def property_list(request):
#     return render(request, 'property-list.html')

def property_agent(request):
    return render(request, 'property-agent.html')



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



def propertyregistration(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Property registered successfully!")
            return redirect("listings")  # change to your listing page URL name
    else:
        form = PropertyForm()
    
    return render(request, "property-registration.html", {"form": form})





def propertylist(request):
    all_properties = Property.objects.all().order_by('-id')
    sell_properties = Property.objects.filter(selrent__iexact="Sell").order_by('-id')
    rent_properties = Property.objects.filter(selrent__iexact="Rent").order_by('-id')

    context = {
        "all_properties": all_properties,
        "sell_properties": sell_properties,
        "rent_properties": rent_properties,
    }
    return render(request, "property-list.html", context)



def propertydetail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    return render(request, "property-detail.html", {"property": property_obj})



def properytype(request, type_id):
    # Get the type object
    property_type = get_object_or_404(Type, id=type_id)

    # Filter properties by this type
    properties = Property.objects.filter(type=property_type).order_by("-id")

    return render(request, "property-type.html", {
        "properties": properties,
        "property_type": property_type,
    })


def search(request):
    keyword = request.GET.get('keyword')
    price = request.GET.get('price')
    location = request.GET.get('location')

    properties = Property.objects.all()

    # keyword search
    if keyword:
        properties = properties.filter(title__icontains=keyword)

    # price search (single value or range, with commas handled)
    if price:
        price = price.replace(',', '')  # remove commas like 1,000 → 1000
        if '-' in price:  # range search
            try:
                min_price, max_price = price.split('-')
                min_price = int(min_price.strip())
                max_price = int(max_price.strip())
                properties = properties.filter(price__gte=min_price, price__lte=max_price)
            except ValueError:
                pass  # ignore invalid ranges
        else:  # single value (budget search)
            try:
                price_value = int(price.strip())
                properties = properties.filter(price__lte=price_value)
            except ValueError:
                pass

    # location search
    if location:
        properties = properties.filter(location__icontains=location)

    return render(request, 'searched.html', {'properties': properties})


def notfound(request):
    return render(request, '404.html')