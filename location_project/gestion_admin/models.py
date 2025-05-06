from mongoengine import Document, StringField, EmailField

class Manager(Document):
    nom = StringField(required=True)
    prenom = StringField(required=True)
    email = EmailField(required=True, unique=True)
    telephone = StringField()
    agence = StringField()
