from django.apps import AppConfig


class CardapioConfig(AppConfig):
    name = 'Cardapio'

class CardapioConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"

    name = "Cardapio"

    def ready(self):
        import Cardapio.signals