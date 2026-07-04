from django.contrib import admin
from .models import PerfilUsuario
# Register your models here.
@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    ...