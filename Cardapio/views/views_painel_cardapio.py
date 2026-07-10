from django.shortcuts import render


def painel_cardapio(request):

    cards = [

        {
            "titulo": "Categorias",
            "descricao": "Organize os produtos por categorias.",
            "url_listar": "categorias:listar",
            "url_novo": "categorias:novo",
        },

        {
            "titulo": "Produtos",
            "descricao": "Cadastre os produtos vendidos.",
            "url_listar": "produtos:listar",
            "url_novo": "produtos:novo",
        },

        {
            "titulo": "Sabores",
            "descricao": "Cadastre sabores para pizzas e outros produtos.",
            "url_listar": "sabor:listar",
            "url_novo": "sabor:novo",
        },

        {
            "titulo": "Grupos de Adicionais",
            "descricao": "Organize os adicionais em grupos.",
            "url_listar": "grupos_adicionais:listar",
            "url_novo": "grupos_adicionais:novo",
        },

        {
            "titulo": "Adicionais",
            "descricao": "Cadastre os adicionais disponíveis.",
            "url_listar": "item_adicional:listar",
            "url_novo": "item_adicional:novo",
        },

        # {
        #     "titulo": "Combos",
        #     "descricao": "Monte combos de produtos.",
        #     "url_listar": "combos:listar",
        #     "url_novo": "combos:novo",
        # },

    ]

    return render(
        request,
        "painel/cardapio_painel.html",
        {
            "cards": cards
        }
    )