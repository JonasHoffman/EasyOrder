from django.urls import path

from Cardapio.views import views_grupoadicional

app_name = "grupos_adicionais"

urlpatterns = [
    path("",views_grupoadicional.listar_grupos_adicionais,name="listar"),
    path("novo/",views_grupoadicional.novo_grupo_adicional,name="novo"),
    path("editar/<int:id>/",views_grupoadicional.editar_grupo_adicional,name="editar"),
    path("status/<int:id>/",views_grupoadicional.alterar_status_grupo_adicional,name="status"),

]