from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomLoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    role = forms.ChoiceField(
        choices=[('admin', 'Admin'), ('manager', 'Manager')],
        label="Rôle"
    )

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('admin', 'Admin'), ('manager', 'Manager')])

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')