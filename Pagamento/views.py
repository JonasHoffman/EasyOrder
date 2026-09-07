from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Pagamento.models import Pagamento
import json
from django.utils import timezone
from Pagamento.services.pagamento import processar_webhook_pix,processar_webhook_cartao,simular_pagamento_cartao,simular_pagamento_pix
from Pagamento.services.efi import (
    criar_link_pagamento_cartao,
)
from django.conf import settings
from .services.demo import aprovar_pagamento_demo


@csrf_exempt
def webhook_efi(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "erro": "Método não permitido"
            },
            status=405
        )

    try:

        dados = json.loads(
            request.body
        )

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "erro": "JSON inválido"
            },
            status=400
        )

    pagamentos_pix = (
        processar_webhook_pix(
            dados
        )
    )

    pagamentos_cartao = (
        processar_webhook_cartao(
            dados
        )
    )

    return JsonResponse(
        {
            "status": "ok",

            "pix": len(
                pagamentos_pix
            ),

            "cartao": len(
                pagamentos_cartao
            ),
        }
    )
@login_required
def pagamento_pix(request, pagamento_id):

    pagamento = get_object_or_404(
        Pagamento,
        id=pagamento_id,
        
    )

    dados = pagamento.dados_gateway or {}

    contexto = {
        "pagamento": pagamento,
        "qrcode": dados.get("qrcode"),
        "pix_copia_e_cola": dados.get(
            "pix_copia_e_cola"
        ),
        "expira_em": dados.get(
            "expira_em"
        ),
    }

    return render(
        request,
        "Pagamento/pagamento_pix.html",
        contexto,
    )

@login_required
def pagamento_cartao(
    request,
    pagamento_id
):

    pagamento = get_object_or_404(
        Pagamento,
        id=pagamento_id,
        metodo="cartao",
    )

    dados = pagamento.dados_gateway or {}

    payment_url = dados.get(
        "payment_url"
    )

    if not payment_url:

        pagamento = criar_link_pagamento_cartao(
            pagamento
        )

        dados = pagamento.dados_gateway or {}

        payment_url = dados.get(
            "payment_url"
        )

    if not payment_url:

        return JsonResponse(
            {
                "erro": "Não foi possível gerar o pagamento."
            },
            status=500
        )

    return redirect(
        payment_url
    )

@login_required
def simular_pagamento(request, pagamento_id):

    pagamento = get_object_or_404(
        Pagamento,
        id=pagamento_id,
    )

    if pagamento.metodo == "pix":

        pagamentos = simular_pagamento_pix(
            pagamento
        )

    elif pagamento.metodo == "cartao":

        pagamentos = simular_pagamento_cartao(
            pagamento
        )

    else:

        return JsonResponse(
            {
                "erro": (
                    "Este método de pagamento "
                    "não pode ser simulado."
                )
            },
            status=400
        )

    return JsonResponse(
        {
            "status": "ok",
            "pagamento_id": pagamento.id,
            "pagamento_status": pagamento.status,
            "pedido_id": pagamento.pedido.id,
            "pedido_numero": pagamento.pedido.numero,
            "pedido_status": pagamento.pedido.status.codigo,
            "confirmados": len(pagamentos),
        }
    )

@login_required
def etiqueta_expedicao(request, pedido_id):

    from Pedidos.models import Pedido

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        loja=request.user.perfil.loja,
    )

    # ==========================================
    # IDENTIFICAR CLIENTE
    # ==========================================

    if pedido.telefone_cliente:

        pedidos_cliente = (
            Pedido.objects
            .filter(
                loja=pedido.loja,
                telefone_cliente=pedido.telefone_cliente,
                id__lte=pedido.id,
            )
            .count()
        )

    else:

        pedidos_cliente = (
            Pedido.objects
            .filter(
                loja=pedido.loja,
                nome_cliente=pedido.nome_cliente,
                id__lte=pedido.id,
            )
            .count()
        )

    primeiro_pedido = pedidos_cliente == 1

    return render(
        request,
        "Pagamento/etiqueta_expedicao.html",
        {
            "pedido": pedido,
            "primeiro_pedido": primeiro_pedido,
        },
    )

@login_required
def comanda_cozinha(request, pedido_id):

    from Pedidos.models import Pedido

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        loja=request.user.perfil.loja,
    )

    return render(
        request,
        "Pagamento/comanda_cozinha.html",
        {
            "pedido": pedido,
        },
    )

@login_required
def imprimir_pedido(request, pedido_id):

    from Pedidos.models import Pedido

    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        loja=request.user.perfil.loja,
    )

    if pedido.status.codigo == "recebido":

        return redirect(
            "pagamento:comanda_cozinha",
            pedido_id=pedido.id,
        )

    if pedido.status.codigo == "pronto":

        return redirect(
            "pagamento:etiqueta_expedicao",
            pedido_id=pedido.id,
        )

    return JsonResponse(
        {
            "erro": (
                "Este pedido não possui "
                "uma impressão disponível neste status."
            )
        },
        status=400,
    )

def pagamento_demo_aprovar(request, pagamento_id):

    if not settings.PAGAMENTO_DEMO:
        return redirect("cardapio:home")

    pagamento = get_object_or_404(
        Pagamento,
        id=pagamento_id
    )

    aprovar_pagamento_demo(pagamento)

    return redirect(
        "pagamento:sucesso",
        pedido_id=pagamento.pedido.id
    )