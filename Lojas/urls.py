from django.urls import path,include
from . import views

app_name = "lojas"

urlpatterns = [
    path("", views.lista_lojas, name="lista"),
    path("nova/", views.nova_loja, name="nova"),
    path("<int:pk>/editar/", views.editar_loja, name="editar"),
    path("<int:pk>/", views.detalhe_loja, name="detalhes"),
]