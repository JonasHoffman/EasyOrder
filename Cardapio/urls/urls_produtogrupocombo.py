from django.urls import path

from Cardapio.views import views_produtogrupocombo


app_name = "produtogrupocombo"


urlpatterns = [

    path("<int:produto_id>/", views_produtogrupocombo.listar, name="listar"),

    path("<int:produto_id>/adicionar/<int:grupo_id>/", views_produtogrupocombo.adicionar, name="adicionar", ),

    path("editar/<int:pk>/", views_produtogrupocombo.editar, name="editar"),

    path("excluir/<int:pk>/", views_produtogrupocombo.excluir, name="excluir"),

]