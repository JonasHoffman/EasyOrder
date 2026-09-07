"""
URL configuration for EasyOrder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("cardapio/sabor/",include(("Cardapio.urls.urls_sabor", "sabor"), namespace="sabor"),),##
    path('', include('Interface.urls')),
    path('admin/', admin.site.urls),
    path('lojas/', include('Lojas.urls')),
    path('usuarios/', include('Usuarios.urls')),

    path('cardapio/', include('Cardapio.urls')),
    path("cardapio/categorias/",include(("Cardapio.urls.urls_categorias", "categorias"), namespace="categorias"),), ##
    path("cardapio/produto/",include(("Cardapio.urls.urls_produtos", "produtos"), namespace="produtos"),),##
    path("cardapio/grupodesabores/",include(("Cardapio.urls.urls_grupodesabores", "grupodesabores"), namespace="grupodesabores"),),##
    
    path("cardapio/produtogruposabor/",include(("Cardapio.urls.urls_produtogruposabor", "produtogruposabor"), namespace="produtogruposabor"),),#
    path("cardapio/grupoadicional/",include(("Cardapio.urls.urls_grupoadicional", "grupoadicional"), namespace="grupoadicional"),),##
    path("cardapio/itemadicional/",include(("Cardapio.urls.urls_itemadicional", "sabor"), namespace="itemadicional"),),##
    path("cardapio/painel_cardapio/",include(("Cardapio.urls.urls_painel_cardapio", "painel_cardapio"), namespace="painel_cardapio"),),
    path("cardapio/estrutura_cardapio/",include(("Cardapio.urls.urls_estruturacardapio", "estrutura_cardapio"), namespace="estrutura_cardapio"),),
    path("cardapio/cardapio_cliente/",include(("Cardapio.urls.urls_cardapiocliente", "cardapio_cliente"), namespace="cardapio_cliente"),),
    path("cardapio/promocoes/",include(("Cardapio.urls.urls_promocoes", "promocoes"), namespace="promocoes"),), ##
    path("cardapio/buscar/",include(("Cardapio.urls.urls_buscas", "buscas"), namespace="buscas"),),
    path("cardapio/carrinho/",include(("Cardapio.urls.urls_carrinho", "carrinho"), namespace="carrinho"),),
    path("cardapio/ingredientes/",include(("Cardapio.urls.urls_ingredientes", "ingredientes"), namespace="ingredientes"),),##
    path("cardapio/produtosabor/",include(("Cardapio.urls.urls_produtosabor", "produtosabor"), namespace="produtosabor"),),#
    path("cardapio/saboringrediente/",include(("Cardapio.urls.urls_saboringrediente", "saboringrediente"), namespace="saboringrediente"),),##
    path("cardapio/produtogrupoadicional/",include(("Cardapio.urls.urls_produtogrupoadicional", "produtogrupoadicional"), namespace="produtogrupoadicional"),),##
    path("cardapio/produtoingrediente/",include(("Cardapio.urls.urls_produtoingrediente", "produtoingrediente"), namespace="produtoingrediente"),),##
    path("cardapio/combo/",include(("Cardapio.urls.urls_combo", "combo"), namespace="combo"),),##
    path("cardapio/produtocombogrupo/",include(("Cardapio.urls.urls_produtocombogrupo", "produtocombogrupo"), namespace="produtocombogrupo"),),##
    path("cardapio/produtocombogrupoitem/",include(("Cardapio.urls.urls_produtocombogrupoitem", "produtocombogrupoitem"), namespace="produtocombogrupoitem"),),##
    path("cardapio/produtogrupocombo/",include(("Cardapio.urls.urls_produtogrupocombo", "produtogrupocombo"), namespace="produtogrupocombo"),),
    path("pedidos/",include(("Pedidos.urls", "pedidos"), namespace="pedidos"),),
    path("pagamento/",include(("Pagamento.urls", "pagamento"), namespace="pagamento"),),

    















    ]  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

