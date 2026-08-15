from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from Cardapio.models import Loja

from Cardapio.forms.grupodesabores_form import GrupoDeSaboresForm
from Cardapio.models import GrupoDeSabores

@login_required
def listar(request):

    loja = request.user.perfil.loja

    status = request.GET.get("status", "todos")

    busca = request.GET.get("busca", "")

    grupos = GrupoDeSabores.objects.filter(
    loja=request.user.perfil.loja
)
    
    if status == "ativos":
        grupos = grupos.filter(ativo=True)
    elif status == "inativos":
        grupos = grupos.filter(ativo=False)

    if busca:
        grupos = grupos.filter(
            Q(nome__icontains=busca)
        )

    paginator = Paginator(grupos, 10)

    page = request.GET.get("page")

    grupos = paginator.get_page(page)

    return render(
        request,
        "grupodesabores/grupodesabores_listar.html",
        {
            "grupos": grupos,
            "busca": busca,
            "total": paginator.count,
            "status": status,
        },
    )

@login_required
def novo(request):

    loja = request.user.perfil.loja

    form = GrupoDeSaboresForm(request.POST or None)

    if form.is_valid():

        grupo = form.save(commit=False)

        grupo.loja = loja

        grupo.save()

        messages.success(request, "Grupo criado com sucesso.")

        return redirect("grupos_sabores:listar")

    return render(
        request,
        "grupodesabores/grupodesabores_form.html",
        {
            "form": form,
            "titulo": "Novo Grupo de Sabores",
        },
    )

@login_required
def editar(request, id):

    loja = request.user.perfil.loja

    grupo = get_object_or_404(
        GrupoDeSabores,
        id=id,
        loja=loja,
    )

    form = GrupoDeSaboresForm(
        request.POST or None,
        instance=grupo,
    )

    if form.is_valid():

        form.save()

        messages.success(request, "Grupo atualizado com sucesso.")

        return redirect("grupos_sabores:listar")

    return render(
        request,
        "grupodesabores/grupodesabores_form.html",
        {
            "form": form,
            "titulo": "Editar Grupo de Sabores",
        },
    )

@login_required
def visualizar(request, id):

    loja = request.user.perfil.loja

    grupo = get_object_or_404(
        GrupoDeSabores,
        id=id,
        loja=loja,
    )

    return render(
        request,
        "grupodesabores/grupodesabores_detalhes.html",
        {
            "grupo": grupo,
        },
    )

@login_required
def alterar_status(request, id):

    loja = request.user.perfil.loja

    grupo = get_object_or_404(
        GrupoDeSabores,
        id=id,
        loja=loja,
    )

    grupo.ativo = not grupo.ativo

    grupo.save()

    messages.success(
        request,
        "Status atualizado com sucesso."
    )

    return redirect("grupos_sabores:listar")