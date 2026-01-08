from django.urls import path, include
from . import views

urlpatterns=[
    path('',views.myAccount),
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

    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    # Path to reset the password
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),

    # Vendor dashboard related URLS
    path('vendor/', include('vendor.urls')),

    # Forwording customers url
    path('customer/', include('customers.urls')),
]