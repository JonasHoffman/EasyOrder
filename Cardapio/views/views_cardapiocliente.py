from django.shortcuts import render, redirect,get_object_or_404

from Cardapio.models import (
    EstruturaCardapio,
    Categoria,
    Produto,
    Promocao,
)
from Lojas.models import Loja


def cardapio_cliente(request,slug):

    loja = get_object_or_404(
        Loja,
        slug=slug,
        ativa=True
    )

    secoes = EstruturaCardapio.objects.filter(
        loja=loja,
        ativo=True
    ).order_by(
        "ordem"
    )

    for secao in secoes:

        # =========================================================
        # CATEGORIAS
        # =========================================================

        if secao.tipo == "categorias":

            secao.dados = Categoria.objects.filter(
                loja=loja,
                ativa=True
            ).order_by(
                "ordem",
                "nome"
            )


        # =========================================================
        # PROMOÇÕES
        # =========================================================

        elif secao.tipo == "promocoes":

            secao.dados = Promocao.objects.filter(
                loja=loja,
                ativa=True,
                destaque=True
            ).order_by(
                "-data_inicio"
            )[:9]


        # =========================================================
        # MAIS VENDIDOS
        # =========================================================

        elif secao.tipo == "mais_vendidos":

            secao.dados = Produto.objects.filter(
                loja=loja,
                disponivel=True,
                destaque=True
            ).order_by(
                "ordem",
                "nome"
            )[:9]


        # =========================================================
        # COMBOS
        # =========================================================

        elif secao.tipo == "combos":

            secao.dados = Produto.objects.filter(
                loja=loja,
                tipo="COMBO",
                disponivel=True
            ).order_by(
                "ordem",
                "nome"
            )[:9]


        # =========================================================
        # NOVIDADES
        # =========================================================

        elif secao.tipo == "novidades":

            secao.dados = Produto.objects.filter(
                loja=loja,
                disponivel=True
            ).order_by(
                "-created_at"
            )[:9]


        # =========================================================
        # RECOMENDADOS
        # =========================================================

        elif secao.tipo == "recomendados":

            secao.dados = Produto.objects.filter(
                loja=loja,
                disponivel=True,
                destaque=True
            ).order_by(
                "ordem",
                "nome"
            )[:9]


        # =========================================================
        # BANNER
        # =========================================================

        elif secao.tipo == "banner":

            secao.dados = None


    return render(
        request,
        "cardapiocliente/cardapiocliente.html",
        {
            "secoes": secoes
        }
    )


def ver_todos(request, tipo):

    loja = request.user.perfil.loja


    # =========================================================
    # PROMOÇÕES
    # =========================================================

    if tipo == "promocoes":

        itens = Promocao.objects.filter(
            loja=loja,
            ativa=True,
            destaque=True
        ).order_by(
            "-data_inicio"
        )

        titulo = "Promoções"


    # =========================================================
    # MAIS VENDIDOS
    # =========================================================

    elif tipo == "mais_vendidos":

        itens = Produto.objects.filter(
            loja=loja,
            disponivel=True,
            destaque=True
        ).order_by(
            "ordem",
            "nome"
        )

        titulo = "Mais vendidos"


    # =========================================================
    # COMBOS
    # =========================================================

    elif tipo == "combos":

        itens = Produto.objects.filter(
            loja=loja,
            tipo="COMBO",
            disponivel=True
        ).order_by(
            "ordem",
            "nome"
        )

        titulo = "Combos"


    # =========================================================
    # NOVIDADES
    # =========================================================

    elif tipo == "novidades":

        itens = Produto.objects.filter(
            loja=loja,
            disponivel=True
        ).order_by(
            "-created_at"
        )

        titulo = "Novidades"


    # =========================================================
    # RECOMENDADOS
    # =========================================================

    elif tipo == "recomendados":

        itens = Produto.objects.filter(
            loja=loja,
            disponivel=True,
            destaque=True
        ).order_by(
            "ordem",
            "nome"
        )

        titulo = "Recomendados"


    # =========================================================
    # TIPO INVÁLIDO
    # =========================================================

    else:

        return redirect(
            "cardapio_cliente:cliente"
        )


    return render(
        request,
        "cardapiocliente/vertodos.html",
        {
            "tipo": tipo,
            "titulo": titulo,
            "itens": itens,
            "loja": loja,
        }
    )