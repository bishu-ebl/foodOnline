# The purpose of context proccesssor is to enable accessable vendor model objects like cover photo,
# profile picture etc to all html objects.
# Context processor is a function that only take argument as request and return dictionary 
# that get addded to the context. The following function take vendor as request asd pass it this function as argument

from vendor.models import Vendor


def get_vendor(request):
    # we fetch the vendor using the login user. In case user is not logged in it will go to except block
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor = vendor)