from django.db import models

class Endereco(models.Model):
    cep = models.CharField(max_length=9)

    logradouro = models.CharField(max_length=150)

    numero = models.CharField(max_length=20)

    complemento = models.CharField(
        max_length=100,
        blank=True
    )

    bairro = models.CharField(max_length=100)

    cidade = models.CharField(max_length=100)

    estado = models.CharField(max_length=2)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.cidade}/{self.estado}"

class Loja(models.Model):
    nome = models.CharField(
        max_length=150,
        verbose_name="Nome Fantasia"
    )

    razao_social = models.CharField(
        max_length=200,
        verbose_name="Razão Social"
    )

    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ"
    )

    inscricao_estadual = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Inscrição Estadual"
    )

    inscricao_municipal = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Inscrição Municipal"
    )

    slug = models.SlugField(
        unique=True,
        verbose_name="Slug"
    )

    logo = models.ImageField(
        upload_to="lojas/logos/",
        blank=True,
        null=True,
        verbose_name="Logo"
    )

    telefone = models.CharField(
        max_length=20,
        blank=True
    )

    whatsapp = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    endereco = models.OneToOneField(
        Endereco,
        on_delete=models.CASCADE,
        related_name="loja",
        null=True,
        blank=True
    )
    responsavel = models.CharField(max_length=150, blank=True)

    site = models.URLField(blank=True)

    instagram = models.CharField(max_length=100, blank=True)

    facebook = models.CharField(max_length=100, blank=True)
    
    ativa = models.BooleanField(
        default=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["nome"]
        verbose_name = "Loja"
        verbose_name_plural = "Lojas"

    def __str__(self):
        return self.nome