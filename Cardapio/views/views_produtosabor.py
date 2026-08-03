from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from Cardapio.models import ProdutoSabor,Produto,Sabor
from Cardapio.forms.produtosabor_forms import ProdutoSaborForm
from django.contrib import messages


@login_required
def listar_produto_sabor(request):

    loja = request.user.perfil.loja

    status = request.GET.get(
        "status",
        "todos"
    )
    # FILTRO NENHUM SABOR
    
    
    produtos = (
    Produto.objects.filter(
        loja=request.user.perfil.loja,
        possui_sabores=True
    )
    .prefetch_related(
        "sabores__sabor",
        "sabores__sabor__grupo"
    )
)
    
    if status == "disponiveis":

        produtos = produtos.filter(
            disponivel=True
        )


    elif status == "indisponiveis":

        produtos = produtos.filter(
            disponivel=False
        )
    if request.GET.get("sem_sabor"):
    
            produtos = produtos.exclude(
                id__in=ProdutoSabor.objects.values_list(
                    "produto_id",
                    flat=True
                )
            )


    return render(
        request,
        "produtosabor/produtosabor_listar.html",
        {
            "produtos": produtos,
            "status": status,
        }
    )

def adicionar_produto_sabor(request, produto_id=None):

    loja = request.user.perfil.loja

    produto = None


    if produto_id:

        produto = get_object_or_404(
            Produto,
            id=produto_id,
            loja=loja
        )


    if request.method == "POST":


        sabores = request.POST.getlist("sabor")


        # Remove campos vazios
        sabores = [
            s for s in sabores
            if s
        ]


        # Remove sabores duplicados
        sabores = list(
            dict.fromkeys(sabores)
        )


        # Caso tenha vindo pela tela sem produto definido
        if not produto:

            produto = get_object_or_404(
                Produto,
                id=request.POST.get("produto"),
                loja=loja
            )


        # Verifica limite de sabores
        if len(sabores) > produto.maximo_sabores:

            form = ProdutoSaborForm(
                loja=loja
            )


            if produto_id:
                form.fields.pop("produto")


            return render(
                request,
                "produtosabor/produtosabor_form.html",
                {
                    "form": form,
                    "produto": produto,
                    "titulo": "Adicionar sabor ao produto",
                    "erro": (
                        f"O produto permite no máximo "
                        f"{produto.maximo_sabores} sabores."
                    )
                }
            )


        # ================================
        # VALIDA INGREDIENTES DO SABOR
        # ================================

        sabores_sem_ingredientes = []


        for sabor_id in sabores:


            sabor = get_object_or_404(
                Sabor,
                id=sabor_id,
                loja=loja
            )


            possui_ingredientes = (
                sabor.ingredientes
                .filter(ativo=True)
                .exists()
            )


            if not possui_ingredientes:

                sabores_sem_ingredientes.append(
                    sabor.nome
                )



        if sabores_sem_ingredientes:


            form = ProdutoSaborForm(
                loja=loja
            )


            if produto_id:
                form.fields.pop("produto")


            return render(
                request,
                "produtosabor/produtosabor_form.html",
                {
                    "form": form,
                    "produto": produto,
                    "titulo": "Adicionar sabor ao produto",
                    "erro": (
                        "Os seguintes sabores não possuem "
                        "ingredientes cadastrados: "
                        +
                        ", ".join(
                            sabores_sem_ingredientes
                        )
                    )
                }
            )



        # ================================
        # SALVA OS SABORES
        # ================================

        for sabor_id in sabores:

            ProdutoSabor.objects.create(
                produto=produto,
                sabor_id=sabor_id,
                ordem=request.POST.get(
                    f"ordem_{sabor_id}",
                    0
                ),
                ativo=request.POST.get(
                    f"ativo_{sabor_id}"
                ) == "on"
            )


        messages.success(
            request,
            "Sabores adicionados ao produto com sucesso."
        )


        return redirect(
            "produtosabor:listar"
        )



    # GET

    form = ProdutoSaborForm(
        loja=loja
    )


    if produto:

        form.fields.pop(
            "produto"
        )


    sabores_disponiveis = (
        Sabor.objects
        .filter(
            loja=loja,
            ativo=True
        )
        .prefetch_related(
            "ingredientes__ingrediente"
        )
        .order_by(
            "ordem",
            "nome"
        )
    )


    return render(
        request,
        "produtosabor/produtosabor_form.html",
        {
            "form": form,
            "produto": produto,
            "sabores_disponiveis": sabores_disponiveis,
            "titulo": "Adicionar sabor ao produto"
        }
    )


