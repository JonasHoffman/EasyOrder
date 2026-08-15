from django.utils import timezone


def gerar_comanda_cozinha(pedido):

    linhas = []

    linhas.append("================================")
    linhas.append("          EASYORDER")
    linhas.append(f"          PEDIDO #{pedido.numero}")
    linhas.append(
        timezone.localtime(
            pedido.criado_em
        ).strftime("%d/%m/%Y %H:%M")
    )
    linhas.append("================================")
    linhas.append("")

    for item in pedido.itens.all():

        quantidade = item.quantidade

        # Evita mostrar 2.00 quando for quantidade inteira
        if quantidade == int(quantidade):
            quantidade = int(quantidade)

        linhas.append(
            f"{quantidade}x {item.nome_produto}"
        )

        # ==============================
        # SABORES
        # ==============================

        sabores = item.sabores.all()

        for sabor in sabores:

            linhas.append(
                f"   • {sabor.nome_sabor}"
            )

        # ==============================
        # INGREDIENTES REMOVIDOS
        # ==============================

        ingredientes = item.ingredientes.filter(
            removido=True
        )

        for ingrediente in ingredientes:

            linhas.append(
                f"   • SEM {ingrediente.nome_ingrediente}"
            )

        # ==============================
        # ADICIONAIS
        # ==============================

        adicionais = item.adicionais.all()

        for adicional in adicionais:

            quantidade_adicional = (
                adicional.quantidade
            )

            if quantidade_adicional == int(
                quantidade_adicional
            ):
                quantidade_adicional = int(
                    quantidade_adicional
                )

            linhas.append(
                f"   • +{quantidade_adicional} "
                f"{adicional.nome_adicional}"
            )

        # ==============================
        # COMBO
        # ==============================

        combos = item.itens_combo.all()

        for combo in combos:

            quantidade_combo = combo.quantidade

            if quantidade_combo == int(
                quantidade_combo
            ):
                quantidade_combo = int(
                    quantidade_combo
                )

            linhas.append(
                f"   • {quantidade_combo}x "
                f"{combo.nome_grupo}: "
                f"{combo.nome_produto}"
            )

        # ==============================
        # OBSERVAÇÃO DO ITEM
        # ==============================

        if item.observacao:

            linhas.append(
                f"   • OBS: {item.observacao}"
            )

        linhas.append("")

    # ==============================
    # OBSERVAÇÃO DO PEDIDO
    # ==============================

    if pedido.observacao:

        linhas.append("--------------------------------")
        linhas.append("OBSERVAÇÃO DO PEDIDO:")
        linhas.append(pedido.observacao)
        linhas.append("")

    # ==============================
    # TIPO DE ENTREGA
    # ==============================

    linhas.append("--------------------------------")

    if pedido.tipo_entrega == "ENTREGA":

        linhas.append("ENTREGA")

    elif pedido.tipo_entrega == "RETIRADA":

        linhas.append("RETIRADA")

    elif pedido.tipo_entrega == "CONSUMO_LOCAL":

        linhas.append("CONSUMO NO LOCAL")

    linhas.append("================================")

    return "\n".join(linhas)

from decimal import Decimal
from django.utils import timezone


