from django.shortcuts import render

from Cardapio.models import (
    EstruturaCardapio,
    Categoria,
    Produto,
    Promocao
)


def cardapio_cliente(request):

    loja = request.user.perfil.loja


    secoes = EstruturaCardapio.objects.filter(
        loja=loja,
        ativo=True
    ).order_by(
        "ordem"
    )


    for secao in secoes:


        # Categorias
        if secao.tipo == "categorias":

            secao.dados = Categoria.objects.filter(
                loja=loja,
                ativa=True
            ).order_by(
                "ordem",
                "nome"
            )


        # Promoções
        elif secao.tipo == "promocoes":

            secao.dados = Promocao.objects.filter(
                loja=loja,
                ativa=True,
                destaque=True
            ).order_by(
                "-data_inicio"
            )


        # Mais vendidos
        elif secao.tipo == "mais_vendidos":

            QUAL = secao.dados = Produto.objects.filter(
                loja=loja,
                disponivel=True,
                destaque=True
            ).order_by(
                "ordem",
                "nome"
            )
            print(QUAL)




        # Combos
        elif secao.tipo == "combos":

            secao.dados = Produto.objects.filter(
                loja=loja,
                tipo="COMBO",
                disponivel=True
            ).order_by(
                "ordem",
                "nome"
            )


        # Novidades
        elif secao.tipo == "novidades":

            quel = secao.dados = Produto.objects.filter(
                loja=loja,
                disponivel=True
            ).order_by(
                "-created_at"
            )[:10]
            print('nada ',quel)


        # Recomendados
        elif secao.tipo == "recomendados":

            quil = secao.dados = Produto.objects.filter(
                loja=loja,
                disponivel=True,
                destaque=True
            ).order_by(
                "ordem",
                "nome"
            )
            print('nada 2',quil)


        # Banner (vamos criar o model depois)
        elif secao.tipo == "banner":

            secao.dados = None



    return render(
        request,
        "cardapiocliente/cardapiocliente.html",
        {
            "secoes": secoes
        }
    )