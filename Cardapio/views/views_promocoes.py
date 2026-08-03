from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from Cardapio.models import Produto
from Cardapio.forms.promocoes_form import PromocaoForm
from Cardapio.models import Promocao

@login_required
def listar(request):

    loja = request.user.perfil.loja

    promocoes = Promocao.objects.filter(
        loja=loja
    )

    return render(
        request,
        "promocoes/promocoes_listar.html",
        {
            "promocoes": promocoes
        }
    )

@login_required
def nova(request):

    loja = request.user.perfil.loja


    if request.method == "POST":

        form = PromocaoForm(
            request.POST,
            loja=loja
        )


        if form.is_valid():

            promocao = form.save(
                commit=False
            )


            promocao.loja = loja


            promocao.save()


            messages.success(
                request,
                "Promoção cadastrada com sucesso."
            )


            return redirect(
                "promocoes:listar"
            )


    else:

        form = PromocaoForm(
            loja=loja
        )


    return render(
        request,
        "promocoes/promocoes_form.html",
        {
            "form": form
        }
    )

@login_required
def editar(request, pk):

    loja = request.user.perfil.loja

    promocao = get_object_or_404(
        Promocao,
        pk=pk,
        loja=loja
    )

    if request.method == "POST":

        form = PromocaoForm(
            request.POST,
            instance=promocao,
            loja=loja
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Promoção atualizada com sucesso."
            )

            return redirect("promocoes:listar")

    else:

        form = PromocaoForm(
            instance=promocao,
            loja=loja
        )

    return render(
        request,
        "promocoes/promocoes_form.html",
        {
            "form": form,
            "promocao": promocao
        }
    )

@login_required
def excluir(request, pk):

    loja = request.user.perfil.loja

    promocao = get_object_or_404(
        Promocao,
        pk=pk,
        loja=loja
    )

    promocao.delete()

    messages.success(
        request,
        "Promoção excluída com sucesso."
    )

    return redirect("promocoes:listar")

@login_required
def produto_json(request, pk):

    loja = request.user.perfil.loja

    produto = get_object_or_404(
        Produto,
        pk=pk,
        loja=loja
    )

    return JsonResponse({

        "id": produto.id,
        "nome": produto.nome,
        "preco": float(produto.preco)

    })

@login_required
def pesquisar_produtos(request):

    loja = request.user.perfil.loja

    termo = request.GET.get("q", "")

    produtos = Produto.objects.filter(
        loja=loja,
        disponivel=True,
        nome__icontains=termo
    ).order_by("nome")[:20]

    resultado = []

    for produto in produtos:

        resultado.append({

            "id": produto.id,
            "text": produto.nome,
            "preco": float(produto.preco)

        })

    return JsonResponse(resultado, safe=False)