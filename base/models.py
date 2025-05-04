from djongo import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    )
    
    id = models.ObjectIdField(primary_key=True, db_column='_id')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        app_label = 'base'
