from django.urls import path
from .views import *


urlpatterns=[
    path('',Home,name='book-home'),
    path('getHours',getHours,name='get-hours'),
    path('book',book,name='book'),
    path('submit',reserve,name='submit')
]