from django.urls import path

from Cardapio.views import views_ingredientes


app_name = "ingredientes"

urlpatterns = [
    path("", views_ingredientes.ingrediente_listar, name="listar"),
    path("novo/", views_ingredientes.ingrediente_novo, name="novo"),
    path("<int:pk>/editar/", views_ingredientes.ingrediente_editar, name="editar"),
    path("<int:pk>/excluir/", views_ingredientes.ingrediente_excluir, name="excluir"),
    path("<int:id>/ingredientes/",views_ingredientes.produto_ingredientes,name="ingredientes"),
]