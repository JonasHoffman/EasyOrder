document.addEventListener("DOMContentLoaded", function () {


    /*
    ====================================
    ADICIONAR PRODUTO SIMPLES
    ====================================
    */

    document
    .querySelectorAll(".btn-adicionar-carrinho")
    .forEach(function (btn) {


        btn.addEventListener(
            "click",
            function () {


                const produtoId =
                this.dataset.produtoId;



                fetch(
                    `/cardapio/carrinho/adicionar/${produtoId}/`,
                    {

                        method: "POST",

                        headers: {

                            "X-CSRFToken":
                            getCookie("csrftoken"),

                            "Content-Type":
                            "application/x-www-form-urlencoded"

                        },


                        body:
                        "quantidade=1"

                    }
                )


                .then(
                    response => response.json()
                )


                .then(
                    data => {


                        if(data.sucesso){

                            atualizarWidgetCarrinho();

                        }


                    }
                );


            }
        );


    });



    /*
    ====================================
    ADICIONAR PRODUTO PERSONALIZADO
    ====================================
    */


    const formularioPersonalizar =
    document.getElementById(
        "form-personalizar"
    );


    if(formularioPersonalizar){


        formularioPersonalizar.addEventListener(
            "submit",
            function(e){


                e.preventDefault();



                const produtoId =
                this.dataset.produtoId;



                const dados =
                new FormData(this);



                fetch(
                    `/cardapio/carrinho/adicionar/${produtoId}/`,
                    {

                        method:"POST",

                        headers:{

                            "X-CSRFToken":
                            getCookie("csrftoken")

                        },


                        body:dados

                    }
                )


                .then(
                    response => response.json()
                )


                .then(
                    data => {


                        if(data.sucesso){


                            window.location.href =
                            "/cardapio/cardapio_cliente/";


                        }


                    }
                );


            }
        );


    }





    /*
    ====================================
    ATIVA BOTÕES REMOVER
    ====================================
    */


    ativarBotoesRemover();



});






/*
====================================
ATUALIZAR WIDGET CARRINHO
====================================
*/


function atualizarWidgetCarrinho(){


    fetch(
        "/cardapio/carrinho/widget/"
    )


    .then(
        response => response.json()
    )


    .then(
        data => {


            const itens =
            document.getElementById(
                "carrinho-itens"
            );


            if(itens){

                itens.innerHTML =
                data.html;

            }



            const total =
            document.getElementById(
                "carrinho-total-valor"
            );


            if(total){

                total.textContent =
                "R$ " +
                data.total_valor.replace(
                    ".",
                    ","
                );

            }



            const badge =
            document.getElementById(
                "carrinho-badge"
            );



            if(badge){


                badge.textContent =
                data.total_itens;



                if(data.total_itens > 0){

                    badge.style.display =
                    "inline-block";

                }else{

                    badge.style.display =
                    "none";

                }


            }



            ativarBotoesRemover();


        }
    );

}







/*
====================================
REMOVER ITEM DO CARRINHO
====================================
*/


function ativarBotoesRemover(){


    document
    .querySelectorAll(".btn-remover-carrinho")
    .forEach(function(btn){



        btn.addEventListener(
            "click",
            function(){



                const chave =
                this.dataset.chave;



                fetch(
                    "/cardapio/carrinho/remover/",
                    {


                        method:"POST",


                        headers:{


                            "X-CSRFToken":
                            getCookie(
                                "csrftoken"
                            ),


                            "Content-Type":
                            "application/x-www-form-urlencoded"


                        },


                        body:
                        `chave=${chave}`


                    }
                )


                .then(
                    response => response.json()
                )


                .then(
                    data => {


                        if(data.sucesso){


                            atualizarWidgetCarrinho();


                        }


                    }
                );



            }
        );



    });


}







/*
====================================
CSRF COOKIE
====================================
*/


function getCookie(name){


    let cookieValue = null;



    if(document.cookie &&
       document.cookie !== ""){


        document
        .cookie
        .split(";")
        .forEach(function(cookie){



            cookie =
            cookie.trim();



            if(
                cookie.startsWith(
                    name + "="
                )
            ){


                cookieValue =
                decodeURIComponent(
                    cookie.substring(
                        name.length + 1
                    )
                );


            }



        });



    }



    return cookieValue;


}