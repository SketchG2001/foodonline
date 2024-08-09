from django.conf import settings

from accounts.models import UserProfile
from vendor.models import Vendor


def get_vendor(request):
    try:
        vendors = Vendor.objects.get(user=request.user)
    except:
        vendors = None
    return dict(vendors=vendors)

def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)


def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}
