"""
URL configuration for foodOnline_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# These two library are imported for inheriting media folder
# from django.conf import settings
# from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from . import views # this . means current directory
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views as MarketplaceView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), # URL path for home page
    #path('accounts/', include('accounts.urls')),
    path('', include('accounts.urls')),

    # URL to route to marketplace
    path('marketplace/', include('marketplace.urls')),

    # CART
    path('cart/', MarketplaceView.cart, name='cart'),
    # SEARCH URL
    path('search/', MarketplaceView.search,name='search'),

    # CKECKOUT
    path('checkout/', MarketplaceView.checkout, name='checkout'),

    # ORDERS
    path('orders/', include('orders.urls')),
    
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
