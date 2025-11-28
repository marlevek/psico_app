from django.db import models
from django.contrib.auth.models import User


class PlanoTratamento(models.Model):
    # Campos obrigatórios para o contexto do plano
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1
    )
    titulo = models.CharField(max_length=255)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    # Informações chave para a revisão da IA
    diagnostico_base = models.TextField(
        help_text="Hipótese ou diagnóstico (ex: F32.9 - Episódio depressivo não especificado)."
    )
    
    # O conteúdo principal do plano
    metas_longo_prazo = models.TextField(
        help_text="O que se espera alcançar no final do tratamento."
    )
    metas_curto_prazo = models.TextField(
        help_text="Metas para as próximas sessões, alinhadas à Terapia Cognitivo Comportamental (TCC), por exemplo."
    )
    tecnicas_abordagem = models.TextField(
        help_text="As principais técnicas e a abordagem teórica utilizada (ex: TCC, Psicanálise, Humanista)."
    )
    
    # O feedback da IA será salvo aqui
    feedback_ia = models.TextField(
        blank=True, 
        null=True, 
        help_text="O resumo ou a revisão fornecida pela Inteligência Artificial."
    )

    def __str__(self):
        return f"{self.titulo} ({self.data_criacao.strftime('%d/%m/%Y')})"
