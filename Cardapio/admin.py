from django.contrib import admin
from Cardapio.models import ProdutoGrupoAdicional,ProdutoSabor,ProdutoGrupoSabor

# Register your models here.
@admin.register(ProdutoGrupoAdicional)
class ProdutoGrupoAdicionalAdmin(admin.ModelAdmin):
    ...

@admin.register(ProdutoSabor)
class ProdutoSaborAdmin(admin.ModelAdmin):
    ...

@admin.register(ProdutoGrupoSabor)
class ProdutoGrupoSaborAdmin(admin.ModelAdmin):
    ...