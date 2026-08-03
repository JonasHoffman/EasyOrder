from django.urls import path
from Cardapio.views import views_buscas


app_name = "buscas"

urlpatterns = [
    path('', views_buscas.buscar_sugestoes, name='buscar_sugestoes'),
    path("produto-info/<int:produto_id>/",views_buscas.produto_info,name="produto_info"),
]