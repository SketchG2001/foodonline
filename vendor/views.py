from django.shortcuts import render



def vProfile(request):
    return render(request, 'vendor/vprofile.html')
