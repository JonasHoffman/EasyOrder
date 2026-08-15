from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from Cardapio.models import (
    Ingrediente,
    Produto,
    ProdutoIngrediente,
)

from Cardapio.forms.ingredientes_form import IngredienteForm

from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def selecionar_produto_ingredientes(request):

    loja = request.user.perfil.loja

    busca = request.GET.get("busca", "")

    produtos = Produto.objects.filter(
        loja=loja
    ).order_by(
        "nome"
    )

    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca)
        )

    if request.method == "POST":

        produto_id = request.POST.get("produto")

        if produto_id:
            return redirect(
                "produtos:ingredientes",
                id=produto_id
            )

        messages.error(
            request,
            "Selecione um produto."
        )

    return render(
        request,
        "produtoingrediente/produtoingrediente_listar.html",
        {
            "produtos": produtos,
            "busca": busca,
        }
    )