document.addEventListener("DOMContentLoaded", function () {

    // ============================================================
    // INICIALIZAÇÃO
    // ============================================================

    inicializarSaboresPagina();
    inicializarProdutosCombo();
    inicializarFormularioProduto();
    inicializarFormularioCombo();
    inicializarBotoesAdicionar();
    ativarBotoesRemover();

});


// =================================================================
// SABORES - PRODUTO NORMAL
// =================================================================

function inicializarSaboresPagina() {

    document
        .querySelectorAll(
            "[data-sabores-container]"
        )
        .forEach(function (container) {

            inicializarSabores(container);

        });

}


// =================================================================
// INICIALIZAR SABORES
// =================================================================

function inicializarSabores(container) {

    const maximo =
        parseInt(
            container.dataset.maximoSabores
        ) || 1;


    const permiteMultiplos =
        container.dataset.multiplosSabores === "true";


    const contador =
        container.querySelector(
            "[data-contador-sabores] strong"
        );


    function obterTotal() {

        let total = 0;


        container
            .querySelectorAll(
                "[data-sabor-contador]"
            )
            .forEach(function (sabor) {

                const elemento =
                    sabor.querySelector(
                        "[data-sabor-quantidade]"
                    );


                total +=
                    parseInt(
                        elemento?.textContent || 0
                    ) || 0;

            });


        return total;

    }


    function atualizar() {

        const total =
            obterTotal();


        if (contador) {

            contador.textContent =
                total;

        }


        container
            .querySelectorAll(
                "[data-sabor-contador]"
            )
            .forEach(function (sabor) {

                const quantidadeElemento =
                    sabor.querySelector(
                        "[data-sabor-quantidade]"
                    );


                const quantidade =
                    parseInt(
                        quantidadeElemento?.textContent || 0
                    ) || 0;


                const mais =
                    sabor.querySelector(
                        '[data-sabor-acao="mais"]'
                    );


                const menos =
                    sabor.querySelector(
                        '[data-sabor-acao="menos"]'
                    );


                if (menos) {

                    menos.disabled =
                        quantidade <= 0;

                }


                if (mais) {

                    if (!permiteMultiplos) {

                        mais.disabled =
                            quantidade >= 1 ||
                            (
                                total >= maximo &&
                                quantidade === 0
                            );

                    } else {

                        mais.disabled =
                            total >= maximo;

                    }

                }

            });

    }


    container
        .querySelectorAll(
            "[data-sabor-contador]"
        )
        .forEach(function (sabor) {

            const mais =
                sabor.querySelector(
                    '[data-sabor-acao="mais"]'
                );


            const menos =
                sabor.querySelector(
                    '[data-sabor-acao="menos"]'
                );


            const contadorSabor =
                sabor.querySelector(
                    "[data-sabor-quantidade]"
                );


            if (
                !mais ||
                !menos ||
                !contadorSabor
            ) {

                return;

            }


            mais.addEventListener(
                "click",
                function () {

                    const quantidade =
                        parseInt(
                            contadorSabor.textContent || 0
                        ) || 0;


                    const total =
                        obterTotal();


                    if (
                        total >= maximo
                    ) {

                        return;

                    }


                    if (
                        !permiteMultiplos &&
                        quantidade >= 1
                    ) {

                        return;

                    }


                    contadorSabor.textContent =
                        quantidade + 1;


                    atualizar();

                }
            );


            menos.addEventListener(
                "click",
                function () {

                    const quantidade =
                        parseInt(
                            contadorSabor.textContent || 0
                        ) || 0;


                    if (
                        quantidade <= 0
                    ) {

                        return;

                    }


                    contadorSabor.textContent =
                        quantidade - 1;


                    atualizar();

                }
            );

        });


    atualizar();

}


// =================================================================
// PRODUTOS DO COMBO
// =================================================================

function inicializarProdutosCombo() {

    document
        .querySelectorAll(
            "[data-item-contador]"
        )
        .forEach(function (controle) {

            inicializarControleProdutoCombo(
                controle
            );

        });

}


// =================================================================
// CONTROLE DE UM PRODUTO DO COMBO
// =================================================================

