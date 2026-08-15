from django.urls import path
from Cardapio.views import views_produtoingrediente


app_name = "produtoingrediente"

urlpatterns = [
    path("",
    views_produtoingrediente.selecionar_produto_ingredientes,
    name="selecionar_produto_ingredientes",
),
]