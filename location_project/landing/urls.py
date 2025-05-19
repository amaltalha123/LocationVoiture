from django.urls import path , include
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views


app_name = 'landing'

urlpatterns = [
    #Pour la page d'acceuill
    path('landing/', views.landing_page, name='landing_page'),

    path('indexpage/', views.index_page, name='index_page'),
    path('contactpage/', views.contact_page, name='contact_page'),
    path('servicepage/', views.service_page, name='service_page'),
    path('aboutpage/', views.about_page, name='about_page'),

    #Pour la connexion
    path('accounts/login/', views.login_page, name='login'),
    path('loginUser/', views.login_view, name='login_view'),
    path("deux/", views.deux , name="deux"), 

    # Pour le login/logout
    path("accounts/", include("django.contrib.auth.urls")),  

    #Pour retourner la page du manager
    path("manager/", views.Manager_page, name="Manager_page"),

    #Pour retourner la page de l'admin
    path("adminpage/", views.Admin_page, name="Admin_page")
    
]
