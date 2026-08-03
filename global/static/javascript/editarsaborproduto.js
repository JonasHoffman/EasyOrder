document.addEventListener("DOMContentLoaded", function () {


    const container =
        document.getElementById(
            "sabores-container"
        );


    const botaoContainer =
        document.getElementById(
            "botao-container"
        );


    const maximo =
        Number(
            window.maximoSabores
        );



    if (
        !container ||
        !botaoContainer ||
        !maximo
    ) {
        return;
    }



    function criarBotaoAdicionar() {


        botaoContainer.innerHTML = "";


        const botao =
            document.createElement(
                "button"
            );


        botao.type = "button";


        botao.className =
            "btn btn-outline-primary btn-sm";


        botao.innerHTML =
            '<i class="fa-solid fa-plus"></i> Adicionar sabor';



        botao.addEventListener(
            "click",
            adicionarSabor
        );


        botaoContainer.appendChild(
            botao
        );


    }





    function adicionarSabor() {


        const quantidade =
            container.querySelectorAll(
                ".sabor-item"
            ).length;



        if (quantidade >= maximo) {

            return;

        }



        const primeiro =
            container.querySelector(
                ".sabor-item"
            );



        const novo =
            primeiro.cloneNode(true);



        const select =
            novo.querySelector(
                "select"
            );


        if (select) {

            select.selectedIndex = 0;

        }



        const numero =
            quantidade + 1;



        const label =
            novo.querySelector(
                "label"
            );


        if (label) {

            label.textContent =
                `${numero}º Sabor`;

        }



        adicionarBotaoRemover(
            novo
        );


        container.appendChild(
            document.createElement("br")
        );
        container.appendChild(
            document.createElement("br")
        );

        container.appendChild(
            novo
        );


        atualizarTela();

    }





    function adicionarBotaoRemover(item) {


    let botao =
        item.querySelector(
            ".btn-remover-sabor"
        );


    if (botao) {
        return;
    }


    const divBotao =
        document.createElement(
            "div"
        );


    divBotao.className =
        "mt-3";


    botao =
        document.createElement(
            "button"
        );


    botao.type =
        "button";


    botao.className =
        "btn btn-outline-danger btn-sm btn-remover-sabor";


    botao.innerHTML =
        '<i class="fa-solid fa-trash"></i> Remover';



    botao.addEventListener(
        "click",
        function () {

            item.remove();

            atualizarTela();

        }
    );


    divBotao.appendChild(
        botao
    );


    item.appendChild(
        divBotao
    );

}





    function atualizarTela() {


        const itens =
            container.querySelectorAll(
                ".sabor-item"
            );



        itens.forEach(
            (item, index) => {


                const label =
                    item.querySelector(
                        "label"
                    );


                if (label) {

                    label.textContent =
                        `${index + 1}º Sabor`;

                }



                if (index > 0) {

                    adicionarBotaoRemover(
                        item
                    );

                }


            }
        );



        const botao =
            botaoContainer.querySelector(
                "button"
            );



        if (botao) {


            if (itens.length >= maximo) {

                botao.style.display =
                    "none";

            } else {

                botao.style.display =
                    "";

            }

        }


    }





    criarBotaoAdicionar();


    atualizarTela();


});