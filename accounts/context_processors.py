from django.conf import settings
from vendor.models import vendor


def get_vendor(request):
    try:
        vendors = vendor.objects.get(user=request.user)
    except:
        vendors = None
    return dict(vendors=vendors)
def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}