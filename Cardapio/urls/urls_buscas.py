from django.urls import path
from Cardapio.views import views_buscas


app_name = "buscas"

urlpatterns = [
    path('', views_buscas.buscar_sugestoes, name='buscar_sugestoes'),
]