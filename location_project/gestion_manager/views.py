from django.shortcuts import redirect, render
from .models import Reservation
from .models import Voiture
from landing.models_nosql import Manager
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

from typing import Type
from mongoengine.queryset.queryset import QuerySet


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

