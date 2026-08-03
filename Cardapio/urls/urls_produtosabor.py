from django.urls import path
from Cardapio.views import views_produtosabor

app_name = "produtosabor"

urlpatterns = [



    path("", views_produtosabor.listar_produto_sabor, name="listar"),

    path("novo/", views_produtosabor.adicionar_produto_sabor, name="novo"),
    
    path("novo/<int:produto_id>/",views_produtosabor.adicionar_produto_sabor,name="novo_produto"),

    path("<int:id>/excluir/", views_produtosabor.excluir_produto_sabor, name="excluir"),

    path("produto/<int:produto_id>/",views_produtosabor.editar_sabores_produto,name="editar",),

    path("status/<int:produto_id>/",views_produtosabor.alterar_status_produto_sabor,name="status"),
]