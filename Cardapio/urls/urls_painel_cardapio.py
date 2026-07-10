from django.urls import path

from Cardapio.views.views_painel_cardapio import painel_cardapio

app_name = "cardapio"

urlpatterns = [

    path(
        "",
        painel_cardapio,
        name="painel",
    ),

]