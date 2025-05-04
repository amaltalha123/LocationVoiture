from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.


def home(request):
    return render(request, 'home.html')  # Afficher home.html

@login_required
def deux(request):
    if hasattr(request.user, 'role'):
        if request.user.role == "admin":
            return redirect("base:manager_page")
        elif request.user.role == "manager":
            return redirect("base:voitures_page")
    return HttpResponse("Rôle inconnu")


def manager_page(request):
    return render(request, 'manager.html')

def voitures_page(request):
    return render(request, 'voitures.html')
