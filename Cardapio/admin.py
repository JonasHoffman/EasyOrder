from django.contrib import admin
from Cardapio.models import ProdutoGrupoAdicional,ProdutoSabor

# Register your models here.
@admin.register(ProdutoGrupoAdicional)
class ProdutoGrupoAdicionalAdmin(admin.ModelAdmin):
    ...

@admin.register(ProdutoSabor)
class ProdutoSaborAdmin(admin.ModelAdmin):
    ...