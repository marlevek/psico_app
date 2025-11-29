// app.js - JavaScript global do Psico Assist

console.log('🌿 Psico Assist - Carregado com sucesso!');

// Funções utilitárias globais
const PsicoApp = {
    // Mostrar loading
    showLoading: function(element) {
        if (element) {
            element.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"></div><p class="mt-2">Carregando...</p></div>';
        }
    },
    
    // Formatar data
    formatDate: function(dateString) {
        const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
        return new Date(dateString).toLocaleDateString('pt-BR', options);
    },
    
    // Validar email
    isValidEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },
    
    // Busca em tempo real
    setupSearch: function(inputId, itemsSelector) {
        const searchInput = document.getElementById(inputId);
        if (searchInput) {
            searchInput.addEventListener('input', function(e) {
                const searchTerm = e.target.value.toLowerCase();
                const items = document.querySelectorAll(itemsSelector);
                
                items.forEach(item => {
                    const text = item.textContent.toLowerCase();
                    item.style.display = text.includes(searchTerm) ? '' : 'none';
                });
            });
        }
    },
    
    // Inicializar tooltips
    initTooltips: function() {
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(tooltip => {
            new bootstrap.Tooltip(tooltip);
        });
    },
    
    // Copiar para clipboard
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.showToast('Copiado para a área de transferência!');
        });
    },
    
    // Mostrar toast notification
    showToast: function(message, type = 'success') {
        // Implementação simples de toast
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <span>${message}</span>
                <button type="button" class="btn-close" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }
};

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    PsicoApp.initTooltips();
    console.log('🚀 Psico Assist inicializado');
});

// Exportar para uso global
window.PsicoApp = PsicoApp;