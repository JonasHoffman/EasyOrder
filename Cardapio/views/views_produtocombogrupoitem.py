from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from Cardapio.forms.produtocombogrupoitem_form import ProdutoComboGrupoItemForm
from Cardapio.models import (
    ProdutoComboGrupo,
    ProdutoComboGrupoItem,
)

def listar_itens_grupo(request, grupo_id):

    loja = request.user.perfil.loja

    grupo = get_object_or_404(
        ProdutoComboGrupo,
        pk=grupo_id,
        loja=loja
    )

    itens = (
        ProdutoComboGrupoItem.objects
        .filter(grupo=grupo)
        .select_related("produto")
        .order_by("ordem", "id")
    )

    return render(
        request,
        "produtocombogrupoitem/produtocombogrupoitem_listar.html",
        {
            "grupo": grupo,
            "itens": itens,
        }
    )


def novo_item_grupo(request, grupo_id):

    loja = request.user.perfil.loja

    grupo = get_object_or_404(
        ProdutoComboGrupo,
        pk=grupo_id,
        loja=loja
    )

    if request.method == "POST":

        form = ProdutoComboGrupoItemForm(
            request.POST,
            loja=loja
        )

        if form.is_valid():

            item = form.save(commit=False)

            item.grupo = grupo

            item.save()

            messages.success(
                request,
                "Item adicionado ao grupo com sucesso."
            )

            return redirect(
                "produtocombogrupoitem:listar",
                grupo.id
            )

    else:

        form = ProdutoComboGrupoItemForm(
            loja=loja
        )

    return render(
        request,
        "produtocombogrupoitem/produtocombogrupoitem_form.html",
        {
            "form": form,
            "grupo": grupo,
            "titulo": "Novo Item"
        }
    )


def editar_item_grupo(request, pk):

    loja = request.user.perfil.loja

    item = get_object_or_404(
        ProdutoComboGrupoItem.objects.select_related(
            "grupo",
            "grupo__produto"
        ),
        pk=pk,
        grupo__produto__loja=loja,
        grupo__produto__tipo="COMBO"
    )

    if request.method == "POST":

        form = ProdutoComboGrupoItemForm(
            request.POST,
            instance=item,
            loja=loja
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Item atualizado com sucesso."
            )

            return redirect(
                "produtocombogrupoitem:listar",
                item.grupo.id
            )

    else:

        form = ProdutoComboGrupoItemForm(
            instance=item,
            loja=loja
        )

    return render(
        request,
        "produtocombogrupoitem/produtocombogrupoitem_form.html",
        {
            "form": form,
            "grupo": item.grupo,
            "combo": item.grupo.produto,
            "titulo": "Editar Item"
        }
    )


def excluir_item_grupo(request, pk):

    loja = request.user.perfil.loja

    item = get_object_or_404(
        ProdutoComboGrupoItem.objects.select_related(
            "grupo",
            "produto"
        ),
        pk=pk,
        grupo__loja=loja
    )

    grupo_id = item.grupo.id

    item.delete()

    messages.success(
        request,
        "Item removido com sucesso."
    )

    return redirect(
        "produtocombogrupoitem:listar",
        grupo_id
    )