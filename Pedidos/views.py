from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from Pagamento.services.impressao import (
    gerar_etiqueta_expedicao,
)
from django.db.models import Count
from Pedidos.forms import PedidoStatusForm
from Pedidos.models import PedidoStatus
from Cardapio.carrinho import Cart
from Pedidos.models import (
    Pedido,
    PedidoItem,
    PedidoItemSabor,
    PedidoItemIngrediente,
    PedidoItemAdicional,
    PedidoItemCombo,
    PedidoStatus,
    PedidoStatusHistorico,
    Produto,
    Sabor,
    ProdutoComboGrupo
)
from django.conf import settings

from Pagamento.models import Pagamento


def finalizar_pedido(request):

    

    cart = Cart(request)

    

    # ==============================
    # CARRINHO VAZIO
    # ==============================

    if len(cart) == 0:

        messages.warning(
            request,
            "Seu carrinho está vazio."
        )

        return redirect(
            "carrinho:carrinho_detalhe"
        )

    # ==============================
    # LOJA
    # ==============================

    try:

        loja = request.user.perfil.loja

    except Exception as erro:

        
        raise

    # ==============================
    # GET
    # ==============================

    if request.method == "GET":

        return render(
            request,
            "pedidos/finalizar_pedido.html",
            {
                "carrinho": cart,
                "loja": loja,
            }
        )

    # ==============================
    # DADOS DO CLIENTE
    # ==============================

    nome_cliente = request.POST.get(
        "nome_cliente",
        ""
    ).strip()

    telefone_cliente = request.POST.get(
        "telefone_cliente",
        ""
    ).strip()

    # ==============================
    # ENTREGA
    # ==============================

    tipo_entrega = request.POST.get(
        "tipo_entrega",
        "ENTREGA"
    )

    endereco = request.POST.get(
        "endereco",
        ""
    ).strip()

    numero_endereco = request.POST.get(
        "numero_endereco",
        ""
    ).strip()

    complemento = request.POST.get(
        "complemento",
        ""
    ).strip()

    bairro = request.POST.get(
        "bairro",
        ""
    ).strip()

    cidade = request.POST.get(
        "cidade",
        ""
    ).strip()

    estado = request.POST.get(
        "estado",
        ""
    ).strip().upper()

    cep = request.POST.get(
        "cep",
        ""
    ).strip()

    referencia = request.POST.get(
        "referencia",
        ""
    ).strip()

    # ==============================
    # OUTROS
    # ==============================

    observacao = request.POST.get(
        "observacao",
        ""
    ).strip()

    forma_pagamento = request.POST.get(
        "forma_pagamento",
        ""
    ).strip().lower()

    # ==============================
    # VALIDAÇÕES
    # ==============================

    if not nome_cliente:

        messages.error(
            request,
            "Informe seu nome."
        )

        return redirect(
            "pedidos:finalizar_pedido"
        )

    if tipo_entrega not in (
        "ENTREGA",
        "RETIRADA",
        "CONSUMO_LOCAL",
    ):

        messages.error(
            request,
            "Tipo de atendimento inválido."
        )

        return redirect(
            "pedidos:finalizar_pedido"
        )

    # ==============================
    # VALIDAÇÃO ENTREGA
    # ==============================

    if tipo_entrega == "ENTREGA":

        if not endereco:

            messages.error(
                request,
                "Informe o endereço."
            )

            return redirect(
                "pedidos:finalizar_pedido"
            )

        if not numero_endereco:

            messages.error(
                request,
                "Informe o número do endereço."
            )

            return redirect(
                "pedidos:finalizar_pedido"
            )

        if not bairro:

            messages.error(
                request,
                "Informe o bairro."
            )

            return redirect(
                "pedidos:finalizar_pedido"
            )

    # ==============================
    # PAGAMENTO
    # ==============================

    metodos_validos = {
        "pix": "pix",
        "cartao": "cartao",
        "dinheiro": "dinheiro",
    }

    metodo = metodos_validos.get(
        forma_pagamento
    )

    if not metodo:

        messages.error(
            request,
            "Selecione uma forma de pagamento válida."
        )

        return redirect(
            "pedidos:finalizar_pedido"
        )

    # ==============================
    # GATEWAY
    # ==============================

    gateway = (
        "efi"
        if metodo in (
            "pix",
            "cartao",
        )
        else "manual"
    )

    # ==============================
    # CRIAÇÃO
    # ==============================

    try:

        with transaction.atomic():

            # ==============================
            # STATUS
            # ==============================

            if metodo in ("pix", "cartao"):

                status = (
                    PedidoStatus.objects
                    .filter(
                        loja=loja,
                        codigo="aguardando-pagamento",
                        ativo=True
                    )
                    .first()
                )

            else:

                status = (
                    PedidoStatus.objects
                    .filter(
                        loja=loja,
                        codigo="recebido",
                        ativo=True
                    )
                    .first()
                )

            if not status:

                messages.error(
                    request,
                    "Status necessário para criar o pedido não foi configurado."
                )

                return redirect(
                    "pedidos:finalizar_pedido"
                )

            # ==============================
            # NUMERO PEDIDO
            # ==============================

            ultimo_numero = (
                Pedido.objects
                .filter(
                    loja=loja
                )
                .order_by("-numero")
                .values_list(
                    "numero",
                    flat=True
                )
                .first()
            )

            if ultimo_numero is None:

                numero = 1

            else:

                numero = ultimo_numero + 1

            # ==============================
            # VALORES
            # ==============================

            subtotal = cart.get_total()

            taxa_entrega = Decimal(
                "0.00"
            )

            desconto = Decimal(
                "0.00"
            )

            total = (
                subtotal
                + taxa_entrega
                - desconto
            )

            # ==============================
            # PEDIDO
            # ==============================

            pedido = Pedido.objects.create(

                loja=loja,

                numero=numero,

                status=status,

                tipo_entrega=tipo_entrega,

                nome_cliente=nome_cliente,

                telefone_cliente=telefone_cliente,

                endereco=(
                    endereco
                    if tipo_entrega == "ENTREGA"
                    else ""
                ),

                numero_endereco=(
                    numero_endereco
                    if tipo_entrega == "ENTREGA"
                    else ""
                ),

                complemento=(
                    complemento
                    if tipo_entrega == "ENTREGA"
                    else ""
                ),

                bairro=(
                    bairro
                    if tipo_entrega == "ENTREGA"
                    else ""
                ),

                cidade=(
                    cidade
                    if tipo_entrega == "ENTREGA"
                    else ""
                ),

                estado=(
                    estado
                    if tipo_entrega == "ENTREGA"
                    else ""
                ),

                cep=(
                    cep
                    if tipo_entrega == "ENTREGA"
                    else ""
                ),

                referencia=(
                    referencia
                    if tipo_entrega == "ENTREGA"
                    else ""
                ),

                observacao=observacao,

                subtotal=subtotal,

                taxa_entrega=taxa_entrega,

                desconto=desconto,

                total=total,
            )

            

            # ==============================
            # HISTÓRICO
            # ==============================

            PedidoStatusHistorico.objects.create(

                pedido=pedido,

                status_anterior=None,

                status_novo=status,

                usuario=(
                    request.user
                    if request.user.is_authenticated
                    else None
                ),

                observacao="Pedido criado.",
            )

            # ==============================
            # ITENS
            # ==============================

            for ordem, item in enumerate(
                cart,
                start=1
            ):

                produto = item["produto"]

                quantidade = Decimal(
                    str(
                        item["quantidade"]
                    )
                )

                preco_unitario = Decimal(
                    str(
                        item["preco_unitario"]
                    )
                )

                subtotal_item = (
                    preco_unitario
                    * quantidade
                )

                # ==============================
                # PEDIDO ITEM
                # ==============================

                pedido_item = (
                    PedidoItem.objects.create(

                        pedido=pedido,

                        produto=produto,

                        nome_produto=produto.nome,

                        descricao_produto=(
                            produto.descricao
                        ),

                        quantidade=quantidade,

                        preco_unitario=(
                            preco_unitario
                        ),

                        desconto=Decimal(
                            "0.00"
                        ),

                        subtotal=subtotal_item,

                        observacao="",

                        ordem=ordem,
                    )
                )

                # ==============================
                # SABORES
                # ==============================

                # ==============================
                # SABORES
                # ==============================

                sabores = item.get(
                    "sabores",
                    []
                )

                for ordem_sabor, sabor in enumerate(
                    sabores,
                    start=1
                ):

                    if not isinstance(sabor, Sabor):
                        continue

                    PedidoItemSabor.objects.create(

                        item=pedido_item,

                        sabor=sabor,

                        nome_sabor=sabor.nome,

                        valor_adicional=(
                            sabor.valor_adicional
                            or Decimal("0.00")
                        ),

                        ordem=ordem_sabor,
                    )
                # ==============================
                # INGREDIENTES
                # ==============================

                ingredientes = item.get(
                    "ingredientes_removidos",
                    []
                )

                for ingrediente_relacao in ingredientes:

                    ingrediente = (
                        ingrediente_relacao.ingrediente
                    )

                    PedidoItemIngrediente.objects.create(

                        item=pedido_item,

                        ingrediente=ingrediente,

                        nome_ingrediente=(
                            ingrediente.nome
                        ),

                        removido=True,
                    )

                # ==============================
                # ADICIONAIS
                # ==============================

                adicionais = item.get(
                    "adicionais",
                    []
                )

                for adicional in adicionais:

                    preco_adicional = (
                        adicional.preco
                        or Decimal("0.00")
                    )

                    PedidoItemAdicional.objects.create(

                        item=pedido_item,

                        adicional=adicional,

                        nome_adicional=(
                            adicional.nome
                        ),

                        quantidade=Decimal(
                            "1.00"
                        ),

                        preco_unitario=(
                            preco_adicional
                        ),

                        subtotal=(
                            preco_adicional
                        ),
                    )

                # ==============================
                # COMBO
                # ==============================

                combo = item.get(
                    "combo",
                    {}
                )

                if combo:

                    ordem_combo = 1

                    itens_combo = combo.get(
                        "itens",
                        {}
                    )

                    for item_combo_id, quantidade_combo in itens_combo.items():

                        try:

                            item_combo_id = int(
                                item_combo_id
                            )

                            quantidade_combo = Decimal(
                                str(
                                    quantidade_combo
                                )
                            )

                        except (
                            TypeError,
                            ValueError
                        ):

                            continue

                        try:

                            item_combo = (
                                ProdutoComboGrupo.objects
                                .get(
                                    itens__id=item_combo_id
                                )
                                .itens
                                .get(
                                    id=item_combo_id
                                )
                            )

                        except (
                            ProdutoComboGrupo.DoesNotExist,
                            Produto.DoesNotExist,
                            TypeError,
                            ValueError
                        ):

                            continue

                        grupo = (
                            ProdutoComboGrupo.objects
                            .get(
                                itens__id=item_combo_id
                            )
                        )

                        produto_combo = item_combo.produto

                        if quantidade_combo <= 0:

                            quantidade_combo = Decimal(
                                "1.00"
                            )

                        preco_combo = (
                            produto_combo.preco
                            or Decimal("0.00")
                        )

                        PedidoItemCombo.objects.create(

                            item=pedido_item,

                            grupo=grupo,

                            produto=produto_combo,

                            nome_grupo=grupo.nome,

                            nome_produto=produto_combo.nome,

                            quantidade=quantidade_combo,

                            preco_unitario=preco_combo,

                            subtotal=(
                                preco_combo
                                * quantidade_combo
                            ),

                            ordem=ordem_combo,
                        )

                        ordem_combo += 1

            # ==============================
            # PAGAMENTO
            # ==============================

            pagamento = Pagamento.objects.create(

                pedido=pedido,

                metodo=metodo,

                gateway=gateway,

                status="pendente",

                valor=pedido.total,

            )
            

            

            # ==============================
            # LIMPAR CARRINHO
            # ==============================

            cart.limpar()

            if settings.PAGAMENTO_DEMO:
                from Pagamento.services.pagamento import confirmar_pagamento

                confirmar_pagamento(pagamento)

                cart.limpar()

                return redirect(
                    "pedidos:pedido_sucesso",
                    pedido_id=pedido.id
                )

        # ==================================================
        # TRANSACTION FINALIZADA
        # ==================================================

        

        # ==================================================
        # PIX
        # ==================================================

        if pagamento.metodo == "pix":

            from Pagamento.services.efi import (
                criar_cobranca_pix
            )

            pagamento = criar_cobranca_pix(
                pagamento
            )

            return redirect(
                "pagamento:pix",
                pagamento_id=pagamento.id
            )
        
        if forma_pagamento == "cartao":

            return redirect(
                "pagamento:cartao",
                pagamento_id=pagamento.id
            )

        if forma_pagamento == "dinheiro":

            return redirect(
                "pedidos:pedido_sucesso",
                pedido_id=pedido.id
            )
        # ==================================================
        # CARTÃO / DINHEIRO
        # ==================================================

        return redirect(
            "pedidos:pedido_sucesso",
            pedido_id=pedido.id
        )

    except Exception as erro:

        
        raise


