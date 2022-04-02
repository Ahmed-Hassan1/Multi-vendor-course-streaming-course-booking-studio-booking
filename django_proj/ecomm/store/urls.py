from unicodedata import name
from django.urls import path
from . import views

urlpatterns=[
    path('',views.homeView,name="home"),

    path('register/',views.registerView,name='register'),
    path('login/',views.logInView,name='login'),
    path('logout/',views.logOutView,name='logout'),
    path('inst/<str:pk>/',views.instrumentView,name='instruments'),
    path('category/<str:pk>/',views.subCatView,name='subCategory'),
    path('product/<slug:pk>/',views.productView,name='product'),
    path('ouds',views.oudView,name="ouds"),
]