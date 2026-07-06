from django.urls import path

from Cardapio.views import views_grupodesabores

app_name = "grupos_sabores"

urlpatterns = [

    path("",views_grupodesabores.listar,name="listar",),
    path("novo/",views_grupodesabores.novo,name="novo",),
    path("<int:id>/", views_grupodesabores.visualizar,name="visualizar",),
    path("<int:id>/editar/",views_grupodesabores.editar,name="editar",),
    path("<int:id>/status/",views_grupodesabores.alterar_status,name="status",),
]