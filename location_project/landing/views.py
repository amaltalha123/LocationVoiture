from django.shortcuts import render, redirect
from .forms import CustomLoginForm
from django.contrib import messages
from django.http import HttpResponse
from pymongo import MongoClient
from django.contrib.auth.hashers import check_password

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

def Admin_page(request):
    if request.session.get('role') != 'Admin':
        return redirect('landing:login_page')
    return redirect('gestion_admin:admin_dashboard')

def Manager_page(request):
    if request.session.get('role') != 'Manager':
        return redirect('landing:login_page')
    return redirect('gestion_manager:dashboard_Manager')

def login_page(request):
    form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role'].capitalize()  

            client = MongoClient("mongodb://localhost:27017/")
            db = client.location_voitures
            collection = db.manager

            user_doc = collection.find_one({
                "username": username,
                "role": role
            })

            if user_doc and check_password(password, user_doc.get("password", "")):
                request.session['user_id'] = str(user_doc['_id'])
                request.session['username'] = user_doc['username']
                request.session['role'] = user_doc['role']

                if role == 'Manager':
                    request.session['manager_id'] = str(user_doc['_id'])

                return redirect('landing:deux')
            else:
                messages.error(request, "Identifiants ou rôle incorrects.")
        else:
            messages.error(request, "Formulaire invalide.")
    else:
        form = CustomLoginForm()

    return render(request, 'registration/login.html', {'form': form})

def deux(request):
    role = request.session.get('role')

    if role == "Admin":
        return redirect("gestion_admin:admin_dashboard")
    elif role == "Manager":
        return redirect("gestion_manager:dashboard_Manager")

    return HttpResponse("Rôle inconnu")
