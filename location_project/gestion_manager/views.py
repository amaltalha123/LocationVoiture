from django.shortcuts import render
from .models import Reservation

def liste_reservations(request):
    reservations = Reservation.objects.select_related()
    return render(request, 'liste_reservations.html', {
        'reservations': reservations
    })
