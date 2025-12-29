from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from accounts.views import check_role_customer
from marketplace.context_processors import get_cart_amounts, get_cart_counter
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from .models import Cart
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html',context)

def vendor_detail(request, vendor_slug):
    # Returns categories of particular vendor
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    # categories = Category.objects.all, return all categories
    # prefetch_related method is look for the data in reverse manner. For exampple,
    # We do not have the access to food items data inside Category model because there is no foreign key relation 
    # with FoodItem Model. In this case to fetch the data from FoodItem model for the particular category,
    # prefetch_related is used. For that related_name='fooditems' is set in FoodItem model
   
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch('fooditems',# related name from FoodItem model will come here to fetch food items
                 queryset=FoodItem.objects.filter(is_available=True)
                 ) 
    )
    # To find the number of items in cart model of this particular logged in user
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # if request.is_ajax():
            # Check if the food item is exists with the food id
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check whether the user already added this food to the cart
                # If true then increase the Quantity to the cart, otherwise add a new cart.
                try:
                    # Check whether this logged in user has this particular item in his cart.
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status':'Success', 'message': 'Cart quantity has increased',
                                         'cart_counter': get_cart_counter(request),
                                         'qty': chkCart.quantity,
                                         'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':'Success', 'message': 'Added the food to the cart',
                                         'cart_counter': get_cart_counter(request),
                                         'qty': chkCart.quantity,
                                         'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status':'Failed', 'message': 'This food does not exists!'})
        else:
            return JsonResponse({'status':'Failed', 'message': 'Invalid Request'})
        # return JsonResponse({'status':'success', 'message': 'User is logged in'})
    else:
        # return HttpResponse(food_id)
        return JsonResponse({'status':'login_required', 'message': 'Please Login to continue'})

def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # if request.is_ajax():
            # Check if the food item is exists with the food id
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check whether the user already added this food to the cart
                # If true then increase the Quantity to the cart, otherwise add a new cart.
                try:
                    # Check whether this logged in user has this particular item in his cart.
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Decrease the quantity
                    if  chkCart.quantity>1:
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity=0
                    return JsonResponse({'status':'Success', 'cart_counter': get_cart_counter(request),
                                            'qty': chkCart.quantity,
                                            'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status':'Failed', 'message': 'You do not have this item in your CART'})
            except:
                return JsonResponse({'status':'Failed', 'message': 'This food does not exists!'})
        else:
            return JsonResponse({'status':'Failed', 'message': 'Invalid Request'})
        # return JsonResponse({'status':'success', 'message': 'User is logged in'})
    else:
        # return HttpResponse(food_id)
        return JsonResponse({'status':'login_required', 'message': 'Please Login to continue'})
    # return HttpResponse(food_id)
    # return JsonResponse({'status':'Failed', 'message': 'Please Login to continue'})

@login_required(login_url = 'login')
#@user_passes_test(check_role_customer)
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html',context)

def delete_cart(request,cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart is exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success', 'message': 'Cart item has been deleted',
                                         'cart_counter': get_cart_counter(request),
                                         'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status':'Failed', 'message': 'Cart item does not exists!'})
        else:
            return JsonResponse({'status':'Failed', 'message': 'Invalid Request'})