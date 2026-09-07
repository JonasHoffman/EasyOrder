from django.urls import path
from Usuarios import views

app_name = "usuarios"

urlpatterns = [
    path(
        "login/",
        views.login_usuario,
        name="login"
    ),
]