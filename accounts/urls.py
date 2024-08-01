from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
]