def gerar_etiqueta_expedicao(pedido):

    linhas = []

    # ==========================================
    # CABEÇALHO
    # ==========================================

    linhas.append("================================")
    linhas.append("          EASYORDER")
    linhas.append("================================")

    linhas.append(
        f"PEDIDO: #{pedido.numero}"
    )

    linhas.append(
        "DATA: "
        + timezone.localtime(
            pedido.criado_em
        ).strftime("%d/%m/%Y %H:%M")
    )

    # ==========================================
    # CLIENTE
    # ==========================================

    linhas.append("")

    linhas.append(
        f"CLIENTE: {pedido.nome_cliente}"
    )

    # ==========================================
    # PRIMEIRO PEDIDO
    # ==========================================

    quantidade_pedidos = pedido.loja.pedidos.filter(
        nome_cliente=pedido.nome_cliente
    ).count()

    if quantidade_pedidos == 1:

        linhas.append(
            "CLIENTE: 1º PEDIDO"
        )

    else:

        linhas.append(
            "CLIENTE: CLIENTE RECORRENTE"
        )

    # ==========================================
    # ID
    # ==========================================

    linhas.append("")

    linhas.append(
        f"ID: {pedido.id}"
    )

    # ==========================================
    # ENTREGA / RETIRADA
    # ==========================================

    linhas.append("")
    linhas.append("--------------------------------")

    if pedido.tipo_entrega == "ENTREGA":

        linhas.append("ENTREGA")
        linhas.append("--------------------------------")

        if pedido.endereco:
            linhas.append(
                pedido.endereco
            )

        if pedido.numero_endereco:
            linhas.append(
                f"Nº {pedido.numero_endereco}"
            )

        if pedido.complemento:
            linhas.append(
                pedido.complemento
            )

        if pedido.bairro:
            linhas.append(
                pedido.bairro
            )

        if pedido.cidade or pedido.estado:

            cidade_estado = (
                f"{pedido.cidade}"
            )

            if pedido.estado:
                cidade_estado += (
                    f" - {pedido.estado}"
                )

            linhas.append(
                cidade_estado
            )

        if pedido.cep:
            linhas.append(
                f"CEP: {pedido.cep}"
            )

        if pedido.referencia:

            linhas.append("")

            linhas.append(
                f"REFERÊNCIA: "
                f"{pedido.referencia}"
            )

    elif pedido.tipo_entrega == "RETIRADA":

        linhas.append(
            "RETIRADA NO LOCAL"
        )

    elif pedido.tipo_entrega == "CONSUMO_LOCAL":

        linhas.append(
            "CONSUMO NO LOCAL"
        )

    # ==========================================
    # ITENS
    # ==========================================

    linhas.append("")
    linhas.append("--------------------------------")
    linhas.append("ITENS")
    linhas.append("--------------------------------")

    for item in pedido.itens.all():

        quantidade = item.quantidade

        if quantidade == int(quantidade):
            quantidade = int(quantidade)

        linhas.append(
            f"{quantidade}x "
            f"{item.nome_produto}"
        )

        # SABORES

        for sabor in item.sabores.all():

            linhas.append(
                f"   • {sabor.nome_sabor}"
            )

        # INGREDIENTES REMOVIDOS

        for ingrediente in item.ingredientes.filter(
            removido=True
        ):

            linhas.append(
                f"   • SEM "
                f"{ingrediente.nome_ingrediente}"
            )

        # ADICIONAIS

        for adicional in item.adicionais.all():

            quantidade_adicional = (
                adicional.quantidade
            )

            if quantidade_adicional == int(
                quantidade_adicional
            ):
                quantidade_adicional = int(
                    quantidade_adicional
                )

            linhas.append(
                f"   • +{quantidade_adicional} "
                f"{adicional.nome_adicional}"
            )

        # COMBOS

        for combo in item.itens_combo.all():

            quantidade_combo = (
                combo.quantidade
            )

            if quantidade_combo == int(
                quantidade_combo
            ):
                quantidade_combo = int(
                    quantidade_combo
                )

            linhas.append(
                f"   • {quantidade_combo}x "
                f"{combo.nome_grupo}: "
                f"{combo.nome_produto}"
            )

        # OBSERVAÇÃO DO ITEM

        if item.observacao:

            linhas.append(
                f"   • OBS: "
                f"{item.observacao}"
            )

    # ==========================================
    # PAGAMENTO
    # ==========================================

    pagamento = getattr(
        pedido,
        "pagamento",
        None
    )

    linhas.append("")
    linhas.append("--------------------------------")
    linhas.append("PAGAMENTO")
    linhas.append("--------------------------------")

    if pagamento:

        metodo = dict(
            pagamento.METODOS
        ).get(
            pagamento.metodo,
            pagamento.metodo
        )

        linhas.append(
            metodo
        )

        if pagamento.status == "pago":

            linhas.append(
                "PAGO"
            )

        else:

            linhas.append(
                pagamento.status.upper()
            )

    else:

        linhas.append(
            "PAGAMENTO NÃO INFORMADO"
        )

    # ==========================================
    # RESUMO FINANCEIRO
    # ==========================================

    linhas.append("")
    linhas.append("--------------------------------")
    linhas.append("RESUMO")
    linhas.append("--------------------------------")

    linhas.append(
        f"PEDIDO:    R$ {pedido.subtotal:.2f}"
    )

    linhas.append(
        f"ENTREGA:   R$ {pedido.taxa_entrega:.2f}"
    )

    linhas.append(
        f"DESCONTO:  R$ {pedido.desconto:.2f}"
    )

    linhas.append("--------------------------------")

    linhas.append(
        f"TOTAL:     R$ {pedido.total:.2f}"
    )

    # ==========================================
    # COBRAR
    # ==========================================

    valor_cobrar = pedido.total

    if pagamento and pagamento.status == "pago":

        valor_cobrar = Decimal("0.00")

    linhas.append("")

    linhas.append(
        f"COBRAR DO CLIENTE: "
        f"R$ {valor_cobrar:.2f}"
    )

    linhas.append("================================")

    return "\n".join(linhas)