function inicializarControleProdutoCombo(
    controle
) {

    const itemId =
        controle.dataset.item;


    const grupoId =
        controle.dataset.grupo;


    const maximo =
        parseInt(
            controle.dataset.maximo
        ) || 0;


    const quantidadeElemento =
        document.querySelector(
            `[data-quantidade="${itemId}"]`
        );


    const botaoMais =
        controle.querySelector(
            '[data-acao="mais"]'
        );


    const botaoMenos =
        controle.querySelector(
            '[data-acao="menos"]'
        );


    const containerPersonalizacoes =
        document.querySelector(
            `[data-personalizacoes="${itemId}"]`
        );


    const template =
        document.getElementById(
            `template-personalizacao-${itemId}`
        );


    if (
        !quantidadeElemento ||
        !botaoMais ||
        !botaoMenos
    ) {

        return;

    }


    // ============================================================
    // TOTAL DO GRUPO
    // ============================================================

    function obterTotalGrupo() {

        let total = 0;


        document
            .querySelectorAll(
                `[data-item-contador][data-grupo="${grupoId}"]`
            )
            .forEach(function (outroControle) {

                const outroItemId =
                    outroControle.dataset.item;


                const elemento =
                    document.querySelector(
                        `[data-quantidade="${outroItemId}"]`
                    );


                if (!elemento) {

                    return;

                }


                total +=
                    parseInt(
                        elemento.textContent || 0
                    ) || 0;

            });


        return total;

    }


    // ============================================================
    // CRIAR PERSONALIZAÇÃO
    // ============================================================

    function criarPersonalizacao(numero) {

        if (
            !template ||
            !containerPersonalizacoes
        ) {

            return;

        }


        const clone =
            template.content.cloneNode(true);


        const numeroElemento =
            clone.querySelector(
                "[data-numero-unidade]"
            );


        if (numeroElemento) {

            numeroElemento.textContent =
                `#${numero}`;

        }


        // --------------------------------------------------------
        // SABORES
        // --------------------------------------------------------

        clone
            .querySelectorAll(
                "[data-sabores-container]"
            )
            .forEach(function (container) {

                inicializarSabores(
                    container
                );

            });


        // --------------------------------------------------------
        // INGREDIENTES
        // --------------------------------------------------------

        inicializarIngredientes(
            clone
        );


        // --------------------------------------------------------
        // ADICIONAIS
        // --------------------------------------------------------

        inicializarAdicionais(
            clone
        );


        containerPersonalizacoes.appendChild(
            clone
        );

    }


    // ============================================================
    // REMOVER PERSONALIZAÇÃO
    // ============================================================

    function removerPersonalizacao() {

        if (
            !containerPersonalizacoes
        ) {

            return;

        }


        const personalizacoes =
            containerPersonalizacoes.querySelectorAll(
                "[data-personalizacao-unidade]"
            );


        if (
            personalizacoes.length > 0
        ) {

            personalizacoes[
                personalizacoes.length - 1
            ].remove();

        }

    }


    // ============================================================
    // ATUALIZAR CONTROLE
    // ============================================================

    function atualizar() {

        const quantidade =
            parseInt(
                quantidadeElemento.textContent || 0
            ) || 0;


        quantidadeElemento.textContent =
            quantidade;


        // --------------------------------------------------------
        // PERSONALIZAÇÕES
        // --------------------------------------------------------

        if (containerPersonalizacoes) {

            let existentes =
                containerPersonalizacoes.querySelectorAll(
                    "[data-personalizacao-unidade]"
                ).length;


            while (
                existentes < quantidade
            ) {

                existentes++;


                criarPersonalizacao(
                    existentes
                );

            }


            while (
                containerPersonalizacoes.querySelectorAll(
                    "[data-personalizacao-unidade]"
                ).length > quantidade
            ) {

                removerPersonalizacao();

            }

        }


        // --------------------------------------------------------
        // CONTADOR DO GRUPO
        // --------------------------------------------------------

        const total =
            obterTotalGrupo();


        const contadorGrupo =
            document.querySelector(
                `[data-contador-grupo="${grupoId}"]`
            );


        if (contadorGrupo) {

            const strong =
                contadorGrupo.querySelector(
                    "strong"
                );


            if (strong) {

                strong.textContent =
                    total;

            }

        }


        // --------------------------------------------------------
        // BOTÕES
        // --------------------------------------------------------

        botaoMenos.disabled =
            quantidade <= 0;


        botaoMais.disabled =
            total >= maximo;


        // --------------------------------------------------------
        // ATUALIZAR TODOS OS PRODUTOS DO GRUPO
        // --------------------------------------------------------

        document
            .querySelectorAll(
                `[data-item-contador][data-grupo="${grupoId}"]`
            )
            .forEach(function (outroControle) {

                const outroItemId =
                    outroControle.dataset.item;


                const outroQuantidadeElemento =
                    document.querySelector(
                        `[data-quantidade="${outroItemId}"]`
                    );


                const outroMais =
                    outroControle.querySelector(
                        '[data-acao="mais"]'
                    );


                if (
                    !outroQuantidadeElemento ||
                    !outroMais
                ) {

                    return;

                }


                const outroQuantidade =
                    parseInt(
                        outroQuantidadeElemento.textContent || 0
                    ) || 0;


                outroMais.disabled =
                    total >= maximo &&
                    outroQuantidade === 0;

            });

    }


    // ============================================================
    // +
    // ============================================================

    botaoMais.addEventListener(
        "click",
        function () {

            const total =
                obterTotalGrupo();


            if (
                total >= maximo
            ) {

                return;

            }


            const quantidade =
                parseInt(
                    quantidadeElemento.textContent || 0
                ) || 0;


            quantidadeElemento.textContent =
                quantidade + 1;


            atualizar();

        }
    );


    // ============================================================
    // -
    // ============================================================

    botaoMenos.addEventListener(
        "click",
        function () {

            const quantidade =
                parseInt(
                    quantidadeElemento.textContent || 0
                ) || 0;


            if (
                quantidade <= 0
            ) {

                return;

            }


            quantidadeElemento.textContent =
                quantidade - 1;


            atualizar();

        }
    );


    atualizar();

}


