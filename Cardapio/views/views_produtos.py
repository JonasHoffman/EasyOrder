from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Cardapio.models import Produto,ItemAdicional,Sabor,SaborIngrediente
from Cardapio.forms.produtos_form import ProdutoForm




@login_required
def listar_produtos(request):
    
    status = request.GET.get("status", "todos")

    produtos = Produto.objects.filter(
        loja=request.user.perfil.loja
    ).select_related(
        "categoria"
    ).prefetch_related(
        "sabores",
        "ingredientes"
    ).order_by(
        "ordem",
        "nome"
    )


    if status == "disponiveis":
        produtos = produtos.filter(disponivel=True)

    elif status == "indisponiveis":
        produtos = produtos.filter(disponivel=False)


    for produto in produtos:

        produto.tem_ingredientes = produto.ingredientes.exists()

        produto.tem_sabores = produto.sabores.exists()


    return render(
        request,
        "produtos/produtos_listar.html",
        {
            "produtos": produtos,
            "status": status,
        }
    )


@login_required
def novo_produto(request):

    form = ProdutoForm(request.POST or None, request.FILES or None)

    if request.method == "POST":

        if form.is_valid():
            produto = form.save(commit=False)

            produto.loja = request.user.perfil.loja
            produto.save()

            
            if produto.possui_sabores:
                messages.success(
                                request,
                                "Produto criado. Agora cadastre os sabores."
                            )
                return redirect("produtosabor:novo_produto", produto.id)


            messages.success(
                            request,
                            "Produto criado. Agora cadastre os ingredientes."
                        )
            return redirect(
                "ingredientes:ingredientes",
                produto.id
            )

    return render(request, "produtos/produtos_form.html", {
        "form": form,
        "titulo": "Novo Produto"
    })


@login_required
def editar_produto(request, id):

    produto = get_object_or_404(
        Produto,
        id=id,
        loja=request.user.perfil.loja
    )

    form = ProdutoForm(
        request.POST or None,
        request.FILES or None,
        instance=produto
    )

    if request.method == "POST":

         if form.is_valid():
            produto = form.save(commit=False)

            if request.POST.get("remover_imagem"):
                if produto.imagem:
                    produto.imagem.delete(save=False)
                produto.imagem = None

            produto.save()

            messages.success(request, "Produto atualizado com sucesso!")
            return redirect("produtos:listar")

    return render(request, "produtos/produtos_form.html", {
        "form": form,
        "titulo": "Editar Produto",
        "produto": produto
    })


@login_required
def detalhe_produto(request, id):

    produto = get_object_or_404(
        Produto,
        id=id,
        loja=request.user.perfil.loja
    )

    return render(request, "produtos/produtos_detalhes.html", {
        "produto": produto
    })


@login_required
def alterar_status_produto(request, id):

    produto = get_object_or_404(
        Produto,
        id=id,
        loja=request.user.perfil.loja
    )

    produto.disponivel = not produto.disponivel
    produto.save()

    messages.success(request, "Status atualizado com sucesso!")
    return redirect("produtos:listar")

# views.py
@login_required
def produto_detalhe(request, slug):
    produto = get_object_or_404(
    Produto,
    slug=slug,
    disponivel=True,
    categoria__ativa=True,
    loja__ativa=True,
)
    # produtos relacionados da mesma categoria (opcional, mas fica legal)
    relacionados = Produto.objects.filter(
        categoria=produto.categoria
    ).exclude(id=produto.id)[:4]

    context = {
        'produto': produto,
        'relacionados': relacionados,
    }
    return render(request, 'produtos/produtos_detalhe_cardapio.html', context)

@login_required
def personalizar_produto(request, slug):

    produto = get_object_or_404(
        Produto,
        slug=slug,
        loja=request.user.perfil.loja
    )

    possui_sabores = produto.possui_sabores


    # ==========================
    # GET
    # ==========================
    if request.method == "GET":


        # Produto com sabores
        if possui_sabores:

            sabores = Sabor.objects.filter(
                produtos__produto=produto,
                produtos__ativo=True,
                ativo=True
            ).distinct()


            return render(
                request,
                "ingredientes/ingredientes_personalizar.html",
                {
                    "produto": produto,
                    "etapa": "sabores",
                    "sabores": sabores,
                }
            )


        # Produto normal

        ingredientes = produto.ingredientes.filter(
            ativo=True
        )


        adicionais = ItemAdicional.objects.filter(
            grupo__produtos__produto=produto,
            ativo=True
        ).distinct()



        return render(
            request,
            "ingredientes/ingredientes_personalizar.html",
            {
                "produto": produto,
                "etapa": "personalizar",
                "ingredientes": ingredientes,
                "adicionais": adicionais,
            }
        )



    # ==========================
    # POST
    # ==========================

    etapa = request.POST.get("etapa")


    # ==================================
    # ETAPA 1 - ESCOLHA DOS SABORES
    # ==================================

    if etapa == "sabores":


        sabores_ids = request.POST.getlist(
            "sabores"
        )


        sabores = Sabor.objects.filter(
            id__in=sabores_ids,
            ativo=True
        )



        # Busca ingredientes dos sabores escolhidos

        ingredientes = SaborIngrediente.objects.filter(
            sabor__in=sabores,
            ativo=True
        ).distinct()



        adicionais = ItemAdicional.objects.filter(
            grupo__produtos__produto=produto,
            ativo=True
        ).distinct()



        return render(
            request,
            "ingredientes/ingredientes_personalizar.html",
            {
                "produto": produto,
                "etapa": "personalizar",

                # mantém sabores escolhidos
                "sabores": sabores,

                "sabores_ids": sabores_ids,

                "ingredientes": ingredientes,

                "adicionais": adicionais,
            }
        )



    # ==================================
    # ETAPA 2 - FINALIZA PERSONALIZAÇÃO
    # ==================================

    elif etapa == "personalizar":


        sabores_ids = request.POST.getlist(
            "sabores"
        )


        ingredientes_removidos = request.POST.getlist(
            "ingredientes_removidos"
        )


        adicionais_ids = request.POST.getlist(
            "adicionais"
        )


        try:
            quantidade = int(request.POST.get("quantidade", 1))
        except ValueError:
            quantidade = 1

        quantidade = max(1, min(quantidade, 99))



        # ==============================
        # AQUI ENTRA O CARRINHO
        # ==============================


        """
        carrinho.adicionar(
            produto=produto,
            sabores=sabores_ids,
            ingredientes_removidos=ingredientes_removidos,
            adicionais=adicionais_ids,
            quantidade=quantidade
        )
        """



        return redirect(
            "carrinho"
        )