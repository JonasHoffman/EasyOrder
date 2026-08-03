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
def ingrediente_listar(request):

    loja = request.user.perfil.loja

    busca = request.GET.get("busca", "")
    status = request.GET.get("status", "")

    ingredientes = Ingrediente.objects.filter(
        loja=loja
    )

    if busca:
        ingredientes = ingredientes.filter(
            Q(nome__icontains=busca)
        )

    if status == "ativo":
        ingredientes = ingredientes.filter(
            ativo=True
        )

    elif status == "inativo":
        ingredientes = ingredientes.filter(
            ativo=False
        )

    ingredientes = ingredientes.order_by(
        "ordem",
        "nome"
    )

    return render(
        request,
        "ingredientes/ingredientes_listar.html",
        {
            "ingredientes": ingredientes,
            "total": ingredientes.count(),
        }
    )


@login_required
def ingrediente_novo(request):

    form = IngredienteForm(
        request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            ingrediente = form.save(
                commit=False
            )

            ingrediente.loja = request.user.perfil.loja

            ingrediente.save()

            messages.success(
                request,
                "Ingrediente cadastrado com sucesso."
            )

            return redirect(
                "ingredientes:listar"
            )

    return render(
        request,
        "ingredientes/ingredientes_form.html",
        {
            "form": form
        }
    )


@login_required
def ingrediente_editar(request, pk):

    ingrediente = get_object_or_404(
        Ingrediente,
        pk=pk,
        loja=request.user.perfil.loja
    )

    form = IngredienteForm(
        request.POST or None,
        instance=ingrediente
    )

    if request.method == "POST":

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Ingrediente atualizado com sucesso."
            )

            return redirect(
                "ingredientes:listar"
            )

    return render(
        request,
        "ingredientes/ingredientes_form.html",
        {
            "form": form,
            "ingrediente": ingrediente
        }
    )


@login_required
def ingrediente_excluir(request, pk):

    ingrediente = get_object_or_404(
        Ingrediente,
        pk=pk,
        loja=request.user.perfil.loja
    )

    if request.method == "POST":

        ingrediente.delete()

        messages.success(
            request,
            "Ingrediente excluído com sucesso."
        )

    return redirect(
        "ingredientes:listar"
    )


@login_required
def produto_ingredientes(request, id):

    produto = get_object_or_404(
        Produto,
        id=id,
        loja=request.user.perfil.loja
    )

    ingredientes = Ingrediente.objects.filter(
        loja=request.user.perfil.loja,
        ativo=True
    ).order_by(
        "ordem",
        "nome"
    )

    if request.method == "POST":

        ingredientes_ids = request.POST.getlist(
            "ingredientes"
        )

        if not ingredientes_ids:

            messages.error(
                request,
                "Selecione pelo menos um ingrediente para o produto."
            )

            return redirect(
                "produtos:ingredientes",
                id=produto.id
            )

        ProdutoIngrediente.objects.filter(
            produto=produto
        ).delete()

        for ingrediente in ingredientes:

            if str(ingrediente.id) in ingredientes_ids:

                ProdutoIngrediente.objects.create(
                    produto=produto,
                    ingrediente=ingrediente,
                    permite_remocao=(
                        f"removivel_{ingrediente.id}" in request.POST
                    )
                )

        messages.success(
            request,
            "Ingredientes salvos com sucesso."
        )

        return redirect(
            "produtos:listar"
        )

    relacionados = ProdutoIngrediente.objects.filter(
        produto=produto
    )

    selecionados = {}

    for relacionamento in relacionados:

        selecionados[
            relacionamento.ingrediente_id
        ] = relacionamento

    for ingrediente in ingredientes:

        relacionamento = selecionados.get(
            ingrediente.id
        )

        ingrediente.selecionado = (
            relacionamento is not None
        )

        ingrediente.removivel = (
            relacionamento.permite_remocao
            if relacionamento
            else False
        )

    return render(
        request,
        "ingredientes/ingredientes_produto.html",
        {
            "produto": produto,
            "ingredientes": ingredientes,
        }
    )