from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion_admin.urls')),
    path('', include('gestion_manager.urls')),
    path('', include('landing.urls')),

]
