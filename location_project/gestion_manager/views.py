from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from bson import ObjectId

from mongoengine import DoesNotExist
from mongoengine.queryset.queryset import QuerySet

from .models import Voiture, Client, Reservation
from landing.models_nosql import Manager


def voitures_manager(request):
    if not request.session.get('username'):
        return redirect('landing:login')

    try:
        manager = Manager.objects.get(username=request.session['username'])
        voitures = Voiture.objects(manager=manager)
        return render(request, 'Voir_voitures.html', {'voitures': voitures})
    except Manager.DoesNotExist:
        return redirect('landing:login')


def voir_voitures(request):
    return render(request, 'Voir_Voitures.html')


def dashboard_vehicule(request):
    if not request.session.get('username'):
        return redirect('landing:login')

    try:
        manager = Manager.objects.get(username=request.session['username'])
        voitures = Voiture.objects(manager=manager)
        return render(request, 'Dashboard_vehicules.html', {'voitures': voitures})
    except Manager.DoesNotExist:
        return redirect('landing:login')


def ajouter_voiture(request):
    if not request.session.get('username'):
        return redirect('landing:login')

    if request.method == 'POST':
        marque = request.POST.get('marque')
        modele = request.POST.get('modele')
        annee = int(request.POST['annee'])
        prix_jour = float(request.POST['prix_jour'])
        couleur = request.POST.get('couleur', '')
        matricule = request.POST['matricule']
        statut = request.POST['statut']
        image_file = request.FILES.get('image')

        nbr_places = int(request.POST.get('nbr_places', 0))
        nbr_portes = int(request.POST.get('nbr_portes', 0))
        carburant = request.POST.get('carburant', '')
        boite_vitesse = request.POST.get('boite_vitesse', '')
        kilometrage = int(request.POST.get('kilometrage', 0))
        description = request.POST.get('description', '')

        image_path = None
        if image_file:
            path = default_storage.save(f'voitures/{image_file.name}', ContentFile(image_file.read()))
            image_path = path

        try:
            manager = Manager.objects.get(username=request.session['username'])
        except Manager.DoesNotExist:
            manager = None

        Voiture(
            marque=marque,
            modele=modele,
            annee=annee,
            prix_jour=prix_jour,
            couleur=couleur,
            matricule=matricule,
            statut=statut,
            image=image_path,
            manager=manager,
            nbr_places=nbr_places,
            nbr_portes=nbr_portes,
            carburant=carburant,
            boite_vitesse=boite_vitesse,
            kilometrage=kilometrage,
            description=description
        ).save()

        return redirect('gestion_manager:dashboard_vehicule')

    return render(request, 'ajouter_voiture.html')


def modifier_voiture(request, voiture_id):
    if not request.session.get('username'):
        return redirect('landing:login')

    voiture = Voiture.objects.get(id=voiture_id)

    if request.method == 'POST':
        voiture.marque = request.POST['marque']
        voiture.modele = request.POST['modele']
        voiture.annee = int(request.POST['annee'])
        voiture.prix_jour = float(request.POST['prix_jour'])
        voiture.couleur = request.POST.get('couleur', '')
        voiture.matricule = request.POST['matricule']
        voiture.statut = request.POST['statut']
        voiture.nbr_places = int(request.POST['nbr_places'])
        voiture.nbr_portes = int(request.POST['nbr_portes'])
        voiture.carburant = request.POST['carburant']
        voiture.boite_vitesse = request.POST['boite_vitesse']
        voiture.kilometrage = int(request.POST['kilometrage'])
        voiture.description = request.POST.get('description', '')

        try:
            manager = Manager.objects.get(username=request.session['username'])
            voiture.manager = manager
        except Manager.DoesNotExist:
            voiture.manager = None

        image_file = request.FILES.get('image')
        if image_file:
            path = default_storage.save(f'voitures/{image_file.name}', ContentFile(image_file.read()))
            voiture.image = path

        voiture.save()
        return redirect('gestion_manager:dashboard_vehicule')

    return render(request, 'modifier_voiture.html', {'voiture': voiture})


