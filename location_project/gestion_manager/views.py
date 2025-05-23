from django.shortcuts import redirect, render
from .models import Reservation
from .models import Voiture
from landing.models_nosql import Manager
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
import os
from typing import Type
from mongoengine.queryset.queryset import QuerySet
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from bson import ObjectId


@login_required
def voitures_manager(request):
    try:
        # Trouver le manager MongoEngine lié à l'utilisateur Django connecté
        manager = Manager.objects.get(username=request.user.username)
        
        # Récupérer les voitures liées à ce manager
        voitures = Voiture.objects(manager=manager)

        return render(request, 'Voir_voitures.html', {'voitures': voitures})
    
    except Manager.DoesNotExist:
        # Si aucun manager n'est trouvé : redirection ou erreur
        return redirect('landing:login')  # Ou afficher un message d’erreur


def voir_voitures(request):
    return render(request, 'Voir_Voitures.html')


@login_required
def ajouter_voiture(request):
    if request.method == 'POST':
        marque = request.POST.get('marque')
        modele = request.POST.get('modele')
        image_file = request.FILES.get('image')

        image_path = None
        if image_file:
            path = default_storage.save(f'voitures/{image_file.name}', ContentFile(image_file.read()))
            image_path = path

        # Trouver le manager MongoDB lié à l'utilisateur connecté
        try:
            manager = Manager.objects.get(email=request.user.email)
        except Manager.DoesNotExist:
            manager = None

        # Enregistrer la voiture avec le manager MongoDB
        Voiture(
            marque=marque,
            modele=modele,
            annee=int(request.POST['annee']),
            prix_jour=float(request.POST['prix_jour']),
            couleur=request.POST.get('couleur', ''),
            matricule=request.POST['matricule'],
            image=image_path,
            statut=request.POST['statut'],
            manager=manager
        ).save()

        return redirect('gestion_manager:dashboard_Manager')

    return render(request, 'ajouter_voiture.html')

def modifier_voiture(request, voiture_id):
    voiture = Voiture.objects.get(id=voiture_id)
    
    if request.method == 'POST':
        voiture.marque = request.POST['marque']
        voiture.modele = request.POST['modele']
        voiture.annee = int(request.POST['annee'])
        voiture.prix_jour = float(request.POST['prix_jour'])
        voiture.couleur = request.POST.get('couleur', '')
        voiture.matricule = request.POST['matricule']
        voiture.statut = request.POST['statut']

        # 🔄 Récupérer automatiquement le manager à partir de l'utilisateur connecté
        try:
            manager = Manager.objects.get(email=request.user.email)
            voiture.manager = manager
        except Manager.DoesNotExist:
            voiture.manager = None

        image_file = request.FILES.get('image')
        if image_file:
            image_path = f"voitures/{image_file.name}"
            full_path = os.path.join(settings.MEDIA_ROOT, image_path)
            with open(full_path, 'wb+') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
            voiture.image = image_path

        voiture.save()
        return redirect('Voir_Voitures')

    return render(request, 'modifier_voiture.html', {'voiture': voiture})


def supprimer_voiture(request, voiture_id):
    voiture = Voiture.objects.get(id=voiture_id)

    # Optionnel : vérifier que le manager connecté est bien celui qui a créé la voiture
    try:
        manager = Manager.objects.get(email=request.user.email)
        if voiture.manager != manager:
            return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer cette voiture.")
    except Manager.DoesNotExist:
        return HttpResponseForbidden("Manager introuvable.")

    voiture.delete()
    return redirect('Voir_Voitures')


@login_required
def liste_reservations(request):
    try:
        # Récupérer le manager lié à l'utilisateur connecté
        manager = Manager.objects.get(username=request.user.username)

        # Filtrer les réservations où le manager est celui connecté
        reservations = Reservation.objects(manager=manager)

        return render(request, 'liste_reservations.html', {
            'reservations': reservations
        })
    
    except Manager.DoesNotExist:
        # Si l'utilisateur connecté n'est pas un manager, redirige vers la page de login
        return redirect('landing:login')


def dashboard_Manager(request):
    return render(request, 'dashboard_Manager.html')

def reservations_page(request):
    return render(request, 'liste_reservations.html')