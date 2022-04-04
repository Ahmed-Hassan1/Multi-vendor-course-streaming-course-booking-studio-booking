from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder':'password'
            })

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username','email','age')

class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model= CustomUser
        fields = ('username','email','age')