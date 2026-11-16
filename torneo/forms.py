from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Jugador


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    nivel = forms.ChoiceField(choices=Jugador.Nivel.choices, label="Nivel")
    # Redeclarados para pisar el label/ayuda en inglés que traen por defecto
    password1 = forms.CharField(label="Contraseña", strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", strip=False, widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
        labels = {"username": "Nombre de guerrero"}
        help_texts = {"username": None}


class LoginFormulario(AuthenticationForm):
    username = forms.CharField(label="Nombre de guerrero")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)