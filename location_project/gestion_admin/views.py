from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect
from gestion_manager.models import Manager
from .forms import CustomUserCreationForm
from landing.thread_local import set_raw_password
from django.contrib.auth.decorators import login_required
from mongoengine.errors import NotUniqueError


def liste_managers(request):
    managers = Manager.objects.all()
    return render(request, 'gestion_admin/liste_managers.html', {'managers': managers})


def ajouter_manager(request):
    if request.method == 'POST':
        try:
            Manager(
                username=request.POST['email'],
                email=request.POST['email'],
                password=request.POST['password'],
                role='manager',
                nom=request.POST['nom'],         # Ajouté ici
                prenom=request.POST['prenom'],   # Ajouté ici
                telephone=request.POST.get('telephone', ''),
                agence=request.POST.get('agence', '')
            ).save()
            return redirect('gestion_admin:liste_managers')
        except NotUniqueError:
            return render(request, 'gestion_admin/ajouter_manager.html', {
                'error': "Cet email est déjà utilisé."
            })
        except ValidationError as e:
            return render(request, 'gestion_admin/ajouter_manager.html', {
                'error': f"Erreur de validation : {e}"
            })
    return render(request, 'gestion_admin/ajouter_manager.html')


def modifier_manager(request, manager_id):
    try:
        manager = Manager.objects.get(id=manager_id)
    except Manager.DoesNotExist:
        raise Http404("Manager non trouvé")

    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        agence = request.POST.get('agence')
        password = request.POST.get('password')  # Pas obligatoire

        manager.nom = nom
        manager.prenom = prenom
        manager.email = email
        manager.telephone = telephone
        manager.agence = agence

        if password:
            # adapter selon ta méthode de gestion des mots de passe
            manager.set_password(password)

        manager.save()
        return redirect('gestion_admin:liste_managers')

    return render(request, 'gestion_admin/modifier_manager.html', {'manager': manager})


def supprimer_manager(request, manager_id):
    try:
        manager = Manager.objects.get(id=manager_id)
    except Manager.DoesNotExist:
        raise Http404("Manager non trouvé")
    manager.delete()
    return redirect('gestion_admin:liste_managers')


def add_manager(request):
    form = CustomUserCreationForm()
    return render(request, 'gestion_admin/register_user.html', {'form': form})


@login_required(login_url='login')
def register_user(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return HttpResponseForbidden("Accès refusé : vous n'avez pas les droits pour accéder à cette page.")

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            set_raw_password(form.cleaned_data['password'])
            form.save()
            return redirect('gestion_admin:liste_managers')
    else:
        form = CustomUserCreationForm()
    return render(request, 'gestion_admin/register_user.html', {'form': form})


def admin_dashboard(request):
    form = CustomUserCreationForm()
    return render(request, 'gestion_admin/admin_dashboard.html', {'form': form})
