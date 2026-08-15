from django.contrib import admin
from Interface.models import MenuItem,NavTop,SubMenuItem
from django import forms
# Register your models here.
ICONES = [
    ("fa-house", "🏠 Dashboard"),
    ("fa-utensils", "🍽 Cardápio"),
    ("fa-cart-shopping", "🛒 Pedidos"),
    ("fa-box", "📦 Estoque"),
    ("fa-users", "👥 Clientes"),
    ("fa-wallet", "💰 Financeiro"),
    ("fa-gear", "⚙️ Configurações"),
    ("fa-store", "🏪 Loja"),
    ("fa-tags", "🏷 Promoções"),
]


class MenuItemAdminForm(forms.ModelForm):

    icone = forms.ChoiceField(
        choices=ICONES,
        required=False,
        label="Ícone"
    )

    class Meta:
        model = MenuItem
        fields = "__all__"
@admin.register(MenuItem)
class MenuAdmin(admin.ModelAdmin):
    form = MenuItemAdminForm

@admin.register(NavTop)
class NavTopAdmin(admin.ModelAdmin):
    ...

@admin.register(SubMenuItem)
class SubMenuAdmin(admin.ModelAdmin):
    ...