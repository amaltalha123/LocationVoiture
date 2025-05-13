from django.urls import path
from . import views

app_name = 'gestion_manager'
urlpatterns = [

    #url pour voir la page des voitures 
    path('voir_voitures/', views.voir_voitures, name='voir_voitures'),

    #url pour voir la liste des réservation
    path('reservations/', views.liste_reservations, name='liste_reservations'),
    
    #url pour voir la page des reservations
    path('reservations_page/', views.reservations_page, name='reservations_page'),

    #url pour voir la liste des reservations
    path('liste_reservations/', views.liste_reservations, name='liste_reservations'),
   
   
    #url pour voir la page du dashboard du manager
    path('dashboard_Manager/', views.dashboard_Manager, name='dashboard_Manager'),

    #url pour voir la liste des voitures du manager connecté
    path('mes-voitures/', views.voitures_manager, name='voitures_manager')
]
