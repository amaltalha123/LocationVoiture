from django.urls import path
from . import views

urlpatterns = [
    path('reservations/', views.liste_reservations, name='liste_reservations'),
]
