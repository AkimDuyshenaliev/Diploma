from django import forms
from django.contrib import admin
from django.forms import ModelForm

from .models import *


### Admin panel forms

class JournalPageAdmin(admin.ModelAdmin):
    fields='__all__'
    list_display = ('first_name', 'last_name')
    form = JournalPageModel
