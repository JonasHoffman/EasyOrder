from django.db import models

# Create your models here.
from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

from Lojas.models import Loja
from Cardapio.models import (
    Produto,
    Sabor,
    Ingrediente,
    ItemAdicional,
    ProdutoComboGrupo,
)


class PedidoStatus(models.Model):

    loja = models.ForeignKey(
        Loja,
        on_delete=models.CASCADE,
        related_name="status_pedidos"
    )

    nome = models.CharField(
        max_length=60
    )

    codigo = models.SlugField(
        max_length=60
    )

    ordem = models.PositiveIntegerField(
        default=0
    )

    ativo = models.BooleanField(
        default=True
    )

    aparece_kanban = models.BooleanField(
        default=True
    )

    finalizador = models.BooleanField(
        default=False
    )

    cancelamento = models.BooleanField(
        default=False
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["ordem", "nome"]

        constraints = [
            models.UniqueConstraint(
                fields=["loja", "codigo"],
                name="status_pedido_codigo_unico_por_loja"
            )
        ]

        indexes = [
            models.Index(
                fields=["loja", "ativo", "ordem"]
            ),
        ]

    def __str__(self):
        return self.nome


class Pedido(models.Model):

    loja = models.ForeignKey(
        Loja,
        on_delete=models.CASCADE,
        related_name="pedidos"
    )

    numero = models.PositiveIntegerField()

    status = models.ForeignKey(
        PedidoStatus,
        on_delete=models.PROTECT,
        related_name="pedidos"
    )

    tipo_entrega = models.CharField(
        max_length=20,
        choices=[
            ("ENTREGA", "Entrega"),
            ("RETIRADA", "Retirada"),
            ("CONSUMO_LOCAL", "Consumo no local"),
        ],
        default="ENTREGA"
    )

    # Snapshot do cliente

    nome_cliente = models.CharField(
        max_length=150
    )

    telefone_cliente = models.CharField(
        max_length=30,
        blank=True
    )

    # Snapshot do endereço

    endereco = models.CharField(
        max_length=255,
        blank=True
    )

    numero_endereco = models.CharField(
        max_length=20,
        blank=True
    )

    complemento = models.CharField(
        max_length=100,
        blank=True
    )

    bairro = models.CharField(
        max_length=100,
        blank=True
    )

    cidade = models.CharField(
        max_length=100,
        blank=True
    )

    estado = models.CharField(
        max_length=2,
        blank=True
    )

    cep = models.CharField(
        max_length=10,
        blank=True
    )

    referencia = models.CharField(
        max_length=150,
        blank=True
    )

    observacao = models.TextField(
        blank=True
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    taxa_entrega = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    desconto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    criado_em = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    confirmado_em = models.DateTimeField(
        null=True,
        blank=True
    )

    finalizado_em = models.DateTimeField(
        null=True,
        blank=True
    )

    cancelado_em = models.DateTimeField(
        null=True,
        blank=True
    )

    motivo_cancelamento = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["-criado_em"]

        constraints = [
            models.UniqueConstraint(
                fields=["loja", "numero"],
                name="pedido_numero_unico_por_loja"
            )
        ]

        indexes = [
            models.Index(
                fields=["loja", "status"]
            ),
            models.Index(
                fields=["loja", "criado_em"]
            ),
        ]

    def __str__(self):
        return f"Pedido #{self.numero} - {self.nome_cliente}"


class PedidoItem(models.Model):

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="itens"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="pedidos"
    )

    # Snapshot do produto

    nome_produto = models.CharField(
        max_length=120
    )

    descricao_produto = models.TextField(
        blank=True
    )

    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01"))
        ]
    )

    preco_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    desconto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    observacao = models.TextField(
        blank=True
    )

    ordem = models.PositiveIntegerField(
        default=0
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["ordem", "id"]

    def __str__(self):
        return f"{self.quantidade}x {self.nome_produto}"


class PedidoItemSabor(models.Model):

    item = models.ForeignKey(
        PedidoItem,
        on_delete=models.CASCADE,
        related_name="sabores"
    )

    sabor = models.ForeignKey(
        Sabor,
        on_delete=models.PROTECT,
        related_name="pedidos"
    )

    # Snapshot

    nome_sabor = models.CharField(
        max_length=120
    )

    valor_adicional = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    ordem = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["ordem", "id"]

    def __str__(self):
        return self.nome_sabor


class PedidoItemIngrediente(models.Model):

    item = models.ForeignKey(
        PedidoItem,
        on_delete=models.CASCADE,
        related_name="ingredientes"
    )

    ingrediente = models.ForeignKey(
        Ingrediente,
        on_delete=models.PROTECT,
        related_name="pedidos"
    )

    # Snapshot

    nome_ingrediente = models.CharField(
        max_length=80
    )

    removido = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nome_ingrediente


class PedidoItemAdicional(models.Model):

    item = models.ForeignKey(
        PedidoItem,
        on_delete=models.CASCADE,
        related_name="adicionais"
    )

    adicional = models.ForeignKey(
        ItemAdicional,
        on_delete=models.PROTECT,
        related_name="pedidos"
    )

    # Snapshot

    nome_adicional = models.CharField(
        max_length=120
    )

    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("1.00")
    )

    preco_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nome_adicional


class PedidoItemCombo(models.Model):

    item = models.ForeignKey(
        PedidoItem,
        on_delete=models.CASCADE,
        related_name="itens_combo"
    )

    grupo = models.ForeignKey(
        ProdutoComboGrupo,
        on_delete=models.PROTECT,
        related_name="pedidos"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="itens_combo_pedido"
    )

    # Snapshots

    nome_grupo = models.CharField(
        max_length=80
    )

    nome_produto = models.CharField(
        max_length=120
    )

    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("1.00")
    )

    preco_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    ordem = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["ordem", "id"]

    def __str__(self):
        return f"{self.nome_grupo} - {self.nome_produto}"


class PedidoStatusHistorico(models.Model):

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="historico_status"
    )

    status_anterior = models.ForeignKey(
        PedidoStatus,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="historicos_status_anterior"
    )

    status_novo = models.ForeignKey(
        PedidoStatus,
        on_delete=models.PROTECT,
        related_name="historicos_status_novo"
    )

    usuario = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alteracoes_status_pedido"
    )

    observacao = models.CharField(
        max_length=255,
        blank=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["criado_em"]

    def __str__(self):
        return (
            f"Pedido #{self.pedido.numero} - "
            f"{self.status_novo.nome}"
        )


class PedidoPagamento(models.Model):

    STATUS_PENDENTE = "PENDENTE"
    STATUS_APROVADO = "APROVADO"
    STATUS_RECUSADO = "RECUSADO"
    STATUS_CANCELADO = "CANCELADO"

    STATUS_CHOICES = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_APROVADO, "Aprovado"),
        (STATUS_RECUSADO, "Recusado"),
        (STATUS_CANCELADO, "Cancelado"),
    ]

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="pagamentos"
    )

    forma_pagamento = models.CharField(
        max_length=50
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDENTE
    )

    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    observacao = models.CharField(
        max_length=255,
        blank=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.forma_pagamento} - R$ {self.valor}"