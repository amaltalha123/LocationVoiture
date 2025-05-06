from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing/landing.html')

def login_page(request):
    return render(request, 'landing/login.html')
