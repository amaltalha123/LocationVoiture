from mongoengine import Document, StringField, EmailField, IntField, FloatField, BooleanField, ReferenceField, DateTimeField
from landing.models_nosql import Manager 



class Client(Document):
    nom = StringField(required=True)
    prenom = StringField(required=True)
    email = EmailField(required=True, unique=True)
    telephone = StringField()

    meta = {'collection': 'clients'}



class Voiture(Document):
    marque = StringField(required=True)
    modele = StringField(required=True)
    annee = IntField(required=True)
    prix_jour = FloatField(required=True)
    couleur = StringField()
    matricule = StringField(required=True, unique=True)
    image = StringField()  # chemin de l'image
    statut = StringField(choices=('disponible', 'indisponible'), default='disponible')
    manager = ReferenceField(Manager, required=False)
    description = StringField()
    nbr_places = IntField()
    boite_vitesse = StringField(choices=['manuelle', 'automatique'])
    nbr_portes = IntField()
    carburant = StringField(choices=['essence', 'diesel', 'électrique'])
    kilometrage = IntField()

    meta = {'collection': 'voitures'}



class Reservation(Document):
    client = ReferenceField(Client, required=True)
    voiture = ReferenceField(Voiture, required=True)
    manager = ReferenceField(Manager, required=False)
    date_debut = DateTimeField(required=True)
    date_fin = DateTimeField(required=True)
    statut = StringField(choices=('en attente', 'acceptée', 'refusée','confirmée','rejetée'), default='en attente')
    prix_total=FloatField(required=True)

    meta = {'collection': 'reservations'}
