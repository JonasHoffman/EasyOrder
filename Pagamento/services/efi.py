from datetime import timedelta
import uuid

from django.conf import settings
from django.utils import timezone

from efipay import EfiPay


def criar_cliente_pix():

    return EfiPay(
        settings.EFIPAY_PIX_CREDENTIALS
    )
def criar_cliente():

    return EfiPay(
        settings.EFIPAY_CREDENTIALS
    )

def gerar_txid():

    return uuid.uuid4().hex[:35]


def criar_cobranca_pix(pagamento):

    efi = criar_cliente_pix()

    txid = pagamento.identificador_externo

    if not txid:
        txid = gerar_txid()

        pagamento.identificador_externo = txid

        pagamento.save(
            update_fields=[
                "identificador_externo",
                "atualizado_em",
            ]
        )

    body = {
        "calendario": {
            "expiracao": 3600,
        },
        "valor": {
            "original": f"{pagamento.valor:.2f}",
        },
        "chave": settings.EFIPAY_PIX_CHAVE,
        "solicitacaoPagador": (
            f"Pedido {pagamento.pedido.numero}"
        ),
    }

    resposta = efi.pix_create_charge(
        params={
            "txid": txid,
        },
        body=body,
    )

    if "txid" not in resposta:

        raise Exception(
            f"Erro ao criar cobrança Pix: {resposta}"
        )

    loc = resposta.get("loc")

    if not loc or "id" not in loc:

        raise Exception(
            "A Efí criou a cobrança, "
            "mas não retornou o loc.id."
        )

    loc_id = loc["id"]

    qr_code = efi.pix_generate_qrcode(
        params={
            "id": loc_id,
        }
    )

    expiracao = (
        timezone.now()
        + timedelta(seconds=3600)
    )

    pagamento.dados_gateway = {
        "txid": resposta.get("txid"),
        "loc_id": loc_id,
        "pix_copia_e_cola": resposta.get(
            "pixCopiaECola"
        ),
        "qrcode": qr_code.get(
            "imagemQrcode"
        ),
        "link_visualizacao": qr_code.get(
            "linkVisualizacao"
        ),
        "expira_em": expiracao.isoformat(),
    }

    pagamento.status = "pendente"

    pagamento.save(
        update_fields=[
            "dados_gateway",
            "status",
            "atualizado_em",
        ]
    )

    return pagamento

def criar_link_pagamento_cartao(pagamento):

    efi = criar_cliente()

    body = {
        "items": [
            {
                "name": f"Pedido {pagamento.pedido.numero}",
                "value": int(pagamento.valor * 100),
                "amount": 1,
            }
        ],

        "metadata": {
            "custom_id": str(pagamento.id),

            "notification_url": (
                "https://SEU-DOMINIO.com/pagamento/webhook/efi/"
            ),
        },

        "settings": {
            "payment_method": "credit_card",
            "request_delivery_address": False,
            "expire_at": (
                timezone.localdate() + timedelta(days=1)
            ).strftime("%Y-%m-%d"),

            "message": (
                f"Pagamento do Pedido "
                f"#{pagamento.pedido.numero}"
            ),
        },
    }

    resposta = efi.create_one_step_link(
        body=body
    )

    if "data" not in resposta:

        raise Exception(
            f"Erro ao criar link de pagamento: {resposta}"
        )

    data = resposta["data"]

    payment_url = data.get(
        "payment_url"
    )

    if not payment_url:

        raise Exception(
            "A Efí não retornou o payment_url."
        )

    pagamento.identificador_externo = str(
        data.get("charge_id")
    )

    pagamento.dados_gateway = {
        "charge_id": data.get(
            "charge_id"
        ),

        "payment_url": payment_url,

        "payment_method": data.get(
            "payment_method"
        ),

        "status_efi": data.get(
            "status"
        ),
    }

    pagamento.status = "pendente"

    pagamento.save(
        update_fields=[
            "identificador_externo",
            "dados_gateway",
            "status",
            "atualizado_em",
        ]
    )

    return pagamento