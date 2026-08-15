from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from Cardapio.forms.produtogrupocombo_form import ProdutoGrupoComboForm

from Cardapio.models import (
    Produto,
    ProdutoComboGrupo,
    ProdutoGrupoCombo,
)


def listar(request, produto_id):

    loja = request.user.perfil.loja

    combo = get_object_or_404(
        Produto,
        id=produto_id,
        loja=loja,
        tipo="COMBO",
    )

    # Grupos que já estão vinculados ao combo
    grupos = (
        ProdutoGrupoCombo.objects
        .filter(
            produto=combo,
        )
        .select_related(
            "grupo",
        )
        .order_by(
            "ordem",
            "grupo__nome",
        )
    )

    # Busca
    busca = request.GET.get(
        "busca",
        ""
    ).strip()

    # Todos os grupos ativos disponíveis para a loja
    grupos_disponiveis = (
        ProdutoComboGrupo.objects
        .filter(
            loja=loja,
            ativo=True,
        )
        .annotate(
            total_uso=Count(
                "produtos_combos"
            )
        )
        .order_by(
            "-total_uso",
            "nome",
        )
    )

    if busca:

        grupos_disponiveis = grupos_disponiveis.filter(
            nome__icontains=busca
        )

    # IDs dos grupos já vinculados
    grupos_vinculados_ids = set(
        grupos.values_list(
            "grupo_id",
            flat=True,
        )
    )

    return render(
        request,
        "produtogrupocombo/produtogrupocombo_listar.html",
        {
            "combo": combo,
            "grupos": grupos,
            "grupos_disponiveis": grupos_disponiveis,
            "grupos_vinculados_ids": grupos_vinculados_ids,
            "busca": busca,
        },
    )


def adicionar(request, produto_id, grupo_id):

    loja = request.user.perfil.loja

    combo = get_object_or_404(
        Produto,
        id=produto_id,
        loja=loja,
        tipo="COMBO",
    )

    grupo = get_object_or_404(
        ProdutoComboGrupo,
        id=grupo_id,
        loja=loja,
        ativo=True,
    )

    if request.method != "POST":

        return redirect(
            "produtogrupocombo:listar",
            combo.id,
        )

    # Verifica se já existe o vínculo
    if ProdutoGrupoCombo.objects.filter(
        produto=combo,
        grupo=grupo,
    ).exists():

        messages.warning(
            request,
            "Esse grupo já está vinculado ao combo.",
        )

        return redirect(
            "produtogrupocombo:listar",
            combo.id,
        )

    # Descobre a próxima ordem
    ultima_ordem = (
        ProdutoGrupoCombo.objects
        .filter(
            produto=combo,
        )
        .order_by(
            "-ordem",
        )
        .values_list(
            "ordem",
            flat=True,
        )
        .first()
    )

    ordem = (
        ultima_ordem + 1
        if ultima_ordem is not None
        else 0
    )

    ProdutoGrupoCombo.objects.create(
        produto=combo,
        grupo=grupo,
        obrigatorio=True,
        minimo=1,
        maximo=1,
        ordem=ordem,
    )

    messages.success(
        request,
        f'Grupo "{grupo.nome}" adicionado ao combo.',
    )

    return redirect(
        "produtogrupocombo:listar",
        combo.id,
    )


def editar(request, pk):

    loja = request.user.perfil.loja

    vinculo = get_object_or_404(
        ProdutoGrupoCombo.objects.select_related(
            "produto",
            "grupo",
        ),
        pk=pk,
        produto__loja=loja,
    )

    combo = vinculo.produto

    if request.method == "POST":

        form = ProdutoGrupoComboForm(
            request.POST,
            instance=vinculo,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Grupo atualizado com sucesso.",
            )

            return redirect(
                "produtogrupocombo:listar",
                combo.id,
            )

    else:

        form = ProdutoGrupoComboForm(
            instance=vinculo,
        )

    return render(
        request,
        "produtogrupocombo/produtogrupocombo_form.html",
        {
            "titulo": "Editar Grupo",
            "combo": combo,
            "vinculo": vinculo,
            "form": form,
        },
    )


def excluir(request, pk):

    loja = request.user.perfil.loja

    vinculo = get_object_or_404(
        ProdutoGrupoCombo,
        pk=pk,
        produto__loja=loja,
    )

    combo_id = vinculo.produto_id

    if request.method == "POST":

        vinculo.delete()

        messages.success(
            request,
            "Grupo removido do combo.",
        )

    return redirect(
        "produtogrupocombo:listar",
        combo_id,
    )