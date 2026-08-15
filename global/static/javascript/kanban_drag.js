document.addEventListener("DOMContentLoaded", function () {

    console.log("KANBAN: iniciado");


    const cards = document.querySelectorAll(
        ".kanban-card"
    );

    const dropzones = document.querySelectorAll(
        ".kanban-dropzone"
    );


    console.log(
        "CARDS:",
        cards.length
    );

    console.log(
        "DROPZONES:",
        dropzones.length
    );


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


                atualizarVazios();

                atualizarContadores();

            }
        );

    });


    // =========================================================
    // DROPZONES
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

                /*
                 * Não remove o destaque quando
                 * o mouse passa por elementos internos.
                 */

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
                // MOVE CARD
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


                /*
                 * POR ENQUANTO:
                 *
                 * Apenas altera visualmente.
                 *
                 * Ainda não salva no banco.
                 */

            }
        );

    });


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