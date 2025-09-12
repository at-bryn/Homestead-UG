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

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = "__all__"     


class PropertyEditForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['agent']


class AgentEditForm(forms.ModelForm):
    class Meta:
        model = Agent
        exclude = ['user']   


class PropertyAlbumForm(forms.ModelForm):
    class Meta:
        model = PropertyAlbum
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }                     


                                                            