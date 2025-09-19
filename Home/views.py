from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from .models import *
from django.shortcuts import redirect
from.forms import *
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users


# def home(request):
#     is_agent = False
#     if request.user.is_authenticated:
#         is_agent = request.user.groups.filter(name="Agents").exists()
#     return render(request, "index.html", {"is_agent": is_agent})


def home(request):
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')





def property_agent(request):
    agents = Agent.objects.all()  # Or filter however you want
    return render(request, 'property-agents.html', {'agents': agents})



@login_required(login_url= "login")
def agent_profile(request, agent_id):
    agent = Agent.objects.get(id=agent_id)
    all_properties = Property.objects.filter(agent=agent)
    sell_properties = all_properties.filter(selrent="Sell")
    rent_properties = all_properties.filter(selrent="Rent")
    context = {
        "agent": agent,
        "all_properties": all_properties,
        "sell_properties": sell_properties,
        "rent_properties": rent_properties
    }
    return render(request, "agent-profile.html", context)





@login_required(login_url= "login")
@allowed_users(allowed_roles=['Agents','Admin'])
def agentdb(request):
    # Get the agent instance for the logged-in user
    agent = get_object_or_404(Agent, user=request.user)

    # Fetch all properties for this agent
    properties = Property.objects.filter(agent=agent)

    # Calculate stats
    stats = {
        'total_properties': properties.count(),
        'sold_properties': properties.filter(selrent__iexact='sell').count(),
        'rented_properties': properties.filter(selrent__iexact='rent').count(),
        
    }

    context = {
        'agent': agent,
        'stats': stats,
    }

    return render(request, 'agent-db.html', context)




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
            return redirect('clientlogin')  # Redirect to login page after signup
    else:
        form = SignUpForm()
    
    return render(request, 'client-signup.html', {'form': form})



def agentsignup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_agent = form.save()  # saves new user into the Agent table

            # Add user to Agents group
            group = Group.objects.get(name='Agents')
            new_agent.groups.add(group)

            # Extract username and password from the form data
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # Authenticate and log in the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Your account has been created successfully!")
                return redirect('agentregistration')  # Redirect after signup

        else:
            # Form is invalid
            messages.error(request, "There was an error with your signup. Please try again.")

    else:
        form = SignUpForm()

    return render(request, 'agent-signup.html', {'form': form})




def agentregistration(request):
    if request.method == "POST":
        form = AgentForm(request.POST, request.FILES)  # include request.FILES for uploads
        if form.is_valid():
            agent = form.save(commit=False)  # Don't save yet
            agent.user = request.user        # Assign logged-in user
            agent.save()                     # Now save to DB

            messages.success(request, "Your registration was successful!")
            return redirect('home')
    else:
        form = AgentForm()

    return render(request, 'agent-registration.html', {'form': form})
            





@login_required(login_url= "login")
@allowed_users(allowed_roles=['Agents','Admin'])

def propertyregistration(request):
    form = PropertyForm()
    current_user = request.user
    agent = Agent.objects.get(user=current_user)   # get the Agent linked to this user
    

    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.agent = agent   # attach the logged-in user's agent
            form.save()
            messages.success(request, "Property registered successfully!")
            return redirect("listings")
        else:
            return render(request, "property-registration.html", {"form": form})
    else:
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
        properties = properties.filter(
            Q(name__icontains=keyword) |                  # property name
            Q(description__icontains=keyword) |           # description
            Q(type__name__icontains=keyword)              # type.name (FK)
        )

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

class CustomLogoutView(LogoutView):
    next_page = 'home'




class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user

        # Check if user has an associated Agent instance
        if Agent.objects.filter(user=user).exists():
            return reverse("agentdb")
        else:
            return reverse("home")
        

def manage(request):
    # Fetch properties for the logged-in agent
    properties = Property.objects.filter(agent__user=request.user)
    return render(request, 'manage.html', {'properties': properties})


def edit_property(request, pk):
    property_instance = get_object_or_404(Property, pk=pk)

    if request.method == "POST":
        form = PropertyEditForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            form.save()
            return redirect("manage")
    else:
        form = PropertyEditForm(instance=property_instance)

    return render(request, "property-edit.html", {"form": form})



def delete_property(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        prop.delete()
        return redirect('agentdb')
    return render(request, 'confirm-delete.html', {'property': prop})

def edit_agent(request, pk):
    agent = get_object_or_404(Agent, pk=pk)

    if request.method == "POST":
        form = AgentEditForm(request.POST, request.FILES, instance=agent)
        if form.is_valid():
            form.save()
            return redirect("agentdb")
    else:
        form = AgentEditForm(instance=agent)

    return render(request, "agent-edit.html", {"form": form})


def add_property_image(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)

    if request.method == "POST":
        form = PropertyAlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album_image = form.save(commit=False)
            album_image.property = property_instance
            album_image.save()
            return redirect('manage')  # Redirect to manage page
    else:
        form = PropertyAlbumForm()

    context = {
        'form': form,
        'property': property_instance
    }
    return render(request, 'add-images.html', context)



def delete_album_image(request, image_id):
    image = get_object_or_404(PropertyAlbum, id=image_id)
    property_id = image.property.id
    image.delete()
    return redirect('add_property_image', property_id=property_id)

