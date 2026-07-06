from django.urls import path
from Cardapio.views import views_produtos

app_name = "produtos"

urlpatterns = [
    path("produtos", views_produtos.listar_produtos, name="listar"),
    path("produtos_novo/", views_produtos.novo_produto, name="novo"),
    path("produtos/<int:id>/", views_produtos.detalhe_produto, name="detalhe"),
    path("produtos/<int:id>/editar/", views_produtos.editar_produto, name="editar"),
    path("produtos/<int:id>/status/", views_produtos.alterar_status_produto, name="status"),
]