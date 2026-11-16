from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "torneo"

urlpatterns = [
    path("", views.home, name="home"),
    path("registro/", views.registro, name="registro"),
    path("login/", auth_views.LoginView.as_view(template_name="torneo/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("juegos/", views.lista_juegos, name="juegos"),
    path("juegos/<int:juego_id>/inscribir/", views.inscribir, name="inscribir"),
    path("juegos/<int:juego_id>/desinscribir/", views.desinscribir, name="desinscribir"),
    path("tabla/", views.tabla_posiciones, name="tabla"),
    path("mis-partidos/", views.mis_partidos, name="mis_partidos"),
    path("estadisticas/", views.estadisticas, name="estadisticas"),
]