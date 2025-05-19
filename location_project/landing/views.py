from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm
from django.contrib.auth import authenticate, login

from django.contrib import messages
from django.http import  HttpResponse


def landing_page(request):
    return render(request, 'home.html')

def index_page(request):
    return render(request, 'index.html')

def contact_page(request):
    return render(request, 'contact.html')

def service_page(request):
    return render(request, 'service.html')

def about_page(request):
    return render(request, 'about.html')

@login_required
def Admin_page(request):
    if request.user.role != 'admin':
        return redirect('login')
    return redirect('gestion_admin:admin_dashboard')

@login_required
def Manager_page(request):
    if request.user.role != 'manager':
        return redirect('login')
    return render(request, 'gestion_manager:dashboard_Manager')


def login_page(request):
    form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, 
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password']
            )
            if user is not None and user.role == form.cleaned_data['role']:
                login(request, user)
                return redirect('landing:deux')
            else:
                messages.error(request, "Identifiants ou rôle incorrects.")
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})
      
@login_required
def deux(request):
    if hasattr(request.user, 'role'):
        if request.user.role == "admin":
            return redirect("gestion_admin:admin_dashboard")
        elif request.user.role == "manager":
            return redirect("gestion_manager:dashboard_Manager")
    return HttpResponse("Rôle inconnu")

