from django.contrib import admin
from .models import Juego, Jugador, Inscripcion, Partido


@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "genero")
    search_fields = ("nombre", "genero")


@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ("user", "nivel")
    list_filter = ("nivel",)
    search_fields = ("user__username",)


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ("jugador", "juego", "fecha")
    list_filter = ("juego",)


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ("juego", "jugador1", "puntos1", "puntos2", "jugador2", "fecha")
    list_filter = ("juego", "fecha")