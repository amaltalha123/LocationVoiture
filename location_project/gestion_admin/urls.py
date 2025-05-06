from django.urls import path
from . import views

urlpatterns = [
    path('managers/', views.liste_managers, name='liste_managers'),
    path('managers/ajouter/', views.ajouter_manager, name='ajouter_manager'),
    path('managers/modifier/<str:manager_id>/', views.modifier_manager, name='modifier_manager'),
    path('managers/supprimer/<str:manager_id>/', views.supprimer_manager, name='supprimer_manager'),
]
