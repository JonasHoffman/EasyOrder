document.addEventListener("DOMContentLoaded", function () {

    const cepInput = document.getElementById("id_cep");

    cepInput.addEventListener("input", async function () {

        const cep = this.value.replace(/\D/g, "");

        if (cep.length !== 8) return;

        try {

            const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
            const data = await response.json();

            if (data.erro) return;

            document.getElementById("id_logradouro").value = data.logradouro || "";
            document.getElementById("id_bairro").value = data.bairro || "";
            document.getElementById("id_cidade").value = data.localidade || "";
            document.getElementById("id_estado").value = data.uf || "";

            document.getElementById("id_numero").focus();

        } catch (e) {
            console.error(e);
        }

    });

});