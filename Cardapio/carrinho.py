from decimal import Decimal

from Cardapio.models import Produto, ItemAdicional,Ingrediente,ProdutoIngrediente


class Cart:

    def __init__(self, request):

        self.session = request.session

        self.carrinho = self.session.setdefault(
            "carrinho",
            {}
        )


    def adicionar(
        self,
        produto,
        quantidade=1,
        ingredientes_removidos=None,
        adicionais=None
    ):

        ingredientes_removidos = ingredientes_removidos or []
        adicionais = adicionais or []


        chave = (
            f"{produto.id}-"
            f"{','.join(map(str, ingredientes_removidos))}-"
            f"{','.join(map(str, adicionais))}"
        )


        if chave not in self.carrinho:

            self.carrinho[chave] = {

                "produto_id": produto.id,

                "quantidade": quantidade,

                "preco": str(produto.preco),

                "ingredientes_removidos": ingredientes_removidos,

                "adicionais": adicionais,

            }

        else:

            self.carrinho[chave]["quantidade"] += quantidade


        self.salvar()



    def remover(self, chave):

        if chave in self.carrinho:

            del self.carrinho[chave]

            self.salvar()



    def atualizar_quantidade(
        self,
        chave,
        quantidade
    ):

        if chave in self.carrinho:

            if quantidade <= 0:

                self.remover(chave)

            else:

                self.carrinho[chave]["quantidade"] = quantidade

                self.salvar()



    def salvar(self):

        self.session.modified = True



    def __iter__(self):

        for chave, item in self.carrinho.items():


            produto = Produto.objects.get(
                id=item["produto_id"]
            )


            preco = Decimal(item["preco"])


            adicionais_valor = Decimal("0")


            if item["adicionais"]:

                adicionais_valor = sum(
                    ItemAdicional.objects.filter(
                        id__in=item["adicionais"]
                    ).values_list(
                        "preco",
                        flat=True
                    )
                )


            preco_final = preco + adicionais_valor



            ingredientes = ProdutoIngrediente.objects.filter(
                id__in=item["ingredientes_removidos"]
            )


            adicionais = ItemAdicional.objects.filter(
                id__in=item["adicionais"]
            )


            yield {

                "chave": chave,

                "produto": produto,

                "quantidade": item["quantidade"],

                "preco_total": preco_final,

                "subtotal": preco_final * item["quantidade"],

                "ingredientes_removidos": ingredientes,

                "adicionais": adicionais,

            }


    def __len__(self):

        return sum(
            item["quantidade"]
            for item in self.carrinho.values()
        )



    def get_total(self):

        return sum(
            item["subtotal"]
            for item in self
        )