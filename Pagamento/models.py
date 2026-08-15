from django.db import models


class Pagamento(models.Model):

    METODOS = (
        ("pix", "PIX"),
        ("cartao", "Cartão"),
        ("dinheiro", "Dinheiro na entrega"),
    )

    STATUS = (
        ("pendente", "Pendente"),
        ("processando", "Processando"),
        ("pago", "Pago"),
        ("recusado", "Recusado"),
        ("cancelado", "Cancelado"),
        ("expirado", "Expirado"),
    )

    GATEWAYS = (
        ("efi", "Efí"),
        ("manual", "Manual"),
    )

    pedido = models.OneToOneField(
        "Pedidos.Pedido",
        on_delete=models.PROTECT,
        related_name="pagamento"
    )

    metodo = models.CharField(
        max_length=20,
        choices=METODOS
    )

    gateway = models.CharField(
        max_length=20,
        choices=GATEWAYS,
        default="manual"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="pendente"
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    identificador_externo = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    dados_gateway = models.JSONField(
        blank=True,
        null=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    pago_em = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Pagamento #{self.id} - Pedido #{self.pedido.id}"