def pedido_sucesso(
    request,
    pedido_id
):

    loja = request.user.perfil.loja

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        loja=loja
    )

    return render(
        request,
        "pedidos/pedido_sucesso.html",
        {
            "pedido": pedido,
            "loja":loja
        }
    )


@login_required
def kanban_pedidos(request):

    loja = request.user.perfil.loja

    # =========================================================
    # STATUS QUE APARECEM NO KANBAN
    # =========================================================

    status = (
        PedidoStatus.objects
        .filter(
            loja=loja,
            ativo=True,
            aparece_kanban=True
        )
        .order_by("ordem")
    )

    # =========================================================
    # PEDIDOS DA LOJA
    # =========================================================

    pedidos = (
        Pedido.objects
        .filter(
            loja=loja
        )
        .select_related(
            "status"
        )
        .order_by(
            "-id"
        )
    )

    # =========================================================
    # MONTAR COLUNAS
    # =========================================================

    colunas = []

    for status_item in status:

        pedidos_status = [
            pedido
            for pedido in pedidos
            if pedido.status_id == status_item.id
        ]

        colunas.append({
            "status": status_item,
            "pedidos": pedidos_status,
        })

    # =========================================================
    # ÚLTIMOS 10 PEDIDOS
    # =========================================================

    ultimos_pedidos = (
        Pedido.objects
        .filter(
            loja=loja
        )
        .select_related(
            "status"
        )
        .order_by(
            "-id"
        )[:10]
    )

    # =========================================================
    # STATUS DE FINALIZAÇÃO
    #
    # IMPORTANTE:
    # Usa o código e não o nome.
    #
    # Assim o usuário pode alterar:
    #
    # Entregue
    # Finalizados
    # Concluídos
    #
    # sem quebrar a lógica do sistema.
    # =========================================================

    status_entregue = (
        PedidoStatus.objects
        .filter(
            loja=loja,
            codigo="entregue",
            ativo=True
        )
        .first()
    )

    # =========================================================
    # CONTEXTO
    # =========================================================

    return render(
        request,
        "pedidos/kanban.html",
        {
            "colunas": colunas,
            "ultimos_pedidos": ultimos_pedidos,
            "status_entregue": status_entregue,
        }
    )


