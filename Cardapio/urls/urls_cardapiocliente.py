from django.urls import path
from Cardapio.views import views_cardapiocliente


app_name = "cardapio_cliente"


urlpatterns = [

    path(
        "<slug:slug>/",
        views_cardapiocliente.cardapio_cliente,
        name="cliente"
    ),
    path(
        "secao/<str:tipo>/",
        views_cardapiocliente.ver_todos,
        name="ver_todos"
    ),

]