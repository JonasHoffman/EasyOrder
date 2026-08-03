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


        const promocional = parseFloat(precoPromocional.value);


        if (!valorOriginal || isNaN(promocional)) {


            desconto.innerHTML = "0%";


            if (precoFinal) {

                precoFinal.innerHTML = "R$ 0,00";

            }


            return;

        }



        const percentual = ((valorOriginal - promocional) / valorOriginal) * 100;



        desconto.innerHTML = percentual.toFixed(1) + "%";



        if (precoFinal) {

            precoFinal.innerHTML = formatarMoeda(promocional);

        }


    }




    produto.addEventListener("change", function () {


        if (!this.value) {


            precoOriginal.innerHTML = "R$ 0,00";

            desconto.innerHTML = "0%";

            if (precoFinal) {

                precoFinal.innerHTML = "R$ 0,00";

            }


            valorOriginal = 0;


            return;


        }



        fetch(`/cardapio/promocoes/produto/${this.value}/`)


            .then(response => response.json())


            .then(data => {


                valorOriginal = parseFloat(data.preco);



                precoOriginal.innerHTML = formatarMoeda(valorOriginal);



                atualizarDesconto();


            });


    });




    precoPromocional.addEventListener("input", atualizarDesconto);



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



    campoBuscaProduto.addEventListener(
        "input",
        function(){


            const texto = this.value
                .toLowerCase();



            selectProduto.innerHTML = "";



            opcoesOriginais.forEach(
                function(opcao){


                    if (
                        opcao.text
                        .toLowerCase()
                        .includes(texto)
                    ){

                        selectProduto.appendChild(
                            opcao.cloneNode(true)
                        );

                    }


                }
            );


        }
    );


}