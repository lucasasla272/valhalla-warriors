from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Jugador
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


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
    error_messages = {
        "invalid_login": (
            "Ingresá un nombre de guerrero y una contraseña correctos. "
            "Ojo: ambos campos distinguen mayúsculas y minúsculas."
        ),
        "inactive": "Esta cuenta está inactiva.",
    }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {"username": "Nombre de guerrero", "email": "Correo electrónico"}


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = ["avatar", "nivel"]
        labels = {"avatar": "Avatar", "nivel": "Nivel"}


class CambioPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="Contraseña actual", strip=False, widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Contraseña nueva", strip=False, widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirmar contraseña nueva", strip=False, widget=forms.PasswordInput)
        