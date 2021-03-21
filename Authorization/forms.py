from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import *


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserAuthenticationForm(forms.Form):
    username = forms.CharField(max_length=25)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


