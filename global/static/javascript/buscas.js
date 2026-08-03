document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('searchInput');
    const box = document.getElementById('suggestionsBox');
    let timeoutId;

    input.addEventListener('input', function () {
        clearTimeout(timeoutId);
        const termo = this.value.trim();

        if (termo.length < 2) {
            box.innerHTML = '';
            box.style.display = 'none';
            console.log(termo)
            return;
        }

        // debounce: espera 300ms sem digitar antes de buscar
        timeoutId = setTimeout(() => {
            fetch(`/cardapio/buscar/?q=${encodeURIComponent(termo)}`)
                
                .then(res => res.json())
                .then(data => renderSugestoes(data.resultados))
                .catch(err => console.error('Erro na busca:', err));
        }, 300);
        
    });

    function renderSugestoes(resultados) {
        if (resultados.length === 0) {
            box.innerHTML = '<div class="sugestao-vazia">Nenhum resultado encontrado</div>';
            box.style.display = 'block';
            return;
        }

        box.innerHTML = resultados.map(item => {
            if (item.tipo === 'categoria') {
                return `
                    <a href="${item.url}" class="sugestao-item sugestao-categoria">
                        <i class="fa fa-tag"></i> ${item.nome}
                        <span class="sugestao-tipo">Categoria</span>
                    </a>
                `;
            } else {
                return `
                    <a href="${item.url}" class="sugestao-item sugestao-produto">
                        ${item.imagem ? `<img src="${item.imagem}" class="sugestao-img">` : ''}
                        <div class="sugestao-info">
                            <span class="sugestao-nome">${item.nome}</span>
                            <span class="sugestao-categoria">${item.categoria}</span>
                        </div>
                        <span class="sugestao-preco">R$ ${item.preco}</span>
                    </a>
                `;
            }
        }).join('');

        box.style.display = 'block';
    }

    // fecha a caixa de sugestões ao clicar fora
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.search-wrapper')) {
            box.style.display = 'none';
        }
    });
});