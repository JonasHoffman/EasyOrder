from django.urls import path

from Cardapio.views import views_produtocombogrupoitem

app_name = "produtocombogrupoitem"

urlpatterns = [
    path("<int:grupo_id>/", views_produtocombogrupoitem.listar_itens_grupo, name="listar"),
    path("<int:grupo_id>/novo/", views_produtocombogrupoitem.novo_item_grupo, name="novo"),
    path("<int:pk>/editar/", views_produtocombogrupoitem.editar_item_grupo, name="editar"),
    path("<int:pk>/excluir/", views_produtocombogrupoitem.excluir_item_grupo, name="excluir"),
]