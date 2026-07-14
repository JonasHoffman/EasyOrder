document.addEventListener("DOMContentLoaded", function () {

    const produto = document.getElementById("id_produto");

    const precoPromocional = document.getElementById("id_preco_promocional");

    const precoOriginal = document.getElementById("preco-original");

    const desconto = document.getElementById("desconto");

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

            return;

        }

        const percentual = ((valorOriginal - promocional) / valorOriginal) * 100;

        desconto.innerHTML = percentual.toFixed(1) + "%";

    }


    produto.addEventListener("change", function () {

        if (!this.value) {

            precoOriginal.innerHTML = "R$ 0,00";

            desconto.innerHTML = "0%";

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