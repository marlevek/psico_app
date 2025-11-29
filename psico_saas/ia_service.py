# psico_saas/ia_services.py

from openai import OpenAI
from django.conf import settings

# Inicializa o cliente da OpenAI
# Assume que OPENAI_API_KEY está definido em settings.py ou no .env

def generate_task_exercise(abordagem_teorica, tema_principal, detalhes_personalizacao=None):
    """
    Gera um exercício de casa personalizado usando a API Chat Completions.
    """
    
    # 0. Inicialização do Cliente da OpenAI (Tratamento de erro de chave)
    try:
        # Tenta inicializar o cliente
        client = OpenAI(api_key=settings.OPENAI_API_KEY) 
    except AttributeError:
        # Se a chave não estiver configurada no settings.py, retorna imediatamente
        return "Erro de Configuração: A chave OPENAI_API_KEY não foi encontrada nas configurações do Django."

    # 1. Monta o Prompt (Instrução para a IA)
    prompt = f"""
    Você é um assistente de psicólogo especializado em criação de tarefas de casa e exercícios práticos.
    Gere um exercício ou tarefa de casa detalhada e prática para um paciente.
    
    Abordagem Teórica Principal: {abordagem_teorica}
    Tema Principal da Sessão/Tarefa: {tema_principal}
    
    Requisitos Adicionais para Personalização (Detalhes do Paciente):
    {detalhes_personalizacao if detalhes_personalizacao else 'Nenhum detalhe adicional fornecido.'}
    
    A resposta deve ser estruturada em tópicos, contendo:
    1. Título criativo do exercício.
    2. Objetivo (O que o paciente deve aprender).
    3. Instruções passo a passo.
    4. Perguntas de Reflexão (Para a próxima sessão).
    """

    # 2. Chamada à API (Try/Except específico para erros de API, como limites de taxa ou chave inválida)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "Você é um assistente de psicólogo que cria tarefas de casa."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7, 
            max_tokens=800
        )

        # 3. Retorna o conteúdo da resposta
        return response.choices[0].message.content
    
    except Exception as e:
        # Captura erros de rede, limites, ou falha geral da API
        return f"Erro na API: {str(e)}"
# --------------------------------------------------------------------------------------
# Opcional: Função de Revisão do Plano de Tratamento (Será usada mais tarde)
def generate_plano_review(plano_data):
    """
    Gera um feedback de revisão para o Plano de Tratamento.
    """
    
    # ⬅️ PASSO 0: Inicialização do Cliente da OpenAI (Corrigido)
    try:
        # Tenta inicializar o cliente DENTRO da função
        client = OpenAI(api_key=settings.OPENAI_API_KEY) 
    except AttributeError:
        # Se a chave não estiver configurada no settings.py, retorna imediatamente
        return "Erro de Configuração: A chave OPENAI_API_KEY não foi encontrada nas configurações do Django."


    # 1. Monta o Prompt
    prompt = f"Revise e comente o Plano de Tratamento com o Título: {plano_data.get('titulo', 'N/D')}. Diagnóstico: {plano_data.get('diagnostico_base', 'N/D')}. Metas: {plano_data.get('metas_tratamento', 'N/D')}. Abordagem: {plano_data.get('abordagem', 'N/D')}."

    # 2. Chamada à API (Agora o 'client' está definido)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um revisor de planos de tratamento, focando em consistência e clareza."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro na API durante a revisão do plano: {str(e)}"