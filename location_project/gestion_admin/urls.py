from django.urls import path
from . import views


app_name = 'gestion_admin'

urlpatterns = [
    path('managers/', views.liste_managers, name='liste_managers'),
    path('managers/ajouter/', views.ajouter_manager, name='ajouter_manager'),
    path('managers/modifier/<str:manager_id>/', views.modifier_manager, name='modifier_manager'),
    path('managers/supprimer/<str:manager_id>/', views.supprimer_manager, name='supprimer_manager'),
    
    path('registerManager/', views.register_user, name='register_user'),
    path('addManager/', views.add_manager, name='add_manager'),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard')
]
