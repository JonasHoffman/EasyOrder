const lista = document.getElementById("lista-secoes");

Sortable.create(lista, {
    animation: 150
});


document
    .getElementById("btnSalvar")
    .addEventListener("click", function () {

        const formData = new FormData();

        const secoes = [];

        lista
            .querySelectorAll(".secao-item")
            .forEach(function (item, indice) {

                const id = item.dataset.id;

                const toggle = item.querySelector(".toggle-secao");

                secoes.push({
                    id: id,
                    ativo: toggle ? toggle.checked : false,
                    ordem: indice + 1
                });


                // Se for a seção de banner,
                // pega a imagem selecionada.
                if (item.dataset.tipo === "banner") {

                    const inputImagem = item.querySelector(
                        ".input-banner"
                    );

                    if (
                        inputImagem &&
                        inputImagem.files.length > 0
                    ) {

                        formData.append(
                            "banner_" + id,
                            inputImagem.files[0]
                        );

                    }

                }

            });


        formData.append(
            "secoes",
            JSON.stringify(secoes)
        );


        fetch(
            "/cardapio/estrutura_cardapio/salvar/",
            {
                method: "POST",

                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },

                body: formData
            }
        )

        .then(response => response.json())

        .then(data => {

            if (data.sucesso) {

                alert("Alterações salvas com sucesso.");

                window.location.reload();

            } else {

                alert(
                    data.mensagem ||
                    "Não foi possível salvar as alterações."
                );

            }

        })

        .catch(error => {

            console.error(error);

            alert(
                "Ocorreu um erro ao salvar as alterações."
            );

        });

    });


function getCookie(nome) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(nome + "=")) {

                cookieValue = decodeURIComponent(
                    cookie.substring(nome.length + 1)
                );

                break;

            }

        }

    }

    return cookieValue;
}