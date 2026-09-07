from django.urls import path

from Pedidos import views


app_name = "pedidos"


urlpatterns = [

    path(
        "finalizar/",
        views.finalizar_pedido,
        name="finalizar_pedido"
    ),

    path(
        "sucesso/<int:pedido_id>/",
        views.pedido_sucesso,
        name="pedido_sucesso"
    ),

    path(
        "kanban/",
        views.kanban_pedidos,
        name="kanban"
    ),
    path(
    "kanban/alterar-status/",
    views.alterar_status,
    name="kanban_alterar_status"),

    path(
        "status/",
        views.status_lista,
        name="status_lista"
    ),

    path(
        "status/novo/",
        views.status_criar,
        name="status_criar"
    ),

    path(
        "status/<int:pk>/editar/",
        views.status_editar,
        name="status_editar"
    ),

    path(
        "status/<int:pk>/excluir/",
        views.status_excluir,
        name="status_excluir"
    ),


    

    
]