from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import vendor
from accounts.models import UserProfile
from vendor.froms import VendorForm
from accounts.forms import UserProfileForm
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendors = get_object_or_404(vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendors)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings Updated Successfully')
            return redirect('vProfile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendors)
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'vendors': vendors,
        'profile': profile,
    }
    return render(request, 'vendor/vprofile.html', context)
