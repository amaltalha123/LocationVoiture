from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'gestion_manager'
urlpatterns = [

    #url pour voir la page des voitures 
    path('voir_voitures/', views.voir_voitures, name='voir_voitures'),
    path('voitures/ajouter/', views.ajouter_voiture, name='ajouter_voiture'),
    path('voitures/modifier/<str:voiture_id>/', views.modifier_voiture, name='modifier_voiture'),
    path('voitures/supprimer/<str:voiture_id>/', views.supprimer_voiture, name='supprimer_voiture'),

    
    #url pour voir la liste des reservations
    path('liste_reservations/', views.liste_reservations, name='liste_reservations'),
   
   
    #url pour voir la page du dashboard du manager
    path('dashboard_Manager/', views.dashboard_Manager, name='dashboard_Manager'),

    #urls pour voir la liste des voitures du manager connecté
    path('mes-voitures/', views.voitures_manager, name='voitures_manager'),
    path('dashboard_vehicules/', views.dashboard_vehicule, name='dashboard_vehicule'),

    #urls pour ajouter les réservations
    path('ajouter_reservation/<str:voiture_id>/', views.ajouter_reservation, name='ajouter_reservation'),
    path('ajouter_reservation_template/<str:voiture_id>/', views.ajouter_reservation_template, name='ajouter_reservation_template'),
    path('accepter_reservation/<str:reservation_id>/', views.accepter_reservation, name='accepter_reservation'),
    path('refuser_reservation/<str:reservation_id>/', views.refuser_reservation, name='refuser_reservation'),
    path('logout/', LogoutView.as_view(next_page='/accounts/login/'), name='logout'),

]
