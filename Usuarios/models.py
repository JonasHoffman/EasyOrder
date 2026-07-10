from django.contrib.auth.models import User
from django.db import models
from Lojas.models import Loja
from django.contrib.auth.models import User, Group


class PerfilUsuario(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    loja = models.ForeignKey(
        Loja,
        on_delete=models.CASCADE,
        related_name="usuarios"
    )

    def __str__(self):
        return self.user.username
    
class SistemaModulo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=100)

class SistemaView(models.Model):
    modulo = models.ForeignKey(SistemaModulo, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)  # Exemplo: 'entrada_list'
    rota = models.CharField(max_length=200)  # Exemplo: '/estoque/entrada/'

    def __str__(self):
        return f"{self.modulo.nome} - {self.nome}"


class PermissaoView(models.Model):
    view = models.ForeignKey(SistemaView, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pode_acessar = models.BooleanField(default=True)

    class Meta:
        unique_together = ('view', 'grupo', 'usuario')