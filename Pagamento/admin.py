from django.contrib import admin

from .models import Pagamento


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "pedido",
        "metodo",
        "gateway",
        "status",
        "valor",
        "criado_em",
        "pago_em",
    )

    list_filter = (
        "metodo",
        "gateway",
        "status",
    )

    search_fields = (
        "pedido__id",
        "identificador_externo",
    )

    readonly_fields = (
        "criado_em",
        "atualizado_em",
        "pago_em",
    )

    ordering = (
        "-criado_em",
    )