// =================================================================
// INGREDIENTES
// =================================================================

function inicializarIngredientes(
    clone
) {

    clone
        .querySelectorAll(
            "[data-ingrediente-contador]"
        )
        .forEach(function (controle) {

            const mais =
                controle.querySelector(
                    '[data-ingrediente-acao="mais"]'
                );


            const menos =
                controle.querySelector(
                    '[data-ingrediente-acao="menos"]'
                );


            const contador =
                controle.querySelector(
                    "span"
                );


            if (
                !mais ||
                !menos ||
                !contador
            ) {

                return;

            }


            let quantidade =
                0;


            mais.addEventListener(
                "click",
                function () {

                    if (
                        quantidade >= 1
                    ) {

                        return;

                    }


                    quantidade =
                        1;


                    contador.textContent =
                        quantidade;


                    mais.disabled =
                        true;


                    menos.disabled =
                        false;

                }
            );


            menos.addEventListener(
                "click",
                function () {

                    if (
                        quantidade <= 0
                    ) {

                        return;

                    }


                    quantidade =
                        0;


                    contador.textContent =
                        quantidade;


                    mais.disabled =
                        false;


                    menos.disabled =
                        true;

                }
            );


            menos.disabled =
                true;

        });

}


// =================================================================
// ADICIONAIS
// =================================================================

function inicializarAdicionais(
    clone
) {

    clone
        .querySelectorAll(
            "[data-adicional-contador]"
        )
        .forEach(function (controle) {

            const mais =
                controle.querySelector(
                    '[data-adicional-acao="mais"]'
                );


            const menos =
                controle.querySelector(
                    '[data-adicional-acao="menos"]'
                );


            const contador =
                controle.querySelector(
                    "span"
                );


            if (
                !mais ||
                !menos ||
                !contador
            ) {

                return;

            }


            let quantidade =
                0;


            mais.addEventListener(
                "click",
                function () {

                    quantidade++;


                    contador.textContent =
                        quantidade;


                    menos.disabled =
                        false;

                }
            );


            menos.addEventListener(
                "click",
                function () {

                    if (
                        quantidade <= 0
                    ) {

                        return;

                    }


                    quantidade--;


                    contador.textContent =
                        quantidade;


                    menos.disabled =
                        quantidade <= 0;

                }
            );


            menos.disabled =
                true;

        });

}


