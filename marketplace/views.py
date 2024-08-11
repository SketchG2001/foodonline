from datetime import date, datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.gis.geos import GEOSGeometry

from accounts.models import UserProfile
from marketplace.context_processors import get_cart_counter, get_cart_amounts
from marketplace.models import Cart
from menu.models import Category, FoodItem
from orders.forms import OrderForm
from vendor.models import Vendor, OpeningHours
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    opening_hours = OpeningHours.objects.filter(vendor=vendor).order_by('day', '-from_hour')
    #  check for current day's openings hours
    today_date = date.today()
    today = today_date.isoweekday()
    current_opening_hours = OpeningHours.objects.filter(vendor=vendor, day=today)

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                #   check if the user has already added that food to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    #   Increase the cart quantity
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({
                        'status': 'Success',
                        'message': 'Increased the quantity of cart',
                        'cart_counter': get_cart_counter(request),
                        'qty': checkCart.quantity,
                        'cart_amount': get_cart_amounts(request)
                    })
                except:
                    checkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    checkCart.save()
                    return JsonResponse({
                        'status': 'Success',
                        'message': 'Food added to your cart',
                        'cart_counter': get_cart_counter(request),
                        'qty': checkCart.quantity,
                        'cart_amount': get_cart_amounts(request)
                    })
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'message': 'This food does not exist'
                })
        else:
            return JsonResponse({
                'status': 'Failed',
                'message': 'Invalid request.'
            })
    else:
        return JsonResponse({
            'status': 'login_required',
            'message': 'Please login to continue'
        })


def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                #   check if the user has already added that food to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if checkCart.quantity > 1:
                        #   Decrease the cart quantity
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        checkCart.delete()
                        checkCart.quantity = 0

                    return JsonResponse({
                        'status': 'Success',
                        'cart_counter': get_cart_counter(request),
                        'qty': checkCart.quantity,
                        'cart_amount': get_cart_amounts(request)
                    })
                except:
                    return JsonResponse({
                        'status': 'Failed',
                        'message': 'You do not have this item in your cart.',
                    })
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'message': 'This food does not exist'
                })
        else:
            return JsonResponse({
                'status': 'Failed',
                'message': 'Invalid request.'
            })
    else:
        return JsonResponse({
            'status': 'login_required',
            'message': 'Please login to continue'
        })


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'cart_items': cart_items
    }
    return render(request, 'marketplace/cart.html', context)


@login_required(login_url='login')
def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the cart item exist
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({
                        'status': 'Success',
                        'message': 'Cart item has been deleted!',
                        'cart_counter': get_cart_counter(request),
                        'cart_amount': get_cart_amounts(request)
                    })
            except:
                return JsonResponse({
                    'status': 'Failed',
                    'message': 'Cart item does not exist'
                })

        else:
            return JsonResponse({
                'status': 'Failed',
                'message': 'Invalid request.'
            })


def search(request):
    if not 'address' in request.GET:
        return redirect('marketplace')
    else:
        address = request.GET['address']
        latitude = request.GET['lat']
        longitude = request.GET['lng']
        radius = request.GET['radius']
        keyword = request.GET['keyword']
        # get vendor ids that has the food item user is looking for
        fetch_vendor_by_food_names = FoodItem.objects.filter(food_title__icontains=keyword,
                                                             is_available=True).values_list(
            'vendor', flat=True)
        vendors = Vendor.objects.filter(
            Q(id__in=fetch_vendor_by_food_names) | Q(vendor_name__icontains=keyword, is_approved=True,
                                                     user__is_active=True))
        if latitude and longitude and radius:
            pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
            vendors = Vendor.objects.filter(
                Q(id__in=fetch_vendor_by_food_names) | Q(vendor_name__icontains=keyword, is_approved=True,
                                                         user__is_active=True),
                user_profile__location__distance_lte=(pnt, D(km=radius))).annotate(
                distance=Distance("user_profile__location", pnt)).order_by('distance')
            for v in vendors:
                v.kms = round(v.distance.km, 1)

        vendors_count = vendors.count()
        context = {
            'vendors': vendors,
            'vendors_count': vendors_count,
            'source_location': address
        }

        return render(request, 'marketplace/listings.html', context)
# Sketch@123456789

@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('-created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)
    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/checkout.html',context)