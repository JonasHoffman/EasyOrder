from django.http import JsonResponse
from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string

from Cardapio.models import Produto
from Cardapio.carrinho import Cart


@require_POST
def carrinho_adicionar(request, produto_id):

    cart = Cart(request)

    produto = get_object_or_404(
        Produto,
        id=produto_id,
        disponivel=True
    )

    # ============================================================
    # QUANTIDADE
    # ============================================================

    try:
        quantidade = int(
            request.POST.get(
                "quantidade",
                1
            )
        )
    except (TypeError, ValueError):
        quantidade = 1

    if quantidade <= 0:
        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Quantidade inválida."
            },
            status=400
        )

    # ============================================================
    # INGREDIENTES
    # ============================================================

    ingredientes = []

    for valor in request.POST.getlist(
        "ingredientes_removidos"
    ):
        try:
            ingredientes.append(
                int(valor)
            )
        except (TypeError, ValueError):
            continue

    # ============================================================
    # ADICIONAIS
    # ============================================================

    adicionais = []

    for valor in request.POST.getlist(
        "adicionais"
    ):
        try:
            adicionais.append(
                int(valor)
            )
        except (TypeError, ValueError):
            continue

    # ============================================================
    # SABORES
    # ============================================================

    sabores = []

    for valor in request.POST.getlist(
        "sabores"
    ):
        try:
            sabores.append(
                int(valor)
            )
        except (TypeError, ValueError):
            continue

    # ============================================================
    # COMBO
    # ============================================================

    combo = {
        "itens": {},
        "personalizacoes": {},
    }

    for chave, valores in request.POST.lists():

        # --------------------------------------------------------
        # ITEM DO COMBO
        # --------------------------------------------------------

        if chave.startswith("combo_item_"):

            try:
                item_id = int(
                    chave.replace(
                        "combo_item_",
                        ""
                    )
                )

                quantidade_item = int(
                    valores[0]
                )

                combo["itens"][item_id] = (
                    quantidade_item
                )

            except (TypeError, ValueError):
                continue

        # --------------------------------------------------------
        # SABOR
        # --------------------------------------------------------

        elif chave.startswith("sabor_"):

            try:

                _, item_id, numero = chave.split("_")

                item_id = int(item_id)
                numero = int(numero)

                personalizacao = (
                    combo["personalizacoes"]
                    .setdefault(
                        item_id,
                        {}
                    )
                    .setdefault(
                        numero,
                        {
                            "sabores": [],
                            "ingredientes": [],
                            "adicionais": [],
                        }
                    )
                )

                personalizacao["sabores"].extend(
                    int(valor)
                    for valor in valores
                    if valor.isdigit()
                )

            except (ValueError, TypeError):
                continue

        # --------------------------------------------------------
        # INGREDIENTE
        # --------------------------------------------------------

        elif chave.startswith("ingrediente_"):

            try:

                _, item_id, numero = chave.split("_")

                item_id = int(item_id)
                numero = int(numero)

                personalizacao = (
                    combo["personalizacoes"]
                    .setdefault(
                        item_id,
                        {}
                    )
                    .setdefault(
                        numero,
                        {
                            "sabores": [],
                            "ingredientes": [],
                            "adicionais": [],
                        }
                    )
                )

                personalizacao["ingredientes"].extend(
                    int(valor)
                    for valor in valores
                    if valor.isdigit()
                )

            except (ValueError, TypeError):
                continue
            

        # --------------------------------------------------------
        # ADICIONAL
        # --------------------------------------------------------

        elif chave.startswith("adicional_"):

            try:

                _, item_id, numero = chave.split("_")

                item_id = int(item_id)
                numero = int(numero)

                personalizacao = (
                    combo["personalizacoes"]
                    .setdefault(
                        item_id,
                        {}
                    )
                    .setdefault(
                        numero,
                        {
                            "sabores": [],
                            "ingredientes": [],
                            "adicionais": [],
                        }
                    )
                )

                personalizacao["adicionais"].extend(
                    int(valor)
                    for valor in valores
                    if valor.isdigit()
                )

            except (ValueError, TypeError):
                continue

    # ============================================================
    # TESTE
    # ============================================================

    

    # ============================================================
    # ADICIONAR
    # ============================================================

    try:
        
        cart.adicionar(
            produto=produto,
            quantidade=quantidade,
            ingredientes_removidos=ingredientes,
            adicionais=adicionais,
            sabores=sabores,
            combo=combo,
        )
        

    except ValueError as erro:

        return JsonResponse(
            {
                "sucesso": False,
                "erro": str(erro)
            },
            status=400
        )

    return JsonResponse(
        {
            "sucesso": True,
            "total_itens": len(cart),
            "total_valor": f"{cart.get_total():.2f}",
        }
    )


@require_POST
def carrinho_remover(request):

    cart = Cart(request)

    chave = request.POST.get(
        "chave"
    )

    if not chave:

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Item não informado."
            },
            status=400
        )

    cart.remover(chave)

    return JsonResponse(
        {
            "sucesso": True,
            "total_itens": len(cart),
            "total_valor": f"{cart.get_total():.2f}",
        }
    )


@require_POST
def carrinho_atualizar(request):

    cart = Cart(request)

    chave = request.POST.get(
        "chave"
    )

    try:

        quantidade = int(
            request.POST.get(
                "quantidade",
                1
            )
        )

    except (TypeError, ValueError):

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Quantidade inválida."
            },
            status=400
        )

    if not chave:

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Item não informado."
            },
            status=400
        )

    cart.atualizar_quantidade(
        chave,
        quantidade
    )

    return JsonResponse(
        {
            "sucesso": True,
            "total_itens": len(cart),
            "total_valor": f"{cart.get_total():.2f}",
        }
    )


def carrinho_widget(request):

    cart = Cart(request)

    html = render_to_string(
        "templates/carrinho_itens.html",
        {
            "carrinho": cart
        },
        request=request
    )

    return JsonResponse(
        {
            "html": html,
            "total_itens": len(cart),
            "total_valor": f"{cart.get_total():.2f}",
        }
    )


def carrinho_detalhe(request):

    cart = Cart(request)

    return render(
        request,
        "carrinho/carrinho.html",
        {
            "carrinho": cart
        }
    )