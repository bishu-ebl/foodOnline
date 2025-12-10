from django.urls import path
from . import views

urlpatterns=[
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # This will help us to identifed whether the user that logged in is customer or vendor. 
    # Based on what the user dashboard will redirect
    path('myAccount/', views.myAccount, name='myAccount'), 
    # After logout user will redirect to dashboard page
    #path('dashboard/', views.dashboard, name='dashboard'),
    path('custDashboard/', views.custDashboard, name='custDashboard'), 
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'), 
]