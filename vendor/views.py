from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify

from menu.forms import CategoryForm, FoodItemForm
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


# Need to check new user unable to add the category with the same name as another users category
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name) + '-' + str(category.vendor.id)
            print(category.slug)
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


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_category(request, pk)
    vendor = get_vendor(request)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name) + '-' + str(vendor.id)
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


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_category(request, pk)
    category.delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    vendor = get_vendor(request)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title) + '-' + str(vendor.id)
            print(food.slug)
            try:
                form.save()
                messages.success(request, 'Food Item added successfully')
                return redirect('food_items_by_category', food.category.id)
            except:
                messages.error(request, 'food item with this name already exists')
                return redirect('add_food')
    else:
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=vendor)
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_food.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    vendor = get_vendor(request)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food, vendor=vendor)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title) + '-' + str(vendor.id)
            try:
                form.save()
                messages.success(request, 'Food Item Updated Successfully')
                return redirect('food_items_by_category', food.category.id)
            except:
                messages.error(request, f"Can't Update! category with ({food_title}) name already exists")
                return redirect('edit_category', pk=pk)
    else:
        form = FoodItemForm(instance=food, vendor=vendor)
    context = {
        'form': form,
        'food': food,
    }
    return render(request, 'vendor/edit_food.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, 'Food Item deleted successfully')
    return redirect('food_items_by_category', food.category.id)