// =================================================================
// FORMULÁRIO - PRODUTO NORMAL
// =================================================================

function inicializarFormularioProduto() {

    const formulario =
        document.getElementById(
            "form-produto"
        );


    if (!formulario) {

        return;

    }


    formulario.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();


            // ----------------------------------------------------
            // PRODUTO ID
            // ----------------------------------------------------

            const produtoInput =
                formulario.querySelector(
                    'input[name="produto"]'
                );


            const produtoId =
                produtoInput?.value;


            if (!produtoId) {

                alert(
                    "Produto não identificado."
                );

                return;

            }


            // ----------------------------------------------------
            // SABORES
            // ----------------------------------------------------

            formulario
                .querySelectorAll(
                    'input[name="sabores"]'
                )
                .forEach(function (input) {

                    input.remove();

                });


            const containerSabores =
                formulario.querySelector(
                    "[data-sabores-container]"
                );


            if (containerSabores) {

                const maximo =
                    parseInt(
                        containerSabores.dataset.maximoSabores
                    ) || 1;


                const total =
                    obterTotalSabores(
                        containerSabores
                    );


                if (
                    total <= 0
                ) {

                    alert(
                        "Selecione pelo menos um sabor."
                    );

                    return;

                }


                if (
                    total > maximo
                ) {

                    alert(
                        "Você selecionou sabores acima do limite permitido."
                    );

                    return;

                }


                adicionarInputsSabores(
                    formulario,
                    containerSabores
                );

            }


            const dados =
                new FormData(
                    formulario
                );


            enviarDadosParaCarrinho(
                dados,
                produtoId
            );

        }
    );

}


// =================================================================
// TOTAL DE SABORES
// =================================================================

function obterTotalSabores(
    container
) {

    let total =
        0;


    container
        .querySelectorAll(
            "[data-sabor-contador]"
        )
        .forEach(function (sabor) {

            const quantidade =
                parseInt(
                    sabor.querySelector(
                        "[data-sabor-quantidade]"
                    )?.textContent || 0
                ) || 0;


            total +=
                quantidade;

        });


    return total;

}


// =================================================================
// INPUTS DOS SABORES
// =================================================================

function adicionarInputsSabores(
    formulario,
    container
) {

    container
        .querySelectorAll(
            "[data-sabor-contador]"
        )
        .forEach(function (sabor) {

            const saborId =
                sabor.dataset.saborId;


            const quantidade =
                parseInt(
                    sabor.querySelector(
                        "[data-sabor-quantidade]"
                    )?.textContent || 0
                ) || 0;


            if (
                !saborId ||
                quantidade <= 0
            ) {

                return;

            }


            for (
                let i = 0;
                i < quantidade;
                i++
            ) {

                const input =
                    document.createElement(
                        "input"
                    );


                input.type =
                    "hidden";


                input.name =
                    "sabores";


                input.value =
                    saborId;


                formulario.appendChild(
                    input
                );

            }

        });

}


// =================================================================
// FORMULÁRIO - COMBO
// =================================================================

