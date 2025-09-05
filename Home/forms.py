from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


#This is python form that is to register new users in the database.
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add email to save it

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')




class AgentForm(ModelForm):
    class Meta:
        model = Agent
        fields = "__all__"


                                                            