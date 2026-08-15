from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from Cardapio.forms.produtocombogrupo_form import ProdutoComboGrupoForm
from Cardapio.models import ProdutoComboGrupo


def listar_grupos_combo(request):

    loja = request.user.perfil.loja

    grupos = (
        ProdutoComboGrupo.objects
        .filter(
            loja=loja
        )
        .order_by(
            "ordem",
            "nome"
        )
    )

    return render(
        request,
        "produtocombogrupo/produtocombogrupo_listar.html",
        {
            "grupos": grupos
        }
    )


def novo_grupo_combo(request):

    loja = request.user.perfil.loja

    if request.method == "POST":

        form = ProdutoComboGrupoForm(
            request.POST
        )

        if form.is_valid():

            grupo = form.save(
                commit=False
            )

            grupo.loja = loja

            grupo.save()

            messages.success(
                request,
                "Grupo criado com sucesso."
            )

            return redirect(
                "produtocombogrupo:listar"
            )

    else:

        form = ProdutoComboGrupoForm()

    return render(
        request,
        "produtocombogrupo/produtocombogrupo_form.html",
        {
            "form": form,
            "titulo": "Novo Grupo de Combo"
        }
    )


def editar_grupo_combo(request, pk):

    loja = request.user.perfil.loja

    grupo = get_object_or_404(
        ProdutoComboGrupo,
        pk=pk,
        loja=loja
    )

    if request.method == "POST":

        form = ProdutoComboGrupoForm(
            request.POST,
            instance=grupo
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Grupo atualizado com sucesso."
            )

            return redirect(
                "produtocombogrupo:listar"
            )

    else:

        form = ProdutoComboGrupoForm(
            instance=grupo
        )

    return render(
        request,
        "produtocombogrupo/produtocombogrupo_form.html",
        {
            "form": form,
            "titulo": "Editar Grupo de Combo"
        }
    )


def excluir_grupo_combo(request, pk):

    loja = request.user.perfil.loja

    grupo = get_object_or_404(
        ProdutoComboGrupo,
        pk=pk,
        loja=loja
    )

    grupo.delete()

    messages.success(
        request,
        "Grupo excluído com sucesso."
    )

    return redirect(
        "produtocombogrupo:listar"
    )