function inicializarFormularioCombo() {

    const formulario =
        document.getElementById(
            "form-combo"
        );


    if (!formulario) {

        return;

    }


    formulario.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();


            // ====================================================
            // IDENTIFICAR COMBO
            // ====================================================

            const produtoInput =
                formulario.querySelector(
                    'input[name="produto"]'
                );

            const produtoId =
                produtoInput?.value;

            if (!produtoId) {

                alert(
                    "Produto combo não identificado."
                );

                return;

            }


            // ====================================================
            // VALIDAR GRUPOS
            // ====================================================

            if (
                !validarGruposCombo()
            ) {

                alert(
                    "Verifique as opções selecionadas no combo."
                );

                return;

            }


            // ====================================================
            // FORM DATA
            // ====================================================

            const dados =
                new FormData(
                    formulario
                );


            // ====================================================
            // PRODUTOS DO COMBO
            // ====================================================

            document
                .querySelectorAll(
                    "[data-item-contador]"
                )
                .forEach(function (controle) {

                    const itemId =
                        controle.dataset.item;


                    const quantidadeElemento =
                        document.querySelector(
                            `[data-quantidade="${itemId}"]`
                        );


                    if (!quantidadeElemento) {

                        return;

                    }


                    const quantidade =
                        parseInt(
                            quantidadeElemento.textContent || 0
                        ) || 0;


                    if (
                        quantidade <= 0
                    ) {

                        return;

                    }


                    /*
                     * ProdutoComboGrupoItem
                     *
                     * itemId = ID do ProdutoComboGrupoItem
                     *
                     * quantidade = quantidade escolhida
                     */

                    dados.append(
                        `combo_item_${itemId}`,
                        quantidade
                    );

                });


            // ====================================================
            // PERSONALIZAÇÕES
            // ====================================================

            document
                .querySelectorAll(
                    "[data-personalizacao-unidade]"
                )
                .forEach(function (personalizacao) {

                    const wrapper =
                        personalizacao.closest(
                            "[data-item-wrapper]"
                        );


                    if (!wrapper) {

                        return;

                    }


                    const itemId =
                        wrapper.dataset.itemWrapper;


                    const numeroElemento =
                        personalizacao.querySelector(
                            "[data-numero-unidade]"
                        );


                    let numero =
                        "1";


                    if (numeroElemento) {

                        numero =
                            numeroElemento.textContent
                                .replace(
                                    "#",
                                    ""
                                )
                                .trim();

                    }


                    // ==========================================
                    // SABORES
                    // ==========================================

                    personalizacao
                        .querySelectorAll(
                            "[data-sabores-container]"
                        )
                        .forEach(function (container) {

                            adicionarSaboresCombo(
                                dados,
                                container,
                                itemId,
                                numero
                            );

                        });


                    // ==========================================
                    // INGREDIENTES
                    // ==========================================

                    personalizacao
                        .querySelectorAll(
                            "[data-ingrediente-contador]"
                        )
                        .forEach(function (controle) {

                            const ingredienteId =
                                controle.dataset.ingredienteId;


                            const quantidade =
                                parseInt(
                                    controle.querySelector(
                                        "span"
                                    )?.textContent || 0
                                ) || 0;


                            if (
                                !ingredienteId ||
                                quantidade <= 0
                            ) {

                                return;

                            }


                            /*
                             * Ingrediente removido
                             *
                             * A chave identifica:
                             *
                             * item do combo
                             * unidade
                             * ingrediente
                             */

                            dados.append(
                                `ingrediente_${itemId}_${numero}`,
                                ingredienteId
                            );

                        });


                    // ==========================================
                    // ADICIONAIS
                    // ==========================================

                    personalizacao
                        .querySelectorAll(
                            "[data-adicional-contador]"
                        )
                        .forEach(function (controle) {

                            const adicionalId =
                                controle.dataset.adicionalId;


                            const quantidade =
                                parseInt(
                                    controle.querySelector(
                                        "span"
                                    )?.textContent || 0
                                ) || 0;


                            if (
                                !adicionalId ||
                                quantidade <= 0
                            ) {

                                return;

                            }


                            for (
                                let i = 0;
                                i < quantidade;
                                i++
                            ) {

                                dados.append(
                                    `adicional_${itemId}_${numero}`,
                                    adicionalId
                                );

                            }

                        });

                });


            // ====================================================
            // ENVIAR
            // ====================================================

            enviarDadosParaCarrinho(
                dados,
                produtoId
            );

        }
    );

}


// =================================================================
// VALIDAR GRUPOS DO COMBO
// =================================================================

