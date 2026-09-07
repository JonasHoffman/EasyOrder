from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Cardapio.models import (
    Produto,
    ItemAdicional,
    Sabor,
    SaborIngrediente,
    ProdutoComboGrupoItem,
    ProdutoComboGrupo,ProdutoSabor,ProdutoIngrediente,ProdutoGrupoCombo,ProdutoGrupoSabor
)
from Cardapio.carrinho import Cart

from Cardapio.forms.produtos_form import ProdutoForm


# ============================================================
# PRODUTOS - ADMIN
# ============================================================

@login_required
def listar_produtos(request):

    status = request.GET.get("status", "todos")
    busca = request.GET.get("q", "").strip()

    produtos = (
        Produto.objects
        .filter(
            loja=request.user.perfil.loja
        )
        .select_related(
            "categoria"
        )
        .prefetch_related(
            "sabores",
            "ingredientes",
        )
        .order_by(
            "ordem",
            "nome"
        )
    )

    # ============================
    # BUSCA
    # ============================

    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca)
        )

    # ============================
    # STATUS
    # ============================

    if status == "disponiveis":

        produtos = produtos.filter(
            disponivel=True
        )

    elif status == "indisponiveis":

        produtos = produtos.filter(
            disponivel=False
        )

    # ============================
    # SABORES / INGREDIENTES
    # ============================

    for produto in produtos:

        produto.tem_ingredientes = (
            produto.ingredientes.exists()
        )

        produto.tem_sabores = (
            produto.sabores.exists()
        )

    return render(
        request,
        "produtos/produtos_listar.html",
        {
            "produtos": produtos,
            "status": status,
            "busca": busca,
        }
    )


@login_required
def novo_produto(request):

    form = ProdutoForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST":

        if form.is_valid():

            produto = form.save(
                commit=False
            )

            produto.loja = (
                request.user.perfil.loja
            )

            produto.save()

            if produto.possui_sabores:

                messages.success(
                    request,
                    "Produto criado. Agora cadastre os sabores."
                )

                return redirect(
                    "produtogruposabor:listar",
                    produto.id
                )

            messages.success(
                request,
                "Produto criado. Agora cadastre os ingredientes."
            )

            return redirect(
                "ingredientes:ingredientes",
                produto.id
            )

    return render(
        request,
        "produtos/produtos_form.html",
        {
            "form": form,
            "titulo": "Novo Produto",
        }
    )


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

            produto = form.save(
                commit=False
            )

            if request.POST.get("remover_imagem"):

                if produto.imagem:
                    produto.imagem.delete(
                        save=False
                    )

                produto.imagem = None

            produto.save()

            messages.success(
                request,
                "Produto atualizado com sucesso!"
            )

            return redirect(
                "produtos:listar"
            )

    return render(
        request,
        "produtos/produtos_form.html",
        {
            "form": form,
            "titulo": "Editar Produto",
            "produto": produto,
        }
    )


@login_required
def detalhe_produto(request, id):

    produto = get_object_or_404(
        Produto,
        id=id,
        loja=request.user.perfil.loja
    )

    return render(
        request,
        "produtos/produtos_detalhes.html",
        {
            "produto": produto,
        }
    )


@login_required
def alterar_status_produto(request, id):

    produto = get_object_or_404(
        Produto,
        id=id,
        loja=request.user.perfil.loja
    )

    produto.disponivel = (
        not produto.disponivel
    )

    produto.save()

    messages.success(
        request,
        "Status atualizado com sucesso!"
    )

    return redirect(
        "produtos:listar"
    )


# ============================================================
# DETALHE DO PRODUTO NO CARDÁPIO
# ============================================================

@login_required
def produto_detalhe(request, slug):

    produto = get_object_or_404(
        Produto,
        slug=slug,
        disponivel=True,
        categoria__ativa=True,
        loja__ativa=True,
    )

    relacionados = (
        Produto.objects
        .filter(
            categoria=produto.categoria,
            disponivel=True,
            loja=produto.loja,
        )
        .exclude(
            id=produto.id
        )
        .order_by(
            "ordem",
            "nome"
        )[:4]
    )

    return render(
        request,
        "produtos/produtos_detalhe_cardapio.html",
        {
            "produto": produto,
            "relacionados": relacionados,
        }
    )


# ============================================================
# PERSONALIZAÇÃO
# ============================================================

