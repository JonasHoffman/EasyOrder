from Cardapio.models import Categoria
from django.shortcuts import render


def secao_categorias(request):

    loja = request.user.perfil.loja


    categorias = Categoria.objects.filter(
        loja=loja,
        ativo=True
    )


    return render(
        request,
        "cardapio/secoes/categorias.html",
        {
            "categorias": categorias
        }
    )