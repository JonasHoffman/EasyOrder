from django.urls import path
from Cardapio.views import views_sabor


app_name = "sabor"

urlpatterns = [
    path("",views_sabor.listar_sabores,name="listar"),
    path("novo/",views_sabor.novo_sabor,name="novo"),
    path("<int:id>detalhe/",views_sabor.detalhe,name="detalhe",),
    path("<int:id>/editar/",views_sabor.editar_sabor,name="editar"),
    path("<int:id>/status/",views_sabor.alterar_status_sabor, name="status"
    ),
]