from django.urls import path

from Cardapio.views.views_sabor import (
    listar_sabores,
    novo_sabor,
    editar_sabor,
    excluir_sabor,
    alterar_status_sabor,
)

app_name = "sabor"

urlpatterns = [
    path("",listar_sabores,name="listar"),
    path("novo/",novo_sabor,name="novo"),
    path("<int:id>/editar/",editar_sabor,name="editar"),
    path("<int:id>/excluir/",excluir_sabor,name="excluir"),
    path("<int:id>/status/",alterar_status_sabor, name="status"
    ),
]