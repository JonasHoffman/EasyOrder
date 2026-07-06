from django.urls import path
from Cardapio.views import views_produtos

app_name = "produtos"

urlpatterns = [
    path("", views_produtos.listar_produtos, name="listar"),
    path("novo/", views_produtos.novo_produto, name="novo"),
    path("<int:id>/", views_produtos.detalhe_produto, name="detalhe"),
    path("<int:id>/editar/", views_produtos.editar_produto, name="editar"),
    path("<int:id>/status/", views_produtos.alterar_status_produto, name="status"),
]