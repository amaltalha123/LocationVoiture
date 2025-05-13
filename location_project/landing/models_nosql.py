from mongoengine import Document, StringField, EmailField

class Manager(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True)
    password = StringField(required=True)
    role = StringField(default='manager')
    meta = {'collection': 'manager'}