@require_POST
@login_required
def alterar_status(request):

    pedido_id = request.POST.get(
        "pedido_id"
    )

    status_id = request.POST.get(
        "status_id"
    )

    

    # =========================================================
    # VALIDAÇÕES
    # =========================================================

    if not pedido_id:

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Pedido não informado."
            },
            status=400
        )

    if not status_id:

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Status não informado."
            },
            status=400
        )

    # =========================================================
    # LOJA
    # =========================================================

    try:

        loja = request.user.perfil.loja

    except Exception as erro:

        

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Loja não encontrada."
            },
            status=400
        )

    # =========================================================
    # PEDIDO
    # =========================================================

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        loja=loja
    )

    # =========================================================
    # NOVO STATUS
    # =========================================================

    novo_status = get_object_or_404(
        PedidoStatus,
        id=status_id,
        loja=loja,
        ativo=True
    )

    # =========================================================
    # MESMO STATUS
    # =========================================================

    if pedido.status_id == novo_status.id:

        return JsonResponse(
            {
                "sucesso": True,

                "mensagem": (
                    "Pedido já está neste status."
                ),

                "pedido_id": pedido.id,

                "status_id": novo_status.id,

                "status_nome": novo_status.nome,

                "finalizador": novo_status.finalizador,
            }
        )

    # =========================================================
    # STATUS ANTERIOR
    # =========================================================

    status_anterior = pedido.status

    # =========================================================
    # VERIFICAR SE É FINALIZADOR
    # =========================================================

    finalizando = novo_status.finalizador

    

    # =========================================================
    # ATUALIZAR PEDIDO
    # =========================================================

    pedido.status = novo_status

    pedido.save(
        update_fields=[
            "status"
        ]
    )

    # =========================================================
    # HISTÓRICO
    # =========================================================

    PedidoStatusHistorico.objects.create(

        pedido=pedido,

        status_anterior=status_anterior,

        status_novo=novo_status,

        usuario=(
            request.user
            if request.user.is_authenticated
            else None
        ),

        observacao=(
            "Pedido finalizado."
            if finalizando
            else "Status alterado pelo Kanban."
        )
    )

    # =========================================================
    # ETIQUETA
    # =========================================================

    if novo_status.codigo == "pronto":

        etiqueta = gerar_etiqueta_expedicao(
            pedido
        )

        

    # =========================================================
    # RESPOSTA
    # =========================================================

    return JsonResponse(
        {
            "sucesso": True,

            "pedido_id": pedido.id,

            "status_id": novo_status.id,

            "status_nome": novo_status.nome,

            "finalizador": finalizando,
        }
    )






