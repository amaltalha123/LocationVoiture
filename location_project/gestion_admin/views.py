from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from gestion_manager.models import Manager
from .forms import CustomUserCreationForm
from landing.thread_local import set_raw_password
from django.contrib.auth.decorators import login_required

def liste_managers(request):
    managers = Manager.objects.all()
    return render(request, 'gestion_admin/liste_managers.html', {'managers': managers})

def ajouter_manager(request):
    if request.method == 'POST':
        Manager(
            nom=request.POST['nom'],
            prenom=request.POST['prenom'],
            email=request.POST['email'],
            telephone=request.POST['telephone'],
            agence=request.POST['agence'],
            password=request.POST['password']
        ).save()
        return redirect('liste_managers')
    return render(request, 'gestion_admin/ajouter_manager.html')

def modifier_manager(request, manager_id):
    manager = Manager.objects.get(id=manager_id)
    if request.method == 'POST':
        manager.nom = request.POST['nom']
        manager.prenom = request.POST['prenom']
        manager.email = request.POST['email']
        manager.telephone = request.POST['telephone']
        manager.agence = request.POST['agence']
        manager.save()
        return redirect('liste_managers')
    return render(request, 'gestion_admin/modifier_manager.html', {'manager': manager})

def supprimer_manager(request, manager_id):
    manager = Manager.objects.get(id=manager_id)
    manager.delete()
    return redirect('liste_managers')



#ajouté après
def add_manager(request):
    form = CustomUserCreationForm()
    return render(request, 'gestion_admin/register_user.html',{'form': form})

@login_required(login_url='login')
def register_user(request):
    # Vérifie si l'utilisateur connecté est admin
    if not request.user.is_authenticated or request.user.role != 'admin':
        return HttpResponseForbidden("Accès refusé : vous n'avez pas les droits pour accéder à cette page.")

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            set_raw_password(form.cleaned_data['password']) 
            form.save()
            return render(request, 'gestion_admin/register_user.html', {'form': form})  # Rediriger vers une page que tu veux
    else:
        form = CustomUserCreationForm()
    return render(request, 'gestion_admin/register_user.html', {'form': form})

def admin_dashboard(request):
    form = CustomUserCreationForm()
    return render(request, 'gestion_admin/admin_dashboard.html',{'form': form})
