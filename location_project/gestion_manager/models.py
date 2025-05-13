from mongoengine import Document, StringField, EmailField, ReferenceField, DateTimeField
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
    immatriculation = StringField(required=True, unique=True)
    statut = StringField(choices=('disponible', 'indisponible'), default='disponible')
    manager = ReferenceField(Manager)
    meta = {'collection': 'voitures'}



class Reservation(Document):
    client = ReferenceField(Client, required=True)
    voiture = ReferenceField(Voiture, required=True)
    manager = ReferenceField(Manager, required=False)
    date_debut = DateTimeField(required=True)
    date_fin = DateTimeField(required=True)
    statut = StringField(choices=('en attente', 'acceptée', 'refusée'), default='en attente')

    meta = {'collection': 'reservations'}
