from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from .models import Partido
from django.db.models import Q, Count
from .forms import RegistroForm, UsuarioForm, PerfilForm
from .models import Inscripcion, Juego, Jugador


def home(request):
    return render(request, "torneo/home.html")


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            Jugador.objects.create(user=user, nivel=form.cleaned_data["nivel"])
            messages.success(request, f"¡Bienvenido al Valhalla, {user.username}! Iniciá sesión para entrar a la batalla.")
            return redirect("torneo:login")
    else:
        form = RegistroForm()
    return render(request, "torneo/registro.html", {"form": form})


def lista_juegos(request):
    juegos = Juego.objects.all()
    jugador = getattr(request.user, "jugador", None) if request.user.is_authenticated else None
    mis_ids = []
    if jugador:
        mis_ids = list(
            Inscripcion.objects.filter(jugador=jugador).values_list("juego_id", flat=True)
        )
    return render(request, "torneo/juegos.html",
                  {"juegos": juegos, "mis_ids": mis_ids, "mi_jugador": jugador})

@login_required
def inscribir(request, juego_id):
    if getattr(request.user, "jugador", None) is None:
        messages.error(request, "Tu cuenta no tiene perfil de jugador.")
        return redirect("torneo:juegos")
    juego = get_object_or_404(Juego, pk=juego_id)
    try:
        Inscripcion.objects.create(jugador=request.user.jugador, juego=juego)
        messages.success(request, f"Inscripción confirmada en {juego.nombre}. ¡Éxito en la batalla!")
    except IntegrityError:
        messages.error(request, "Ya estás inscripto en ese juego.")
    return redirect("torneo:juegos")


@login_required
def desinscribir(request, juego_id):
    if getattr(request.user, "jugador", None) is None:
        messages.error(request, "Tu cuenta no tiene perfil de jugador.")
        return redirect("torneo:juegos")
    juego = get_object_or_404(Juego, pk=juego_id)
    Inscripcion.objects.filter(jugador=request.user.jugador, juego=juego).delete()
    messages.success(request, f"Te desinscribiste de {juego.nombre}.")
    return redirect("torneo:juegos")

def tabla_posiciones(request):
    partidos = Partido.objects.select_related("jugador1__user", "jugador2__user")
    filas = {}
    for p in partidos:
        for jugador, gf, gc in ((p.jugador1, p.puntos1, p.puntos2),
                                (p.jugador2, p.puntos2, p.puntos1)):
            f = filas.setdefault(jugador, {"jugador": jugador, "pj": 0, "pg": 0,
                                         "pe": 0, "pp": 0, "pts": 0, "gf": 0, "gc": 0})
            f["pj"] += 1
            f["gf"] += gf
            f["gc"] += gc
            if gf > gc:
                f["pg"] += 1
                f["pts"] += 3
            elif gf == gc:
                f["pe"] += 1
                f["pts"] += 1
            else:
                f["pp"] += 1
    # Desempate: puntos > partidos ganados > puntos a favor > puntos en contra
    tabla = sorted(filas.values(), key=lambda f: (-f["pts"], -f["pg"], -f["gf"], f["gc"]))
    return render(request, "torneo/tabla.html", {"tabla": tabla})

@login_required
def mis_partidos(request):
    jugador = getattr(request.user, "jugador", None)
    if jugador is None:
        messages.error(request, "Tu cuenta no tiene perfil de jugador (es de administrador).")
        return redirect("torneo:home")

    historial = []
    partidos = Partido.objects.filter(
        Q(jugador1=jugador) | Q(jugador2=jugador)
    ).select_related("juego", "jugador1__user", "jugador2__user").order_by("-fecha")
    for p in partidos:
        # Mismo truco de la tabla: mirar el partido desde MI perspectiva
        soy1 = (p.jugador1 == jugador)
        historial.append({
            "juego": p.juego,
            "rival": p.jugador2 if soy1 else p.jugador1,
            "gf": p.puntos1 if soy1 else p.puntos2,
            "gc": p.puntos2 if soy1 else p.puntos1,
            "fecha": p.fecha,
        })

    return render(request, "torneo/mis_partidos.html",
                  {"historial": historial, "jugador": jugador})

def estadisticas(request):
    # 1) Puntos por jugador (misma lógica de la tabla)
    partidos = Partido.objects.select_related("jugador1__user", "jugador2__user")
    filas = {}
    for p in partidos:
        for jugador, gf, gc in ((p.jugador1, p.puntos1, p.puntos2),
                                (p.jugador2, p.puntos2, p.puntos1)):
            f = filas.setdefault(jugador, {"nombre": jugador.user.username, "pts": 0, "pg": 0})
            if gf > gc:
                f["pts"] += 3
                f["pg"] += 1
            elif gf == gc:
                f["pts"] += 1
    orden = sorted(filas.values(), key=lambda f: (-f["pts"], -f["pg"]))
    nombres = [f["nombre"] for f in orden]
    puntos = [f["pts"] for f in orden]

    # 2) Jugadores por nivel (una sola consulta con agregación)
    niveles_qs = Jugador.objects.values("nivel").annotate(total=Count("id"))
    niveles_labels = [dict(Jugador.Nivel.choices)[r["nivel"]] for r in niveles_qs]
    niveles_valores = [r["total"] for r in niveles_qs]

    # 3) Partidos por juego (misma idea, sobre Partido)
    juegos_qs = Partido.objects.values("juego__nombre").annotate(total=Count("id"))
    juegos_labels = [r["juego__nombre"] for r in juegos_qs]
    juegos_valores = [r["total"] for r in juegos_qs]

    return render(request, "torneo/estadisticas.html", {
        "nombres": nombres, "puntos": puntos,
        "niveles_labels": niveles_labels, "niveles_valores": niveles_valores,
        "juegos_labels": juegos_labels, "juegos_valores": juegos_valores,
    })

@login_required
def editar_perfil(request):
    jugador = getattr(request.user, "jugador", None)
    if jugador is None:
        messages.error(request, "Tu cuenta no tiene perfil de jugador.")
        return redirect("torneo:home")

    if request.method == "POST":
        form_u = UsuarioForm(request.POST, instance=request.user)
        form_p = PerfilForm(request.POST, request.FILES, instance=jugador)   # FILES: archivos
        if form_u.is_valid() and form_p.is_valid():
            form_u.save()
            form_p.save()
            messages.success(request, "Perfil actualizado, guerrero.")
            return redirect("torneo:editar_perfil")
    else:
        form_u = UsuarioForm(instance=request.user)
        form_p = PerfilForm(instance=jugador)

    return render(request, "torneo/editar_perfil.html",
                  {"form_u": form_u, "form_p": form_p, "jugador": jugador})