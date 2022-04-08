from unicodedata import name
from django.urls import path
from .views import CustomerSignUpView,VendorSignUpView,signInView,signOutView

urlpatterns=[
    path('signin/',signInView,name='signin'),
    path('customer-signup/',CustomerSignUpView.as_view(),name='customer-signup'),
    path('vendor-signup/',VendorSignUpView.as_view(),name='vendor-signup'),
    path('signout/',signOutView,name='signout'),
]