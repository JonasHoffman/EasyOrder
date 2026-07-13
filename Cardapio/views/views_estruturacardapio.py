import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from Cardapio.models import EstruturaCardapio

def listar(request):

    secoes = EstruturaCardapio.objects.filter(
        loja=request.user.perfil.loja
    )

    return render(
        request,
        "estruturacardapio/estruturacardapio_listar.html",
        {
            "secoes": secoes
        }
    )


@require_POST
def salvar_ordem(request):

    dados = json.loads(request.body)

    for indice, item in enumerate(dados):

        EstruturaCardapio.objects.filter(
            id=item["id"],
            loja=request.user.perfil.loja
        ).update(
            ordem=indice + 1,
            ativo=item["ativo"]
        )

    return JsonResponse(
        {
            "sucesso": True
        }
    )