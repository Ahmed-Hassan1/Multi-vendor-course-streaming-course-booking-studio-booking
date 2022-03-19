from unicodedata import name
from django.urls import path
from . import views

urlpatterns=[
    path('',views.homeView,name="home"),
    path('ouds',views.oudView,name="ouds"),
]