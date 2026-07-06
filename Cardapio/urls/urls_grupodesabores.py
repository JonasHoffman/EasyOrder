from django.urls import path

from Cardapio.views import views_grupodesabores

app_name = "grupos_sabores"

urlpatterns = [

    path("grupodesabores/",views_grupodesabores.listar,name="listar",),
    path("grupodesabores/novo/",views_grupodesabores.novo,name="novo",),
    path("grupodesabores/<int:id>/", views_grupodesabores.visualizar,name="visualizar",),
    path("grupodesabores/<int:id>/editar/",views_grupodesabores.editar,name="editar",),
    path("grupodesabores/<int:id>/status/",views_grupodesabores.alterar_status,name="status",),
]