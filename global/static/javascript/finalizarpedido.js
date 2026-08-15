document.addEventListener("DOMContentLoaded", function () {

    const formulario = document.querySelector("form");

    if (!formulario) {
        return;
    }


    // ==========================================
    // ELEMENTOS
    // ==========================================

    const nomeCliente = document.getElementById("nome_cliente");
    const telefoneCliente = document.getElementById("telefone_cliente");

    const tipoEntrega = document.getElementById("tipo_entrega");
    const tipoRetirada = document.getElementById("tipo_retirada");
    const tipoConsumo = document.getElementById("tipo_consumo");

    const cardEndereco = document.getElementById("card-endereco");

    const endereco = document.getElementById("endereco");
    const numeroEndereco = document.getElementById("numero_endereco");
    const complemento = document.getElementById("complemento");
    const bairro = document.getElementById("bairro");
    const cidade = document.getElementById("cidade");
    const estado = document.getElementById("estado");
    const cep = document.getElementById("cep");
    const referencia = document.getElementById("referencia");

    const pagamentos = document.querySelectorAll(
        'input[name="forma_pagamento"]'
    );


    // ==========================================
    // FUNÇÕES
    // ==========================================

    function limparErros() {

        const campos = formulario.querySelectorAll(
            ".is-invalid"
        );

        campos.forEach(function (campo) {

            campo.classList.remove("is-invalid");

        });


        const mensagens = formulario.querySelectorAll(
            ".mensagem-erro-js"
        );

        mensagens.forEach(function (mensagem) {

            mensagem.remove();

        });
    }


    function mostrarErro(campo, mensagem) {

        campo.classList.add("is-invalid");


        const mensagemErro = document.createElement("div");

        mensagemErro.className =
            "invalid-feedback mensagem-erro-js";

        mensagemErro.textContent = mensagem;


        campo.parentElement.appendChild(
            mensagemErro
        );

    }


    function valorVazio(campo) {

        return !campo.value.trim();

    }


    // ==========================================
    // TIPO DE ATENDIMENTO
    // ==========================================

    function atualizarEndereco() {

        if (tipoEntrega.checked) {

            cardEndereco.style.display = "";

            endereco.required = true;
            numeroEndereco.required = true;
            bairro.required = true;

        } else {

            cardEndereco.style.display = "none";

            endereco.required = false;
            numeroEndereco.required = false;
            bairro.required = false;

        }

    }


    tipoEntrega.addEventListener(
        "change",
        atualizarEndereco
    );


    tipoRetirada.addEventListener(
        "change",
        atualizarEndereco
    );


    tipoConsumo.addEventListener(
        "change",
        atualizarEndereco
    );


    // Executa ao carregar a página
    atualizarEndereco();


    // ==========================================
    // PAGAMENTO
    // ==========================================

    function verificarPagamento() {

        let selecionado = false;


        pagamentos.forEach(function (pagamento) {

            if (pagamento.checked) {

                selecionado = true;

            }

        });


        return selecionado;

    }


    // ==========================================
    // VALIDAÇÃO DO FORMULÁRIO
    // ==========================================

    formulario.addEventListener(
        "submit",
        function (event) {

            limparErros();


            let formularioValido = true;


            // ==================================
            // NOME
            // ==================================

            if (valorVazio(nomeCliente)) {

                mostrarErro(
                    nomeCliente,
                    "Informe seu nome."
                );

                formularioValido = false;

            }


            // ==================================
            // TIPO DE ATENDIMENTO
            // ==================================

            if (
                !tipoEntrega.checked &&
                !tipoRetirada.checked &&
                !tipoConsumo.checked
            ) {

                alert(
                    "Selecione como deseja receber o pedido."
                );

                formularioValido = false;

            }


            // ==================================
            // ENDEREÇO
            // ==================================

            if (tipoEntrega.checked) {


                if (valorVazio(endereco)) {

                    mostrarErro(
                        endereco,
                        "Informe o endereço."
                    );

                    formularioValido = false;

                }


                if (valorVazio(numeroEndereco)) {

                    mostrarErro(
                        numeroEndereco,
                        "Informe o número do endereço."
                    );

                    formularioValido = false;

                }


                if (valorVazio(bairro)) {

                    mostrarErro(
                        bairro,
                        "Informe o bairro."
                    );

                    formularioValido = false;

                }

            }


            // ==================================
            // PAGAMENTO
            // ==================================

            if (!verificarPagamento()) {

                alert(
                    "Selecione uma forma de pagamento."
                );

                formularioValido = false;

            }


            // ==================================
            // IMPEDIR ENVIO
            // ==================================

            if (!formularioValido) {

                event.preventDefault();


                const primeiroErro =
                    formulario.querySelector(
                        ".is-invalid"
                    );


                if (primeiroErro) {

                    primeiroErro.focus();

                    primeiroErro.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });

                }

            }

        }
    );

});