from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Cardapio.models import (
    ProdutoSabor,
    Produto,
    Sabor,
    GrupoDeSabores,
)

from Cardapio.forms.produtosabor_forms import ProdutoSaborForm


@login_required
def listar_produto_sabor(request):

    loja = request.user.perfil.loja

    status = request.GET.get(
        "status",
        "todos"
    )

    produtos = (
        Produto.objects
        .filter(
            loja=loja,
            possui_sabores=True
        )
        .prefetch_related(
            "sabores__sabor",
            "sabores__sabor__grupo"
        )
        .order_by(
            "ordem",
            "nome"
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
            id__in=ProdutoSabor.objects.filter(
                produto__loja=loja
            ).values_list(
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


@login_required
def adicionar_produto_sabor(
    request,
    produto_id=None
):

    loja = request.user.perfil.loja

    produto = None

    # =========================================================
    # PRODUTO
    # =========================================================

    if produto_id:

        produto = get_object_or_404(
            Produto,
            id=produto_id,
            loja=loja,
            possui_sabores=True
        )

    # =========================================================
    # POST
    # =========================================================

    if request.method == "POST":

        sabores_ids = request.POST.getlist(
            "sabor"
        )

        # Remove vazios
        sabores_ids = [
            sabor_id
            for sabor_id in sabores_ids
            if sabor_id
        ]

        # Remove duplicados
        sabores_ids = list(
            dict.fromkeys(
                sabores_ids
            )
        )

        # -----------------------------------------------------
        # PRODUTO NÃO INFORMADO NA URL
        # -----------------------------------------------------

        if not produto:

            produto = get_object_or_404(
                Produto,
                id=request.POST.get("produto"),
                loja=loja,
                possui_sabores=True
            )

        # -----------------------------------------------------
        # NENHUM SABOR
        # -----------------------------------------------------

        if not sabores_ids:

            form = ProdutoSaborForm(
                loja=loja
            )

            if produto_id:
                form.fields.pop(
                    "produto",
                    None
                )

            grupos_sabores = _buscar_grupos_sabores(
                loja
            )

            return render(
                request,
                "produtosabor/produtosabor_form.html",
                {
                    "form": form,
                    "produto": produto,
                    "grupos_sabores": grupos_sabores,
                    "titulo": "Adicionar sabores ao produto",
                    "erro": "Selecione pelo menos um sabor."
                }
            )

        # -----------------------------------------------------
        # BUSCA SABORES
        # -----------------------------------------------------

        sabores = (
            Sabor.objects
            .filter(
                id__in=sabores_ids,
                loja=loja,
                ativo=True
            )
            .select_related(
                "grupo"
            )
        )

        # -----------------------------------------------------
        # GARANTE QUE TODOS OS IDs EXISTEM
        # -----------------------------------------------------

        sabores_validos = set(
            sabores.values_list(
                "id",
                flat=True
            )
        )

        ids_recebidos = set(
            int(sabor_id)
            for sabor_id in sabores_ids
            if sabor_id.isdigit()
        )

        if sabores_validos != ids_recebidos:

            messages.error(
                request,
                "Um ou mais sabores selecionados são inválidos."
            )

            return redirect(
                request.path
            )

        # -----------------------------------------------------
        # SABORES JÁ VINCULADOS
        # -----------------------------------------------------

        sabores_existentes = set(
            ProdutoSabor.objects
            .filter(
                produto=produto,
                sabor_id__in=sabores_validos
            )
            .values_list(
                "sabor_id",
                flat=True
            )
        )

        # -----------------------------------------------------
        # CRIA OS VÍNCULOS
        # -----------------------------------------------------

        ordem_atual = (
            ProdutoSabor.objects
            .filter(
                produto=produto
            )
            .count()
        )

        novos = 0

        for sabor in sabores:

            # Já existe
            if sabor.id in sabores_existentes:
                continue

            ordem_atual += 1

            ProdutoSabor.objects.create(
                produto=produto,
                sabor=sabor,
                ordem=ordem_atual,
                ativo=True
            )

            novos += 1

        # -----------------------------------------------------
        # MENSAGEM
        # -----------------------------------------------------

        if novos:

            messages.success(
                request,
                f"{novos} sabor(es) adicionado(s) ao produto."
            )

        else:

            messages.info(
                request,
                "Os sabores selecionados já estão vinculados ao produto."
            )

        return redirect(
            "produtosabor:listar"
        )

    # =========================================================
    # GET
    # =========================================================

    form = ProdutoSaborForm(
        loja=loja
    )

    if produto:

        form.fields.pop(
            "produto",
            None
        )

    grupos_sabores = _buscar_grupos_sabores(
        loja
    )

    return render(
        request,
        "produtosabor/produtosabor_form.html",
        {
            "form": form,
            "produto": produto,
            "grupos_sabores": grupos_sabores,
            "titulo": "Adicionar sabores ao produto"
        }
    )


@login_required
def excluir_produto_sabor(
    request,
    id
):

    loja = request.user.perfil.loja

    produto_sabor = get_object_or_404(
        ProdutoSabor,
        id=id,
        produto__loja=loja
    )

    if request.method == "POST":

        produto_sabor.delete()

        messages.success(
            request,
            "Sabor removido do produto."
        )

    return redirect(
        "produtosabor:listar"
    )


@login_required
def editar_sabores_produto(
    request,
    produto_id
):

    loja = request.user.perfil.loja

    produto = get_object_or_404(
        Produto,
        id=produto_id,
        loja=loja,
        possui_sabores=True
    )

    # =========================================================
    # SABORES ATUAIS
    # =========================================================

    sabores_cadastrados = (
        ProdutoSabor.objects
        .filter(
            produto=produto
        )
        .select_related(
            "sabor",
            "sabor__grupo"
        )
        .order_by(
            "ordem"
        )
    )

    sabores_produto = {
        ps.sabor_id: ps
        for ps in sabores_cadastrados
    }

    # =========================================================
    # GRUPOS
    # =========================================================

    grupos_sabores = _buscar_grupos_sabores(
        loja
    )

    # =========================================================
    # MARCA SABORES SELECIONADOS
    # =========================================================

    for grupo in grupos_sabores:

        for sabor in grupo.sabores.all():

            produto_sabor = (
                sabores_produto.get(
                    sabor.id
                )
            )

            if produto_sabor:

                sabor.selecionado = True
                sabor.ordem_produto = (
                    produto_sabor.ordem
                )
                sabor.ativo_produto = (
                    produto_sabor.ativo
                )

            else:

                sabor.selecionado = False
                sabor.ordem_produto = 0
                sabor.ativo_produto = True

    # =========================================================
    # POST
    # =========================================================

    if request.method == "POST":

        sabores_ids = request.POST.getlist(
            "sabor"
        )

        sabores_ids = [
            sabor_id
            for sabor_id in sabores_ids
            if sabor_id
        ]

        sabores_ids = list(
            dict.fromkeys(
                sabores_ids
            )
        )

        # -----------------------------------------------------
        # VALIDA SABORES
        # -----------------------------------------------------

        sabores = (
            Sabor.objects
            .filter(
                id__in=sabores_ids,
                loja=loja,
                ativo=True
            )
        )

        ids_validos = set(
            sabores.values_list(
                "id",
                flat=True
            )
        )

        ids_recebidos = {
            int(sabor_id)
            for sabor_id in sabores_ids
            if sabor_id.isdigit()
        }

        if ids_validos != ids_recebidos:

            messages.error(
                request,
                "Um ou mais sabores selecionados são inválidos."
            )

            return redirect(
                request.path
            )

        # -----------------------------------------------------
        # REMOVE VÍNCULOS ANTIGOS
        # -----------------------------------------------------

        ProdutoSabor.objects.filter(
            produto=produto
        ).delete()

        # -----------------------------------------------------
        # CRIA NOVAMENTE
        # -----------------------------------------------------

        for ordem, sabor_id in enumerate(
            sabores_ids,
            start=1
        ):

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

        return redirect(
            "produtosabor:listar"
        )

    # =========================================================
    # GET
    # =========================================================

    form = ProdutoSaborForm(
        loja=loja
    )

    form.fields.pop(
        "produto",
        None
    )

    return render(
        request,
        "produtosabor/produtosabor_form.html",
        {
            "form": form,
            "produto": produto,
            "grupos_sabores": grupos_sabores,
            "sabores_cadastrados": sabores_cadastrados,
            "titulo": "Editar sabores do produto",
        }
    )


@login_required
def alterar_status_produto_sabor(
    request,
    produto_id
):

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


# =============================================================
# FUNÇÃO AUXILIAR
# =============================================================

def _buscar_grupos_sabores(loja):

    return (
        GrupoDeSabores.objects
        .filter(
            loja=loja,
            ativo=True
        )
        .prefetch_related(
            "sabores"
        )
        .order_by(
            "ordem",
            "nome"
        )
    )