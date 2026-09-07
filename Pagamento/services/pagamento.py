from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from Pagamento.models import Pagamento
from Pedidos.models import PedidoStatus, PedidoStatusHistorico
from Pagamento.services.impressao import gerar_comanda_cozinha

@transaction.atomic
def confirmar_pagamento(pagamento):

    if pagamento.status == "pago":
        return pagamento

    agora = timezone.now()

    pagamento.status = "pago"
    pagamento.pago_em = agora

    pagamento.save(
        update_fields=[
            "status",
            "pago_em",
            "atualizado_em",
        ]
    )

    pedido = pagamento.pedido

    status_recebido = PedidoStatus.objects.get(
        loja=pedido.loja,
        codigo="recebido",
        ativo=True,
    )

    status_anterior = pedido.status

    pedido.status = status_recebido
    pedido.confirmado_em = agora

    pedido.save(
        update_fields=[
            "status",
            "confirmado_em",
            "atualizado_em",
        ]
    )

    PedidoStatusHistorico.objects.create(
        pedido=pedido,
        status_anterior=status_anterior,
        status_novo=status_recebido,
        observacao="Pagamento aprovado.",
    )
    comanda = gerar_comanda_cozinha(pedido)

    
    return pagamento


def processar_webhook_pix(dados):

    pix_list = dados.get("pix", [])

    pagamentos_confirmados = []

    for pix in pix_list:

        txid = pix.get("txid")

        if not txid:
            continue

        try:

            pagamento = Pagamento.objects.get(
                identificador_externo=txid
            )

        except Pagamento.DoesNotExist:

            continue

        valor_recebido = pix.get("valor")

        if valor_recebido:

            if str(valor_recebido) != str(
                pagamento.valor
            ):
                continue

        pagamento = confirmar_pagamento(
            pagamento
        )

        pagamentos_confirmados.append(
            pagamento
        )

    return pagamentos_confirmados

def processar_webhook_cartao(dados):

    pagamentos_confirmados = []

    data = dados.get(
        "data",
        []
    )

    for evento in data:

        identifiers = evento.get(
            "identifiers",
            {}
        )

        charge_id = identifiers.get(
            "charge_id"
        )

        if not charge_id:
            continue

        status = (
            evento
            .get("status", {})
            .get("current")
        )

        if status != "paid":
            continue

        try:

            pagamento = Pagamento.objects.get(
                identificador_externo=str(
                    charge_id
                ),
                metodo="cartao",
            )

        except Pagamento.DoesNotExist:

            continue

        valor_recebido = evento.get(
            "value"
        )

        if valor_recebido is not None:

            valor_recebido = Decimal(
                str(valor_recebido)
            ) / Decimal("100")

            if valor_recebido != pagamento.valor:

                continue

        pagamento = confirmar_pagamento(
            pagamento
        )

        pagamentos_confirmados.append(
            pagamento
        )

    return pagamentos_confirmados

def simular_pagamento_pix(pagamento):
    """
    Simula a confirmação de pagamento enviada pela Efí.
    """

    dados = {
        "pix": [
            {
                "endToEndId": "TESTE-EFI-123456",
                "txid": pagamento.identificador_externo,
                "valor": str(pagamento.valor),
                "horario": timezone.now().isoformat(),
            }
        ]
    }

    return processar_webhook_pix(dados)


def simular_pagamento_cartao(pagamento):
    """
    Simula a confirmação de pagamento enviada pela Efí.
    """

    dados = {
        "data": [
            {
                "identifiers": {
                    "charge_id": str(
                        pagamento.identificador_externo
                    )
                },
                "status": {
                    "current": "paid"
                },
                "value": int(
                    pagamento.valor * Decimal("100")
                ),
            }
        ]
    }

    return processar_webhook_cartao(dados)