# landing/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from .models_nosql import Manager as MongoManager
from landing.thread_local import get_raw_password, clear_raw_password
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=CustomUser)
def create_manager_in_mongo(sender, instance, created, **kwargs):
    if created and instance.role == 'manager':
        raw_password = get_raw_password()
        clear_raw_password()
        # Créer un document MongoEngine
        MongoManager.objects.create(
            username=instance.username,
            email=instance.email,
            password=instance.password
        )
        # Contenu de l'e-mail
        subject = 'Bienvenue sur notre plateforme RentCar'
        message = f"""
Bonjour {instance.username},

Votre compte a été créé avec succès avec les informations suivantes :

Nom d'utilisateur : {instance.username}
Email : {instance.email}
Rôle : {instance.role}
Mot de passe : {raw_password if raw_password else 'Indisponible'}

Merci de rejoindre notre plateforme.

Cordialement,
L’équipe d'administration
        """

        # Envoyer l'e-mail
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,   # From
            [instance.email],           # To
            fail_silently=False
        )