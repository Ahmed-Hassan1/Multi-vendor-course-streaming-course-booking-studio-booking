from unicodedata import name
from django.urls import path
from .views import *



urlpatterns=[
    path('',home,name='courses-home'),
    path('cat/<str:pk>/',courseCat,name='course-cat'),
    path('course/<int:pk>/',courseView,name='course'),
    path('enroll/',enrollConfirm,name='course-enroll'),
]