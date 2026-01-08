from django.urls import path, include
from accounts import views as AccountViews
from . import views

urlpatterns =[
    # This path is responsible for sending the 'customer' to custDashboard url in accounts model
    path('', AccountViews.custDashboard, name='customer'), 
    path('profile/', views.cprofile, name='cprofile'),
]