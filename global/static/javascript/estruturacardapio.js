const lista = document.getElementById("lista-secoes");

Sortable.create(lista, {

    animation: 150

});

document
.getElementById("btnSalvar")
.addEventListener("click", function () {

    let dados = [];

    lista
    .querySelectorAll("li")
    .forEach(function (item) {

        dados.push({

            id: item.dataset.id,

            ativo: item.querySelector("input").checked

        });

    });

    fetch("/cardapio/estrutura_cardapio/salvar/", {

        method: "POST",

        headers: {

            "Content-Type": "application/json",

            "X-CSRFToken": getCookie("csrftoken")

        },

        body: JSON.stringify(dados)

    })

    .then(response => response.json())

    .then(data => {

        if(data.sucesso){

            alert("Salvo com sucesso.");

        }

    });

});


function getCookie(nome){

    let cookieValue = null;

    if(document.cookie && document.cookie !== ""){

        const cookies = document.cookie.split(";");

        for(let cookie of cookies){

            cookie = cookie.trim();

            if(cookie.startsWith(nome + "=")){

                cookieValue = decodeURIComponent(cookie.substring(nome.length + 1));

                break;

            }

        }

    }

    return cookieValue;

}

