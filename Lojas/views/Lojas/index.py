from django.shortcuts import render, redirect, get_object_or_404
from Lojas.models import Loja
from Lojas.forms import LojaForm, EnderecoForm
from django.core.paginator import Paginator
from django.db.models import Q


def lista_lojas(request):

    busca = request.GET.get("busca", "")
    status = request.GET.get("status", "")

    lojas = Loja.objects.all()

    if busca:
        lojas = lojas.filter(
            Q(nome__icontains=busca)
        )

    if status == "ativas":
        lojas = lojas.filter(ativa=True)

    elif status == "inativas":
        lojas = lojas.filter(ativa=False)

    total_lojas = lojas.count()

    paginator = Paginator(lojas.order_by("nome"), 10)

    page = request.GET.get("page")

    lojas = paginator.get_page(page)

    context = {
        "lojas": lojas,
        "busca": busca,
        "status": status,
        "total_lojas": total_lojas,
    }

    return render(request, "lojas/list_shop.html", context)

def nova_loja(request):
    if request.method == "POST":
        form = LojaForm(request.POST, request.FILES)
        endereco_form = EnderecoForm(request.POST)
        form = LojaForm(request.POST, request.FILES)
        endereco_form = EnderecoForm(request.POST)

        print("Loja válida:", form.is_valid())
        print("Endereço válido:", endereco_form.is_valid())

        print("Erros Loja:", form.errors)
        print("Erros Endereço:", endereco_form.errors)

        if form.is_valid() and endereco_form.is_valid():
            endereco = endereco_form.save()

            loja = form.save(commit=False)
            loja.endereco = endereco
            loja.save()

            return redirect("lojas:lista")

    else:
        form = LojaForm()
        endereco_form = EnderecoForm()

    context = {
        "form": form,
        "endereco_form": endereco_form,
    }

    return render(request, "lojas/new_shop.html", context)


def editar_loja(request, pk):
    loja = get_object_or_404(Loja, pk=pk)

    if request.method == "POST":
        form = LojaForm(request.POST, request.FILES, instance=loja)
        endereco_form = EnderecoForm(
            request.POST,
            instance=loja.endereco
        )

        if form.is_valid() and endereco_form.is_valid():
            endereco_form.save()
            form.save()

            return redirect("lojas:lista")

    else:
        form = LojaForm(instance=loja)
        endereco_form = EnderecoForm(instance=loja.endereco)

    context = {
        "form": form,
        "endereco_form": endereco_form,
        "object": loja,   # mantém compatibilidade com seu template
    }

    return render(request, "lojas/new_shop.html", context)


def detalhe_loja(request, pk):
    loja = get_object_or_404(Loja, pk=pk)

    context = {
        "loja": loja,
    }

    return render(request, "lojas/detail_shop.html", context)