@login_required
def personalizar_produto(request, slug):

    produto = get_object_or_404(
        Produto,
        slug=slug,
        loja=request.user.perfil.loja,
        disponivel=True,
    )
    loja = produto.loja

    # ============================================================
    # POST
    # ============================================================

    if request.method == "POST":

        cart = Cart(request)
        

        # ========================================================
        # PRODUTO NORMAL
        # ========================================================

        if produto.tipo != "COMBO":


            try:
                quantidade = int(
                    request.POST.get(
                        "quantidade",
                        1
                    )
                )
            except (TypeError, ValueError):
                quantidade = 1

            if quantidade <= 0:
                quantidade = 1

            # ----------------------------------------------------
            # INGREDIENTES REMOVIDOS
            # ----------------------------------------------------

            ingredientes = []

            for valor in request.POST.getlist(
                "ingredientes_removidos"
            ):

                try:
                    ingredientes.append(
                        int(valor)
                    )

                except (TypeError, ValueError):
                    continue

            # ----------------------------------------------------
            # ADICIONAIS
            # ----------------------------------------------------

            adicionais = []

            for valor in request.POST.getlist(
                "adicionais"
            ):

                try:
                    adicionais.append(
                        int(valor)
                    )

                except (TypeError, ValueError):
                    continue

            # ----------------------------------------------------
            # SABORES
            # ----------------------------------------------------

            sabores = []

            for valor in request.POST.getlist(
                "sabores"
            ):

                try:
                    sabores.append(
                        int(valor)
                    )

                except (TypeError, ValueError):
                    continue

            # ----------------------------------------------------
            # ADICIONAR
            # ----------------------------------------------------

            try:

                cart.adicionar(
                    produto=produto,
                    quantidade=quantidade,
                    ingredientes_removidos=ingredientes,
                    adicionais=adicionais,
                    sabores=sabores,
                )

            except ValueError as erro:

                messages.error(
                    request,
                    str(erro)
                )

                return redirect(
                    request.path
                )

            # ----------------------------------------------------
            # SUCESSO
            # ----------------- -----------------------------------
            
            return redirect(        
                "carrinho:carrinho_detalhe"
            )

    # ============================================================
    # FUNÇÃO PARA MONTAR OS DADOS DE UM PRODUTO
    # ============================================================

    def montar_dados_produto(produto_item):

        dados = {
            "produto": produto_item,

            "possui_sabores":
                produto_item.possui_sabores,

            "permite_multiplos_sabores":
                produto_item.permite_multiplos_sabores,

            "maximo_sabores":
                produto_item.maximo_sabores,

            "sabores": [],

            "ingredientes": [],

            "adicionais": [],
        }

        # ========================================================
        # PRODUTO COM SABORES
        # ========================================================

        if produto_item.possui_sabores:

            grupos_sabores = (
                ProdutoGrupoSabor.objects
                .filter(
                    produto=produto_item,
                    ativo=True,
                    grupo__ativo=True,
                    grupo__loja=produto_item.loja,
                )
                .select_related(
                    "grupo",
                )
                .prefetch_related(
                    "grupo__sabores",
                    "grupo__sabores__ingredientes",
                    "grupo__sabores__ingredientes__ingrediente",
                )
                .order_by(
                    "ordem",
                    "grupo__ordem",
                    "grupo__nome",
                )
            )

            for relacao_grupo in grupos_sabores:

                grupo = relacao_grupo.grupo

                for sabor in grupo.sabores.all():

                    if not sabor.ativo:
                        continue

                    ingredientes_sabor = [
                        ingrediente_sabor
                        for ingrediente_sabor
                        in sabor.ingredientes.all()
                        if (
                            ingrediente_sabor.ativo
                            and ingrediente_sabor.ingrediente.ativo
                        )
                    ]

                    dados["sabores"].append(
                        {
                            "grupo": grupo,
                            "relacao_grupo": relacao_grupo,
                            "sabor": sabor,
                            "ingredientes": ingredientes_sabor,
                        }
                    )

        # ========================================================
        # PRODUTO SEM SABORES
        # ========================================================

        else:

            dados["ingredientes"] = (
                ProdutoIngrediente.objects
                .filter(
                    produto=produto_item,
                    ativo=True,
                    ingrediente__ativo=True,
                )
                .select_related(
                    "ingrediente",
                )
                .order_by(
                    "ordem",
                    "ingrediente__ordem",
                    "ingrediente__nome",
                )
            )

        # ========================================================
        # ADICIONAIS
        # ========================================================

        dados["adicionais"] = (
            ItemAdicional.objects
            .filter(
                grupo__produtos__produto=produto_item,
                grupo__ativo=True,
                grupo__loja=produto_item.loja,
                ativo=True,
            )
            .select_related(
                "grupo",
            )
            .distinct()
            .order_by(
                "grupo__ordem",
                "ordem",
                "nome",
            )
        )

        return dados

    # ============================================================
    # PRODUTO NORMAL
    # ============================================================

    if produto.tipo != "COMBO":

        dados_produto = montar_dados_produto(
            produto
        )

        return render(
            request,
            "ingredientes/ingredientes_personalizar.html",
            {
                "produto": produto,
                "dados_produto": dados_produto,
                "loja": loja,
            }
        )

    # ============================================================
    # COMBO
    # ============================================================

    grupos = (
        ProdutoGrupoCombo.objects
        .filter(
            produto=produto,
            grupo__ativo=True,
            grupo__loja=produto.loja,
        )
        .select_related(
            "grupo",
        )
        .prefetch_related(
            "grupo__itens",
            "grupo__itens__produto",
        )
        .order_by(
            "ordem",
            "grupo__ordem",
            "grupo__nome",
        )
    )

    dados_combo = []

    # ============================================================
    # GRUPOS
    # ============================================================

    for grupo_combo in grupos:

        grupo = grupo_combo.grupo

        dados_grupo = {
            "grupo": grupo,

            "obrigatorio":
                grupo_combo.obrigatorio,

            "minimo":
                grupo_combo.minimo,

            "maximo":
                grupo_combo.maximo,

            "itens": [],
        }

        # ========================================================
        # ITENS DO GRUPO
        # ========================================================

        for item in grupo.itens.all():

            produto_item = item.produto

            if not produto_item.disponivel:
                continue

            dados_item = montar_dados_produto(
                produto_item
            )

            dados_item["item"] = item

            dados_grupo["itens"].append(
                dados_item
            )

        dados_combo.append(
            dados_grupo
        )

    # ============================================================
    # RENDER
    # ============================================================

    return render(
        request,
        "ingredientes/ingredientes_personalizar.html",
        {
            "produto": produto,
            "dados_combo": dados_combo,
            "loja":loja,
        }
    )