from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Cardapio.models import (
    Produto,
    GrupoDeSabores,
    ProdutoGrupoSabor,
)

from Cardapio.forms.produtosabor_forms import ProdutoSaborForm


# ============================================================
# LISTAR PRODUTOS E SEUS GRUPOS DE SABORES
# ============================================================

@login_required
def listar_produto_grupo_sabor(request):

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
            "grupos_sabores__grupo",
            "grupos_sabores__grupo__sabores"
        )
        .order_by(
            "ordem",
            "nome"
        )
    )

    # ========================================================
    # FILTRO DE STATUS
    # ========================================================

    if status == "disponiveis":

        produtos = produtos.filter(
            disponivel=True
        )

    elif status == "indisponiveis":

        produtos = produtos.filter(
            disponivel=False
        )

    # ========================================================
    # PRODUTOS SEM GRUPO
    # ========================================================

    if request.GET.get("sem_grupo"):

        produtos = produtos.exclude(
            id__in=ProdutoGrupoSabor.objects.filter(
                produto__loja=loja
            ).values_list(
                "produto_id",
                flat=True
            )
        )

    return render(
        request,
        "produtogruposabor/produtogruposabor_listar.html",
        {
            "produtos": produtos,
            "status": status,
        }
    )


# ============================================================
# ADICIONAR GRUPOS DE SABORES AO PRODUTO
# ============================================================

@login_required
def adicionar_produto_grupo_sabor(
    request,
    produto_id=None
):

    loja = request.user.perfil.loja

    produto = None

    # ========================================================
    # PRODUTO
    # ========================================================

    if produto_id:

        produto = get_object_or_404(
            Produto,
            id=produto_id,
            loja=loja,
            possui_sabores=True
        )

    # ========================================================
    # POST
    # ========================================================

    if request.method == "POST":

        grupos_ids = request.POST.getlist(
            "grupo"
        )

        # Remove valores vazios
        grupos_ids = [
            grupo_id
            for grupo_id in grupos_ids
            if grupo_id
        ]

        # Remove duplicados
        grupos_ids = list(
            dict.fromkeys(
                grupos_ids
            )
        )

        # ----------------------------------------------------
        # BUSCA PRODUTO CASO NÃO TENHA VINDO PELA URL
        # ----------------------------------------------------

        if not produto:

            produto = get_object_or_404(
                Produto,
                id=request.POST.get("produto"),
                loja=loja,
                possui_sabores=True
            )

        # ----------------------------------------------------
        # NENHUM GRUPO SELECIONADO
        # ----------------------------------------------------

        if not grupos_ids:

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
                "produtogruposabor/produtogruposabor_form.html",
                {
                    "form": form,
                    "produto": produto,
                    "grupos_sabores": grupos_sabores,
                    "titulo": "Adicionar grupos de sabores",
                    "erro": "Selecione pelo menos um grupo de sabores."
                }
            )

        # ====================================================
        # BUSCA OS GRUPOS
        # ====================================================

        grupos = (
            GrupoDeSabores.objects
            .filter(
                id__in=grupos_ids,
                loja=loja,
                ativo=True
            )
        )

        # ----------------------------------------------------
        # VALIDA IDS
        # ----------------------------------------------------

        ids_validos = set(
            grupos.values_list(
                "id",
                flat=True
            )
        )

        ids_recebidos = set()

        for grupo_id in grupos_ids:

            if grupo_id.isdigit():

                ids_recebidos.add(
                    int(grupo_id)
                )

        if ids_validos != ids_recebidos:

            messages.error(
                request,
                "Um ou mais grupos selecionados são inválidos."
            )

            return redirect(
                request.path
            )

        # ====================================================
        # GRUPOS JÁ VINCULADOS
        # ====================================================

        grupos_existentes = set(
            ProdutoGrupoSabor.objects
            .filter(
                produto=produto,
                grupo_id__in=ids_validos
            )
            .values_list(
                "grupo_id",
                flat=True
            )
        )

        # ====================================================
        # ORDEM ATUAL
        # ====================================================

        ordem_atual = (
            ProdutoGrupoSabor.objects
            .filter(
                produto=produto
            )
            .count()
        )

        novos = 0

        # ====================================================
        # CRIA VÍNCULOS
        # ====================================================

        for grupo in grupos:

            if grupo.id in grupos_existentes:
                continue

            ordem_atual += 1

            ProdutoGrupoSabor.objects.create(
                produto=produto,
                grupo=grupo,
                ordem=ordem_atual,
                ativo=True
            )

            novos += 1

        # ====================================================
        # MENSAGEM
        # ====================================================

        if novos:

            messages.success(
                request,
                f"{novos} grupo(s) de sabores adicionado(s) ao produto."
            )

        else:

            messages.info(
                request,
                "Os grupos selecionados já estão vinculados ao produto."
            )

        return redirect(
            "produtogruposabor:listar"
        )

    # ========================================================
    # GET
    # ========================================================

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
        "produtogruposabor/produtogruposabor_form.html",
        {
            "form": form,
            "produto": produto,
            "grupos_sabores": grupos_sabores,
            "titulo": "Adicionar grupos de sabores"
        }
    )


