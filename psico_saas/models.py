from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import date
from django.utils import timezone


User = get_user_model()


class Paciente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField(blank=True, null=True)
    contato_emergencia = models.CharField(
        max_length=100, blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_completo

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        unique_together = ('usuario', 'nome_completo')

    def get_idade(self):
        """Calcula a idade do paciente com base na data de nascimento."""
        if self.data_nascimento:
            today = date.today()
            # Calcula a diferença de anos e subtrai 1 se o aniversário ainda não ocorreu este ano
            idade = today.year - self.data_nascimento.year - \
                ((today.month, today.day) <
                 (self.data_nascimento.month, self.data_nascimento.day))
            return idade
        return "N/D"  # Não Disponível


class PlanoTratamento(models.Model):
    # Campos obrigatórios para o contexto do plano
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # Se você ainda precisa do default=1 para migração:
        # default=1
    )
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='planos',
        # Removendo blank=True, null=True, pois o Paciente deve ser obrigatório agora.
        # Se você ainda precisa disso por conta de migração, mantenha.
    )
    data_inicio_prevista = models.DateField(
        verbose_name='Data de Início Prevista', default=timezone.now)
    titulo = models.CharField(max_length=255)
    data_criacao = models.DateTimeField(auto_now_add=True)

    # Informações chave para a revisão da IA
    diagnostico_base = models.TextField(
        help_text="Hipótese ou diagnóstico (ex: F32.9 - Episódio depressivo não especificado)."
    )

    # ⬅️ NOVO CAMPO UNIFICADO
    metas_tratamento = models.TextField(
        help_text="Metas a Longo e Curto Prazo (unificadas)."
    )

    # ⬅️ NOVO CAMPO PARA ABORDAGEM TEÓRICA
    abordagem = models.TextField(
        help_text="A abordagem teórica utilizada (ex: TCC, Psicanálise, Humanista)."
    )

    # ⬅️ NOVO CAMPO PARA FREQUÊNCIA (Adicionado no template)
    frequencia_sessoes = models.CharField(
        max_length=100,
        help_text="Ex: Semanalmente, Quinzenalmente."
    )

    # O feedback da IA será salvo aqui
    feedback_ia = models.TextField(
        blank=True,
        null=True,
        help_text="O resumo ou a revisão fornecida pela Inteligência Artificial."
    )

    def __str__(self):
        return f"Plano p/ {self.paciente.nome_completo} ({self.data_inicio_prevista.strftime('%d/%m/%Y')})"

    class Meta:
        # Se você tinha uma classe Meta aqui, mantenha-a.
        pass


class DocumentacaoSessao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name='documentacoes', blank=True, null=True)
    data_sessao = models.DateField()
    anotacoes_brutas = models.TextField()  # Entrada do usuário (notas/transcrição)

    # Saídas da IA
    resumo_ia = models.TextField(blank=True, null=True)
    sugestao_diagnostico = models.CharField(
        max_length=255, blank=True, null=True)  # CID/DSM
    padroes_linguagem = models.TextField(blank=True, null=True)

    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sessão de {self.data_sessao} por {self.usuario.username}"

    class Meta:
        verbose_name = "Documentação da Sessão"
        verbose_name_plural = "Documentações das Sessões"


class TarefaExercicios(models.Model):
    ABORDAGENS = [
        ('TCC', 'Terapia Cognitivo-Comportamental (TCC)'),
        ('PSICANALISE', 'Psicanálise'),
        ('HUMANISTA', 'Abordagem Humanista/Centrada na Pessoa'),
        ('OUTRA', 'Outra Abordagem'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name='tarefas', blank=True, null=True)

    # Entradas do Usuário
    abordagem_teorica = models.CharField(max_length=50, choices=ABORDAGENS)
    tema_principal = models.CharField(max_length=255)
    # Ex: "Paciente tem 16 anos e gosta de música"
    detalhes_personalizacao = models.TextField(blank=True, null=True)

    # Saída da IA
    exercicio_ia = models.TextField(blank=True, null=True)

    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exercício de {self.paciente.nome_completo} sobre '{self.tema_principal}' ({self.abordagem_teorica})"

    class Meta:
        verbose_name = "Tarefa/Exercício"
        verbose_name_plural = "Tarefas/Exercícios"


class ConteudoEducacional(models.Model):
    TIPOS_CONTEUDO = [
        ('POST_REDES_SOCIAIS', 'Post para Redes Sociais'),
        ('TEXTO_CONSULTORIO', 'Texto para Consultório'),
        ('ARTIGO_BLOG', 'Artigo para Blog'),
        ('MATERIAL_PACIENTE', 'Material para Paciente'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    tipo_conteudo = models.CharField(max_length=50, choices=TIPOS_CONTEUDO)
    tema_principal = models.CharField(max_length=255)
    publico_alvo = models.CharField(max_length=100, blank=True, null=True)
    tom_voz = models.CharField(max_length=100, default='Profissional e acolhedor')
    palavras_chave = models.TextField(blank=True, null=True)
    
    # Saída da IA
    conteudo_gerado = models.TextField(blank=True, null=True)
    sugestoes_titulos = models.TextField(blank=True, null=True)
    hashtags = models.TextField(blank=True, null=True)
    sugestoes_imagens = models.TextField(blank=True, null=True)  # NOVO CAMPO
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_conteudo_display()})"