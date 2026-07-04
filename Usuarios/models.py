from django.contrib.auth.models import User
from django.db import models
from Lojas.models import Loja


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