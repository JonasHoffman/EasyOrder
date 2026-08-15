from django.contrib import admin
from Pedidos.models import PedidoStatus

# Register your models here.
@admin.register(PedidoStatus)
class PedidosAdmin(admin.ModelAdmin):
    ...

