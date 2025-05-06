from django.shortcuts import render, redirect, get_object_or_404
from .models import Manager

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
            agence=request.POST['agence']
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
