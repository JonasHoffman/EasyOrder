from django.urls import path
from Cardapio.views import views_cardapiocliente


app_name = "cardapio_cliente"


urlpatterns = [

    path(
        "",
        views_cardapiocliente.cardapio_cliente,
        name="cliente"
    ),

]