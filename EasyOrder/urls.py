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
    path('admin/', admin.site.urls),
    path('lojas/', include('Lojas.urls')),
    path('cardapio/', include('Cardapio.urls')),
    path("cardapio/categorias/",include(("Cardapio.urls.urls_categorias", "categorias"), namespace="categorias"),),
    path("cardapio/produto/",include(("Cardapio.urls.urls_produtos", "produtos"), namespace="produtos"),),
    path("cardapio/grupodesabores/",include(("Cardapio.urls.urls_grupodesabores", "grupodesabores"), namespace="grupodesabores"),),
    path("cardapio/sabor/",include(("Cardapio.urls.urls_sabor", "sabor"), namespace="sabor"),),
    path("cardapio/grupoadicional/",include(("Cardapio.urls.urls_grupoadicional", "grupoadicional"), namespace="grupoadicional"),),
    path("cardapio/itemadicional/",include(("Cardapio.urls.urls_itemadicional", "sabor"), namespace="itemadicional"),),
    path("cardapio/painel_cardapio/",include(("Cardapio.urls.urls_painel_cardapio", "painel_cardapio"), namespace="painel_cardapio"),),
    path("cardapio/estrutura_cardapio/",include(("Cardapio.urls.urls_estruturacardapio", "estrutura_cardapio"), namespace="estrutura_cardapio"),),
    path("cardapio/cardapio_cliente/",include(("Cardapio.urls.urls_cardapiocliente", "cardapio_cliente"), namespace="cardapio_cliente"),),




    ]  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

