document.addEventListener("DOMContentLoaded", () => {


    document.querySelectorAll(".categorias-container").forEach(container => {


        const scroll = container.querySelector(".categorias-scroll");
        const track = container.querySelector(".categorias-track");

        const next = container.querySelector(".categorias-btn.next");
        const prev = container.querySelector(".categorias-btn.prev");


        if (!track) return;



        let posicao = 0;

        let automatico = true;

        let velocidade = 0.5;



        function moverAutomatico(){


            if(automatico){


                posicao -= velocidade;


                const limite = track.offsetWidth / 2;


                if(Math.abs(posicao) >= limite){

                    posicao = 0;

                }


                track.style.transform =
                    `translateX(${posicao}px)`;

            }


            requestAnimationFrame(moverAutomatico);

        }



        moverAutomatico();




        // =========================
        // SETAS
        // =========================


        next?.addEventListener("click", () => {


            automatico = false;


            posicao -= 250;


            track.style.transform =
                `translateX(${posicao}px)`;


        });



        prev?.addEventListener("click", () => {


            automatico = false;


            posicao += 250;


            track.style.transform =
                `translateX(${posicao}px)`;


        });






        // =========================
        // CLIQUE NO CARROSSEL
        // =========================


        scroll.addEventListener("mousedown", () => {


            automatico = false;


        });






        // =========================
        // RODA DO MOUSE
        // =========================


        window.addEventListener("wheel", (e) => {


            // usuário está rolando a página

            if(Math.abs(e.deltaY) > 0){


                automatico = true;


            }


        });






        // =========================
        // TOUCH CELULAR
        // =========================


        let inicioY = 0;



        scroll.addEventListener("touchstart", (e) => {


            inicioY = e.touches[0].clientY;


        });




        scroll.addEventListener("touchmove", (e) => {


            const atualY = e.touches[0].clientY;


            const diferenca = Math.abs(atualY - inicioY);



            if(diferenca > 10){


                automatico = true;


            }


        });



    });


});