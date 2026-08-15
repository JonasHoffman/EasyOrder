from decimal import Decimal

from Cardapio.models import (
    Produto,
    ItemAdicional,
    ProdutoIngrediente,
    Sabor,
    ProdutoGrupoSabor,
    ProdutoComboGrupo,
)


class Cart:

    def __init__(self, request):

        self.session = request.session

        self.carrinho = self.session.setdefault(
            "carrinho",
            {}
        )

    # ============================================================
    # ADICIONAR
    # ============================================================

    def adicionar(
        self,
        produto,
        quantidade=1,
        ingredientes_removidos=None,
        adicionais=None,
        sabores=None,
        combo=None,
    ):

        ingredientes_removidos = sorted(
            set(ingredientes_removidos or [])
        )

        adicionais = sorted(
            set(adicionais or [])
        )

        # --------------------------------------------------------
        # SABORES
        # --------------------------------------------------------
        # Não usar set().
        #
        # Exemplo:
        #
        # [1, 1, 2]
        #
        # significa:
        #
        # sabor 1 x2
        # sabor 2 x1
        # --------------------------------------------------------

        sabores = sorted(
            sabores or []
        )

        combo = combo or {}

        # ========================================================
        # VALIDAÇÕES
        # ========================================================

        self._validar_ingredientes(
            produto,
            ingredientes_removidos
        )

        self._validar_adicionais(
            produto,
            adicionais
        )

        self._validar_sabores(
            produto,
            sabores
        )

        # ========================================================
        # CRIAR CHAVE
        # ========================================================

        chave = self._criar_chave(
            produto.id,
            ingredientes_removidos,
            adicionais,
            sabores,
            combo
        )

        # ========================================================
        # ADICIONAR
        # ========================================================

        if chave not in self.carrinho:

            self.carrinho[chave] = {

                "produto_id":
                    produto.id,

                "quantidade":
                    quantidade,

                "ingredientes_removidos":
                    ingredientes_removidos,

                "adicionais":
                    adicionais,

                "sabores":
                    sabores,

                "combo":
                    combo,
            }

        else:

            self.carrinho[chave]["quantidade"] += quantidade

        self.salvar()

    # ============================================================
    # VALIDAR INGREDIENTES
    # ============================================================

    def _validar_ingredientes(
        self,
        produto,
        ingredientes_ids
    ):

        if not ingredientes_ids:
            return

        permitidos = set(
            ProdutoIngrediente.objects.filter(
                produto=produto,
                id__in=ingredientes_ids
            ).values_list(
                "id",
                flat=True
            )
        )

        enviados = set(
            ingredientes_ids
        )

        invalidos = enviados - permitidos

        if invalidos:

            raise ValueError(
                "Um ou mais ingredientes "
                "não pertencem ao produto."
            )

    # ============================================================
    # VALIDAR ADICIONAIS
    # ============================================================

    def _validar_adicionais(
        self,
        produto,
        adicionais_ids
    ):

        if not adicionais_ids:
            return

        permitidos = set(
            ItemAdicional.objects.filter(
                grupo__produtos__produto=produto,
                id__in=adicionais_ids,
                ativo=True,
                grupo__ativo=True,
                grupo__loja=produto.loja,
            ).values_list(
                "id",
                flat=True
            )
        )

        enviados = set(
            adicionais_ids
        )

        invalidos = enviados - permitidos

        if invalidos:

            raise ValueError(
                "Um ou mais adicionais "
                "não estão disponíveis para este produto."
            )

    # ============================================================
    # VALIDAR SABORES
    # ============================================================

    def _validar_sabores(
        self,
        produto,
        sabores_ids
    ):

        if not sabores_ids:
            return

        # --------------------------------------------------------
        # GRUPOS DE SABORES
        # --------------------------------------------------------

        grupos_ids = set(
            ProdutoGrupoSabor.objects.filter(
                produto=produto,
                ativo=True,
                grupo__ativo=True,
                grupo__loja=produto.loja,
            ).values_list(
                "grupo_id",
                flat=True
            )
        )

        # --------------------------------------------------------
        # SABORES PERMITIDOS
        # --------------------------------------------------------

        permitidos = set(
            Sabor.objects.filter(
                grupo_id__in=grupos_ids,
                ativo=True,
            ).values_list(
                "id",
                flat=True
            )
        )

        # --------------------------------------------------------
        # CONVERTER
        # --------------------------------------------------------

        try:

            enviados_lista = [
                int(sabor_id)
                for sabor_id in sabores_ids
            ]

        except (TypeError, ValueError):

            raise ValueError(
                "Um ou mais sabores são inválidos."
            )

        enviados = set(
            enviados_lista
        )

        # --------------------------------------------------------
        # VERIFICAR
        # --------------------------------------------------------

        invalidos = enviados - permitidos

        if invalidos:

            raise ValueError(
                "Um ou mais sabores "
                "não estão disponíveis para este produto."
            )

    # ============================================================
    # NORMALIZAR COMBO
    # ============================================================

    def _normalizar_combo(
        self,
        combo
    ):

        if not combo:
            return ""

        partes = []

        # ========================================================
        # ITENS DO COMBO
        # ========================================================

        itens = combo.get(
            "itens",
            {}
        )

        for item_id in sorted(
            itens.keys(),
            key=lambda valor: int(valor)
        ):

            partes.append(
                f"item:{item_id}:{itens[item_id]}"
            )

        # ========================================================
        # PERSONALIZAÇÕES
        # ========================================================

        personalizacoes = combo.get(
            "personalizacoes",
            {}
        )

        for item_id in sorted(
            personalizacoes.keys(),
            key=lambda valor: int(valor)
        ):

            unidades = personalizacoes[item_id]

            for numero in sorted(
                unidades.keys(),
                key=lambda valor: int(valor)
            ):

                dados = unidades[numero]

                # ------------------------------------------------
                # SABORES
                # ------------------------------------------------

                sabores = ",".join(
                    map(
                        str,
                        sorted(
                            dados.get(
                                "sabores",
                                []
                            )
                        )
                    )
                )

                # ------------------------------------------------
                # INGREDIENTES
                # ------------------------------------------------

                ingredientes = ",".join(
                    map(
                        str,
                        sorted(
                            dados.get(
                                "ingredientes",
                                []
                            )
                        )
                    )
                )

                # ------------------------------------------------
                # ADICIONAIS
                # ------------------------------------------------

                adicionais = ",".join(
                    map(
                        str,
                        sorted(
                            dados.get(
                                "adicionais",
                                []
                            )
                        )
                    )
                )

                partes.append(
                    f"p:{item_id}:{numero}:"
                    f"s:{sabores}:"
                    f"i:{ingredientes}:"
                    f"a:{adicionais}"
                )

        return "|".join(
            partes
        )

    # ============================================================
    # CRIAR CHAVE
    # ============================================================

    def _criar_chave(
        self,
        produto_id,
        ingredientes_removidos,
        adicionais,
        sabores,
        combo
    ):

        ingredientes_str = ",".join(
            map(
                str,
                ingredientes_removidos
            )
        )

        adicionais_str = ",".join(
            map(
                str,
                adicionais
            )
        )

        sabores_str = ",".join(
            map(
                str,
                sabores
            )
        )

        combo_str = self._normalizar_combo(
            combo
        )

        return (
            f"{produto_id}|"
            f"i:{ingredientes_str}|"
            f"a:{adicionais_str}|"
            f"s:{sabores_str}|"
            f"c:{combo_str}"
        )

    # ============================================================
    # REMOVER
    # ============================================================

    def remover(
        self,
        chave
    ):

        if chave in self.carrinho:

            del self.carrinho[chave]

            self.salvar()

    # ============================================================
    # ATUALIZAR QUANTIDADE
    # ============================================================

    def atualizar_quantidade(
        self,
        chave,
        quantidade
    ):

        if chave not in self.carrinho:
            return

        if quantidade <= 0:

            self.remover(
                chave
            )

            return

        self.carrinho[chave]["quantidade"] = quantidade

        self.salvar()

    # ============================================================
    # SALVAR
    # ============================================================

    def salvar(self):

        self.session.modified = True

    # ============================================================
    # ITERAR CARRINHO
    # ============================================================

    def __iter__(self):

        for chave, item in self.carrinho.items():

            # ====================================================
            # PRODUTO PRINCIPAL
            # ====================================================

            produto = Produto.objects.get(
                id=item["produto_id"]
            )

            # ====================================================
            # ADICIONAIS DO PRODUTO NORMAL
            # ====================================================

            adicionais = list(
                ItemAdicional.objects.filter(
                    id__in=item.get(
                        "adicionais",
                        []
                    ),
                    ativo=True
                ).select_related(
                    "grupo"
                )
            )

            adicionais_valor = sum(
                (
                    adicional.preco
                    for adicional in adicionais
                ),
                Decimal("0.00")
            )

            # ====================================================
            # SABORES DO PRODUTO NORMAL
            # ====================================================

            sabores_ids = item.get(
                "sabores",
                []
            )

            sabores = []

            if sabores_ids:

                sabores_queryset = (
                    Sabor.objects
                    .filter(
                        id__in=sabores_ids,
                        ativo=True
                    )
                    .select_related(
                        "grupo"
                    )
                )

                sabores_por_id = {
                    sabor.id: sabor
                    for sabor in sabores_queryset
                }

                for sabor_id in sabores_ids:

                    sabor = sabores_por_id.get(
                        int(sabor_id)
                    )

                    if sabor:

                        sabores.append(
                            sabor
                        )

            # ====================================================
            # VALOR DOS SABORES
            # ====================================================

            sabores_valor = sum(
                (
                    sabor.valor_adicional
                    or Decimal("0.00")
                    for sabor in sabores
                ),
                Decimal("0.00")
            )

            # ====================================================
            # INGREDIENTES REMOVIDOS
            # ====================================================

            ingredientes = (
                ProdutoIngrediente.objects
                .filter(
                    id__in=item.get(
                        "ingredientes_removidos",
                        []
                    )
                )
                .select_related(
                    "ingrediente"
                )
            )

            # ====================================================
            # COMBO
            # ====================================================

            combo = item.get(
                "combo",
                {}
            )

            combo_detalhes = []

            if produto.tipo == "COMBO" and combo:

                itens_combo = combo.get(
                    "itens",
                    {}
                )

                personalizacoes_combo = combo.get(
                    "personalizacoes",
                    {}
                )

                # =================================================
                # IDS DOS ITENS DO COMBO
                # =================================================

                item_ids = []

                for item_id in itens_combo.keys():

                    try:

                        item_ids.append(
                            int(item_id)
                        )

                    except (TypeError, ValueError):

                        continue

                # =================================================
                # BUSCAR GRUPOS
                # =================================================

                grupos = (
                    ProdutoComboGrupo.objects
                    .filter(
                        itens__id__in=item_ids
                    )
                    .prefetch_related(
                        "itens__produto"
                    )
                    .distinct()
                )

                # =================================================
                # MAPEAR ITEM
                # =================================================

                itens_por_id = {}

                for grupo_combo in grupos:

                    for item_grupo in grupo_combo.itens.all():

                        if item_grupo.id in item_ids:

                            itens_por_id[
                                item_grupo.id
                            ] = item_grupo

                # =================================================
                # AGRUPAR POR GRUPO
                # =================================================

                grupos_detalhes = {}

                for item_id, quantidade_item in itens_combo.items():

                    try:

                        item_id_int = int(
                            item_id
                        )

                        quantidade_item = int(
                            quantidade_item
                        )

                    except (TypeError, ValueError):

                        continue

                    item_grupo = itens_por_id.get(
                        item_id_int
                    )

                    if not item_grupo:
                        continue

                    produto_item = item_grupo.produto
                    grupo = item_grupo.grupo

                    # =============================================
                    # PERSONALIZAÇÕES
                    # =============================================

                    personalizacoes = []

                    unidades = personalizacoes_combo.get(
                        str(item_id_int),
                        personalizacoes_combo.get(
                            item_id,
                            {}
                        )
                    )

                    for numero, dados_personalizacao in unidades.items():

                        try:

                            numero_int = int(
                                numero
                            )

                        except (TypeError, ValueError):

                            continue

                        # =========================================
                        # SABORES
                        # =========================================

                        sabores_personalizacao = []

                        sabor_ids = dados_personalizacao.get(
                            "sabores",
                            []
                        )

                        if sabor_ids:

                            try:

                                sabor_ids_int = [
                                    int(sabor_id)
                                    for sabor_id in sabor_ids
                                ]

                            except (TypeError, ValueError):

                                sabor_ids_int = []

                            sabores_queryset = (
                                Sabor.objects
                                .filter(
                                    id__in=sabor_ids_int,
                                    ativo=True
                                )
                                .select_related(
                                    "grupo"
                                )
                            )

                            sabores_por_id = {
                                sabor.id: sabor
                                for sabor in sabores_queryset
                            }

                            for sabor_id in sabor_ids_int:

                                sabor = sabores_por_id.get(
                                    sabor_id
                                )

                                if sabor:

                                    sabores_personalizacao.append(
                                        sabor
                                    )

                        # =========================================
                        # INGREDIENTES
                        # =========================================

                        ingredientes_personalizacao = []

                        ingrediente_ids = (
                            dados_personalizacao.get(
                                "ingredientes",
                                []
                            )
                        )

                        if ingrediente_ids:

                            try:

                                ingrediente_ids_int = [
                                    int(ingrediente_id)
                                    for ingrediente_id
                                    in ingrediente_ids
                                ]

                            except (TypeError, ValueError):

                                ingrediente_ids_int = []

                            ingredientes_personalizacao = list(
                                ProdutoIngrediente.objects
                                .filter(
                                    id__in=ingrediente_ids_int
                                )
                                .select_related(
                                    "ingrediente"
                                )
                            )

                        # =========================================
                        # ADICIONAIS
                        # =========================================

                        adicionais_personalizacao = []

                        adicional_ids = (
                            dados_personalizacao.get(
                                "adicionais",
                                []
                            )
                        )

                        if adicional_ids:

                            try:

                                adicional_ids_int = [
                                    int(adicional_id)
                                    for adicional_id
                                    in adicional_ids
                                ]

                            except (TypeError, ValueError):

                                adicional_ids_int = []

                            adicionais_queryset = (
                                ItemAdicional.objects
                                .filter(
                                    id__in=adicional_ids_int,
                                    ativo=True
                                )
                                .select_related(
                                    "grupo"
                                )
                            )

                            adicionais_por_id = {
                                adicional.id: adicional
                                for adicional
                                in adicionais_queryset
                            }

                            for adicional_id in adicional_ids_int:

                                adicional = adicionais_por_id.get(
                                    adicional_id
                                )

                                if adicional:

                                    adicionais_personalizacao.append(
                                        adicional
                                    )

                        # =========================================
                        # ADICIONAR PERSONALIZAÇÃO
                        # =========================================

                        personalizacoes.append({

                            "numero":
                                numero_int,

                            "sabores":
                                sabores_personalizacao,

                            "ingredientes":
                                ingredientes_personalizacao,

                            "adicionais":
                                adicionais_personalizacao,

                        })

                    # =============================================
                    # CRIAR GRUPO
                    # =============================================

                    if grupo.id not in grupos_detalhes:

                        grupos_detalhes[grupo.id] = {

                            "grupo":
                                grupo,

                            "produtos":
                                [],

                            # Mantemos as informações
                            # completas internamente.
                            "itens":
                                [],

                        }

                    # =============================================
                    # ADICIONAR PRODUTO
                    # =============================================

                    grupos_detalhes[
                        grupo.id
                    ]["produtos"].append(
                        produto_item
                    )

                    # =============================================
                    # GUARDAR DADOS COMPLETOS
                    # =============================================

                    grupos_detalhes[
                        grupo.id
                    ]["itens"].append({

                        "item":
                            item_grupo,

                        "produto":
                            produto_item,

                        "quantidade":
                            quantidade_item,

                        "personalizacoes":
                            personalizacoes,

                    })

                # =================================================
                # TRANSFORMAR EM LISTA
                # =================================================

                combo_detalhes = list(
                    grupos_detalhes.values()
                )

            # ====================================================
            # PREÇO BASE
            # ====================================================

            preco = produto.preco

            preco_final = (
                preco
                + adicionais_valor
                + sabores_valor
            )

            # ====================================================
            # SUBTOTAL
            # ====================================================

            subtotal = (
                preco_final
                * item["quantidade"]
            )

            # ====================================================
            # RETORNO DO ITEM
            # ====================================================

            yield {

                "chave":
                    chave,

                "produto":
                    produto,

                "quantidade":
                    item["quantidade"],

                "preco_base":
                    preco,

                "preco_unitario":
                    preco_final,

                "preco_total":
                    preco_final,

                "subtotal":
                    subtotal,

                # ------------------------------------------------
                # PRODUTO NORMAL
                # ------------------------------------------------

                "ingredientes_removidos":
                    ingredientes,

                "adicionais":
                    adicionais,

                "adicionais_valor":
                    adicionais_valor,

                "sabores":
                    sabores,

                "sabores_valor":
                    sabores_valor,

                # ------------------------------------------------
                # COMBO ORIGINAL
                # ------------------------------------------------

                "combo":
                    combo,

                # ------------------------------------------------
                # COMBO PRONTO PARA O TEMPLATE
                # ------------------------------------------------

                "combo_detalhes":
                    combo_detalhes,
            }

    # ============================================================
    # QUANTIDADE TOTAL
    # ============================================================

    def __len__(self):

        return sum(
            item["quantidade"]
            for item in self.carrinho.values()
        )

    # ============================================================
    # TOTAL
    # ============================================================

    def get_total(self):

        return sum(
            (
                item["subtotal"]
                for item in self
            ),
            Decimal("0.00")
        )

    # ============================================================
    # LIMPAR
    # ============================================================

    def limpar(self):

        self.carrinho.clear()

        self.salvar()