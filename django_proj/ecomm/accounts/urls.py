from django.urls import path
from .views import *

urlpatterns=[
    path('signin/',signInView,name='signin'),
    path('customer-signup/',CustomerSignUpView.as_view(),name='customer-signup'),
    path('vendor-signup/',VendorSignUpView.as_view(),name='vendor-signup'),
    path('signout/',signOutView,name='signout'),



    path('profile/',customerProfileView,name='customer-profile'),
    path('profile/details/',customerProfileDetailsView,name='customer-profile-details'),
    path('profile/orders/',customerProfileOrdersView,name='customer-profile-orders'),
    path('profile/orders/<int:pk>/',customerProfileOrdersDetailsView,name='customer-profile-orders-details'),
    path('profile/address-book/',customerProfileAddressView,name='customer-profile-address'),


    path('dashboard/',dashboardView,name='dashboard'),
    path('dashboard-finances/',dashboardFinancesView,name='dashboard-finances'),
    path('dashboard-orders/',dashboardOrdersView,name='dashboard-orders'),
    path('dashboard-orders/<int:pk>/',dashboardOrderDetailsView,name='dashboard-ordersdetails'),
    path('dashboard-products/',dashboardProductsView,name='dashboard-products'),
    path('dashboard-products/modify/<int:pk>/',dashboardProductsDetailsView,name='dashboard-productsdetails'),
    path('dashboard-products/delete/<int:pk>/',dashboardProductsDeleteView,name='dashboard-productsdelete'),
    path('add-product/',add_product,name='add-product'),


    path('cart/',cartView,name='cart'),
    path('checkout/',checkoutView,name='checkout'),
    path('update-item/',updateItem,name='updateitem'),
    path('process-order/',processOrder,name='processorder'),
    path('callback/',callBack,name='callback'),
    path('payment-response/',paymentResponse,name='payment-response'),
]