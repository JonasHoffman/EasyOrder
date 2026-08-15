document.addEventListener("DOMContentLoaded", function () {

});


const campoBuscaProduto = document.getElementById(
    "buscar-produto"
);


const selectProduto = document.getElementById(
    "id_produto"
);



if (campoBuscaProduto && selectProduto) {


    const opcoesOriginais = Array.from(
        selectProduto.options
    );


    let tempoBusca;



    campoBuscaProduto.addEventListener(
        "input",
        function () {


            clearTimeout(tempoBusca);



            tempoBusca = setTimeout(function () {


                const texto = campoBuscaProduto.value
                    .toLowerCase();



                selectProduto.innerHTML = "";


                let quantidade = 0;



                opcoesOriginais.forEach(
                    function (opcao) {


                        if (
                            opcao.text
                            .toLowerCase()
                            .includes(texto)
                        ) {


                            selectProduto.appendChild(
                                opcao.cloneNode(true)
                            );


                            quantidade++;

                        }


                    }
                );



                // Só abre depois que terminou de digitar
                if (quantidade > 1) {

                    selectProduto.focus();

                    selectProduto.size = quantidade;

                } else {

                    selectProduto.size = 1;

                }



            }, 600); // aguarda 600ms sem digitar


        }
    );



    selectProduto.addEventListener(
        "change",
        function () {

            selectProduto.size = 1;

        }
    );


}