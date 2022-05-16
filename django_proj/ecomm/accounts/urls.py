from unicodedata import name
from django.urls import path
from .views import *

urlpatterns=[
    path('signin/',signInView,name='signin'),
    path('customer-signup/',CustomerSignUpView.as_view(),name='customer-signup'),
    path('vendor-signup/',VendorSignUpView.as_view(),name='vendor-signup'),
    path('signout/',signOutView,name='signout'),
    path('profile/',customerProfileView,name='customer-profile'),
    path('dashboard/',dashboardView,name='dashboard'),
    path('dashboard-orders/',dashboardOrdersView,name='dashboard-orders'),
    path('dashboard-orders/<int:pk>/',dashboardOrderDetailsView,name='dashboard-ordersdetails'),
    path('dashboard-products/',dashboardProductsView,name='dashboard-products'),
    path('add-product/',add_product,name='add-product'),

    path('cart/',cartView,name='cart'),
    path('checkout/',checkoutView,name='checkout'),
    path('update-item/',updateItem,name='updateitem'),
    path('process-order/',processOrder,name='processorder'),
]