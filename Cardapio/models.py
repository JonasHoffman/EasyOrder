from django.db import models
from Lojas.models import Loja
from django.utils import timezone
from django.utils.text import slugify

class Categoria(models.Model):

    loja = models.ForeignKey(
        Loja,
        on_delete=models.CASCADE,
        related_name="categorias"
    )

    nome = models.CharField(max_length=80)

    descricao = models.TextField(blank=True)

    slug = models.SlugField(
    max_length=120,
    blank=True,
    unique=False
    )

    imagem = models.ImageField(
        upload_to="categorias/",
        blank=True,
        null=True
    )

    ordem = models.PositiveIntegerField()

    ativa = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
    
class Produto(models.Model):

    loja = models.ForeignKey(
        Loja,
        on_delete=models.CASCADE,
        related_name="produtos"
    )
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="produtos"
    )
    TIPO_PRODUTO = (
    ("SIMPLES", "Produto Simples"),
    ("COMBO", "Combo"),
)

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_PRODUTO,
        default="SIMPLES"
    )

    nome = models.CharField(max_length=120)

    descricao = models.TextField(blank=True)

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    imagem = models.ImageField(
        upload_to="produtos/",
        blank=True,
        null=True
    )

    disponivel = models.BooleanField(default=True)

    destaque = models.BooleanField(default=False)

    permite_multiplos_sabores = models.BooleanField(default=False)

    maximo_sabores = models.PositiveSmallIntegerField(default=1)

    tempo_preparo = models.PositiveIntegerField(default=20)

    codigo = models.CharField(max_length=30, blank=True)

    ordem = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
    
class ProdutoComboGrupo(models.Model):

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="grupos_combo"
    )

    nome = models.CharField(max_length=80)

    obrigatorio = models.BooleanField(default=True)

    minimo = models.PositiveSmallIntegerField(default=1)

    maximo = models.PositiveSmallIntegerField(default=1)

    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem"]

class ProdutoComboGrupoItem(models.Model):

    grupo = models.ForeignKey(
        ProdutoComboGrupo,
        on_delete=models.CASCADE,
        related_name="itens"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE
    )

    quantidade = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=1
    )

    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem"]
    
class GrupoDeSabores(models.Model):

    loja = models.ForeignKey(
        Loja,
        on_delete=models.CASCADE,
        related_name="grupos_sabores"
    )
    descricao = models.TextField(blank=True)

    nome = models.CharField(max_length=60)

    ordem = models.PositiveIntegerField(default=0)

    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome
    

class Sabor(models.Model):

    loja = models.ForeignKey(
        Loja,
        on_delete=models.CASCADE,
        related_name="sabores"
    )

    grupo = models.ForeignKey(
        GrupoDeSabores,
        on_delete=models.PROTECT,
        related_name="sabores"
    )

    nome = models.CharField(max_length=120)

    descricao = models.TextField(blank=True)

    imagem = models.ImageField(
        upload_to="sabores/",
        blank=True,
        null=True
    )

    valor_adicional = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )

    ativo = models.BooleanField(default=True)

    ordem = models.PositiveIntegerField()

    class Meta:
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome
    
class ProdutoSabor(models.Model):

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="sabores"
    )

    sabor = models.ForeignKey(
        Sabor,
        on_delete=models.CASCADE,
        related_name="produtos"
    )

    ordem = models.PositiveIntegerField(default=0)

    ativo = models.BooleanField(default=True)

    class Meta:

        ordering = ["ordem"]

        constraints = [
            models.UniqueConstraint(
                fields=["produto", "sabor"],
                name="produto_sabor_unico"
            )
        ]

    def __str__(self):
        return f"{self.produto} - {self.sabor}"
    
class GrupoAdicional(models.Model):

    loja = models.ForeignKey(
        Loja,
        on_delete=models.CASCADE,
        related_name="grupos_adicionais"
    )

    nome = models.CharField(max_length=100)

    descricao = models.TextField(blank=True)

    obrigatorio = models.BooleanField(default=False)

    minimo = models.PositiveSmallIntegerField(default=0)

    maximo = models.PositiveSmallIntegerField(default=1)

    ordem = models.PositiveIntegerField(default=0)

    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome
    
class ItemAdicional(models.Model):

    grupo = models.ForeignKey(
        GrupoAdicional,
        on_delete=models.CASCADE,
        related_name="itens"
    )

    nome = models.CharField(max_length=120)

    descricao = models.TextField(blank=True)

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    ativo = models.BooleanField(default=True)

    imagem = models.ImageField(
    upload_to="adicionais/",
    blank=True,
    null=True
)

    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome
    
    
    
class ProdutoGrupoAdicional(models.Model):

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="grupos_adicionais"
    )

    grupo = models.ForeignKey(
        GrupoAdicional,
        on_delete=models.CASCADE,
        related_name="produtos"
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["produto", "grupo"],
                name="produto_grupo_unico"
            )
        ]

    def __str__(self):
        return f"{self.produto} - {self.grupo}"
    


class Promocao(models.Model):

    loja = models.ForeignKey(
        Loja,
        on_delete=models.CASCADE,
        related_name="promocoes"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="promocoes"
    )

    nome = models.CharField(
        max_length=120,
        help_text="Ex.: Promoção da Semana"
    )

    descricao = models.TextField(
        blank=True
    )

    preco_promocional = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    data_inicio = models.DateTimeField(
        default=timezone.now
    )

    data_fim = models.DateTimeField()

    ativa = models.BooleanField(
        default=True
    )

    destaque = models.BooleanField(
        default=True,
        help_text="Exibir na seção Promoções do cardápio."
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-data_inicio"]

    def __str__(self):
        return f"{self.nome} - {self.produto}"
    
class EstruturaCardapio(models.Model):

    TIPOS = (
        ("banner", "BANNER"),
        ("promocoes", "PROMOÇÕES"),
        ("mais_vendidos", "MAIS VENDIDOS"),
        ("categorias", "CATEGORIAS"),
        ("combos", "COMBOS"),
        ("novidades", "NOVIDADES"),
        ("recomendados", "RECOMENDADOS"),
    )

    loja = models.ForeignKey(
        Loja,
        on_delete=models.CASCADE
    )

    tipo = models.CharField(
        max_length=30,
        choices=TIPOS
    )

    ordem = models.PositiveIntegerField(default=0)

    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordem"]