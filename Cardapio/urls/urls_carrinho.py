from django.urls import path

from Cardapio.views import views_carrinho


app_name = "carrinho"

urlpatterns = [
    path('', views_carrinho.carrinho_detalhe, name='carrinho_detalhe'),
    path('adicionar/<int:produto_id>/', views_carrinho.carrinho_adicionar, name='carrinho_adicionar'),
    path('remover/', views_carrinho.carrinho_remover, name='carrinho_remover'),
    # path('atualizar/<int:produto_id>/', views_carrinho.carrinho_atualizar, name='carrinho_atualizar'),
    path('widget/', views_carrinho.carrinho_widget, name='carrinho_widget'),
]