function validarGruposCombo() {

    let valido =
        true;


    document
        .querySelectorAll(
            "[data-contador-grupo]"
        )
        .forEach(function (contador) {

            const grupoId =
                contador.dataset.contadorGrupo;


            /*
             * Caso o navegador não tenha colocado
             * data-contador-grupo, tentamos obter
             * do próprio elemento.
             */

            if (!grupoId) {

                return;

            }


            const container =
                document.querySelector(
                    `[data-grupo-container="${grupoId}"]`
                );


            if (!container) {

                return;

            }


            // ----------------------------------------------------
            // TOTAL SELECIONADO
            // ----------------------------------------------------

            let total =
                0;


            document
                .querySelectorAll(
                    `[data-item-contador][data-grupo="${grupoId}"]`
                )
                .forEach(function (controle) {

                    const itemId =
                        controle.dataset.item;


                    const quantidadeElemento =
                        document.querySelector(
                            `[data-quantidade="${itemId}"]`
                        );


                    if (!quantidadeElemento) {

                        return;

                    }


                    total +=
                        parseInt(
                            quantidadeElemento.textContent || 0
                        ) || 0;

                });


            // ----------------------------------------------------
            // MINIMO / MAXIMO
            // ----------------------------------------------------

            const texto =
                container.textContent
                    .replace(/\s+/g, " ")
                    .trim();


            let minimo =
                0;


            let maximo =
                0;


            const intervalo =
                texto.match(
                    /Escolha\s+de\s+(\d+)\s+até\s+(\d+)/
                );


            const escolha =
                texto.match(
                    /Escolha\s+(\d+)/
                );


            if (intervalo) {

                minimo =
                    parseInt(
                        intervalo[1]
                    ) || 0;


                maximo =
                    parseInt(
                        intervalo[2]
                    ) || 0;

            } else if (escolha) {

                minimo =
                    parseInt(
                        escolha[1]
                    ) || 0;


                maximo =
                    minimo;

            }


            // ----------------------------------------------------
            // ULTRAPASSOU MÁXIMO
            // ----------------------------------------------------

            if (
                total > maximo
            ) {

                valido =
                    false;

            }


            // ----------------------------------------------------
            // OBRIGATÓRIO
            // ----------------------------------------------------

            if (
                texto.includes(
                    "Obrigatório"
                ) &&
                total < minimo
            ) {

                valido =
                    false;

            }

        });


    return valido;

}


// =================================================================
// ADICIONAR SABORES DO COMBO
// =================================================================

function adicionarSaboresCombo(
    dados,
    container,
    itemId,
    numero
) {

    container
        .querySelectorAll(
            "[data-sabor-contador]"
        )
        .forEach(function (sabor) {

            const saborId =
                sabor.dataset.saborId;


            const quantidade =
                parseInt(
                    sabor.querySelector(
                        "[data-sabor-quantidade]"
                    )?.textContent || 0
                ) || 0;


            if (
                !saborId ||
                quantidade <= 0
            ) {

                return;

            }


            for (
                let i = 0;
                i < quantidade;
                i++
            ) {

                dados.append(
                    `sabor_${itemId}_${numero}`,
                    saborId
                );

            }

        });

}


// =================================================================
// BOTÕES DE ADICIONAR PRODUTO
// =================================================================

function inicializarBotoesAdicionar() {

    document
        .querySelectorAll(
            ".btn-adicionar-carrinho"
        )
        .forEach(function (btn) {

            if (
                btn.dataset.eventoAdicionar === "true"
            ) {

                return;

            }


            btn.dataset.eventoAdicionar =
                "true";


            btn.addEventListener(
                "click",
                function () {

                    const produtoId =
                        this.dataset.produtoId;


                    if (!produtoId) {

                        alert(
                            "Produto não identificado."
                        );

                        return;

                    }


                    const dados =
                        new URLSearchParams();


                    dados.append(
                        "quantidade",
                        "1"
                    );


                    fetch(
                        `/cardapio/carrinho/adicionar/${produtoId}/`,
                        {

                            method: "POST",

                            headers: {

                                "X-CSRFToken":
                                    getCookie(
                                        "csrftoken"
                                    ),

                                "Content-Type":
                                    "application/x-www-form-urlencoded"

                            },

                            body:
                                dados

                        }
                    )
                    .then(function (response) {

                        return response.json();

                    })
                    .then(function (data) {

                        if (
                            data.sucesso
                        ) {

                            atualizarWidgetCarrinho();

                        } else {

                            alert(
                                data.erro ||
                                "Não foi possível adicionar o produto."
                            );

                        }

                    })
                    .catch(function (erro) {

                        console.error(
                            "Erro ao adicionar produto:",
                            erro
                        );

                    });

                }
            );

        });

}


// =================================================================
// ENVIAR PARA O CARRINHO
// =================================================================

