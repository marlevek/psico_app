# psico_saas/ia_service.py

import os
import openai

# Use um modelo de chat. gpt-3.5-turbo é mais rápido e barato.
MODEL_NAME = "gpt-3.5-turbo" 

def revisar_plano_tratamento(plano_data: dict) -> str:
    """
    Chama a API da OpenAI para revisar a coerência de um plano de tratamento.
    """
    
    # 1. Configura o cliente da OpenAI
    # Ele usará a variável de ambiente OPENAI_API_KEY
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # 2. Define a persona e a instrução (SYSTEM PROMPT)
    system_prompt = """
    Você é um assistente de supervisão clínica altamente experiente, especializado em Terapia Cognitivo-Comportamental (TCC).
    Sua tarefa é analisar o Plano de Tratamento Psicológico fornecido pelo usuário e fornecer uma REVISÃO CONSTRUTIVA detalhada.

    Seu feedback deve ser estruturado nos seguintes pontos:
    1. **Coerência Diagnóstico-Metas:** Avalie se as Metas de Longo Prazo são uma resposta lógica ao Diagnóstico Base.
    2. **Alinhamento Terapêutico (TCC):** Verifique se as Metas de Curto Prazo estão formuladas de forma CLARA, MENSURÁVEL, e se são diretamente ALINHADAS com os princípios da TCC (focadas em pensamentos/comportamentos).
    3. **Sugestões de Refinamento:** Sugira até 2 pequenos ajustes nas metas de Curto Prazo ou nas Técnicas/Abordagens para maximizar a eficácia do plano.

    Formate sua resposta usando markdown (títulos, listas, negrito) para fácil leitura.
    Comece com um breve resumo de aprovação ou ressalva.
    """

    # 3. Monta o conteúdo do plano (USER PROMPT)
    user_content = f"""
    [PLANO DE TRATAMENTO PARA REVISÃO]
    
    Diagnóstico Base: {plano_data.get('diagnostico_base', 'Não fornecido')}
    Metas de Longo Prazo: {plano_data.get('metas_longo_prazo', 'Não fornecido')}
    Metas de Curto Prazo: {plano_data.get('metas_curto_prazo', 'Não fornecido')}
    Técnicas/Abordagem: {plano_data.get('tecnicas_abordagem', 'Não fornecido')}
    """
    
    try:
        # 4. Chamada da API
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.5, # Temperatura mais baixa para respostas focadas
        )
        # Retorna o conteúdo da resposta
        return response.choices[0].message.content
        
    except openai.APIError as e:
        # Em caso de erro (ex: chave inválida, limite de uso), retorna uma mensagem de erro
        return f"ERRO NA IA (OpenAI API): Não foi possível obter o feedback. Verifique sua chave e uso. Detalhes: {str(e)}"
    except Exception as e:
        return f"ERRO GERAL: Ocorreu um erro ao processar a requisição. Detalhes: {str(e)}"