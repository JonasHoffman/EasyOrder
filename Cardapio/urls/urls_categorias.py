from django.urls import path
from Cardapio.views import views_categorias

app_name = "categorias"

urlpatterns = [
    path("", views_categorias.listar_categorias, name="listar"),
    path("nova/", views_categorias.nova_categoria, name="novo"),
    path("<int:id>/", views_categorias.detalhe_categoria, name="detalhe"),
    path("<int:id>/editar/", views_categorias.editar_categoria, name="editar"),
    path("<int:id>/status/", views_categorias.alterar_status_categoria, name="status"),
    path('categoria/<slug:slug>/', views_categorias.categoria_detalhe, name='categoria_detalhe'),
]