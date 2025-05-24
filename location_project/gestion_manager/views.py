from django.shortcuts import redirect, render,get_object_or_404
from .models import Voiture,Client,Reservation
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
from datetime import datetime
from mongoengine import DoesNotExist

from django.core.mail import send_mail
from django.conf import settings


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

def dashboard_vehicule(request):
    try:
        # Trouver le manager MongoEngine lié à l'utilisateur Django connecté
        manager = Manager.objects.get(username=request.user.username)
        
        # Récupérer les voitures liées à ce manager
        voitures = Voiture.objects(manager=manager)

        return render(request, 'Dashboard_vehicules.html', {'voitures': voitures})
    
    except Manager.DoesNotExist:
        # Si aucun manager n'est trouvé : redirection ou erreur
        return redirect('landing:login')  # Ou afficher un message d’erreur
        
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

        #  Récupérer automatiquement le manager à partir de l'utilisateur connecté
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
        return redirect('dashboard_vehicule')

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
    return redirect('dashboard_vehicule')


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


#Gestion des resrvations
def ajouter_reservation_template(request, voiture_id):
    try:
        voiture = Voiture.objects.get(id=voiture_id)
    except DoesNotExist:
        return render(request, '404.html') 
    return render(request, 'Ajouter_Reservation.html', {'voiture': voiture})


def ajouter_reservation(request, voiture_id):
    try:
        voiture = Voiture.objects.get(id=voiture_id)
        manager = Manager.objects.get(username=request.user.username)
    except DoesNotExist:
        return render(request, '404.html') 

   
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        prix_total_str = request.POST.get('total_price')

        # Vérifier que prix_total est fourni et peut être converti en float
        if prix_total_str is None:
            return render(request, 'Ajouter_Reservation.html', {
                'voiture': voiture,
                'error': "Le prix total doit être fourni."
            })

        try:
            prix_total = float(prix_total_str)
        except ValueError:
            return render(request, 'Ajouter_Reservation.html', {
                'voiture': voiture,
                'error': "Le prix total doit être un nombre valide."
            })

        # Vérifier que les dates sont valides
        if date_debut and date_fin:
            date_debut = datetime.strptime(date_debut, '%Y-%m-%dT%H:%M')  # Format de datetime-local
            date_fin = datetime.strptime(date_fin, '%Y-%m-%dT%H:%M')

            if date_debut >= date_fin:
                # Gérer l'erreur de date
                return render(request, 'Ajouter_Reservation.html', {
                    'voiture': voiture,
                    'error': "La date de début doit être antérieure à la date de fin."
                })

            # Créer ou récupérer le client
            try:
                client = Client.objects.get(email=email)
            except DoesNotExist:
                client = Client(
                    nom=nom,
                    prenom=prenom,
                    telephone=telephone,
                    email=email
                )
                client.save()

            # Créer la réservation
            reservation = Reservation(
                client=client,
                voiture=voiture,
                manager=manager,
                date_debut=date_debut,
                date_fin=date_fin,
                statut='en attente',  # Statut par défaut
                prix_total=prix_total
            )
            reservation.save()

            # Envoyer un e-mail de confirmation
            subject = 'Confirmation de votre réservation'
            accept_link = request.build_absolute_uri(f'/accepter_reservation/{reservation.id}/')
            refuse_link = request.build_absolute_uri(f'/refuser_reservation/{reservation.id}/')

            message = f"""
            Bonjour {client.prenom} {client.nom},

            Votre réservation a été effectuée avec succès !

            Détails de la réservation :
            Voiture : {voiture.marque} {voiture.modele}
            Date de début : {date_debut.strftime('%Y-%m-%d %H:%M')}
            Date de fin : {date_fin.strftime('%Y-%m-%d %H:%M')}
            Statut : {reservation.statut}
            Total à payer: {reservation.prix_total}
            Pour confirmer votre réservation, cliquez sur le lien suivant :
            [Accepter la réservation]({accept_link})

            Si vous souhaitez refuser la réservation, cliquez sur le lien suivant :
            [Refuser la réservation]({refuse_link})

            Merci de votre confiance !

            Cordialement,
            L'équipe CityDrive
            """
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

            # Rediriger ou afficher un message de succès
            voitures = Voiture.objects(manager=manager)
            return render(request, 'Dashboard_Vehicules.html', {'voitures':voitures,'success': "Votre réservation a été effectuée avec succès."})

    return render(request, 'Ajouter_Reservation.html', {'voiture': voiture})



from mongoengine import DoesNotExist

from datetime import datetime
from mongoengine import DoesNotExist

def accepter_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        
        # Vérifier si la réservation a déjà été acceptée ou refusée
        if reservation.statut in ['acceptée', 'refusée']:
            return render(request, 'confirmation.html', {'message': "Cette réservation a déjà été traitée."})

        # Vérifier si la date de début est déjà atteinte
        if reservation.date_debut <= datetime.now():
            return render(request, 'confirmation.html', {'message': "Vous ne pouvez pas accepter cette réservation car la date de début est déjà atteinte."})

        # Mettre à jour le statut de la réservation
        reservation.statut = 'acceptée'
        reservation.save()
        return render(request, 'confirmation.html', {'message': "Votre réservation a été confirmée."})
    
    except DoesNotExist:
        return render(request, '404.html')  # Assurez-vous que ce template existe


def refuser_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        
        # Vérifier si la réservation a déjà été acceptée ou refusée
        if reservation.statut in ['acceptée', 'refusée']:
            return render(request, 'confirmation.html', {'message': "Cette réservation a déjà été traitée."})

        # Vérifier si la date de début est déjà atteinte
        if reservation.date_debut <= datetime.now():
            return render(request, 'confirmation.html', {'message': "Vous ne pouvez pas refuser cette réservation car la date de début est déjà atteinte."})

        # Mettre à jour le statut de la réservation
        reservation.statut = 'refusée'
        reservation.save()
        return render(request, 'confirmation.html', {'message': "Votre réservation a été refusée."})
    
    except DoesNotExist:
        return render(request, '404.html')
