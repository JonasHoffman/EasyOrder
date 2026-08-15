from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from Cardapio.forms.combo_form import ComboForm
from Cardapio.models import Produto


def listar_combo(request):

    loja = request.user.perfil.loja

    busca = request.GET.get("busca", "")

    status = request.GET.get("status", "")

    combos = Produto.objects.filter(
        loja=loja,
        tipo="COMBO"
    ).select_related("categoria")

    if busca:
        combos = combos.filter(
            Q(nome__icontains=busca) |
            Q(codigo__icontains=busca)
        )

    if status == "ativos":
        combos = combos.filter(disponivel=True)

    elif status == "inativos":
        combos = combos.filter(disponivel=False)

    paginator = Paginator(combos.order_by("ordem", "nome"), 10)

    page = request.GET.get("page")

    combos = paginator.get_page(page)

    context = {
        "combos": combos,
        "busca": busca,
        "status": status,
    }

    return render(
        request,
        "combos/combo_listar.html",
        context
    )


def novo_combo(request):

    loja = request.user.perfil.loja

    if request.method == "POST":

        form = ComboForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            combo = form.save(commit=False)

            combo.loja = loja
            combo.tipo = "COMBO"

            combo.possui_sabores = False
            combo.permite_multiplos_sabores = False
            combo.maximo_sabores = 1

            combo.save()

            messages.success(
                request,
                "Combo cadastrado com sucesso."
            )

            return redirect(
                "combos:editar",
                combo.pk
            )

    else:

        form = ComboForm()

    return render(
        request,
        "combos/combo_form.html",
        {
            "form": form,
            "titulo": "Novo Combo"
        }
    )


def editar_combo(request, pk):

    loja = request.user.perfil.loja

    combo = get_object_or_404(
        Produto,
        pk=pk,
        loja=loja,
        tipo="COMBO"
    )

    if request.method == "POST":

        form = ComboForm(
            request.POST,
            request.FILES,
            instance=combo
        )

        if form.is_valid():

            combo = form.save(commit=False)

            combo.tipo = "COMBO"

            combo.possui_sabores = False
            combo.permite_multiplos_sabores = False
            combo.maximo_sabores = 1

            combo.save()

            messages.success(
                request,
                "Combo atualizado com sucesso."
            )

            return redirect(
                "combos:listar"
            )

    else:

        form = ComboForm(instance=combo)

    return render(
        request,
        "combos/combo_form.html",
        {
            "form": form,
            "combo": combo,
            "titulo": "Editar Combo"
        }
    )


def excluir_combo(request, pk):

    loja = request.user.perfil.loja

    combo = get_object_or_404(
        Produto,
        pk=pk,
        loja=loja,
        tipo="COMBO"
    )

    combo.delete()

    messages.success(
        request,
        "Combo excluído com sucesso."
    )

    return redirect("combos:listar")