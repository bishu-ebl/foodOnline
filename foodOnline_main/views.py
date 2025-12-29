from django.shortcuts import render
from django.http import HttpResponse

from vendor.models import Vendor

def home(request):
    #return HttpResponse('Hello World')
    # This is showing vendor which are aproved and activation staus Trus in home page
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    # print(vendors)
    context = {
        'vendors': vendors,
    }
    return render(request, 'home.html', context) # Create a folder templates and crete home.html in this folder. Later confiugure the template folder in settings.py
