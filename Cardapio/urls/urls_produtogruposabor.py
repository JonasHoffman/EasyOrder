from django.urls import path

from Cardapio.views import views_produtogruposabor


app_name = "produtogruposabor"


urlpatterns = [

    # Lista produtos e seus grupos
    path(
        "",
        views_produtogruposabor.listar_produto_grupo_sabor,
        name="listar"
    ),

    # Adicionar grupos sem produto na URL
    path(
        "novo/",
        views_produtogruposabor.adicionar_produto_grupo_sabor,
        name="novo"
    ),

    # Adicionar grupos diretamente para um produto
    path(
        "novo/<int:produto_id>/",
        views_produtogruposabor.adicionar_produto_grupo_sabor,
        name="novo_produto"
    ),

    # Editar grupos de um produto
    path(
        "editar/<int:produto_id>/",
        views_produtogruposabor.editar_grupos_produto,
        name="editar"
    ),

    # Excluir vínculo ProdutoGrupoSabor
    path(
        "excluir/<int:id>/",
        views_produtogruposabor.excluir_produto_grupo_sabor,
        name="excluir"
    ),

    # Alterar disponibilidade do produto
    path(
        "status/<int:produto_id>/",
        views_produtogruposabor.alterar_status_produto_grupo_sabor,
        name="status"
    ),
]