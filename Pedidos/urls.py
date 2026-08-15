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
    

    
]