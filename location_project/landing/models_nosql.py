from mongoengine import Document, StringField, EmailField
from django.contrib.auth.models import User

class Manager(Document):
    
    username = StringField(required=True, unique=True)
    nom = StringField(required=True)
    prenom = StringField(required=True)
    telephone = StringField()
    agence = StringField()
    email = EmailField(required=True)
    password = StringField(required=True)
    role = StringField(default='manager')
    meta = {'collection': 'manager'}
