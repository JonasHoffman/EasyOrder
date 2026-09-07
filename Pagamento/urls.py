from django.urls import path

from Pagamento.views import pagamento_pix,webhook_efi,pagamento_cartao,simular_pagamento,etiqueta_expedicao,comanda_cozinha,imprimir_pedido,pagamento_demo_aprovar


app_name = "pagamento"


urlpatterns = [

    path(
        "pix/<int:pagamento_id>/",
        pagamento_pix,
        name="pix",
    ),
    path(
        "webhook/efi/",
        webhook_efi,
        name="webhook_efi",
    ),
    path(
    "cartao/<int:pagamento_id>/",
    pagamento_cartao,
    name="cartao",),
    path(
    "teste/<int:pagamento_id>/",
    simular_pagamento,
    name="simular_pagamento",
    ), path(
        "etiqueta/<int:pedido_id>/",
        etiqueta_expedicao,
        name="etiqueta_expedicao",
    ),
    path(
    "comanda/<int:pedido_id>/",
    comanda_cozinha,
    name="comanda_cozinha",
),  path(
    "imprimir/<int:pedido_id>/",
    imprimir_pedido,
    name="imprimir_pedido",
    
),path(
    "demo/aprovar/<int:pagamento_id>/",
    pagamento_demo_aprovar,
    name="pagamento_demo_aprovar",
),

]