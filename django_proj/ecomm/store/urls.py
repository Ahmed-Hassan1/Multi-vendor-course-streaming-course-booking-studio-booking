from django.urls import path, re_path
from . import views

urlpatterns=[
    path('',views.homeView,name="home"),
    path('new-products',views.newView,name="new-products"),
    path('inst/<str:pk>/',views.instrumentView,name='instruments'),
    path('category/<str:pk>/',views.subCatView,name='subCategory'),
    re_path(r'product/(?P<pk>[-\w]+)/$',views.productView,name='product'),#fixed unicode in URL with regex
    path('ouds',views.oudView,name="ouds"),
]