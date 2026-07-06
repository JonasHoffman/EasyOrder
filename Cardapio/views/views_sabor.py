from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from Cardapio.forms.sabor_form import SaborForm
from Cardapio.models import GrupoDeSabores, Sabor

def listar_sabores(request):

    loja = request.user.perfil.loja

    busca = request.GET.get("busca")
    grupo = request.GET.get("grupo")
    status = request.GET.get("status")

    sabores = Sabor.objects.filter(
        loja=loja
    ).select_related("grupo")

    if busca:
        sabores = sabores.filter(
            Q(nome__icontains=busca)
        )

    if grupo:
        sabores = sabores.filter(
            grupo_id=grupo
        )

    if status == "ativo":
        sabores = sabores.filter(
            ativo=True
        )

    elif status == "inativo":
        sabores = sabores.filter(
            ativo=False
        )

    paginator = Paginator(sabores, 15)

    page = request.GET.get("page")

    sabores = paginator.get_page(page)

    grupos = GrupoDeSabores.objects.filter(
        loja=loja,
        ativo=True
    )

    context = {
        "sabores": sabores,
        "grupos": grupos,
        "total": paginator.count,
    }

    return render(
        request,
        "sabor/sabor_listar.html",
        context,
    )

def novo_sabor(request):

    loja = request.user.perfil.loja

    if request.method == "POST":

        form = SaborForm(
            request.POST,
            request.FILES,
            loja=loja
        )

        if form.is_valid():

            sabor = form.save(commit=False)

            sabor.loja = loja

            sabor.save()

            messages.success(
                request,
                "Sabor cadastrado com sucesso."
            )

            return redirect("sabor:listar")

    else:

        form = SaborForm(loja=loja)

    return render(
        request,
        "sabor/sabor_form.html",
        {
            "form": form,
            "titulo": "Novo Sabor"
        },
    )

def editar_sabor(request, id):

    loja = request.user.perfil.loja

    sabor = get_object_or_404(
        Sabor,
        id=id,
        loja=loja
    )
    print(sabor)
    if request.method == "POST":

        form = SaborForm(
            request.POST,
            request.FILES,
            instance=sabor,
            loja=loja
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Sabor atualizado com sucesso."
            )

            return redirect("sabor:listar")

    else:

        form = SaborForm(
            instance=sabor,
            loja=loja
        )

    return render(
        request,
        "sabor/sabor_form.html",
        {
            "form": form,
            "titulo": "Editar Sabor"
        },
    )

def excluir_sabor(request, id):

    loja = request.user.perfil.loja

    sabor = get_object_or_404(
        Sabor,
        id=id,
        loja=loja
    )

    sabor.delete()

    messages.success(
        request,
        "Sabor excluído com sucesso."
    )

    return redirect("sabor:listar")


def alterar_status_sabor(request, id):

    loja = request.user.perfil.loja

    sabor = get_object_or_404(
        Sabor,
        id=id,
        loja=loja
    )

    sabor.ativo = not sabor.ativo

    sabor.save()

    messages.success(
        request,
        "Status atualizado com sucesso."
    )

    return redirect("sabor:listar")