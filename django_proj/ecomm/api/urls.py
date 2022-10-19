from unicodedata import name
from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns=[
    path('',api_home),
    path('mainCat/<int:pk>',api_mainCat),
    path('subCat/<int:pk>',api_subCat),
    path('hello/',hello.as_view()),

    #JWT urls
    path('token/obtain/', ObtainTOkenPairWithFirstName.as_view(), name='token_create'),
    path('token/refresh/',jwt_views.TokenRefreshView.as_view(),name='token_refresh'),
    path('user/create/',CustomerCreate.as_view(),name="create_user"),
]