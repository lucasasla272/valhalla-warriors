from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Jugador


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nivel = forms.ChoiceField(choices=Jugador.Nivel.choices)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", "nivel")