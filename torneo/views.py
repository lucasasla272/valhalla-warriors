from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegistroForm
from .models import Inscripcion, Juego, Jugador


def home(request):
    return render(request, "torneo/home.html")


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            Jugador.objects.create(user=user, nivel=form.cleaned_data["nivel"])
            return redirect("torneo:login")
    else:
        form = RegistroForm()
    return render(request, "torneo/registro.html", {"form": form})


def lista_juegos(request):
    juegos = Juego.objects.all()
    mis_ids = []
    if request.user.is_authenticated:
        mis_ids = list(
            Inscripcion.objects.filter(jugador=request.user.jugador)
            .values_list("juego_id", flat=True)
        )
    return render(request, "torneo/juegos.html",
                  {"juegos": juegos, "mis_ids": mis_ids})


@login_required
def inscribir(request, juego_id):
    juego = get_object_or_404(Juego, pk=juego_id)
    try:
        Inscripcion.objects.create(jugador=request.user.jugador, juego=juego)
        messages.success(request, f"Inscripción confirmada en {juego.nombre}. ¡Éxito en la batalla!")
    except IntegrityError:
        messages.error(request, "Ya estás inscripto en ese juego.")
    return redirect("torneo:juegos")


@login_required
def desinscribir(request, juego_id):
    juego = get_object_or_404(Juego, pk=juego_id)
    Inscripcion.objects.filter(jugador=request.user.jugador, juego=juego).delete()
    messages.success(request, f"Te desinscribiste de {juego.nombre}.")
    return redirect("torneo:juegos")