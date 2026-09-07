import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
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


def alterar_banner(request, id):

    secao = get_object_or_404(
        EstruturaCardapio,
        id=id,
        loja=request.user.perfil.loja,
        tipo="banner"
    )

    if request.method == "POST":

        imagem = request.FILES.get("imagem")

        if imagem:
            secao.imagem = imagem
            secao.save(update_fields=["imagem"])

            messages.success(
                request,
                "Banner atualizado com sucesso."
            )
        else:
            messages.error(
                request,
                "Nenhuma imagem foi selecionada."
            )

    return redirect("estrutura_cardapio:listar")

@require_POST
def salvar_ordem(request):

    try:

        dados = json.loads(
            request.POST.get("secoes", "[]")
        )

        loja = request.user.perfil.loja

        for item in dados:

            secao = EstruturaCardapio.objects.filter(
                id=item["id"],
                loja=loja
            ).first()

            if not secao:
                continue

            secao.ordem = item["ordem"]
            secao.ativo = item["ativo"]

            # Se for banner, verifica se
            # uma nova imagem foi enviada.
            if secao.tipo == "banner":

                imagem = request.FILES.get(
                    f"banner_{secao.id}"
                )

                if imagem:
                    secao.imagem = imagem

            secao.save()

        return JsonResponse({
            "sucesso": True
        })

    except Exception as e:

        return JsonResponse(
            {
                "sucesso": False,
                "mensagem": str(e)
            },
            status=400
        )