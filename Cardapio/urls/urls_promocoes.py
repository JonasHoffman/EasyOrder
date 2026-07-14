from django.urls import path

from Cardapio.views import views_promocoes

app_name = "promocoes"

urlpatterns = [

    path("", views_promocoes.listar, name="listar"),

    path("nova/", views_promocoes.nova, name="nova"),

    path("editar/<int:pk>/", views_promocoes.editar, name="editar"),

    path("excluir/<int:pk>/", views_promocoes.excluir, name="excluir"),

    path("produto/<int:pk>/", views_promocoes.produto_json, name="produto_json"),

    path("pesquisar-produtos/", views_promocoes.pesquisar_produtos, name="pesquisar_produtos"),

]