// forms.js - Validações e interações de formulários

const FormValidator = {
    // Validar formulário de plano
    validatePlanoForm: function(form) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                this.markFieldInvalid(field, 'Este campo é obrigatório.');
                isValid = false;
            } else {
                this.markFieldValid(field);
            }
        });
        
        // Validação específica da data
        const dataField = form.querySelector('#data_inicio_prevista');
        if (dataField && dataField.value) {
            const selectedDate = new Date(dataField.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (selectedDate < today) {
                this.markFieldInvalid(dataField, 'A data não pode ser no passado.');
                isValid = false;
            }
        }
        
        return isValid;
    },
    
    // Marcar campo como inválido
    markFieldInvalid: function(field, message) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        
        // Remover feedback anterior
        const existingFeedback = field.parentNode.querySelector('.invalid-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }
        
        // Adicionar novo feedback
        const feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        feedback.textContent = message;
        field.parentNode.appendChild(feedback);
    },
    
    // Marcar campo como válido
    markFieldValid: function(field) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        
        // Remover feedback de erro
        const existingFeedback = field.parentNode.querySelector('.invalid-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }
    },
    
    // Limpar validações
    clearValidations: function(form) {
        const fields = form.querySelectorAll('.is-invalid, .is-valid');
        fields.forEach(field => {
            field.classList.remove('is-invalid', 'is-valid');
        });
        
        const feedbacks = form.querySelectorAll('.invalid-feedback');
        feedbacks.forEach(feedback => feedback.remove());
    },
    
    // Inicializar validação em tempo real
    initRealTimeValidation: function(form) {
        const fields = form.querySelectorAll('[required]');
        
        fields.forEach(field => {
            field.addEventListener('blur', function() {
                if (!this.value.trim()) {
                    FormValidator.markFieldInvalid(this, 'Este campo é obrigatório.');
                } else {
                    FormValidator.markFieldValid(this);
                }
            });
        });
    }
};

// Inicializar forms quando o DOM carregar
document.addEventListener('DOMContentLoaded', function() {
    // Configurar validação em tempo real para todos os forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        FormValidator.initRealTimeValidation(form);
        
        // Validar no submit
        form.addEventListener('submit', function(e) {
            if (!FormValidator.validatePlanoForm(this)) {
                e.preventDefault();
                PsicoApp.showToast('Por favor, corrija os erros no formulário.', 'error');
            }
        });
    });
});

window.FormValidator = FormValidator;