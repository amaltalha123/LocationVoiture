
from django.urls import path , include
from . import views 
from .views import  home

urlpatterns = [
    path("", views.home, name="homepage"),  # Page d'accueil
    path("manager/", views.manager_page, name="manager_page"),
    path("voitures/", views.voitures_page, name="voitures_page"),
    path("deux/", views.deux , name="deux"),  # pas de template, redirige seulement
    path("accounts/", include("django.contrib.auth.urls")),  # Pour le login/logout
]