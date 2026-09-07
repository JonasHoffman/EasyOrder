from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from django.utils.text import slugify
from Interface.models import (
    MenuItem,
    SubMenuItem,
    SubSubMenuItem,
)
from Cardapio.models import (
    Categoria,
    Produto,
    GrupoDeSabores,
    Sabor,
    ProdutoGrupoSabor,
    Ingrediente,
    ProdutoIngrediente,
    SaborIngrediente,
    GrupoAdicional,
    ItemAdicional,
    ProdutoGrupoAdicional,
    ProdutoComboGrupo,
    ProdutoComboGrupoItem,
    ProdutoGrupoCombo,
    ProdutoGrupoCombo,
    Promocao,
    EstruturaCardapio,
)
from Pedidos.models import (
    Pedido,
    PedidoItem,
    PedidoItemSabor,
    PedidoItemIngrediente,
    PedidoItemAdicional,
    PedidoItemCombo,
    PedidoStatusHistorico,
    PedidoPagamento,
    PedidoStatus
)

from Pagamento.models import Pagamento
from Lojas.models import Loja
from Usuarios.models import PerfilUsuario


class Command(BaseCommand):

    help = "Cria os dados de demonstração do EasyOrder"

    def handle(self, *args, **options):

        self.stdout.write(
            self.style.WARNING(
                "Criando dados de demonstração..."
            )
        )

        # =====================================================
        # LOJA
        # =====================================================

        loja, criada = Loja.objects.get_or_create(
            slug="easyorder-demo",
            defaults={
                "nome": "EasyOrder Demo",
                "razao_social": "EasyOrder Demonstração",
                "cnpj": "00.000.000/0001-00",
                "telefone": "(48) 99999-9999",
                "email": "demo@easyorder.com",
                "ativa": True,
            }
        )

        if criada:
            self.stdout.write(
                self.style.SUCCESS(
                    "✓ Loja criada."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "→ Loja já existe."
                )
            )

        # =====================================================
        # USUÁRIO
        # =====================================================

        user, criado = User.objects.get_or_create(
            username="avaliador",
            defaults={
                "first_name": "Avaliador",
                "email": "avaliador@easyorder.com",
                "is_active": True,
            }
        )

        user.set_password("avaliador123")
        user.save()

        if criado:
            self.stdout.write(
                self.style.SUCCESS(
                    "✓ Usuário avaliador criado."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "→ Usuário avaliador já existe."
                )
            )

        # =====================================================
        # PERFIL
        # =====================================================

        perfil, criado = PerfilUsuario.objects.get_or_create(
            user=user,
            defaults={
                "loja": loja,
            }
        )

        if perfil.loja_id != loja.id:
            perfil.loja = loja
            perfil.save()

        if criado:
            self.stdout.write(
                self.style.SUCCESS(
                    "✓ Perfil do avaliador criado."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "→ Perfil do avaliador já existe."
                )
            )

        # =====================================================
        # CATEGORIAS
        # =====================================================

        self.criar_categorias(loja)
        # =====================================================
        # PRODUTOS
        # =====================================================

        self.criar_produtos(loja)



        self.criar_sabores(loja)



        self.criar_ingredientes(loja)



        self.criar_adicionais(loja)


        
        self.criar_combos(loja)



        self.criar_promocoes(loja)



        self.criar_estrutura_cardapio(loja)



        status_map = self.criar_status_pedidos(loja)



        self.criar_pedidos(loja, status_map)



        self.criar_navegacao()
        # =====================================================
        # FINAL
        # =====================================================

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "  DEMO CONFIGURADA COM SUCESSO"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )

        self.stdout.write("")

        self.stdout.write("Usuário: avaliador")
        self.stdout.write("Senha: avaliador123")
        self.stdout.write(f"Loja: {loja.nome}")

    # =========================================================
    # CATEGORIAS
    # =========================================================

    def criar_categorias(self, loja):

        categorias = [
            {
                "nome": "Pizzas",
                "descricao": "Pizzas tradicionais preparadas com ingredientes selecionados.",
                "ordem": 1,
            },
            {
                "nome": "Pizzas Especiais",
                "descricao": "Pizzas especiais com combinações exclusivas da casa.",
                "ordem": 2,
            },
            {
                "nome": "Combos",
                "descricao": "Combos completos para compartilhar com a família e amigos.",
                "ordem": 3,
            },
            {
                "nome": "Bebidas",
                "descricao": "Refrigerantes, águas e outras bebidas.",
                "ordem": 4,
            },
            {
                "nome": "Sobremesas",
                "descricao": "Sobremesas para finalizar seu pedido.",
                "ordem": 5,
            },
        ]

        for dados in categorias:

            categoria, criada = Categoria.objects.get_or_create(
                loja=loja,
                nome=dados["nome"],
                defaults={
                    "descricao": dados["descricao"],
                    "ordem": dados["ordem"],
                    "ativa": True,
                }
            )

            if criada:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Categoria criada: {categoria.nome}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"→ Categoria já existe: {categoria.nome}"
                    )
                )

    def criar_produtos(self, loja):

        categorias = {
            categoria.nome: categoria
            for categoria in Categoria.objects.filter(loja=loja)
        }

        produtos = [
            {
                "categoria": "Pizzas",
                "nome": "Pizza Grande",
                "descricao": "Molho de tomate, muçarela, calabresa fatiada, cebola e azeitonas.",
                "preco": 70.90,
                "possui_sabores": True,
                "permite_multiplos_sabores": True,
                "maximo_sabores": 3,
                "tempo_preparo": 30,
                "destaque": True,
                "ordem": 1,
            },
            {
                "categoria": "Pizzas",
                "nome": "Pizza Calabresa",
                "descricao": "Molho de tomate, muçarela, calabresa fatiada, cebola e azeitonas.",
                "preco": 49.90,
                "possui_sabores": True,
                "permite_multiplos_sabores": True,
                "maximo_sabores": 1,
                "tempo_preparo": 30,
                "destaque": True,
                "ordem": 1,
            },
            {
                "categoria": "Pizzas",
                "nome": "Pizza Frango com Catupiry",
                "descricao": "Molho de tomate, muçarela, frango desfiado e catupiry.",
                "preco": 54.90,
                "possui_sabores": True,
                "permite_multiplos_sabores": True,
                "maximo_sabores": 1,
                "tempo_preparo": 30,
                "destaque": True,
                "ordem": 2,
            },
            {
                "categoria": "Pizzas",
                "nome": "Pizza Portuguesa",
                "descricao": "Muçarela, presunto, ovos, cebola, tomate e azeitonas.",
                "preco": 52.90,
                "possui_sabores": True,
                "permite_multiplos_sabores": True,
                "maximo_sabores": 1,
                "tempo_preparo": 30,
                "destaque": False,
                "ordem": 3,
            },
            {
                "categoria": "Pizzas",
                "nome": "Pizza Quatro Queijos",
                "descricao": "Muçarela, provolone, parmesão e gorgonzola.",
                "preco": 56.90,
                "possui_sabores": True,
                "permite_multiplos_sabores": True,
                "maximo_sabores": 1,
                "tempo_preparo": 30,
                "destaque": True,
                "ordem": 4,
            },
            {
                "categoria": "Pizzas Especiais",
                "nome": "Pizza da Casa",
                "descricao": "Uma combinação especial criada pela pizzaria.",
                "preco": 64.90,
                "possui_sabores": True,
                "permite_multiplos_sabores": False,
                "maximo_sabores": 1,
                "tempo_preparo": 35,
                "destaque": True,
                "ordem": 1,
            },
            {
                "categoria": "Bebidas",
                "nome": "Coca-Cola 2L",
                "descricao": "Refrigerante Coca-Cola garrafa 2 litros.",
                "preco": 12.00,
                "possui_sabores": False,
                "ordem": 1,
            },
            {
                "categoria": "Bebidas",
                "nome": "Guaraná Antarctica 2L",
                "descricao": "Refrigerante Guaraná Antarctica garrafa 2 litros.",
                "preco": 10.00,
                "possui_sabores": False,
                "ordem": 2,
            },
            {
                "categoria": "Bebidas",
                "nome": "Água Mineral 500ml",
                "descricao": "Água mineral sem gás.",
                "preco": 4.00,
                "possui_sabores": False,
                "ordem": 3,
            },
            {
                "categoria": "Sobremesas",
                "nome": "Brownie com Chocolate",
                "descricao": "Brownie de chocolate servido como sobremesa.",
                "preco": 12.90,
                "possui_sabores": False,
                "ordem": 1,
            },
            {
                "categoria": "Sobremesas",
                "nome": "Pudim de Leite",
                "descricao": "Pudim de leite condensado com calda de caramelo.",
                "preco": 10.90,
                "possui_sabores": False,
                "ordem": 2,
            },
        ]

        for dados in produtos:

            categoria = categorias[dados["categoria"]]

            produto, criado = Produto.objects.get_or_create(
                loja=loja,
                slug=slugify(dados["nome"]),
                defaults={
                    "categoria": categoria,
                    "nome": dados["nome"],
                    "descricao": dados["descricao"],
                    "preco": dados["preco"],
                    "disponivel": True,
                    "destaque": dados.get("destaque", False),
                    "possui_sabores": dados.get("possui_sabores", False),
                    "permite_multiplos_sabores": dados.get(
                        "permite_multiplos_sabores",
                        False
                    ),
                    "maximo_sabores": dados.get("maximo_sabores", 1),
                    "tempo_preparo": dados.get("tempo_preparo", 20),
                    "ordem": dados["ordem"],
                }
            )

            if criado:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Produto criado: {produto.nome}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"→ Produto já existe: {produto.nome}"
                    )
                )

    def criar_sabores(self, loja):

        sabores_por_produto = {
            "Pizza Calabresa": {
                "grupo_nome": "Sabores Pizza Calabresa",
                "grupo_descricao": "Sabor disponível para a Pizza Calabresa.",
                "sabor_nome": "Calabresa",
                "sabor_descricao": "Calabresa fatiada, cebola e azeitonas.",
                "valor_adicional": Decimal("0.00"),
            },

            "Pizza Frango com Catupiry": {
                "grupo_nome": "Sabores Pizza Frango com Catupiry",
                "grupo_descricao": "Sabor disponível para a Pizza Frango com Catupiry.",
                "sabor_nome": "Frango com Catupiry",
                "sabor_descricao": "Frango desfiado com catupiry.",
                "valor_adicional": Decimal("0.00"),
            },

            "Pizza Portuguesa": {
                "grupo_nome": "Sabores Pizza Portuguesa",
                "grupo_descricao": "Sabor disponível para a Pizza Portuguesa.",
                "sabor_nome": "Portuguesa",
                "sabor_descricao": "Presunto, ovos, cebola, tomate e azeitonas.",
                "valor_adicional": Decimal("0.00"),
            },

            "Pizza Quatro Queijos": {
                "grupo_nome": "Sabores Pizza Quatro Queijos",
                "grupo_descricao": "Sabor disponível para a Pizza Quatro Queijos.",
                "sabor_nome": "Quatro Queijos",
                "sabor_descricao": "Muçarela, provolone, parmesão e gorgonzola.",
                "valor_adicional": Decimal("0.00"),
            },

            "Pizza da Casa": {
                "grupo_nome": "Sabores Pizza da Casa",
                "grupo_descricao": "Sabor disponível para a Pizza da Casa.",
                "sabor_nome": "Pizza da Casa",
                "sabor_descricao": "Combinação especial criada pela pizzaria.",
                "valor_adicional": Decimal("0.00"),
            },
        }

        for nome_produto, dados in sabores_por_produto.items():

            produto = Produto.objects.get(
                loja=loja,
                nome=nome_produto
            )

            # =====================================================
            # GRUPO DE SABORES DA PIZZA
            # =====================================================

            grupo, criado = GrupoDeSabores.objects.get_or_create(
                loja=loja,
                nome=dados["grupo_nome"],
                defaults={
                    "descricao": dados["grupo_descricao"],
                    "ordem": produto.ordem,
                    "ativo": True,
                }
            )

            if criado:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Grupo de sabores criado: "
                        f"{grupo.nome}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"→ Grupo de sabores já existe: "
                        f"{grupo.nome}"
                    )
                )
    def criar_sabores(self, loja):
        produtos_sabores = {
            "Pizza Grande": {
                "grupo_nome": "Sabores Pizza Grande",
                "grupo_descricao": "Escolha até 3 sabores para sua pizza.",
                "sabores": [
                    {
                        "nome": "Calabresa",
                        "descricao": "Calabresa fatiada, cebola e azeitonas.",
                        "valor_adicional": Decimal("0.00"),
                    },
                    {
                        "nome": "Frango com Catupiry",
                        "descricao": "Frango desfiado com catupiry.",
                        "valor_adicional": Decimal("0.00"),
                    },
                    {
                        "nome": "Portuguesa",
                        "descricao": "Presunto, ovos, cebola, tomate e azeitonas.",
                        "valor_adicional": Decimal("0.00"),
                    },
                    {
                        "nome": "Quatro Queijos",
                        "descricao": "Muçarela, provolone, parmesão e gorgonzola.",
                        "valor_adicional": Decimal("0.00"),
                    },
                    {
                        "nome": "Margherita",
                        "descricao": "Muçarela, tomate e manjericão.",
                        "valor_adicional": Decimal("0.00"),
                    },
                    {
                        "nome": "Bacon",
                        "descricao": "Muçarela e bacon.",
                        "valor_adicional": Decimal("0.00"),
                    },
                ],
            },

            "Pizza Calabresa": {
                "grupo_nome": "Sabores Pizza Calabresa",
                "grupo_descricao": "Sabor disponível para a Pizza Calabresa.",
                "sabores": [
                    {
                        "nome": "Calabresa",
                        "descricao": "Calabresa fatiada, cebola e azeitonas.",
                        "valor_adicional": Decimal("0.00"),
                    },
                ],
            },

            "Pizza Frango com Catupiry": {
                "grupo_nome": "Sabores Pizza Frango com Catupiry",
                "grupo_descricao": "Sabor disponível para a Pizza Frango com Catupiry.",
                "sabores": [
                    {
                        "nome": "Frango com Catupiry",
                        "descricao": "Frango desfiado com catupiry.",
                        "valor_adicional": Decimal("0.00"),
                    },
                ],
            },

            "Pizza Portuguesa": {
                "grupo_nome": "Sabores Pizza Portuguesa",
                "grupo_descricao": "Sabor disponível para a Pizza Portuguesa.",
                "sabores": [
                    {
                        "nome": "Portuguesa",
                        "descricao": "Presunto, ovos, cebola, tomate e azeitonas.",
                        "valor_adicional": Decimal("0.00"),
                    },
                ],
            },

            "Pizza Quatro Queijos": {
                "grupo_nome": "Sabores Pizza Quatro Queijos",
                "grupo_descricao": "Sabor disponível para a Pizza Quatro Queijos.",
                "sabores": [
                    {
                        "nome": "Quatro Queijos",
                        "descricao": "Muçarela, provolone, parmesão e gorgonzola.",
                        "valor_adicional": Decimal("0.00"),
                    },
                ],
            },

            "Pizza da Casa": {
                "grupo_nome": "Sabores Pizza da Casa",
                "grupo_descricao": "Sabor disponível para a Pizza da Casa.",
                "sabores": [
                    {
                        "nome": "Pizza da Casa",
                        "descricao": "Combinação especial criada pela pizzaria.",
                        "valor_adicional": Decimal("0.00"),
                    },
                ],
            },
        }

        for nome_produto, dados_produto in produtos_sabores.items():

            produto = Produto.objects.get(
                loja=loja,
                nome=nome_produto
            )

            # =====================================================
            # GRUPO DE SABORES DO PRODUTO
            # =====================================================

            grupo, criado = GrupoDeSabores.objects.get_or_create(
                loja=loja,
                nome=dados_produto["grupo_nome"],
                defaults={
                    "descricao": dados_produto["grupo_descricao"],
                    "ordem": produto.ordem,
                    "ativo": True,
                }
            )

            if criado:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Grupo de sabores criado: {grupo.nome}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"→ Grupo de sabores já existe: {grupo.nome}"
                    )
                )

            # =====================================================
            # SABORES DO GRUPO
            # =====================================================

            for ordem, dados_sabor in enumerate(
                dados_produto["sabores"],
                start=1
            ):

                sabor, criado = Sabor.objects.get_or_create(
                    loja=loja,
                    grupo=grupo,
                    nome=dados_sabor["nome"],
                    defaults={
                        "descricao": dados_sabor["descricao"],
                        "valor_adicional": dados_sabor["valor_adicional"],
                        "ativo": True,
                        "ordem": ordem,
                    }
                )

                if criado:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Sabor criado: "
                            f"{produto.nome} → {sabor.nome}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"→ Sabor já existe: "
                            f"{produto.nome} → {sabor.nome}"
                        )
                    )

            # =====================================================
            # VINCULAR GRUPO AO PRODUTO
            # =====================================================

            vinculo, criado = ProdutoGrupoSabor.objects.get_or_create(
                produto=produto,
                grupo=grupo,
                defaults={
                    "ordem": 1,
                    "ativo": True,
                }
            )

            if criado:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Grupo vinculado: "
                        f"{produto.nome} → {grupo.nome}"
                    )
                )
    def criar_ingredientes(self, loja):

        ingredientes = [
            {
                "nome": "Muçarela",
                "ordem": 1,
            },
            {
                "nome": "Calabresa",
                "ordem": 2,
            },
            {
                "nome": "Cebola",
                "ordem": 3,
            },
            {
                "nome": "Azeitona",
                "ordem": 4,
            },
            {
                "nome": "Frango",
                "ordem": 5,
            },
            {
                "nome": "Catupiry",
                "ordem": 6,
            },
            {
                "nome": "Presunto",
                "ordem": 7,
            },
            {
                "nome": "Ovo",
                "ordem": 8,
            },
            {
                "nome": "Tomate",
                "ordem": 9,
            },
            {
                "nome": "Bacon",
                "ordem": 10,
            },
            {
                "nome": "Provolone",
                "ordem": 11,
            },
            {
                "nome": "Parmesão",
                "ordem": 12,
            },
            {
                "nome": "Gorgonzola",
                "ordem": 13,
            },
            {
                "nome": "Manjericão",
                "ordem": 14,
            },
        ]

        ingredientes_criados = {}

        for dados in ingredientes:

            ingrediente, criado = Ingrediente.objects.get_or_create(
                loja=loja,
                nome=dados["nome"],
                defaults={
                    "ordem": dados["ordem"],
                    "ativo": True,
                }
            )

            ingredientes_criados[ingrediente.nome] = ingrediente

            if criado:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Ingrediente criado: {ingrediente.nome}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"→ Ingrediente já existe: {ingrediente.nome}"
                    )
                )

        # =====================================================
        # INGREDIENTES DOS PRODUTOS
        # =====================================================

        ingredientes_produtos = {
            "Pizza Calabresa": [
                "Muçarela",
                "Calabresa",
                "Cebola",
                "Azeitona",
            ],

            "Pizza Frango com Catupiry": [
                "Muçarela",
                "Frango",
                "Catupiry",
            ],

            "Pizza Portuguesa": [
                "Muçarela",
                "Presunto",
                "Ovo",
                "Cebola",
                "Tomate",
                "Azeitona",
            ],

            "Pizza Quatro Queijos": [
                "Muçarela",
                "Provolone",
                "Parmesão",
                "Gorgonzola",
            ],

            "Pizza da Casa": [
                "Muçarela",
                "Calabresa",
                "Bacon",
                "Cebola",
                "Tomate",
            ],
        }

        for nome_produto, nomes_ingredientes in ingredientes_produtos.items():

            produto = Produto.objects.get(
                loja=loja,
                nome=nome_produto
            )

            for ordem, nome_ingrediente in enumerate(
                nomes_ingredientes,
                start=1
            ):

                ingrediente = ingredientes_criados[nome_ingrediente]

                vinculo, criado = ProdutoIngrediente.objects.get_or_create(
                    produto=produto,
                    ingrediente=ingrediente,
                    defaults={
                        "permite_remocao": True,
                        "ordem": ordem,
                        "ativo": True,
                    }
                )

                if criado:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Ingrediente vinculado: "
                            f"{produto.nome} → {ingrediente.nome}"
                        )
                    )

        # =====================================================
        # INGREDIENTES DOS SABORES
        # =====================================================

        ingredientes_sabores = {
            "Calabresa": [
                "Muçarela",
                "Calabresa",
                "Cebola",
                "Azeitona",
            ],

            "Frango com Catupiry": [
                "Muçarela",
                "Frango",
                "Catupiry",
            ],

            "Portuguesa": [
                "Muçarela",
                "Presunto",
                "Ovo",
                "Cebola",
                "Tomate",
                "Azeitona",
            ],

            "Quatro Queijos": [
                "Muçarela",
                "Provolone",
                "Parmesão",
                "Gorgonzola",
            ],

            "Margherita": [
                "Muçarela",
                "Tomate",
                "Manjericão",
            ],

            "Bacon": [
                "Muçarela",
                "Bacon",
            ],
        }

        for nome_sabor, nomes_ingredientes in ingredientes_sabores.items():

            sabores = Sabor.objects.filter(
                loja=loja,
                nome=nome_sabor
            )

            for sabor in sabores:

                for ordem, nome_ingrediente in enumerate(
                    nomes_ingredientes,
                    start=1
                ):
                    ingrediente = ingredientes_criados[nome_ingrediente]

                    vinculo, criado = SaborIngrediente.objects.get_or_create(
                        sabor=sabor,
                        ingrediente=ingrediente,
                        defaults={
                            "permite_remocao": True,
                            "ordem": ordem,
                            "ativo": True,
                        }
                    )

                    if criado:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"✓ Ingrediente do sabor criado: "
                                f"{sabor.nome} → {ingrediente.nome}"
                            )
                        )
    def criar_adicionais(self, loja):

        grupos = [
            {
                "nome": "Borda Recheada",
                "descricao": "Escolha uma opção de borda recheada.",
                "obrigatorio": False,
                "minimo": 0,
                "maximo": 1,
                "ordem": 1,
            },
            {
                "nome": "Ingredientes Extras",
                "descricao": "Adicione ingredientes extras à sua pizza.",
                "obrigatorio": False,
                "minimo": 0,
                "maximo": 5,
                "ordem": 2,
            },
        ]

        grupos_criados = {}

        for dados in grupos:

            grupo, criado = GrupoAdicional.objects.get_or_create(
                loja=loja,
                nome=dados["nome"],
                defaults={
                    "descricao": dados["descricao"],
                    "obrigatorio": dados["obrigatorio"],
                    "minimo": dados["minimo"],
                    "maximo": dados["maximo"],
                    "ordem": dados["ordem"],
                    "ativo": True,
                }
            )

            grupos_criados[grupo.nome] = grupo

            if criado:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Grupo de adicional criado: {grupo.nome}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"→ Grupo de adicional já existe: {grupo.nome}"
                    )
                )

        adicionais = {
            "Borda Recheada": [
                ("Catupiry", 7.00, 1),
                ("Cheddar", 6.00, 2),
                ("Chocolate", 8.00, 3),
            ],

            "Ingredientes Extras": [
                ("Bacon", 5.00, 1),
                ("Calabresa", 5.00, 2),
                ("Catupiry", 4.00, 3),
                ("Muçarela", 4.00, 4),
                ("Cheddar", 4.00, 5),
            ],
        }

        for nome_grupo, itens in adicionais.items():

            grupo = grupos_criados[nome_grupo]

            for nome, preco, ordem in itens:

                item, criado = ItemAdicional.objects.get_or_create(
                    grupo=grupo,
                    nome=nome,
                    defaults={
                        "preco": preco,
                        "ativo": True,
                        "ordem": ordem,
                    }
                )

                if criado:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Adicional criado: "
                            f"{grupo.nome} → {item.nome}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"→ Adicional já existe: "
                            f"{grupo.nome} → {item.nome}"
                        )
                    )

        # =====================================================
        # VINCULAR GRUPOS ÀS PIZZAS
        # =====================================================

        produtos = Produto.objects.filter(
            loja=loja,
            categoria__nome__in=[
                "Pizzas",
                "Pizzas Especiais",
            ]
        )

        for produto in produtos:

            for grupo in grupos_criados.values():

                vinculo, criado = ProdutoGrupoAdicional.objects.get_or_create(
                    produto=produto,
                    grupo=grupo
                )

                if criado:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✓ Adicionais vinculados: "
                            f"{produto.nome} → {grupo.nome}"
                        )
                    )

    def criar_combos(self, loja):

        categoria = Categoria.objects.get(
            loja=loja,
            nome="Combos"
        )

        # =====================================================
        # PRODUTOS COMBO
        # =====================================================

        combos = [
            {
                "nome": "Combo Família",
                "descricao": "Duas pizzas grandes, uma bebida de 2 litros e uma sobremesa.",
                "preco": 89.90,
                "ordem": 1,
            },
            {
                "nome": "Combo Casal",
                "descricao": "Uma pizza grande, uma bebida de 2 litros e uma sobremesa.",
                "preco": 59.90,
                "ordem": 2,
            },
        ]

        produtos_combo = {}

        for dados in combos:

            produto, criado = Produto.objects.get_or_create(
                loja=loja,
                slug=slugify(f"combo-{dados['nome']}"),
                defaults={
                    "categoria": categoria,
                    "tipo": "COMBO",
                    "nome": dados["nome"],
                    "descricao": dados["descricao"],
                    "preco": dados["preco"],
                    "disponivel": True,
                    "destaque": True,
                    "possui_sabores": False,
                    "permite_multiplos_sabores": False,
                    "maximo_sabores": 1,
                    "tempo_preparo": 30,
                    "ordem": dados["ordem"],
                }
            )

            produtos_combo[produto.nome] = produto

            if criado:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Combo criado: {produto.nome}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"→ Combo já existe: {produto.nome}"
                    )
                )

        # =====================================================
        # COMBO FAMÍLIA
        # =====================================================

        combo_familia = produtos_combo["Combo Família"]

        grupo_pizzas, criado = ProdutoComboGrupo.objects.get_or_create(
            loja=loja,
            nome="Pizzas",
            defaults={
                "descricao": "Escolha duas pizzas para o combo.",
                "ativo": True,
                "ordem": 1,
            }
        )

        grupo_bebidas, criado = ProdutoComboGrupo.objects.get_or_create(
            loja=loja,
            nome="Bebidas",
            defaults={
                "descricao": "Escolha uma bebida de 2 litros.",
                "ativo": True,
                "ordem": 2,
            }
        )

        grupo_sobremesas, criado = ProdutoComboGrupo.objects.get_or_create(
            loja=loja,
            nome="Sobremesas",
            defaults={
                "descricao": "Escolha uma sobremesa.",
                "ativo": True,
                "ordem": 3,
            }
        )

        # =====================================================
        # VINCULAR GRUPOS AO COMBO
        # =====================================================

        ProdutoGrupoCombo.objects.get_or_create(
            produto=combo_familia,
            grupo=grupo_pizzas,
            defaults={
                "obrigatorio": True,
                "minimo": 2,
                "maximo": 2,
                "ordem": 1,
            }
        )

        ProdutoGrupoCombo.objects.get_or_create(
            produto=combo_familia,
            grupo=grupo_bebidas,
            defaults={
                "obrigatorio": True,
                "minimo": 1,
                "maximo": 1,
                "ordem": 2,
            }
        )

        ProdutoGrupoCombo.objects.get_or_create(
            produto=combo_familia,
            grupo=grupo_sobremesas,
            defaults={
                "obrigatorio": True,
                "minimo": 1,
                "maximo": 1,
                "ordem": 3,
            }
        )

        # =====================================================
        # ITENS - PIZZAS
        # =====================================================

        pizzas = [
            "Pizza Calabresa",
            "Pizza Frango com Catupiry",
            "Pizza Portuguesa",
            "Pizza Quatro Queijos",
            "Pizza da Casa",
        ]

        for ordem, nome in enumerate(pizzas, start=1):

            produto = Produto.objects.get(
                loja=loja,
                nome=nome
            )

            ProdutoComboGrupoItem.objects.get_or_create(
                grupo=grupo_pizzas,
                produto=produto,
                defaults={
                    "quantidade": 1,
                    "ordem": ordem,
                }
            )

        # =====================================================
        # ITENS - BEBIDAS
        # =====================================================

        bebidas = [
            "Coca-Cola 2L",
            "Guaraná Antarctica 2L",
        ]

        for ordem, nome in enumerate(bebidas, start=1):

            produto = Produto.objects.get(
                loja=loja,
                nome=nome
            )

            ProdutoComboGrupoItem.objects.get_or_create(
                grupo=grupo_bebidas,
                produto=produto,
                defaults={
                    "quantidade": 1,
                    "ordem": ordem,
                }
            )

        # =====================================================
        # ITENS - SOBREMESAS
        # =====================================================

        sobremesas = [
            "Brownie com Chocolate",
            "Pudim de Leite",
        ]

        for ordem, nome in enumerate(sobremesas, start=1):

            produto = Produto.objects.get(
                loja=loja,
                nome=nome
            )

            ProdutoComboGrupoItem.objects.get_or_create(
                grupo=grupo_sobremesas,
                produto=produto,
                defaults={
                    "quantidade": 1,
                    "ordem": ordem,
                }
            )

        self.stdout.write(
            self.style.SUCCESS(
                "✓ Estrutura do Combo Família criada."
            )
        )
        combo_casal = produtos_combo["Combo Casal"]

        ProdutoGrupoCombo.objects.get_or_create(
            produto=combo_casal,
            grupo=grupo_pizzas,
            defaults={
                "obrigatorio": True,
                "minimo": 1,
                "maximo": 1,
                "ordem": 1,
            }
        )

        ProdutoGrupoCombo.objects.get_or_create(
            produto=combo_casal,
            grupo=grupo_bebidas,
            defaults={
                "obrigatorio": True,
                "minimo": 1,
                "maximo": 1,
                "ordem": 2,
            }
        )

        ProdutoGrupoCombo.objects.get_or_create(
            produto=combo_casal,
            grupo=grupo_sobremesas,
            defaults={
                "obrigatorio": True,
                "minimo": 1,
                "maximo": 1,
                "ordem": 3,
            }
        )

        self.stdout.write(
            self.style.SUCCESS(
                "✓ Estrutura do Combo Casal criada."
            )
        )

    def criar_promocoes(self, loja):

        agora = timezone.now()

        promocoes = [
            {
                "produto": "Pizza da Casa",
                "nome": "Pizza da Casa em Oferta",
                "descricao": "Aproveite nossa pizza especial com preço promocional.",
                "preco_promocional": 39.90,
                "data_inicio": agora,
                "data_fim": agora + timezone.timedelta(days=30),
            },
            {
                "produto": "Pizza Calabresa",
                "nome": "Quarta-feira da Pizza",
                "descricao": "Pizza Calabresa com preço especial por tempo limitado.",
                "preco_promocional": 34.90,
                "data_inicio": agora,
                "data_fim": agora + timezone.timedelta(days=30),
            },
        ]

        for dados in promocoes:

            produto = Produto.objects.get(
                loja=loja,
                nome=dados["produto"]
            )

            promocao, criada = Promocao.objects.get_or_create(
                loja=loja,
                produto=produto,
                nome=dados["nome"],
                defaults={
                    "descricao": dados["descricao"],
                    "preco_promocional": dados["preco_promocional"],
                    "data_inicio": dados["data_inicio"],
                    "data_fim": dados["data_fim"],
                    "ativa": True,
                    "destaque": True,
                }
            )

            if criada:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Promoção criada: {promocao.nome}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"→ Promoção já existe: {promocao.nome}"
                    )
                )
    def criar_estrutura_cardapio(self, loja):

        estruturas = [
            ("banner", 1),
            ("promocoes", 2),
            ("mais_vendidos", 3),
            ("categorias", 4),
            ("combos", 5),
            ("novidades", 6),
            ("recomendados", 7),
        ]

        for tipo, ordem in estruturas:

            estrutura, criada = EstruturaCardapio.objects.get_or_create(
                loja=loja,
                tipo=tipo,
                defaults={
                    "ordem": ordem,
                    "ativo": True,
                }
            )

            if criada:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Estrutura criada: {tipo}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"→ Estrutura já existe: {tipo}"
                    )
                )
    def criar_status_pedidos(self, loja):

        statuses = [
            {
                "codigo": "aguardando-pagamento",
                "nome": "Aguardando pagamento",
                "ordem": 0,
                "aparece_kanban": False,
                "finalizador": False,
                "cancelamento": False,
                "sistema": True,
            },
            {
                "codigo": "recebido",
                "nome": "Recebido",
                "ordem": 1,
                "aparece_kanban": True,
                "finalizador": False,
                "cancelamento": False,
                "sistema": True,
            },
            {
                "codigo": "em-preparo",
                "nome": "Em preparo",
                "ordem": 2,
                "aparece_kanban": True,
                "finalizador": False,
                "cancelamento": False,
                "sistema": True,
            },
            {
                "codigo": "pronto",
                "nome": "Pronto",
                "ordem": 3,
                "aparece_kanban": True,
                "finalizador": False,
                "cancelamento": False,
                "sistema": True,
            },
            {
                "codigo": "entregue",
                "nome": "Entregue",
                "ordem": 4,
                "aparece_kanban": True,
                "finalizador": True,
                "cancelamento": False,
                "sistema": True,
            },
            {
                "codigo": "cancelado",
                "nome": "Cancelado",
                "ordem": 5,
                "aparece_kanban": False,
                "finalizador": False,
                "cancelamento": True,
                "sistema": True,
            },
        ]

        status_map = {}

        for dados in statuses:

            status, criada = PedidoStatus.objects.update_or_create(
                loja=loja,
                codigo=dados["codigo"],
                defaults={
                    "nome": dados["nome"],
                    "ordem": dados["ordem"],
                    "ativo": True,
                    "aparece_kanban": dados["aparece_kanban"],
                    "finalizador": dados["finalizador"],
                    "cancelamento": dados["cancelamento"],
                    "sistema": dados["sistema"],
                }
            )

            status_map[dados["codigo"]] = status

            if criada:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Status criado: {status.nome}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"→ Status já existe: {status.nome}"
                    )
                )

        return status_map

    def criar_pedidos(self, loja, status_map):

        produtos = {
            produto.nome: produto
            for produto in Produto.objects.filter(loja=loja)
        }

        pedidos_demo = [
            {
                "numero": 1001,
                "status": "recebido",
                "cliente": "Carlos Silva",
                "telefone": "(48) 99999-1001",
                "tipo_entrega": "ENTREGA",
                "endereco": "Rua das Palmeiras",
                "numero_endereco": "120",
                "complemento": "Apto 202",
                "bairro": "Centro",
                "cidade": "Palhoça",
                "estado": "SC",
                "cep": "88130-000",
                "referencia": "Próximo à praça",
                "observacao": "Entregar na portaria",
                "taxa_entrega": Decimal("8.00"),
                "desconto": Decimal("0.00"),
                "pagamento": {
                    "metodo": "pix",
                    "status": "pago",
                },
                "itens": [
                    ("Pizza Calabresa", 1, Decimal("49.90")),
                    ("Coca-Cola 2L", 1, Decimal("12.00")),
                ],
            },
            {
                "numero": 1002,
                "status": "em-preparo",
                "cliente": "Mariana Oliveira",
                "telefone": "(48) 98888-2002",
                "tipo_entrega": "ENTREGA",
                "endereco": "Rua dos Ipês",
                "numero_endereco": "450",
                "complemento": "",
                "bairro": "Pagani",
                "cidade": "Palhoça",
                "estado": "SC",
                "cep": "88132-000",
                "referencia": "",
                "observacao": "Retirar cebola da pizza",
                "taxa_entrega": Decimal("7.00"),
                "desconto": Decimal("5.00"),
                "pagamento": {
                    "metodo": "cartao",
                    "status": "pago",
                },
                "itens": [
                    ("Pizza Frango com Catupiry", 1, Decimal("54.90")),
                    ("Guaraná Antarctica 2L", 1, Decimal("10.00")),
                ],
            },
            {
                "numero": 1003,
                "status": "pronto",
                "cliente": "João Santos",
                "telefone": "(48) 97777-3003",
                "tipo_entrega": "RETIRADA",
                "endereco": "",
                "numero_endereco": "",
                "complemento": "",
                "bairro": "",
                "cidade": "",
                "estado": "",
                "cep": "",
                "referencia": "",
                "observacao": "Cliente irá retirar no balcão",
                "taxa_entrega": Decimal("0.00"),
                "desconto": Decimal("0.00"),
                "pagamento": {
                    "metodo": "dinheiro",
                    "status": "pendente",
                },
                "itens": [
                    ("Pizza Portuguesa", 1, Decimal("49.90")),
                    ("Brownie com Chocolate", 2, Decimal("12.00")),
                ],
            },
            {
                "numero": 1004,
                "status": "entregue",
                "cliente": "Ana Costa",
                "telefone": "(48) 96666-4004",
                "tipo_entrega": "ENTREGA",
                "endereco": "Avenida Central",
                "numero_endereco": "800",
                "complemento": "Casa",
                "bairro": "Centro",
                "cidade": "Palhoça",
                "estado": "SC",
                "cep": "88130-100",
                "referencia": "Casa com portão branco",
                "observacao": "",
                "taxa_entrega": Decimal("8.00"),
                "desconto": Decimal("10.00"),
                "pagamento": {
                    "metodo": "pix",
                    "status": "pago",
                },
                "itens": [
                    ("Combo Família", 1, Decimal("129.90")),
                ],
            },
            {
                "numero": 1005,
                "status": "em-preparo",
                "cliente": "Pedro Almeida",
                "telefone": "(48) 95555-5005",
                "tipo_entrega": "CONSUMO_LOCAL",
                "endereco": "",
                "numero_endereco": "",
                "complemento": "",
                "bairro": "",
                "cidade": "",
                "estado": "",
                "cep": "",
                "referencia": "",
                "observacao": "Mesa 05",
                "taxa_entrega": Decimal("0.00"),
                "desconto": Decimal("0.00"),
                "pagamento": {
                    "metodo": "cartao",
                    "status": "pago",
                },
                "itens": [
                    ("Pizza Quatro Queijos", 1, Decimal("54.90")),
                    ("Coca-Cola 2L", 1, Decimal("12.00")),
                ],
            },
        ]

        for dados in pedidos_demo:

            status = status_map[dados["status"]]

            pedido, criada = Pedido.objects.get_or_create(
                loja=loja,
                numero=dados["numero"],
                defaults={
                    "status": status,
                    "tipo_entrega": dados["tipo_entrega"],
                    "nome_cliente": dados["cliente"],
                    "telefone_cliente": dados["telefone"],
                    "endereco": dados["endereco"],
                    "numero_endereco": dados["numero_endereco"],
                    "complemento": dados["complemento"],
                    "bairro": dados["bairro"],
                    "cidade": dados["cidade"],
                    "estado": dados["estado"],
                    "cep": dados["cep"],
                    "referencia": dados["referencia"],
                    "observacao": dados["observacao"],
                    "taxa_entrega": dados["taxa_entrega"],
                    "desconto": dados["desconto"],
                }
            )

            if not criada:
                self.stdout.write(
                    self.style.WARNING(
                        f"→ Pedido já existe: #{pedido.numero}"
                    )
                )
                continue

            subtotal = Decimal("0.00")

            for ordem, (nome, quantidade, preco) in enumerate(
                dados["itens"],
                start=1
            ):

                produto = produtos.get(nome)

                if not produto:
                    self.stdout.write(
                        self.style.ERROR(
                            f"✗ Produto não encontrado: {nome}"
                        )
                    )
                    continue

                item_subtotal = quantidade * preco
                subtotal += item_subtotal

                PedidoItem.objects.create(
                    pedido=pedido,
                    produto=produto,
                    nome_produto=produto.nome,
                    descricao_produto=produto.descricao,
                    quantidade=quantidade,
                    preco_unitario=preco,
                    desconto=Decimal("0.00"),
                    subtotal=item_subtotal,
                    observacao="",
                    ordem=ordem,
                )

            pedido.subtotal = subtotal
            pedido.total = (
                subtotal
                + pedido.taxa_entrega
                - pedido.desconto
            )

            pedido.save()

            # Histórico inicial
            PedidoStatusHistorico.objects.create(
                pedido=pedido,
                status_anterior=None,
                status_novo=status,
                usuario=None,
                observacao="Pedido criado pelo seed de demonstração.",
            )

            self.criar_pagamento_demo(
                pedido,
                dados["pagamento"]
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Pedido criado: #{pedido.numero} - "
                    f"{pedido.nome_cliente} - "
                    f"{status.nome}"
                )
            )

    def criar_pagamento_demo(self, pedido, dados):

        pagamento_status = dados["status"]

        pago_em = (
            timezone.now()
            if pagamento_status == "pago"
            else None
        )

        Pagamento.objects.update_or_create(
            pedido=pedido,
            defaults={
                "metodo": dados["metodo"],
                "gateway": "manual",
                "status": pagamento_status,
                "valor": pedido.total,
                "identificador_externo": (
                    f"DEMO-{pedido.numero}"
                ),
                "dados_gateway": {
                    "demo": True,
                    "pedido": pedido.numero,
                },
                "pago_em": pago_em,
            }
        )

        status_pagamento = (
            PedidoPagamento.STATUS_APROVADO
            if pagamento_status == "pago"
            else PedidoPagamento.STATUS_PENDENTE
        )

        forma_pagamento = {
            "pix": "PIX",
            "cartao": "Cartão",
            "dinheiro": "Dinheiro na entrega",
        }[dados["metodo"]]

        PedidoPagamento.objects.update_or_create(
            pedido=pedido,
            defaults={
                "forma_pagamento": forma_pagamento,
                "status": status_pagamento,
                "valor": pedido.total,
                "observacao": "Pagamento criado pelo seed de demonstração.",
            }
        )

    def criar_navegacao(self):

        menus = {
            "Cardapio": {
                "icone": "fa-utensils",
                "submenus": {
                    "Categorias": {
                        "url": "/cardapio/categorias/",
                    },
                    "Produtos": {
                        "url": "/cardapio/produto/",
                    },
                    "Promoções": {
                        "url": "/cardapio/promocoes/",
                    },
                    "Sabores": {
                        "url": "",
                        "subitens": {
                            "Grupos de Sabores":
                                "/cardapio/grupodesabores/",
                            "Sabor":
                                "/cardapio/sabor/",
                            "Produto x Grupo de Sabores":
                                "/cardapio/produtogruposabor",
                        },
                    },
                    "Ingredientes": {
                        "url": "",
                        "subitens": {
                            "Ingredientes":
                                "/cardapio/ingredientes/",
                            "Ingredientes dos Produtos":
                                "/cardapio/produtoingrediente/",
                            "Ingredientes dos Sabores":
                                "/cardapio/saboringrediente/",
                        },
                    },
                    "Adicionais": {
                        "url": "",
                        "subitens": {
                            "Grupos de Adicionais":
                                "/cardapio/grupoadicional/",
                            "Itens Adicionais":
                                "/cardapio/itemadicional/",
                            "Produtos x Grupos":
                                "/cardapio/produtogrupoadicional/",
                        },
                    },
                    "Combos": {
                        "url": "",
                        "subitens": {
                            "Grupos de Combo":
                                "/cardapio/produtocombogrupo/",
                            "Combos":
                                "/cardapio/combo/",
                        },
                    },
                    "Personalizar": {
                        "url": "",
                        "subitens": {
                            "Personalizar Cardapio":
                                "/cardapio/estrutura_cardapio",
                        },
                    },
                },
            },

            "Pedidos": {
                "icone": "fa-cart-shopping",
                "submenus": {
                    "Kan Ban Pedidos": {
                        "url": "/pedidos/kanban/",
                    },
                    "Personalizar": {
                        "url": "",
                        "subitens": {
                            "Personalizar Kanban":
                                "/pedidos/status",
                        },
                    },
                },
            },

            "Dashboard": {
                "icone": "fa-house",
                "submenus": {},
            },
        }

        for nome_menu, dados_menu in menus.items():

            menu, criada = MenuItem.objects.get_or_create(
                nome=nome_menu,
                defaults={
                    "icone": dados_menu["icone"],
                }
            )

            # Garante que o ícone seja atualizado
            if menu.icone != dados_menu["icone"]:
                menu.icone = dados_menu["icone"]
                menu.save(update_fields=["icone"])

            if criada:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Menu criado: {nome_menu}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"→ Menu já existe: {nome_menu}"
                    )
                )

            for nome_submenu, dados_submenu in dados_menu[
                "submenus"
            ].items():

                submenu, criada = SubMenuItem.objects.get_or_create(
                    menu=menu,
                    nome=nome_submenu,
                    defaults={
                        "url": dados_submenu["url"],
                    }
                )

                if submenu.url != dados_submenu["url"]:
                    submenu.url = dados_submenu["url"]
                    submenu.save(update_fields=["url"])

                if criada:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  ✓ Submenu criado: "
                            f"{nome_menu} → {nome_submenu}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  → Submenu já existe: "
                            f"{nome_menu} → {nome_submenu}"
                        )
                    )

                for (
                    nome_subsubmenu,
                    url
                ) in dados_submenu.get("subitens", {}).items():

                    subsubmenu, criada = (
                        SubSubMenuItem.objects.get_or_create(
                            submenu=submenu,
                            nome=nome_subsubmenu,
                            defaults={
                                "url": url,
                            }
                        )
                    )

                    if subsubmenu.url != url:
                        subsubmenu.url = url
                        subsubmenu.save(update_fields=["url"])

                    if criada:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"    ✓ Subsubmenu criado: "
                                f"{nome_subsubmenu}"
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"    → Subsubmenu já existe: "
                                f"{nome_subsubmenu}"
                            )
                        )