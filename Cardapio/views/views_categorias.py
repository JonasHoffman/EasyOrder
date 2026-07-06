from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from Cardapio.models import Categoria
from Cardapio.forms.categorias_form import CategoriaForm
from django.contrib.auth.decorators import login_required


@login_required
def listar_categorias(request):

    categorias = Categoria.objects.filter(
        loja=request.user.perfil.loja
    ).order_by("ordem", "nome")

    return render(request, "categorias/categorias_listar.html", {
        "categorias": categorias
    })

@login_required
def nova_categoria(request):
    form = CategoriaForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.loja = request.user.perfil.loja  # futuro login por loja
            categoria.save()

            messages.success(request, "Categoria criada com sucesso!")
            return redirect("categorias:listar")

    return render(request, "categorias/categorias_form.html", {
        "form": form,
        "titulo": "Nova Categoria"
    })

@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(
        Categoria,
        id=id,
        loja=request.user.perfil.loja
    )

    form = CategoriaForm(
        request.POST or None,
        request.FILES or None,
        instance=categoria
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()

            messages.success(request, "Categoria atualizada com sucesso!")
            return redirect("categorias:listar")

    return render(request, "categorias/categorias_form.html", {
        "form": form,
        "titulo": "Editar Categoria",
        "categoria": categoria
    })

@login_required
def detalhe_categoria(request, id):
    categoria = get_object_or_404(
    Categoria,
    id=id,
    loja=request.user.perfil.loja
    )

    return render(request, "categorias/categorias_detalhes.html", {
        "categoria": categoria
    })

@login_required
def alterar_status_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    categoria.ativa = not categoria.ativa
    categoria.save()

    messages.success(request, "Status atualizado com sucesso!")
    return redirect("categorias:listar")