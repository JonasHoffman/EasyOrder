from django.urls import path

from Cardapio.views import views_itemadicional


app_name = "item_adicional"

urlpatterns = [
    path("", views_itemadicional.listar_item_adicional, name="listar"),
    path("novo/", views_itemadicional.novo_item_adicional, name="novo"),
    path("editar/<int:id>/", views_itemadicional.editar_item_adicional, name="editar"),
    path("excluir/<int:id>/", views_itemadicional.excluir_item_adicional, name="excluir"),
    path("status/<int:id>/", views_itemadicional.alterar_status_item_adicional, name="status"),
]