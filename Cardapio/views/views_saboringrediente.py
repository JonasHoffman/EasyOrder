from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Cardapio.models import (
    Sabor,
    Ingrediente,
    SaborIngrediente
)


# LISTAR INGREDIENTES DO SABOR
from django.db.models import Q


@login_required
def selecionar_sabor_ingredientes(request):

    loja = request.user.perfil.loja

    busca = request.GET.get(
        "busca",
        ""
    )

    sabores = (
        Sabor.objects
        .filter(
            loja=loja
        )
        .select_related(
            "grupo"
        )
        .order_by(
            "grupo__ordem",
            "ordem",
            "nome"
        )
    )

    if busca:

        sabores = sabores.filter(
            Q(nome__icontains=busca)
        )

    if request.method == "POST":

        sabor_id = request.POST.get(
            "sabor"
        )

        if sabor_id:

            return redirect(
                "saboringrediente:listar",
                sabor_id=sabor_id
            )

        messages.error(
            request,
            "Selecione um sabor."
        )

    return render(
        request,
        "saboringrediente/saboringrediente_selecionar.html",
        {
            "sabores": sabores,
            "busca": busca,
        }
    )

@login_required
def listar_ingredientes_sabor(request, sabor_id):

    loja = request.user.perfil.loja

    sabor = get_object_or_404(
        Sabor,
        id=sabor_id,
        loja=loja
    )

    ingredientes = (
        SaborIngrediente.objects
        .filter(
            sabor=sabor
        )
        .select_related(
            "ingrediente"
        )
        .order_by(
            "ordem",
            "ingrediente__nome"
        )
    )

    return render(
        request,
        "saboringrediente/saboringrediente_listar.html",
        {
            "sabor": sabor,
            "ingredientes": ingredientes
        }
    )


# ADICIONAR INGREDIENTES AO SABOR

@login_required
def adicionar_ingrediente_sabor(request, sabor_id):

    loja = request.user.perfil.loja

    sabor = get_object_or_404(
        Sabor,
        id=sabor_id,
        loja=loja
    )

    ingredientes = Ingrediente.objects.filter(
        loja=loja,
        ativo=True
    ).order_by(
        "ordem",
        "nome"
    )

    ingredientes_selecionados = set(
        SaborIngrediente.objects.filter(
            sabor=sabor
        ).values_list(
            "ingrediente_id",
            flat=True
        )
    )

    if request.method == "POST":

        selecionados = set(
            map(
                int,
                request.POST.getlist("ingredientes")
            )
        )

        atuais = ingredientes_selecionados

        # Adiciona os novos
        for ingrediente_id in selecionados - atuais:

            SaborIngrediente.objects.create(
                sabor=sabor,
                ingrediente_id=ingrediente_id,
                permite_remocao=True,
                ativo=True
            )

        # Remove os desmarcados
        SaborIngrediente.objects.filter(
            sabor=sabor,
            ingrediente_id__in=atuais - selecionados
        ).delete()

        messages.success(
            request,
            "Ingredientes atualizados com sucesso."
        )

        return redirect(
            "saboringrediente:listar",
            sabor.id
        )

    return render(
        request,
        "saboringrediente/saboringrediente_form.html",
        {
            "titulo": "Adicionar ingredientes",
            "sabor": sabor,
            "ingredientes": ingredientes,
            "ingredientes_selecionados": ingredientes_selecionados,
        }
    )


# EDITAR

@login_required
def editar_ingrediente_sabor(request, id):

    loja = request.user.perfil.loja

    item = get_object_or_404(
        SaborIngrediente,
        id=id,
        sabor__loja=loja
    )

    if request.method == "POST":

        item.permite_remocao = (
            request.POST.get("permite_remocao") == "on"
        )

        item.ativo = (
            request.POST.get("ativo") == "on"
        )

        item.ordem = request.POST.get(
            "ordem",
            0
        )

        item.save()

        messages.success(
            request,
            "Ingrediente atualizado."
        )

        return redirect(
            "saboringrediente:listar",
            item.sabor.id
        )

    return render(
        request,
        "saboringrediente/saboringrediente_editar.html",
        {
            "item": item
        }
    )


# EXCLUIR

@login_required
def excluir_ingrediente_sabor(request, id):

    loja = request.user.perfil.loja

    item = get_object_or_404(
        SaborIngrediente,
        id=id,
        sabor__loja=loja
    )

    sabor_id = item.sabor.id

    if request.method == "POST":

        item.delete()

        messages.success(
            request,
            "Ingrediente removido."
        )

    return redirect(
        "saboringrediente:listar",
        sabor_id
    )


# STATUS

@login_required
def status_ingrediente_sabor(request, id):

    loja = request.user.perfil.loja

    item = get_object_or_404(
        SaborIngrediente,
        id=id,
        sabor__loja=loja
    )

    item.ativo = not item.ativo

    item.save()

    messages.success(
        request,
        "Status atualizado."
    )

    return redirect(
        "saboringrediente:listar",
        item.sabor.id
    )