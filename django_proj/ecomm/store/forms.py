from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class newUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder':'name'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder':'name@example.com'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder':'password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'id': 'floatingInput',
            'placeholder':'password'
        })

    class Meta:
        model = User
        fields = ('username','email','password1','password2')