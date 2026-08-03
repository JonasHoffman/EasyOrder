from django.urls import path

from Cardapio.views import views_saboringrediente


app_name = "saboringrediente"


urlpatterns = [

    path("<int:sabor_id>/", views_saboringrediente.listar_ingredientes_sabor, name="listar"),
    path("novo/<int:sabor_id>/", views_saboringrediente.adicionar_ingrediente_sabor, name="novo"),
    path("editar/<int:id>/", views_saboringrediente.editar_ingrediente_sabor, name="editar"),
    path("excluir/<int:id>/", views_saboringrediente.excluir_ingrediente_sabor, name="excluir"),
    path("status/<int:id>/", views_saboringrediente.status_ingrediente_sabor, name="status"),

]