@login_required
def excluir_produto_sabor(request, id):

    loja = request.user.perfil.loja

    produto_sabor = get_object_or_404(
        ProdutoSabor,
        id=id,
        produto__loja=loja
    )


    if request.method == "POST":

        produto_sabor.delete()


    return redirect(
        "produtosabor:listar"
    )

@login_required
def editar_sabores_produto(request, produto_id):

    loja = request.user.perfil.loja

    produto = get_object_or_404(
        Produto,
        id=produto_id,
        loja=loja
    )

    sabores_cadastrados = (
        ProdutoSabor.objects
        .filter(produto=produto)
        .select_related("sabor")
        .order_by("ordem")
    )
    sabores_disponiveis = list(
        Sabor.objects
        .filter(
            loja=loja,
            ativo=True
        )
        .prefetch_related(
            "ingredientes__ingrediente"
        )
        .order_by(
            "ordem",
            "nome"
        )
    )


    # Cria mapa dos sabores já vinculados ao produto
    sabores_produto = {
        ps.sabor_id: ps
        for ps in sabores_cadastrados
    }


    # adiciona informações para o template
    for sabor in sabores_disponiveis:

        if sabor.id in sabores_produto:

            ps = sabores_produto[sabor.id]

            sabor.selecionado = True
            sabor.ordem_produto = ps.ordem
            sabor.ativo_produto = ps.ativo

        else:

            sabor.selecionado = False
            sabor.ordem_produto = 0
            sabor.ativo_produto = True

    if request.method == "POST":

        sabores = request.POST.getlist("sabor")

        # Remove vazios
        sabores = [s for s in sabores if s]

        # Remove duplicados enviados pelo formulário
        sabores = list(dict.fromkeys(sabores))

        if len(sabores) > produto.maximo_sabores:

            form = ProdutoSaborForm(loja=loja)
            form.fields.pop("produto")

            return render(
                request,
                "produtosabor/produtosabor_form.html",
                {
                    "form": form,
                    "produto": produto,
                    "sabores_cadastrados": sabores_cadastrados,
                    "titulo": "Editar sabores do produto",
                    "erro": (
                        f"O produto permite no máximo "
                        f"{produto.maximo_sabores} sabores."
                    )
                }
            )

        # Remove todos os sabores atuais
        ProdutoSabor.objects.filter(
            produto=produto
        ).delete()

        # Cria novamente
        for ordem, sabor_id in enumerate(sabores, start=1):

            ProdutoSabor.objects.create(
                produto=produto,
                sabor_id=sabor_id,
                ordem=ordem,
                ativo=True
            )

        messages.success(
            request,
            "Sabores atualizados com sucesso."
        )

        return redirect("produtosabor:listar")

    form = ProdutoSaborForm(loja=loja)

    form.fields.pop("produto")

    return render(
        request,
        "produtosabor/produtosabor_form.html",
        {
            "form": form,
            "produto": produto,
            "sabores_disponiveis": sabores_disponiveis,
            "sabores_cadastrados": sabores_cadastrados,
            "titulo": "Editar sabores do produto",
        }
    )

@login_required
def alterar_status_produto_sabor(request, produto_id):

    loja = request.user.perfil.loja


    produto = get_object_or_404(
        Produto,
        id=produto_id,
        loja=loja
    )


    produto.disponivel = not produto.disponivel

    produto.save()


    messages.success(
        request,
        "Status do produto alterado com sucesso."
    )


    return redirect(
        "produtosabor:listar"
    )