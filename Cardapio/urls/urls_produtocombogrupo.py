from django.urls import path

from Cardapio.views import views_produtocombogrupo


app_name = "produtocombogrupo"

urlpatterns = [
    path("", views_produtocombogrupo.listar_grupos_combo, name="listar"),
    path("novo/", views_produtocombogrupo.novo_grupo_combo, name="novo"),
    path("<int:pk>/editar/", views_produtocombogrupo.editar_grupo_combo, name="editar"),
    path("<int:pk>/excluir/", views_produtocombogrupo.excluir_grupo_combo, name="excluir"),
    path(
        "itens/",
        views_produtocombogrupo.visualizar_grupos_combo,
        name="itens"
    ),
]