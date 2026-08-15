from django.urls import path
from Cardapio.views import views_combo

app_name = "combos"

urlpatterns = [
    path("", views_combo.listar_combo, name="listar"),
    path("novo/", views_combo.novo_combo, name="novo"),
    path("<int:pk>/editar/", views_combo.editar_combo, name="editar"),
    path("<int:pk>/excluir/", views_combo.excluir_combo, name="excluir"),
]
