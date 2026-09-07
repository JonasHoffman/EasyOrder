from Cardapio.models import EstruturaCardapio
ESTRUTURA_PADRAO_CARDAPIO = [
    ("banner", 1),
    ("promocoes", 2),
    ("mais_vendidos", 3),
    ("categorias", 4),
    ("combos", 5),
    ("novidades", 6),
    ("recomendados", 7),
]


def criar_estrutura_cardapio(loja):

    for tipo, ordem in ESTRUTURA_PADRAO_CARDAPIO:

        EstruturaCardapio.objects.get_or_create(
            loja=loja,
            tipo=tipo,
            defaults={
                "ordem": ordem,
                "ativo": True,
            }
        )