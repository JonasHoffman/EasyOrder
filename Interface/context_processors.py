from django.db.models import Q
from Interface.models import MenuItem, NavTop
from Usuarios.models import PermissaoView
from Cardapio.carrinho import Cart


def menu_items(request):

    user = request.user

    menus = MenuItem.objects.prefetch_related(
        "subitens__subitens"
    )

    if not user.is_authenticated:

        for menu in menus:
            menu.subitens_permitidos = []

            for sub in menu.subitens.all():
                sub.subitens_permitidos = []

        return {
            "menus": menus
        }

    permissoes_ids = set(
        PermissaoView.objects.filter(
            pode_acessar=True
        ).filter(
            Q(usuario=user) |
            Q(grupo__in=user.groups.all())
        ).values_list(
            "view_id",
            flat=True
        )
    )

    for menu in menus:

        menu.subitens_permitidos = []

        for sub in menu.subitens.all():

            # Futuramente a permissão do submenu
            # pode ser aplicada aqui.
            sub.subitens_permitidos = [
                item
                for item in sub.subitens.all()
                # if item.view_id is None
                # or item.view_id in permissoes_ids
            ]

            menu.subitens_permitidos.append(sub)

    return {
        "menus": menus
    }



def nav_top(request):
    return {'nav': NavTop.objects.all()}

# delivery/context_processors.py

def carrinho(request):
    return {'carrinho': Cart(request)}