from django.urls import path
from .views import *


urlpatterns=[
    path('home/',bookingHome,name='booking-home')
]