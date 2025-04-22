// Função para formatar números como moeda
function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

// Função para formatar números com separador de milhares
function formatarNumero(valor) {
    return new Intl.NumberFormat('pt-BR').format(valor);
}

// Função para adicionar classe de hover nas linhas da tabela
function adicionarHoverTabela() {
    const linhas = document.querySelectorAll('table tbody tr');
    linhas.forEach(linha => {
        linha.addEventListener('mouseover', function() {
            this.style.backgroundColor = '#f1f1f1';
        });
        linha.addEventListener('mouseout', function() {
            this.style.backgroundColor = '';
        });
    });
}

// Função para formatar valores monetários na tabela
function formatarValoresMonetarios() {
    const celulas = document.querySelectorAll('table td');
    celulas.forEach(celula => {
        const texto = celula.textContent.trim();
        // Verifica se o texto é um número com até 2 casas decimais
        if (/^\d+(\.\d{1,2})?$/.test(texto)) {
            const valor = parseFloat(texto);
            if (!isNaN(valor)) {
                celula.textContent = formatarMoeda(valor);
            }
        }
    });
}

// Função para adicionar indicador de carregamento ao botão
function adicionarIndicadorCarregamento() {
    const botoes = document.querySelectorAll('button[type="submit"]');
    botoes.forEach(botao => {
        botao.addEventListener('click', function() {
            this.disabled = true;
            this.textContent = 'Carregando...';
        });
    });
}

// Inicializar funções quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Formatação de números
    const formatCurrency = (value) => {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    };

    const formatNumber = (value) => {
        return new Intl.NumberFormat('pt-BR').format(value);
    };

    // Aplicar formatação aos elementos com classes específicas
    document.querySelectorAll('.currency').forEach(element => {
        const value = parseFloat(element.textContent);
        if (!isNaN(value)) {
            element.textContent = formatCurrency(value);
        }
    });

    document.querySelectorAll('.number').forEach(element => {
        const value = parseFloat(element.textContent);
        if (!isNaN(value)) {
            element.textContent = formatNumber(value);
        }
    });

    // Implementação da paginação
    const table = document.getElementById('dadosTable');
    if (table) {
        const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
        const rowsPerPage = 10;
        const pageCount = Math.ceil(rows.length / rowsPerPage);
        let currentPage = 1;

        // Função para mostrar/esconder linhas
        function showPage(page) {
            const start = (page - 1) * rowsPerPage;
            const end = start + rowsPerPage;

            for (let i = 0; i < rows.length; i++) {
                rows[i].style.display = (i >= start && i < end) ? '' : 'none';
            }

            // Atualizar contadores
            document.getElementById('showing-entries-start').textContent = start + 1;
            document.getElementById('showing-entries-end').textContent = Math.min(end, rows.length);
            document.getElementById('total-entries').textContent = rows.length;

            // Atualizar estado dos botões
            document.getElementById('prev-page').classList.toggle('disabled', page === 1);
            document.getElementById('next-page').classList.toggle('disabled', page === pageCount);

            // Atualizar números das páginas
            const pagination = document.querySelector('.pagination');
            pagination.innerHTML = `
                <li class="page-item ${page === 1 ? 'disabled' : ''}" id="prev-page">
                    <a class="page-link" href="#" tabindex="-1" aria-disabled="true">Anterior</a>
                </li>
            `;

            // Adicionar números das páginas
            for (let i = 1; i <= pageCount; i++) {
                if (
                    i === 1 || 
                    i === pageCount || 
                    (i >= page - 1 && i <= page + 1)
                ) {
                    pagination.innerHTML += `
                        <li class="page-item ${i === page ? 'active' : ''}">
                            <a class="page-link" href="#">${i}</a>
                        </li>
                    `;
                } else if (
                    i === page - 2 || 
                    i === page + 2
                ) {
                    pagination.innerHTML += `
                        <li class="page-item disabled">
                            <a class="page-link" href="#">...</a>
                        </li>
                    `;
                }
            }

            pagination.innerHTML += `
                <li class="page-item ${page === pageCount ? 'disabled' : ''}" id="next-page">
                    <a class="page-link" href="#">Próximo</a>
                </li>
            `;

            // Adicionar event listeners aos novos botões
            addPaginationEventListeners();
        }

        // Função para adicionar event listeners à paginação
        function addPaginationEventListeners() {
            document.querySelectorAll('.pagination .page-link').forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const pageText = this.textContent;
                    
                    if (pageText === 'Anterior') {
                        if (currentPage > 1) currentPage--;
                    } else if (pageText === 'Próximo') {
                        if (currentPage < pageCount) currentPage++;
                    } else if (pageText !== '...') {
                        currentPage = parseInt(pageText);
                    }
                    
                    showPage(currentPage);
                });
            });
        }

        // Inicializar a primeira página
        showPage(1);
    }

    // Adicionar tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Adicionar confirmação antes de carregar dados
    const loadDataButton = document.querySelector('.btn-carregar');
    if (loadDataButton) {
        loadDataButton.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja carregar os dados históricos? Isso pode levar alguns minutos.')) {
                e.preventDefault();
            }
        });
    }

    // Adicionar animação de loading
    const showLoading = () => {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'loading-overlay';
        loadingDiv.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
        `;
        document.body.appendChild(loadingDiv);
    };

    const hideLoading = () => {
        const loadingDiv = document.querySelector('.loading-overlay');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    };

    // Adicionar estilos para o loading
    const style = document.createElement('style');
    style.textContent = `
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
    `;
    document.head.appendChild(style);

    // Mostrar loading ao carregar dados
    if (loadDataButton) {
        loadDataButton.addEventListener('click', showLoading);
    }
}); 