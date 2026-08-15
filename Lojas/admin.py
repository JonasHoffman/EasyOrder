from django.contrib import admin
from .models import Loja,Endereco

# Register your models here.
@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = (
        "nome",

        "telefone",
        "ativa",
    )

    list_filter = (
        "ativa",
    )

    search_fields = (
        "nome",
        
    )

    prepopulated_fields = {
        "slug": ("nome",)
    }

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    ...