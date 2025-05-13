from mongoengine import Document, StringField, EmailField
from landing.models_nosql import Manager 

class Admin(Document):
    nom = StringField(required=True)
    prenom = StringField(required=True)
    email = EmailField(required=True, unique=True)
    telephone = StringField()
    password = StringField(required=True)

