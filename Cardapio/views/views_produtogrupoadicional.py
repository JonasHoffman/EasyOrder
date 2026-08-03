from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages


from Cardapio.models import (
    ProdutoGrupoAdicional
)


from Cardapio.forms.produtogrupoadicional_form import ProdutoGrupoAdicionalForm



@login_required
def listar(request):

    loja = request.user.perfil.loja


    grupos = ProdutoGrupoAdicional.objects.filter(
        produto__loja=loja
    ).select_related(
        "produto",
        "grupo"
    )


    return render(
        request,
        "produtogrupoadicional/produtogrupoadicional_listar.html",
        {
            "grupos": grupos
        }
    )





@login_required
def novo(request):

    loja = request.user.perfil.loja


    if request.method == "POST":


        form = ProdutoGrupoAdicionalForm(
            request.POST,
            loja=loja
        )


        if form.is_valid():


            item = form.save()


            messages.success(
                request,
                "Grupo de adicional vinculado com sucesso."
            )


            return redirect(
                "produto_grupo_adicional:listar"
            )



    else:


        form = ProdutoGrupoAdicionalForm(
            loja=loja
        )



    return render(
        request,
        "produtogrupoadicional/produtogrupoadicional_form.html",
        {
            "form":form
        }
    )





@login_required
def editar(request, pk):

    loja = request.user.perfil.loja


    item = get_object_or_404(
        ProdutoGrupoAdicional,
        pk=pk,
        produto__loja=loja
    )



    if request.method == "POST":


        form = ProdutoGrupoAdicionalForm(
            request.POST,
            instance=item,
            loja=loja
        )


        if form.is_valid():


            form.save()


            messages.success(
                request,
                "Vínculo atualizado com sucesso."
            )


            return redirect(
                "produto_grupo_adicional:listar"
            )



    else:


        form = ProdutoGrupoAdicionalForm(
            instance=item,
            loja=loja
        )



    return render(
        request,
        "produtogrupoadicional/produtogrupoadicional_form.html",
        {
            "form":form
        }
    )






@login_required
def excluir(request, pk):

    loja = request.user.perfil.loja


    item = get_object_or_404(
        ProdutoGrupoAdicional,
        pk=pk,
        produto__loja=loja
    )


    if request.method == "POST":

        item.delete()


        messages.success(
            request,
            "Vínculo excluído com sucesso."
        )


    return redirect(
        "produto_grupo_adicional:listar"
    )