# ============================================================
# EDITAR GRUPOS DE SABORES DO PRODUTO
# ============================================================

@login_required
def editar_grupos_produto(
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

    # ========================================================
    # GRUPOS ATUAIS
    # ========================================================

    grupos_cadastrados = (
        ProdutoGrupoSabor.objects
        .filter(
            produto=produto
        )
        .select_related(
            "grupo"
        )
        .order_by(
            "ordem"
        )
    )

    grupos_produto = {
        item.grupo_id: item
        for item in grupos_cadastrados
    }

    # ========================================================
    # TODOS OS GRUPOS DA LOJA
    # ========================================================

    grupos_sabores = _buscar_grupos_sabores(
        loja
    )

    # ========================================================
    # MARCA OS GRUPOS SELECIONADOS
    # ========================================================

    for grupo in grupos_sabores:

        vinculo = grupos_produto.get(
            grupo.id
        )

        if vinculo:

            grupo.selecionado = True

            grupo.ordem_produto = (
                vinculo.ordem
            )

            grupo.ativo_produto = (
                vinculo.ativo
            )

        else:

            grupo.selecionado = False
            grupo.ordem_produto = 0
            grupo.ativo_produto = True

    # ========================================================
    # POST
    # ========================================================

    if request.method == "POST":

        grupos_ids = request.POST.getlist(
            "grupo"
        )

        grupos_ids = [
            grupo_id
            for grupo_id in grupos_ids
            if grupo_id
        ]

        grupos_ids = list(
            dict.fromkeys(
                grupos_ids
            )
        )

        # ====================================================
        # VALIDA GRUPOS
        # ====================================================

        grupos = (
            GrupoDeSabores.objects
            .filter(
                id__in=grupos_ids,
                loja=loja,
                ativo=True
            )
        )

        ids_validos = set(
            grupos.values_list(
                "id",
                flat=True
            )
        )

        ids_recebidos = set()

        for grupo_id in grupos_ids:

            if grupo_id.isdigit():

                ids_recebidos.add(
                    int(grupo_id)
                )

        if ids_validos != ids_recebidos:

            messages.error(
                request,
                "Um ou mais grupos selecionados são inválidos."
            )

            return redirect(
                request.path
            )

        # ====================================================
        # REMOVE VÍNCULOS ANTIGOS
        # ====================================================

        ProdutoGrupoSabor.objects.filter(
            produto=produto
        ).delete()

        # ====================================================
        # CRIA NOVAMENTE
        # ====================================================

        for ordem, grupo_id in enumerate(
            grupos_ids,
            start=1
        ):

            ProdutoGrupoSabor.objects.create(
                produto=produto,
                grupo_id=grupo_id,
                ordem=ordem,
                ativo=True
            )

        messages.success(
            request,
            "Grupos de sabores atualizados com sucesso."
        )

        return redirect(
            "produtogruposabor:listar"
        )

    # ========================================================
    # GET
    # ========================================================

    return render(
        request,
        "produtogruposabor/produtogruposabor_form.html",
        {
            "produto": produto,
            "grupos_sabores": grupos_sabores,
            "grupos_cadastrados": grupos_cadastrados,
            "titulo": "Editar grupos de sabores"
        }
    )


# ============================================================
# EXCLUIR VÍNCULO PRODUTO / GRUPO
# ============================================================

@login_required
def excluir_produto_grupo_sabor(
    request,
    id
):

    loja = request.user.perfil.loja

    produto_grupo = get_object_or_404(
        ProdutoGrupoSabor,
        id=id,
        produto__loja=loja
    )

    if request.method == "POST":

        produto_grupo.delete()

        messages.success(
            request,
            "Grupo de sabores removido do produto."
        )

    return redirect(
        "produtogruposabor:listar"
    )


# ============================================================
# ALTERAR STATUS DO PRODUTO
# ============================================================

@login_required
def alterar_status_produto_grupo_sabor(
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
        "produtogruposabor:listar"
    )


# ============================================================
# FUNÇÃO AUXILIAR
# ============================================================

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