def supprimer_voiture(request, voiture_id):
    if not request.session.get('username'):
        return redirect('landing:login')

    voiture = Voiture.objects.get(id=voiture_id)

    try:
        manager = Manager.objects.get(username=request.session['username'])
        if voiture.manager != manager:
            return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer cette voiture.")
    except Manager.DoesNotExist:
        return HttpResponseForbidden("Manager introuvable.")

    voiture.delete()
    return redirect('gestion_manager:dashboard_vehicule')


def liste_reservations(request):
    if not request.session.get('username'):
        return redirect('landing:login')

    try:
        manager = Manager.objects.get(username=request.session['username'])
        reservations = Reservation.objects(manager=manager)
        return render(request, 'liste_reservations.html', {'reservations': reservations})
    except Manager.DoesNotExist:
        return redirect('landing:login')


def dashboard_Manager(request):
    return render(request, 'dashboard_Manager.html')


def ajouter_reservation_template(request, voiture_id):
    try:
        voiture = Voiture.objects.get(id=voiture_id)
    except DoesNotExist:
        return render(request, '404.html')
    return render(request, 'Ajouter_Reservation.html', {'voiture': voiture})


def ajouter_reservation(request, voiture_id):
    if not request.session.get('username'):
        return redirect('landing:login')

    try:
        voiture = Voiture.objects.get(id=voiture_id)
        manager = Manager.objects.get(username=request.session['username'])
    except DoesNotExist:
        return render(request, '404.html')

    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        prix_total_str = request.POST.get('total_price')

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

        if date_debut and date_fin:
            date_debut = datetime.strptime(date_debut, '%Y-%m-%dT%H:%M')
            date_fin = datetime.strptime(date_fin, '%Y-%m-%dT%H:%M')

            if date_debut >= date_fin:
                return render(request, 'Ajouter_Reservation.html', {
                    'voiture': voiture,
                    'error': "La date de début doit être antérieure à la date de fin."
                })

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

            reservation = Reservation(
                client=client,
                voiture=voiture,
                manager=manager,
                date_debut=date_debut,
                date_fin=date_fin,
                statut='en attente',
                prix_total=prix_total
            )
            reservation.save()

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
            {accept_link}

            Pour refuser la réservation, cliquez sur le lien suivant :
            {refuse_link}

            Merci de votre confiance !

            Cordialement,
            L'équipe CityDrive
            """
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

            voitures = Voiture.objects(manager=manager)
            return render(request, 'Dashboard_Vehicules.html', {'voitures': voitures, 'success': "Votre réservation a été effectuée avec succès."})

    return render(request, 'Ajouter_Reservation.html', {'voiture': voiture})


def accepter_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)

        if reservation.statut in ['acceptée', 'refusée']:
            return render(request, 'confirmation.html', {'message': "Cette réservation a déjà été traitée."})

        if reservation.date_debut <= datetime.now():
            return render(request, 'confirmation.html', {'message': "Vous ne pouvez pas accepter cette réservation car la date de début est déjà atteinte."})

        reservation.statut = 'acceptée'
        reservation.save()
        return render(request, 'confirmation.html', {'message': "Votre réservation a été confirmée."})

    except DoesNotExist:
        return render(request, '404.html')


def refuser_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)

        if reservation.statut in ['acceptée', 'refusée']:
            return render(request, 'confirmation.html', {'message': "Cette réservation a déjà été traitée."})

        if reservation.date_debut <= datetime.now():
            return render(request, 'confirmation.html', {'message': "Vous ne pouvez pas refuser cette réservation car la date de début est déjà atteinte."})

        reservation.statut = 'refusée'
        reservation.save()
        return render(request, 'confirmation.html', {'message': "Votre réservation a été refusée."})

    except DoesNotExist:
        return render(request, '404.html')
