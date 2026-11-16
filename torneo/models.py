from django.contrib.auth.models import User
from django.db import models


class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Jugador(models.Model):
    class Nivel(models.TextChoices):
        AMATEUR = "AMATEUR", "Amateur"
        NORMAL = "NORMAL", "Normal"
        EXPERTO = "EXPERTO", "Experto"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="jugador")
    nivel = models.CharField(max_length=10, choices=Nivel.choices, default=Nivel.NORMAL)

    def __str__(self):
        return self.user.username


class Inscripcion(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name="inscripciones")
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name="inscripciones")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("jugador", "juego")
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.jugador} en {self.juego}"


class Partido(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name="partidos")
    jugador1 = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name="partidos_local")
    jugador2 = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name="partidos_visitante")
    puntos1 = models.PositiveIntegerField()
    puntos2 = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.jugador1} {self.puntos1} - {self.puntos2} {self.jugador2}"
    