from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from Cardapio.forms.itemadicional_form import ItemAdicionalForm
from ..models import ItemAdicional



def listar_item_adicional(request):

    busca = request.GET.get("busca", "")
    status = request.GET.get("status", "")

    itens = ItemAdicional.objects.select_related("grupo").all()

    if busca:
        itens = itens.filter(
            Q(nome__icontains=busca) |
            Q(grupo__nome__icontains=busca)
        )

    if status == "ativo":
        itens = itens.filter(ativo=True)

    elif status == "inativo":
        itens = itens.filter(ativo=False)

    itens = itens.order_by("ordem", "nome")

    total = itens.count()

    paginator = Paginator(itens, 10)

    page = request.GET.get("page")

    itens = paginator.get_page(page)

    context = {
        "itens": itens,
        "busca": busca,
        "status": status,
        "total": total,
    }

    return render(
        request,
        "itemadicional/itemadicional_listar.html",
        context,
    )


def novo_item_adicional(request):
    if request.method == "POST":
        form = ItemAdicionalForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Item adicional cadastrado com sucesso!"
            )
            return redirect("item_adicional:listar")

    else:
        form = ItemAdicionalForm()

    return render(
        request,
        "itemadicional/itemadicional_form.html",
        {
            "form": form
        },
    )


def editar_item_adicional(request, id):
    item = get_object_or_404(
        ItemAdicional,
        id=id
    )

    if request.method == "POST":
        form = ItemAdicionalForm(
            request.POST,
            request.FILES,
            instance=item
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Item adicional atualizado com sucesso!"
            )
            return redirect("item_adicional:listar")

    else:
        form = ItemAdicionalForm(instance=item)

    return render(
        request,
        "itemadicional/itemadicional_form.html",
        {
            "form": form,
            "item": item,
        },
    )


def excluir_item_adicional(request, id):
    item = get_object_or_404(
        ItemAdicional,
        id=id
    )

    if request.method == "POST":
        item.delete()

        messages.success(
            request,
            "Item adicional excluído com sucesso!"
        )

        return redirect("item_adicional:listar")

    return render(
        request,
        "itemadicional/itemadicional_listar.html",
        {
            "item": item
        },
    )


def alterar_status_item_adicional(request, id):
    item = get_object_or_404(
        ItemAdicional,
        id=id
    )

    item.ativo = not item.ativo
    item.save()

    messages.success(
        request,
        "Status atualizado com sucesso!"
    )

    return redirect("item_adicional:listar")