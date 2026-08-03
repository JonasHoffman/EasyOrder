document.addEventListener("DOMContentLoaded", function () {

    const campoBusca = document.getElementById("buscarIngrediente");

    if (!campoBusca) {
        return;
    }

    campoBusca.addEventListener("keyup", function () {

        const texto = this.value.toLowerCase();

        document.querySelectorAll(".ingrediente-item").forEach(function (item) {

            const nome = item.dataset.nome.toLowerCase();

            if (nome.includes(texto)) {

                item.style.display = "";

            } else {

                item.style.display = "none";

            }

        });

    });

});