@login_required
def status_lista(request):

    loja = request.user.perfil.loja

    status = (
        PedidoStatus.objects
        .filter(loja=loja)
        .annotate(
            total_pedidos=Count("pedidos")
        )
        .order_by("ordem", "nome")
    )

    return render(
        request,
        "Pedidos/status_lista.html",
        {
            "status": status,
        }
    )


@login_required
def status_criar(request):

    loja = request.user.perfil.loja

    if request.method == "POST":

        form = PedidoStatusForm(
            request.POST,
            loja=loja
        )

        if form.is_valid():

            status = form.save(
                commit=False
            )

            status.loja = loja

            # Status criado pelo usuário
            status.sistema = False

            # Gera código automaticamente
            # somente na criação.
            status.codigo = (
                status.nome
                .strip()
                .lower()
                .replace(" ", "-")
            )

            # -------------------------------------------------
            # Evitar código duplicado
            # -------------------------------------------------

            codigo_base = status.codigo
            codigo = codigo_base
            contador = 2

            while PedidoStatus.objects.filter(
                loja=loja,
                codigo=codigo
            ).exists():

                codigo = (
                    f"{codigo_base}-{contador}"
                )

                contador += 1

            status.codigo = codigo

            status.save()

            messages.success(
                request,
                "Status criado com sucesso."
            )

            return redirect(
                "pedidos:status_lista"
            )

    else:

        form = PedidoStatusForm(
            loja=loja
        )

    return render(
        request,
        "Pedidos/status_form.html",
        {
            "form": form,
            "titulo": "Novo status",
        }
    )

