from django.urls import path

from Cardapio.views import views_estruturacardapio


app_name = "estrutura_cardapio"

urlpatterns = [

    path(
        "",
        views_estruturacardapio.listar,
        name="listar"
    ),

    path(
        "salvar/",
        views_estruturacardapio.salvar_ordem,
        name="salvar"
    ),

]