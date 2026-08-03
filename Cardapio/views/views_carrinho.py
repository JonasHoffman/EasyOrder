from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string


from Cardapio.models import Produto
from Cardapio.carrinho import Cart



@require_POST
def carrinho_adicionar(request, produto_id):


    cart = Cart(request)


    produto = get_object_or_404(
        Produto,
        id=produto_id
    )


    quantidade = int(
        request.POST.get(
            "quantidade",
            1
        )
    )


    ingredientes = list(
        map(
            int,
            request.POST.getlist(
                "ingredientes_removidos"
            )
        )
    )


    adicionais = list(
        map(
            int,
            request.POST.getlist(
                "adicionais"
            )
        )
    )


    cart.adicionar(
        produto,
        quantidade,
        ingredientes,
        adicionais
    )


    return JsonResponse({

        "sucesso": True,

        "total_itens": len(cart),

        "total_valor": str(
            cart.get_total()
        )

    })




@require_POST
def carrinho_remover(request):


    cart = Cart(request)


    chave = request.POST.get(
        "chave"
    )


    cart.remover(chave)



    return JsonResponse({

        "sucesso": True,

        "total_itens": len(cart),

        "total_valor": str(
            cart.get_total()
        )

    })




def carrinho_widget(request):


    cart = Cart(request)


    html = render_to_string(

        "templates/carrinho_itens.html",

        {
            "carrinho": cart
        },

        request=request

    )


    return JsonResponse({

        "html": html,

        "total_itens": len(cart),

        "total_valor": f"{cart.get_total():.2f}"

    })




def carrinho_detalhe(request):

    cart = Cart(request)


    return render(

        request,

        "delivery/carrinho.html",

        {
            "carrinho": cart
        }

    )