def aplicar_regras_status_sistema(status):
    """
    Garante que os status padrão do sistema
    mantenham suas regras obrigatórias.
    """

    if not status.sistema:
        return

    regras = {

        "recebido": {
            "ativo": True,
            "aparece_kanban": True,
            "finalizador": False,
            "cancelamento": False,
        },

        "em-preparo": {
            "ativo": True,
            "aparece_kanban": True,
            "finalizador": False,
            "cancelamento": False,
        },

        "pronto": {
            "ativo": True,
            "aparece_kanban": True,
            "finalizador": False,
            "cancelamento": False,
        },

        "entregue": {
        "ativo": True,
        "finalizador": True,
        "cancelamento": False,
    },

        "cancelado": {
            "ativo": True,
            "aparece_kanban": False,
            "finalizador": False,
            "cancelamento": True,
        },
    }

    regra = regras.get(status.codigo)

    if not regra:
        return

    for campo, valor in regra.items():
        setattr(status, campo, valor)

@login_required
def status_editar(request, pk):

    loja = request.user.perfil.loja

    status = get_object_or_404(
        PedidoStatus,
        pk=pk,
        loja=loja
    )

    if request.method == "POST":

        form = PedidoStatusForm(
            request.POST,
            instance=status,
            loja=loja
        )

        if form.is_valid():

            status = form.save(
                commit=False
            )

            # =================================================
            # GARANTIR REGRAS DO SISTEMA
            # =================================================

            aplicar_regras_status_sistema(
                status
            )

            status.save()

            messages.success(
                request,
                "Status atualizado com sucesso."
            )

            return redirect(
                "pedidos:status_lista"
            )

    else:

        form = PedidoStatusForm(
            instance=status,
            loja=loja
        )

    return render(
        request,
        "Pedidos/status_form.html",
        {
            "form": form,
            "status": status,
            "titulo": "Editar status",
        }
    )

@login_required
def status_excluir(request, pk):

    loja = request.user.perfil.loja

    status = get_object_or_404(
        PedidoStatus,
        pk=pk,
        loja=loja
    )

    # =========================================================
    # STATUS DO SISTEMA
    # =========================================================

    if status.sistema:

        messages.error(
            request,
            "Este status faz parte do sistema e não pode ser excluído."
        )

        return redirect(
            "pedidos:status_lista"
        )

    # =========================================================
    # STATUS COM PEDIDOS
    # =========================================================

    if status.pedidos.exists():

        messages.error(
            request,
            "Este status possui pedidos vinculados e não pode ser excluído."
        )

        return redirect(
            "pedidos:status_lista"
        )

    # =========================================================
    # EXCLUSÃO
    # =========================================================

    if request.method == "POST":

        status.delete()

        messages.success(
            request,
            "Status excluído com sucesso."
        )

    return redirect(
        "pedidos:status_lista"
    )