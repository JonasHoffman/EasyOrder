from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from Cardapio.forms.grupoadicional_form import GrupoAdicionalForm
from Cardapio.models import GrupoAdicional


@login_required
def listar_grupos_adicionais(request):

    busca = request.GET.get("busca", "")
    status = request.GET.get("status", "")

    grupos = GrupoAdicional.objects.filter(
        loja=request.user.perfil.loja
    )

    if busca:
        grupos = grupos.filter(
            Q(nome__icontains=busca) |
            Q(descricao__icontains=busca)
        )

    if status == "ativo":
        grupos = grupos.filter(ativo=True)

    elif status == "inativo":
        grupos = grupos.filter(ativo=False)

    paginator = Paginator(grupos, 10)

    page = request.GET.get("page")

    grupos = paginator.get_page(page)

    context = {
        "grupos": grupos,
        "total": paginator.count,
        "busca": busca,
        "status": status,
    }

    return render(
        request,
        "grupoadicional/grupoadicional_listar.html",
        context
    )


@login_required
def novo_grupo_adicional(request):

    if request.method == "POST":

        form = GrupoAdicionalForm(request.POST)

        if form.is_valid():

            grupo = form.save(commit=False)
            grupo.loja = request.user.perfil.loja
            grupo.save()

            messages.success(
                request,
                "Grupo cadastrado com sucesso."
            )

            return redirect("grupos_adicionais:listar")

    else:

        form = GrupoAdicionalForm()

    return render(
        request,
        "grupoadicional/grupoadicional_form.html",
        {"form": form}
    )


@login_required
def editar_grupo_adicional(request, id):

    grupo = get_object_or_404(
        GrupoAdicional,
        id=id,
        loja=request.user.perfil.loja
    )

    if request.method == "POST":

        form = GrupoAdicionalForm(
            request.POST,
            instance=grupo
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Grupo atualizado com sucesso."
            )

            return redirect("grupos_adicionais:listar")

    else:

        form = GrupoAdicionalForm(instance=grupo)

    return render(
        request,
        "grupoadicional/grupoadicional_form.html",
        {"form": form}
    )


@login_required
def alterar_status_grupo_adicional(request, id):

    grupo = get_object_or_404(
        GrupoAdicional,
        id=id,
        loja=request.user.perfil.loja
    )

    grupo.ativo = not grupo.ativo
    grupo.save()

    messages.success(
        request,
        "Status atualizado com sucesso."
    )

    return redirect("grupos_adicionais:listar")