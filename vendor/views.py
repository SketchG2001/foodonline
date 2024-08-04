from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify

from menu.forms import CategoryForm
from menu.models import FoodItem
from .models import Vendor
from accounts.models import UserProfile
from vendor.froms import VendorForm
from accounts.forms import UserProfileForm
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


def get_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return category


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
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
        vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'vendor': vendor,
        'profile': profile,
    }
    return render(request, 'vendor/vprofile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def food_items_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    food_items = FoodItem.objects.filter(category=category, vendor=vendor)
    context = {
        'food_items': food_items,
        'category': category,
    }
    return render(request, 'vendor/food_items_by_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            try:
                form.save()
                messages.success(request, 'Category added successfully')
                return redirect('menu_builder')
            except:
                messages.error(request, 'Category with this name already exists')
                return redirect('add_category')
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)


def edit_category(request, pk=None):
    category = get_category(request,pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            try:
                form.save()
                messages.success(request, 'Category Updated successfully')
                return redirect('menu_builder')
            except:
                messages.error(request, f"Can't Update! category with ({category_name}) name already exists")
                return redirect('edit_category', pk=pk)
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/edit_category.html', context)


def delete_category(request, pk=None):
    category = get_category(request, pk)
    category.delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('menu_builder')
