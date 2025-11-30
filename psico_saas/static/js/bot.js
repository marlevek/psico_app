class HelpBot {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.initializeBot();
        this.setupEventListeners();
    }

    initializeBot() {
        // Criar elemento do bot
        this.botElement = document.createElement('div');
        this.botElement.className = 'help-bot';
        this.botElement.innerHTML = `
            <button class="help-bot-btn" type="button" id="helpBotButton">
                <i class="bi bi-question-lg"></i>
            </button>

            <div class="modal fade help-bot-modal" id="helpBotModal" tabindex="-1" aria-hidden="true" data-bs-backdrop="false">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header help-bot-header">
                            <h5 class="modal-title">
                                <i class="bi bi-robot me-2"></i>Assistente Psico
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body help-bot-body">
                            <div class="chat-messages" id="chatMessages"></div>
                            <div class="typing-indicator" id="typingIndicator">
                                <i class="bi bi-three-dots"></i> Digitando...
                            </div>
                            <div class="chat-input-container">
                                <div class="quick-actions" id="quickActions">
                                    <button class="quick-action-btn" data-action="cadastrar">Como cadastrar paciente?</button>
                                    <button class="quick-action-btn" data-action="editar">Como editar informações?</button>
                                    <button class="quick-action-btn" data-action="agenda">Sobre a agenda</button>
                                    <button class="quick-action-btn" data-action="duvidas">Outras dúvidas</button>
                                </div>
                                <div class="chat-input-group">
                                    <input type="text" class="chat-input" id="chatInput" placeholder="Digite sua mensagem..." maxlength="500">
                                    <button class="send-btn" id="sendButton">
                                        <i class="bi bi-send"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(this.botElement);
        
        // Elementos DOM
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInput');
        this.sendButton = document.getElementById('sendButton');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.quickActions = document.getElementById('quickActions');
        this.helpBotButton = document.getElementById('helpBotButton');
        this.modalElement = document.getElementById('helpBotModal');
        this.modal = new bootstrap.Modal(this.modalElement);
    }

    setupEventListeners() {
        // Abrir modal quando clicar no botão
        this.helpBotButton.addEventListener('click', () => {
            this.modal.show();
            if (this.messages.length === 0) {
                this.showWelcomeMessage();
            }
        });

        // Enviar mensagem com Enter
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Enviar mensagem com botão
        this.sendButton.addEventListener('click', () => {
            this.sendMessage();
        });

        // Ações rápidas
        this.quickActions.addEventListener('click', (e) => {
            if (e.target.classList.contains('quick-action-btn')) {
                const action = e.target.getAttribute('data-action');
                this.handleQuickAction(action);
            }
        });

        // Quando o modal abre
        this.modalElement.addEventListener('shown.bs.modal', () => {
            this.isOpen = true;
            this.chatInput.focus();
            this.scrollToBottom();
        });

        // Quando o modal fecha
        this.modalElement.addEventListener('hidden.bs.modal', () => {
            this.isOpen = false;
        });
    }

    showWelcomeMessage() {
        const welcomeMessage = {
            text: "Olá! Sou o assistente virtual do Psico Assist. Como posso ajudá-lo hoje?",
            type: "bot",
            time: new Date()
        };
        this.addMessage(welcomeMessage);
    }

    addMessage(message) {
        this.messages.push(message);
        this.renderMessage(message);
        this.scrollToBottom();
    }

    renderMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${message.type}`;
        
        const time = message.time.toLocaleTimeString('pt-BR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });

        messageElement.innerHTML = `
            <div class="message-content">
                ${message.text}
                <div class="message-time">${time}</div>
            </div>
        `;

        this.chatMessages.appendChild(messageElement);
    }

    sendMessage() {
        const text = this.chatInput.value.trim();
        if (!text) return;

        // Adiciona mensagem do usuário
        const userMessage = {
            text: text,
            type: "user",
            time: new Date()
        };
        this.addMessage(userMessage);

        // Limpa input
        this.chatInput.value = '';

        // Simula resposta do bot
        this.showTypingIndicator();
        setTimeout(() => {
            this.hideTypingIndicator();
            this.generateBotResponse(text);
        }, 1000 + Math.random() * 1000);
    }

    showTypingIndicator() {
        this.typingIndicator.classList.add('show');
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.typingIndicator.classList.remove('show');
    }

    generateBotResponse(userMessage) {
        const lowerMessage = userMessage.toLowerCase();
        let response = '';

        // Respostas baseadas em palavras-chave
        if (lowerMessage.includes('olá') || lowerMessage.includes('oi') || lowerMessage.includes('ola')) {
            response = "Olá! É um prazer ajudá-lo. Em que posso ser útil?";
        } else if (lowerMessage.includes('cadastrar') || lowerMessage.includes('novo') || lowerMessage.includes('criar')) {
            response = "Para cadastrar um novo paciente, clique em 'Novo Paciente' na página de lista de pacientes. Preencha os dados obrigatórios como nome, data de nascimento e telefone, então salve.";
        } else if (lowerMessage.includes('editar') || lowerMessage.includes('alterar') || lowerMessage.includes('modificar')) {
            response = "Para editar um paciente, clique no ícone de lápis (✏️) ao lado do paciente na lista. Faça as alterações necessárias e salve.";
        } else if (lowerMessage.includes('excluir') || lowerMessage.includes('remover') || lowerMessage.includes('deletar')) {
            response = "Para excluir um paciente, clique no ícone de lixeira (🗑️) ao lado do paciente. Confirme a exclusão no modal que aparecer. ⚠️ Esta ação não pode ser desfeita.";
        } else if (lowerMessage.includes('buscar') || lowerMessage.includes('encontrar') || lowerMessage.includes('procurar')) {
            response = "Use a barra de busca na parte superior da lista de pacientes para encontrar pacientes por nome, telefone ou e-mail.";
        } else if (lowerMessage.includes('agenda') || lowerMessage.includes('sessão') || lowerMessage.includes('consulta')) {
            response = "Em breve teremos a funcionalidade de agenda para agendar sessões com seus pacientes. Fique atento às atualizações!";
        } else if (lowerMessage.includes('problema') || lowerMessage.includes('erro') || lowerMessage.includes('bug')) {
            response = "Se estiver enfrentando problemas técnicos, entre em contato com nosso suporte: suporte@psicoassist.com";
        } else if (lowerMessage.includes('obrigado') || lowerMessage.includes('obrigada') || lowerMessage.includes('valeu')) {
            response = "De nada! Estou aqui para ajudar. Se tiver mais alguma dúvida, é só perguntar! 😊";
        } else {
            response = "Desculpe, não entendi completamente. Você pode reformular sua pergunta ou usar uma das opções rápidas abaixo?";
        }

        const botMessage = {
            text: response,
            type: "bot",
            time: new Date()
        };
        this.addMessage(botMessage);
    }

    handleQuickAction(action) {
        let question = '';
        
        switch(action) {
            case 'cadastrar':
                question = 'Como cadastrar um novo paciente?';
                break;
            case 'editar':
                question = 'Como editar informações de um paciente?';
                break;
            case 'agenda':
                question = 'Como funciona a agenda de sessões?';
                break;
            case 'duvidas':
                question = 'Preciso de ajuda com outras funcionalidades';
                break;
        }

        // Adiciona a pergunta como se fosse do usuário
        const userMessage = {
            text: question,
            type: "user",
            time: new Date()
        };
        this.addMessage(userMessage);

        // Gera resposta
        this.showTypingIndicator();
        setTimeout(() => {
            this.hideTypingIndicator();
            this.generateBotResponse(question);
        }, 800);
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }
}

// Inicializar o bot quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    new HelpBot();
});