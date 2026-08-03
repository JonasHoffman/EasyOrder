from django.urls import path

from Cardapio.views import views_produtogrupoadicional


app_name = "produto_grupo_adicional"


urlpatterns = [

    path(
        "",
        views_produtogrupoadicional.listar,
        name="listar"
    ),


    path(
        "novo/",
        views_produtogrupoadicional.novo,
        name="novo"
    ),


    path(
        "editar/<int:pk>/",
        views_produtogrupoadicional.editar,
        name="editar"
    ),


    path(
        "excluir/<int:pk>/",
        views_produtogrupoadicional.excluir,
        name="excluir"
    ),

]