document.addEventListener("DOMContentLoaded", function () {


    const produto = document.getElementById("id_produto");

    const precoPromocional = document.getElementById("id_preco_promocional");

    const precoOriginal = document.getElementById("preco-original");

    const desconto = document.getElementById("desconto");

    const precoFinal = document.getElementById("preco-final");


    let valorOriginal = 0;



    function formatarMoeda(valor) {

        return Number(valor).toLocaleString("pt-BR", {

            style: "currency",

            currency: "BRL"

        });

    }



    function atualizarDesconto() {


        const promocional = parseFloat(
            precoPromocional.value
        );


        if (!valorOriginal || isNaN(promocional)) {


            desconto.innerHTML = "0%";


            if (precoFinal) {

                precoFinal.innerHTML = "R$ 0,00";

            }


            return;

        }



        const percentual = (
            (valorOriginal - promocional) /
            valorOriginal
        ) * 100;



        desconto.innerHTML =
            percentual.toFixed(1) + "%";



        if (precoFinal) {

            precoFinal.innerHTML =
                formatarMoeda(promocional);

        }


    }





    if (produto) {


        produto.addEventListener(
            "change",
            function () {



                if (!this.value) {


                    if (precoOriginal) {

                        precoOriginal.innerHTML =
                            "R$ 0,00";

                    }


                    if (desconto) {

                        desconto.innerHTML =
                            "0%";

                    }


                    if (precoFinal) {

                        precoFinal.innerHTML =
                            "R$ 0,00";

                    }


                    valorOriginal = 0;


                    return;


                }





                fetch(
                    `/cardapio/promocoes/produto/${this.value}/`
                )


                    .then(response => response.json())


                    .then(data => {


                        valorOriginal =
                            parseFloat(data.preco);



                        if (precoOriginal) {

                            precoOriginal.innerHTML =
                                formatarMoeda(valorOriginal);

                        }



                        atualizarDesconto();


                    });



            }
        );


    }




    if (precoPromocional) {

        precoPromocional.addEventListener(
            "input",
            atualizarDesconto
        );

    }



});







// BUSCA DE PRODUTO NO SELECT


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



                const texto =
                    campoBuscaProduto.value
                    .toLowerCase();



                selectProduto.innerHTML = "";



                let quantidade = 0;



                opcoesOriginais.forEach(
                    function(opcao) {



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



                // abre somente depois que terminou de digitar
                if (quantidade > 1) {


                    selectProduto.focus();

                    selectProduto.size =
                        quantidade;


                } else {


                    selectProduto.size =
                        1;


                }



            }, 600);



        }
    );





    selectProduto.addEventListener(
        "change",
        function () {


            selectProduto.size = 1;


        }
    );


}