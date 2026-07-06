from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Cardapio.models import Produto
from Cardapio.forms.produtos_form import ProdutoForm




@login_required
def listar_produtos(request):

    produtos = Produto.objects.filter(
        loja=request.user.perfil.loja
    ).select_related("categoria").order_by("ordem", "nome")

    return render(request, "produtos/produtos_listar.html", {
        "produtos": produtos
    })


@login_required
def novo_produto(request):

    form = ProdutoForm(request.POST or None, request.FILES or None)

    if request.method == "POST":

        if form.is_valid():
            produto = form.save(commit=False)

            produto.loja = request.user.perfil.loja
            produto.save()

            messages.success(request, "Produto criado com sucesso!")
            return redirect("produtos:listar")

    return render(request, "produtos/produtos_form.html", {
        "form": form,
        "titulo": "Novo Produto"
    })


@login_required
def editar_produto(request, id):

    produto = get_object_or_404(
        Produto,
        id=id,
        loja=request.user.perfil.loja
    )

    form = ProdutoForm(
        request.POST or None,
        request.FILES or None,
        instance=produto
    )

    if request.method == "POST":

        if form.is_valid():
            form.save()

            messages.success(request, "Produto atualizado com sucesso!")
            return redirect("produtos:listar")

    return render(request, "produtos/produtos_form.html", {
        "form": form,
        "titulo": "Editar Produto",
        "produto": produto
    })


@login_required
def detalhe_produto(request, id):

    produto = get_object_or_404(
        Produto,
        id=id,
        loja=request.user.perfil.loja
    )

    return render(request, "produtos/produtos_detalhes.html", {
        "produto": produto
    })


@login_required
def alterar_status_produto(request, id):

    produto = get_object_or_404(
        Produto,
        id=id,
        loja=request.user.perfil.loja
    )

    produto.disponivel = not produto.disponivel
    produto.save()

    messages.success(request, "Status atualizado com sucesso!")
    return redirect("produtos:listar")