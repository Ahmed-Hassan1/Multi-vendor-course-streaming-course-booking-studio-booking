from unicodedata import name
from django.urls import path
from . import views

urlpatterns=[
    path('signin/',views.signInView,name='signin'),
    path('signup/',views.signUpView,name='signup'),
    path('signout/',views.signOutView,name='signout'),
]