function enviarDadosParaCarrinho(
    dados,
    produtoId
) {

    if (!produtoId) {

        alert(
            "Produto não identificado."
        );

        return;

    }


    fetch(
        `/cardapio/carrinho/adicionar/${produtoId}/`,
        {

            method: "POST",

            headers: {

                "X-CSRFToken":
                    getCookie(
                        "csrftoken"
                    )

            },

            body:
                dados

        }
    )
    .then(function (response) {

        return response.json()
            .then(function (data) {

                return {
                    ok: response.ok,
                    data: data
                };

            });

    })
    .then(function (resultado) {

        const data =
            resultado.data;


        if (
            !resultado.ok
        ) {

            throw new Error(
                data.erro ||
                "Erro ao adicionar ao carrinho."
            );

        }


        if (
            !data.sucesso
        ) {

            throw new Error(
                data.erro ||
                "Não foi possível adicionar ao carrinho."
            );

        }


        atualizarWidgetCarrinho();


        window.location.href =
            "/cardapio/cardapio_cliente/";

    })
    .catch(function (erro) {

        console.error(
            "Erro ao adicionar ao carrinho:",
            erro
        );


        alert(
            erro.message ||
            "Erro ao adicionar o produto ao carrinho."
        );

    });

}


// =================================================================
// ATUALIZAR WIDGET DO CARRINHO
// =================================================================

function atualizarWidgetCarrinho() {

    fetch(
        "/cardapio/carrinho/widget/"
    )
    .then(function (response) {

        return response.json();

    })
    .then(function (data) {

        const itens =
            document.getElementById(
                "carrinho-itens"
            );


        if (itens) {

            itens.innerHTML =
                data.html;

        }


        const total =
            document.getElementById(
                "carrinho-total-valor"
            );


        if (
            total &&
            data.total_valor !== undefined
        ) {

            total.textContent =
                "R$ " +
                String(
                    data.total_valor
                ).replace(
                    ".",
                    ","
                );

        }


        const badge =
            document.getElementById(
                "carrinho-badge"
            );


        if (badge) {

            badge.textContent =
                data.total_itens;


            if (
                data.total_itens > 0
            ) {

                badge.style.display =
                    "inline-block";

            } else {

                badge.style.display =
                    "none";

            }

        }


        ativarBotoesRemover();

    })
    .catch(function (erro) {

        console.error(
            "Erro ao atualizar carrinho:",
            erro
        );

    });

}


// =================================================================
// REMOVER ITEM DO CARRINHO
// =================================================================

function ativarBotoesRemover() {

    document
        .querySelectorAll(
            ".btn-remover-carrinho"
        )
        .forEach(function (btn) {

            if (
                btn.dataset.eventoRemover === "true"
            ) {

                return;

            }


            btn.dataset.eventoRemover =
                "true";


            btn.addEventListener(
                "click",
                function () {

                    const chave =
                        this.dataset.chave;


                    if (!chave) {

                        return;

                    }


                    const dados =
                        new URLSearchParams();


                    dados.append(
                        "chave",
                        chave
                    );


                    fetch(
                        "/cardapio/carrinho/remover/",
                        {

                            method: "POST",

                            headers: {

                                "X-CSRFToken":
                                    getCookie(
                                        "csrftoken"
                                    ),

                                "Content-Type":
                                    "application/x-www-form-urlencoded"

                            },

                            body:
                                dados

                        }
                    )
                    .then(function (response) {

                        return response.json();

                    })
                    .then(function (data) {

                        if (
                            data.sucesso
                        ) {

                            atualizarWidgetCarrinho();

                        } else {

                            alert(
                                data.erro ||
                                "Não foi possível remover o item."
                            );

                        }

                    })
                    .catch(function (erro) {

                        console.error(
                            "Erro ao remover:",
                            erro
                        );

                    });

                }
            );

        });

}


// =================================================================
// CSRF
// =================================================================

function getCookie(name) {

    let cookieValue =
        null;


    if (
        document.cookie &&
        document.cookie !== ""
    ) {

        document
            .cookie
            .split(";")
            .forEach(function (cookie) {

                cookie =
                    cookie.trim();


                if (
                    cookie.startsWith(
                        name + "="
                    )
                ) {

                    cookieValue =
                        decodeURIComponent(
                            cookie.substring(
                                name.length + 1
                            )
                        );

                }

            });

    }


    return cookieValue;

}