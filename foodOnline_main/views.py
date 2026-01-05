from django.shortcuts import render
from django.http import HttpResponse

from vendor.models import Vendor
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance

def get_or_set_current_location(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        return lng, lat
    elif 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        request.session['lat']=lat
        request.session['lng']=lng
        return lng, lat
    else:
        return None
    

def home(request):
    #return HttpResponse('Hello World')
    # Check whether the lat and lng are in get reuest or not
    # if 'lat' in request.GET:
    #     lat = request.GET.get('lat')
    #     lng = request.GET.get('lng')
    #     pnt = GEOSGeometry('POINT(%s %s)' %(lng, lat))
    if get_or_set_current_location(request) is not None:
        pnt = GEOSGeometry('POINT(%s %s)' %(get_or_set_current_location(request)))
            # Find restaurant nearby location. Since we do not have any distance field in model, we will use annotate here
        vendors = Vendor.objects.filter(user_profile__location__distance_lte=(pnt, D(km=100))
                                            ).annotate(distance_km=Distance("user_profile__location", pnt)).order_by("distance_km")
        for v in vendors:
            v.kms = round(v.distance_km.km, 1)
    else:
        # This is showing vendor which are aproved and activation staus Trus in home page
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
        # print(vendors)
    context = {
        'vendors': vendors,
    }
    return render(request, 'home.html', context) # Create a folder templates and crete home.html in this folder. Later confiugure the template folder in settings.py
