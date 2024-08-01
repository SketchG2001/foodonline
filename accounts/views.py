from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages
def home(request):
    return render(request, 'home.html')


def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # create the user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # form.save()
            # create the user uisng the create user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                            password=password, email=email)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'You have been registered successfully')
            return redirect('registerUser')
        else:
            print('invalid form data')
            print(form.errors)
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'accounts/registerUser.html', context)
