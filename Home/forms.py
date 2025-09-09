from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Agent


#This is python form that is to register new users in the database.
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add email to save it

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class AgentEditForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['name', 'email', 'contacts', 'profilepic', 'description', 'imageID']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contacts': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = [
            'name', 
            'email', 
            'contacts', 
            'profilepic', 
            'description', 
            'imageID'
        ] 

class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = "__all__"        


                                                            