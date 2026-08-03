document.addEventListener("DOMContentLoaded", function () {


    const selectProduto = document.getElementById("id_produto");

    const containerBotao = document.getElementById("botao-container");


    // Produto vindo pela URL /novo/id/
    const produtoSelecionado = window.produtoSelecionado;



    if (!containerBotao) {
        return;
    }



    function buscarInfoProduto(produtoId) {


        fetch(`/cardapio/buscar/produto-info/${produtoId}/`)

            .then(response => response.json())

            .then(data => {


                containerBotao.innerHTML = "";


                if (
                    data.permite_multiplos &&
                    data.maximo_sabores > 1
                ) {


                    criarBotaoAdicionar(
                        data.maximo_sabores
                    );


                }


            })

            .catch(error => {

                console.error(
                    "Erro ao buscar informações do produto:",
                    error
                );

            });


    }



    function criarBotaoAdicionar(maximo) {


        const botao = document.createElement("button");


        botao.type = "button";

        botao.id = "btn-add-sabor";

        botao.className =
            "btn btn-outline-primary btn-sm";


        botao.dataset.maximo = maximo;



        botao.innerHTML =
            '<i class="fa-solid fa-plus"></i> Adicionar sabor';



        containerBotao.appendChild(botao);



        iniciarAdicionarSabores(botao);


    }




    // Caso escolha pelo select

    if (selectProduto) {


        selectProduto.addEventListener(
            "change",
            function () {


                containerBotao.innerHTML = "";


                if (this.value) {

                    buscarInfoProduto(
                        this.value
                    );

                }


            }
        );


    }



    // Caso venha da criação do produto

    if (produtoSelecionado) {


        buscarInfoProduto(
            produtoSelecionado
        );


    }




});





function iniciarAdicionarSabores(botaoAdicionar) {


    const container =
        document.getElementById(
            "sabores-container"
        );


    if (!container) {
        return;
    }



    const maximo =
        Number(
            botaoAdicionar.dataset.maximo
        );




    function atualizarBotao() {


        const quantidade =
            container.querySelectorAll(
                ".sabor-item"
            ).length;



        if (quantidade >= maximo) {

            botaoAdicionar.style.display = "none";

        } else {

            botaoAdicionar.style.display = "";

        }


    }




    function atualizarRemover() {


        const itens =
            container.querySelectorAll(
                ".sabor-item"
            );



        itens.forEach((item, index) => {


            let btn =
                item.querySelector(
                    ".btn-remover-sabor"
                );



            if (index > 0 && !btn) {


                btn =
                    document.createElement(
                        "button"
                    );


                btn.type = "button";

                btn.className =
                    "btn btn-outline-danger btn-sm mt-2 btn-remover-sabor";


                btn.innerHTML =
                    '<i class="fa-solid fa-trash"></i> Remover';



                btn.addEventListener(
                    "click",
                    function () {


                        item.remove();


                        atualizarBotao();

                        atualizarRemover();


                    }
                );



                item.appendChild(btn);


            }



            if (btn) {

                btn.style.display =
                    index === 0
                        ? "none"
                        : "";

            }



        });


    }





    botaoAdicionar.addEventListener(
        "click",
        function () {



            const itens =
                container.querySelectorAll(
                    ".sabor-item"
                );



            if (itens.length >= maximo) {
                return;
            }



            const novo =
                itens[0].cloneNode(true);



            const numero =
                itens.length + 1;



            const label =
                novo.querySelector(
                    "label"
                );



            if (label) {

                label.textContent =
                    `${numero}º Sabor`;

            }



            const select =
                novo.querySelector(
                    "select"
                );



            if (select) {

                select.selectedIndex = 0;

            }



            container.appendChild(novo);



            atualizarBotao();

            atualizarRemover();



        }
    );



    atualizarBotao();

    atualizarRemover();


}