from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from torneo.forms import LoginFormulario
from . import views
from .forms import RegistroForm, LoginFormulario, CambioPasswordForm

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
    path('login/', auth_views.LoginView.as_view(template_name='torneo/login.html',authentication_form=LoginFormulario,), name='login'),
    path("perfil/", views.editar_perfil, name="editar_perfil"),
    path("perfil/password/", auth_views.PasswordChangeView.as_view(template_name="torneo/cambiar_password.html",form_class=CambioPasswordForm,
                                                                   success_url=reverse_lazy("torneo:password_done"),), name="cambiar_password"),
    path("perfil/password/listo/", auth_views.PasswordChangeDoneView.as_view(template_name="torneo/password_listo.html",), name="password_done"),
]