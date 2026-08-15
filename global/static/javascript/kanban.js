document.addEventListener("DOMContentLoaded", function () {

    console.log("KANBAN: iniciado");


    const cards = document.querySelectorAll(
        ".kanban-card"
    );


    const dropzones = document.querySelectorAll(
        ".kanban-dropzone"
    );


    const finalizarDropzone =
        document.querySelector(
            ".kanban-finalizar"
        );


    console.log(
        "CARDS:",
        cards.length
    );


    console.log(
        "DROPZONES:",
        dropzones.length
    );


    console.log(
        "FINALIZAR:",
        !!finalizarDropzone
    );


    // =========================================================
    // CSRF
    // =========================================================

    function obterCSRFToken() {

        const nome = "csrftoken=";

        const cookies =
            document.cookie.split(";");


        for (
            let i = 0;
            i < cookies.length;
            i++
        ) {

            let cookie =
                cookies[i].trim();


            if (
                cookie.indexOf(nome) === 0
            ) {

                return decodeURIComponent(
                    cookie.substring(
                        nome.length
                    )
                );

            }

        }


        return "";

    }


    // =========================================================
    // CLIQUE NO CARD
    // =========================================================

    cards.forEach(function (card) {

        card.addEventListener(
            "click",
            function () {

                /*
                 * Se estiver sendo arrastado,
                 * não expande.
                 */

                if (
                    card.classList.contains(
                        "arrastando"
                    )
                ) {

                    return;

                }


                /*
                 * Fecha todos os outros cards.
                 */

                document
                    .querySelectorAll(
                        ".kanban-card.expandido"
                    )
                    .forEach(function (outroCard) {

                        if (
                            outroCard !== card
                        ) {

                            outroCard.classList.remove(
                                "expandido"
                            );

                        }

                    });


                /*
                 * Abre ou fecha o card clicado.
                 */

                card.classList.toggle(
                    "expandido"
                );

            }
        );


        // =====================================================
        // DRAG START
        // =====================================================

        card.addEventListener(
            "dragstart",
            function (event) {

                const pedidoId =
                    card.dataset.pedidoId;


                console.log(
                    "DRAG START"
                );


                console.log(
                    "PEDIDO ID:",
                    pedidoId
                );


                card.classList.add(
                    "arrastando"
                );


                event.dataTransfer.effectAllowed =
                    "move";


                event.dataTransfer.setData(
                    "text/plain",
                    pedidoId
                );

            }
        );


        // =====================================================
        // DRAG END
        // =====================================================

        card.addEventListener(
            "dragend",
            function () {

                console.log(
                    "DRAG END"
                );


                card.classList.remove(
                    "arrastando"
                );


                dropzones.forEach(
                    function (dropzone) {

                        dropzone.classList.remove(
                            "drag-over"
                        );

                    }
                );


                if (finalizarDropzone) {

                    finalizarDropzone.classList.remove(
                        "drag-over"
                    );

                }


                atualizarVazios();

                atualizarContadores();

            }
        );

    });


    // =========================================================
    // DROPZONES NORMAIS
    // =========================================================

    dropzones.forEach(function (dropzone) {


        // =====================================================
        // DRAG OVER
        // =====================================================

        dropzone.addEventListener(
            "dragover",
            function (event) {

                event.preventDefault();


                event.dataTransfer.dropEffect =
                    "move";


                dropzone.classList.add(
                    "drag-over"
                );

            }
        );


        // =====================================================
        // DRAG LEAVE
        // =====================================================

        dropzone.addEventListener(
            "dragleave",
            function (event) {

                if (
                    event.relatedTarget &&
                    dropzone.contains(
                        event.relatedTarget
                    )
                ) {

                    return;

                }


                dropzone.classList.remove(
                    "drag-over"
                );

            }
        );


        // =====================================================
        // DROP
        // =====================================================

        dropzone.addEventListener(
            "drop",
            function (event) {

                event.preventDefault();


                dropzone.classList.remove(
                    "drag-over"
                );


                // =================================================
                // PEDIDO
                // =================================================

                const pedidoId =
                    event.dataTransfer.getData(
                        "text/plain"
                    );


                console.log(
                    "DROP"
                );


                console.log(
                    "PEDIDO:",
                    pedidoId
                );


                if (!pedidoId) {

                    console.log(
                        "ERRO: pedido não encontrado."
                    );

                    return;

                }


                // =================================================
                // CARD
                // =================================================

                const card =
                    document.querySelector(
                        '.kanban-card[data-pedido-id="' +
                        pedidoId +
                        '"]'
                    );


                if (!card) {

                    console.log(
                        "ERRO: card não encontrado."
                    );

                    return;

                }


                // =================================================
                // DROPZONE ANTERIOR
                // =================================================

                const dropzoneAnterior =
                    card.closest(
                        ".kanban-dropzone"
                    );


                // =================================================
                // STATUS ANTERIOR
                // =================================================

                let statusAnteriorId = null;


                if (dropzoneAnterior) {

                    statusAnteriorId =
                        dropzoneAnterior.dataset.statusId;

                }


                // =================================================
                // NOVO STATUS
                // =================================================

                const novoStatusId =
                    dropzone.dataset.statusId;


                console.log(
                    "STATUS ANTERIOR:",
                    statusAnteriorId
                );


                console.log(
                    "NOVO STATUS:",
                    novoStatusId
                );


                // =================================================
                // MESMA COLUNA
                // =================================================

                if (
                    statusAnteriorId ===
                    novoStatusId
                ) {

                    console.log(
                        "Pedido já está nesta coluna."
                    );

                    return;

                }


                // =================================================
                // REMOVE MENSAGEM DE COLUNA VAZIA
                // =================================================

                const mensagemVazia =
                    dropzone.querySelector(
                        ".kanban-empty"
                    );


                if (mensagemVazia) {

                    mensagemVazia.remove();

                }


                // =================================================
                // MOVE CARD VISUALMENTE
                // =================================================

                dropzone.appendChild(
                    card
                );


                /*
                 * Ao mover o card,
                 * fecha a expansão.
                 */

                card.classList.remove(
                    "expandido"
                );


                // =================================================
                // ATUALIZA INTERFACE
                // =================================================

                atualizarContadores();

                atualizarVazios();


                // =================================================
                // DEBUG
                // =================================================

                console.log(
                    "================================"
                );


                console.log(
                    "PEDIDO MOVIDO"
                );


                console.log(
                    "PEDIDO ID:",
                    pedidoId
                );


                console.log(
                    "STATUS ANTERIOR:",
                    statusAnteriorId
                );


                console.log(
                    "NOVO STATUS:",
                    novoStatusId
                );


                console.log(
                    "================================"
                );


                // =================================================
                // SALVAR NO BANCO
                // =================================================

                alterarStatusPedido(
                    pedidoId,
                    novoStatusId,
                    card,
                    dropzone,
                    dropzoneAnterior,
                    false
                );

            }
        );

    });


    // =========================================================
    // ÁREA FINALIZAR PEDIDO
    // =========================================================

    if (finalizarDropzone) {


        // =====================================================
        // DRAG OVER
        // =====================================================

        finalizarDropzone.addEventListener(
            "dragover",
            function (event) {

                event.preventDefault();


                event.dataTransfer.dropEffect =
                    "move";


                finalizarDropzone.classList.add(
                    "drag-over"
                );

            }
        );


        // =====================================================
        // DRAG LEAVE
        // =====================================================

        finalizarDropzone.addEventListener(
            "dragleave",
            function (event) {

                if (
                    event.relatedTarget &&
                    finalizarDropzone.contains(
                        event.relatedTarget
                    )
                ) {

                    return;

                }


                finalizarDropzone.classList.remove(
                    "drag-over"
                );

            }
        );


        // =====================================================
        // DROP
        // =====================================================

        finalizarDropzone.addEventListener(
            "drop",
            function (event) {

                event.preventDefault();


                finalizarDropzone.classList.remove(
                    "drag-over"
                );


                // =================================================
                // PEDIDO
                // =================================================

                const pedidoId =
                    event.dataTransfer.getData(
                        "text/plain"
                    );


                console.log(
                    "DROP PARA FINALIZAR"
                );


                console.log(
                    "PEDIDO:",
                    pedidoId
                );


                if (!pedidoId) {

                    console.log(
                        "ERRO: pedido não encontrado."
                    );

                    return;

                }


                // =================================================
                // CARD
                // =================================================

                const card =
                    document.querySelector(
                        '.kanban-card[data-pedido-id="' +
                        pedidoId +
                        '"]'
                    );


                if (!card) {

                    console.log(
                        "ERRO: card não encontrado."
                    );

                    return;

                }


                // =================================================
                // DROPZONE ANTERIOR
                // =================================================

                const dropzoneAnterior =
                    card.closest(
                        ".kanban-dropzone"
                    );


                if (!dropzoneAnterior) {

                    console.log(
                        "ERRO: coluna anterior não encontrada."
                    );

                    return;

                }


                // =================================================
                // STATUS ENTREGUE
                // =================================================

                const statusEntregueId =
                    finalizarDropzone.dataset.statusId;


                console.log(
                    "STATUS ENTREGUE:",
                    statusEntregueId
                );


                // =================================================
                // CONFIRMAÇÃO
                // =================================================

                const confirmar =
                    window.confirm(
                        "Finalizar o pedido #" +
                        card.dataset.pedidoId +
                        "?\n\n" +
                        "O pedido será marcado como " +
                        "ENTREGUE e removido do Kanban."
                    );


                // =================================================
                // CANCELADO
                // =================================================

                if (!confirmar) {

                    console.log(
                        "FINALIZAÇÃO CANCELADA."
                    );

                    return;

                }


                // =================================================
                // SALVAR
                // =================================================

                alterarStatusPedido(
                    pedidoId,
                    statusEntregueId,
                    card,
                    null,
                    dropzoneAnterior,
                    true
                );

            }
        );

    }


    // =========================================================
    // ALTERAR STATUS DO PEDIDO
    // =========================================================

    function alterarStatusPedido(
        pedidoId,
        novoStatusId,
        card,
        dropzone,
        dropzoneAnterior,
        finalizando = false
    ) {

        console.log(
            "ENVIANDO STATUS PARA O SERVIDOR..."
        );


        console.log(
            "PEDIDO:",
            pedidoId
        );


        console.log(
            "NOVO STATUS:",
            novoStatusId
        );


        fetch(
            "/pedidos/kanban/alterar-status/",
            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/x-www-form-urlencoded",

                    "X-CSRFToken":
                        obterCSRFToken(),

                    "X-Requested-With":
                        "XMLHttpRequest"

                },

                body:
                    new URLSearchParams({

                        pedido_id:
                            pedidoId,

                        status_id:
                            novoStatusId

                    })

            }
        )
        .then(function (response) {

            console.log(
                "STATUS HTTP:",
                response.status
            );


            if (!response.ok) {

                throw new Error(
                    "Erro HTTP: " +
                    response.status
                );

            }


            return response.json();

        })
        .then(function (data) {

            console.log(
                "RESPOSTA DO SERVIDOR:",
                data
            );


            // =================================================
            // ERRO
            // =================================================

            if (!data.sucesso) {

                console.log(
                    "ERRO AO ALTERAR STATUS:",
                    data.erro
                );


                /*
                 * Se era uma finalização,
                 * o card nunca saiu da coluna.
                 *
                 * Portanto não precisamos
                 * fazer rollback visual.
                 */

                if (!finalizando) {

                    desfazerMovimento(
                        card,
                        dropzone,
                        dropzoneAnterior
                    );

                }


                alert(
                    data.erro ||
                    "Não foi possível alterar o status do pedido."
                );


                return;

            }


            // =================================================
            // FINALIZAÇÃO
            // =================================================

            if (finalizando) {

                console.log(
                    "PEDIDO FINALIZADO COM SUCESSO."
                );


                /*
                 * Remove o card do Kanban.
                 */

                card.remove();


                /*
                 * Atualiza contadores
                 * e mensagens de coluna vazia.
                 */

                atualizarContadores();

                atualizarVazios();


                return;

            }


            // =================================================
            // SUCESSO NORMAL
            // =================================================

            console.log(
                "================================"
            );


            console.log(
                "STATUS SALVO NO BANCO"
            );


            console.log(
                "PEDIDO:",
                data.pedido_id
            );


            console.log(
                "STATUS:",
                data.status_id
            );


            console.log(
                "STATUS:",
                data.status_nome
            );


            console.log(
                "================================"
            );

        })
        .catch(function (erro) {

            console.error(
                "ERRO AO SALVAR STATUS:",
                erro
            );


            /*
             * Se era uma finalização,
             * o card ainda está na coluna original.
             */

            if (!finalizando) {

                desfazerMovimento(
                    card,
                    dropzone,
                    dropzoneAnterior
                );

            }


            alert(
                "Não foi possível atualizar o status do pedido."
            );

        });

    }


    // =========================================================
    // DESFAZER MOVIMENTO
    // =========================================================

    function desfazerMovimento(
        card,
        dropzoneAtual,
        dropzoneAnterior
    ) {

        console.log(
            "DESFAZENDO MOVIMENTO..."
        );


        if (!dropzoneAnterior) {

            console.log(
                "ERRO: dropzone anterior não encontrada."
            );

            return;

        }


        /*
         * Retorna o card para a coluna
         * onde estava originalmente.
         */

        dropzoneAnterior.appendChild(
            card
        );


        /*
         * Atualiza novamente a interface.
         */

        atualizarContadores();

        atualizarVazios();


        console.log(
            "MOVIMENTO DESFEITO."
        );

    }


    // =========================================================
    // ATUALIZAR CONTADORES
    // =========================================================

    function atualizarContadores() {

        document
            .querySelectorAll(
                ".kanban-coluna"
            )
            .forEach(function (coluna) {


                const dropzone =
                    coluna.querySelector(
                        ".kanban-dropzone"
                    );


                const contador =
                    coluna.querySelector(
                        ".kanban-count"
                    );


                if (
                    !dropzone ||
                    !contador
                ) {

                    return;

                }


                const quantidade =
                    dropzone.querySelectorAll(
                        ".kanban-card"
                    ).length;


                contador.textContent =
                    quantidade;

            });

    }


    // =========================================================
    // ATUALIZAR COLUNAS VAZIAS
    // =========================================================

    function atualizarVazios() {

        document
            .querySelectorAll(
                ".kanban-dropzone"
            )
            .forEach(function (dropzone) {


                const quantidade =
                    dropzone.querySelectorAll(
                        ".kanban-card"
                    ).length;


                const mensagem =
                    dropzone.querySelector(
                        ".kanban-empty"
                    );


                // =================================================
                // SEM PEDIDOS
                // =================================================

                if (
                    quantidade === 0
                ) {

                    if (!mensagem) {

                        const div =
                            document.createElement(
                                "div"
                            );


                        div.className =
                            "kanban-empty text-center text-muted py-4";


                        div.textContent =
                            "Nenhum pedido";


                        dropzone.appendChild(
                            div
                        );

                    }

                }


                // =================================================
                // COM PEDIDOS
                // =================================================

                else {

                    if (mensagem) {

                        mensagem.remove();

                    }

                }

            });

    }


    // =========================================================
    // ESTADO INICIAL
    // =========================================================

    atualizarContadores();

    atualizarVazios();


    console.log(
        "KANBAN: pronto"
    );

});