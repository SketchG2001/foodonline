from vendor.models import vendor


def get_vendor(request):
    try:
        vendors = vendor.objects.get(user=request.user)
    except:
        vendors = None
    return dict(vendors=vendors)
