from unicodedata import name
from django.urls import path
from . import views

urlpatterns=[
    path('',views.homeView,name="home"),
    path('inst/<str:pk>/',views.instrumentView,name='instruments'),
    path('ouds',views.oudView,name="ouds"),
]