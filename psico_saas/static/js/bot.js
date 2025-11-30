class HelpBot {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.hasShownWelcome = false;
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

            <div class="help-bot-modal" id="helpBotModal">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header help-bot-header">
                            <h5 class="modal-title">
                                <i class="bi bi-robot me-2"></i>Assistente Psico
                            </h5>
                            <button type="button" class="btn-close-custom" id="closeBotButton">
                                <i class="bi bi-x-lg"></i>
                            </button>
                        </div>
                        <div class="modal-body help-bot-body">
                            <div class="chat-messages" id="chatMessages"></div>
                            <div class="typing-indicator" id="typingIndicator">
                                <i class="bi bi-three-dots"></i> Assistente está digitando...
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
        this.closeBotButton = document.getElementById('closeBotButton');
        this.modalElement = document.getElementById('helpBotModal');
    }

    setupEventListeners() {
        // Abrir modal quando clicar no botão
        this.helpBotButton.addEventListener('click', () => {
            this.openModal();
        });

        // Fechar modal quando clicar no botão de fechar
        this.closeBotButton.addEventListener('click', () => {
            this.closeModal();
        });

        // Fechar modal quando clicar fora (no backdrop)
        this.modalElement.addEventListener('click', (e) => {
            if (e.target === this.modalElement) {
                this.closeModal();
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

        // Fechar modal com ESC
        document.addEventListener('keydown', (e) => {
            if (this.isOpen && e.key === 'Escape') {
                this.closeModal();
            }
        });
    }

    openModal() {
        this.modalElement.classList.add('show');
        this.isOpen = true;
        

        // Mostrar saudação apenas na primeira vez
        if (!this.hasShownWelcome && this.messages.length === 0) {
            setTimeout(() => {
                this.showWelcomeMessage();
                this.hasShownWelcome = true;
            }, 300);
        }

        this.chatInput.focus();
        this.scrollToBottom();
    }

    closeModal() {
        this.modalElement.classList.remove('show');
        this.isOpen = false;
       
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

        if (message.html) {
            messageElement.innerHTML = `
                <div class="message-content">
                    ${message.html}
                    <div class="message-time">${time}</div>
                </div>
            `;
        } else {
            messageElement.innerHTML = `
                <div class="message-content">
                    ${message.text.replace(/\n/g, '<br>')}
                    <div class="message-time">${time}</div>
                </div>
            `;
        }

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
        }, 1500 + Math.random() * 1000);
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
        let html = '';

        // Respostas baseadas em palavras-chave
        if (lowerMessage.includes('olá') || lowerMessage.includes('oi') || lowerMessage.includes('ola')) {
            response = "Olá! É um prazer ajudá-lo. Em que posso ser útil?";
        } else if (lowerMessage.includes('cadastrar') || lowerMessage.includes('novo') || lowerMessage.includes('criar')) {
            response = "Para cadastrar um novo paciente:\n\n1. Clique em 'Cadastrar Paciente' no menu superior\n2. Preencha os dados obrigatórios (nome, data de nascimento, telefone)\n3. Adicione outras informações se desejar\n4. Clique em 'Salvar' para finalizar";
        } else if (lowerMessage.includes('editar') || lowerMessage.includes('alterar') || lowerMessage.includes('modificar')) {
            response = "Para editar um paciente:\n\n1. Vá para a lista de pacientes\n2. Clique no ícone de lápis (✏️) ao lado do paciente\n3. Faça as alterações necessárias\n4. Clique em 'Salvar' para atualizar";
        } else if (lowerMessage.includes('excluir') || lowerMessage.includes('remover') || lowerMessage.includes('deletar')) {
            response = "Para excluir um paciente:\n\n1. Vá para a lista de pacientes\n2. Clique no ícone de lixeira (🗑️) ao lado do paciente\n3. Confirme a exclusão no modal\n\n⚠️ Atenção: Esta ação não pode ser desfeita!";
        } else if (lowerMessage.includes('buscar') || lowerMessage.includes('encontrar') || lowerMessage.includes('procurar')) {
            response = "Para buscar pacientes:\n\nUse a barra de busca na parte superior da lista de pacientes. Você pode buscar por:\n• Nome do paciente\n• Telefone\n• E-mail\n• Qualquer informação do cadastro";
        } else if (lowerMessage.includes('agenda') || lowerMessage.includes('sessão') || lowerMessage.includes('consulta')) {
            response = "Funcionalidade de agenda em breve!\n\nEstamos desenvolvendo um sistema completo de agendamento de sessões. Em breve você poderá:\n• Agendar consultas\n• Gerenciar horários\n• Receber lembretes\n• E muito mais!\n\nFique atento às atualizações!";
        } else if (lowerMessage.includes('problema') || lowerMessage.includes('erro') || lowerMessage.includes('bug')) {
            html = "Lamento ouvir que está com problemas. Entre em contato com nosso suporte:<br><br>📧 Email: <a href='mailto:suporte@psicoassist.codertec.com.br' style='color: var(--primary); text-decoration: none; border-bottom: 1px solid var(--primary);'>suporte@psicoassist.codertec.com.br</a><br>📱 WhatsApp: <a href='https://wa.me/5541996131762' target='_blank' style='color: var(--primary); text-decoration: none; border-bottom: 1px solid var(--primary);'>(41) 99613-1762</a><br><br>Nossa equipe terá prazer em ajudá-lo!";
        } else if (lowerMessage.includes('outras dúvidas') || lowerMessage.includes('outras duvidas') || lowerMessage.includes('mais ajuda')) {
            html = "Claro! Para outras dúvidas ou suporte técnico, entre em contato conosco:<br><br>📧 Email: <a href='mailto:suporte@psicoassist.codertec.com.br' style='color: var(--primary); text-decoration: none; border-bottom: 1px solid var(--primary);'>suporte@psicoassist.codertec.com.br</a><br>📱 WhatsApp: <a href='https://wa.me/5541996131762' target='_blank' style='color: var(--primary); text-decoration: none; border-bottom: 1px solid var(--primary);'>(41) 99613-1762</a><br>💻 Site: <a href='https://www.psicoassist.codertec.com.br' target='_blank' style='color: var(--primary); text-decoration: none; border-bottom: 1px solid var(--primary);'>www.psicoassist.codertec.com.br</a><br><br>Horário de atendimento:<br>Segunda a Sexta: 8h às 18h<br>Sábado: 8h às 12h";
        } else if (lowerMessage.includes('obrigado') || lowerMessage.includes('obrigada') || lowerMessage.includes('valeu')) {
            response = "De nada! Fico feliz em ajudar. 😊\n\nSe tiver mais alguma dúvida, é só perguntar!";
        } else {
            response = "Desculpe, não entendi completamente sua pergunta. 😅\n\nVocê pode:\n• Reformular sua pergunta\n• Usar uma das opções rápidas abaixo\n• Entrar em contato com nosso suporte:\n  📧 suporte@psicoassist.codertec.com.br\n  📱 (41) 99613-1762";
        }

        const botMessage = {
            text: response,
            html: html,
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
                question = 'Outras dúvidas';
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
        }, 1000);
    }

    scrollToBottom() {
        setTimeout(() => {
            if (this.chatMessages) {
                this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
            }
        }, 100);
    }
}

// Inicializar o bot quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    new HelpBot();
});