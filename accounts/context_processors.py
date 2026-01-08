# The purpose of context proccesssor is to enable access vendor model objects like cover photo,
# profile picture etc to all html objects.
# Context processor is a function that only take one argument as request and return dictionary 
# that get addded to the context. The following function take vendor as request asd pass it this function as argument

from django.conf import settings
from vendor.models import Vendor
from .models import UserProfile


def get_vendor(request):
    # we fetch the vendor using the login user. In case user is not logged in it will go to except block
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor = vendor)

def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)

# This function is to enable access GOOGLE_API_KEY from html pages
def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}