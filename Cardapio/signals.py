from django.db.models.signals import post_save
from django.dispatch import receiver

from Lojas.models import Loja

from Cardapio.services.criar_estruturacardapio import (
    criar_estrutura_cardapio
)


@receiver(post_save, sender=Loja)
def criar_estrutura_padrao(sender, instance, created, **kwargs):

    if created:
        criar_estrutura_cardapio(instance)