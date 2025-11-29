# psico_saas/serializers.py

from rest_framework import serializers
from .models import PlanoTratamento, DocumentacaoSessao, TarefaExercicios, Paciente, ConteudoEducacional
import os
import json
from openai import OpenAI  # ⬅️ IMPORT CORRIGIDO

# ------------------------------------------------------------------
# CONFIGURAÇÃO DO CLIENTE OPENAI
# ------------------------------------------------------------------
# O cliente busca a chave automaticamente da variável de ambiente OPENAI_API_KEY
try:
    client = OpenAI()  # ⬅️ CLIENTE CORRIGIDO E INSTANCIADO
except Exception as e:
    # Caso a chave não esteja definida ou haja outro erro de inicialização
    print(
        f"Alerta: Falha ao inicializar o cliente OpenAI. Verifique sua chave API. Erro: {e}")
    client = None

# ------------------------------------------------------------------
# 1. PLANO DE TRATAMENTO SERIALIZER
# ------------------------------------------------------------------


class PlanoTratamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoTratamento
        fields = ['id', 'paciente', 'titulo', 'abordagem', 'diagnostico_base',
                  # ⬅️ ADICIONAR ESTE CAMPO
                  'frequencia_sessoes', 'metas_tratamento', 'data_inicio_prevista',
                  'feedback_ia', 'data_criacao']
        read_only_fields = ['feedback_ia', 'data_criacao']

    def validate(self, data):
        """
        Validação customizada para garantir que campos obrigatórios estão presentes
        """
        campos_obrigatorios = [
            'paciente', 'titulo', 'diagnostico_base', 'metas_tratamento', 'data_inicio_prevista']

        for campo in campos_obrigatorios:
            if campo not in data or not data[campo]:
                raise serializers.ValidationError(
                    {campo: "Este campo é obrigatório."})

        return data

    def create(self, validated_data):
        # 1. Montar a instrução para a IA
        diagnostico = validated_data.get('diagnostico_base')
        metas = validated_data.get('metas_tratamento')

        prompt_texto = f"""
        Você é um assistente de revisão de planos de tratamento. Analise o seguinte plano e forneça um feedback construtivo e conciso (máximo 150 palavras).
        Foque em sugerir aprimoramentos, validação da coerência entre diagnóstico e metas, ou estratégias adicionais (ex: uso de técnicas de mindfulness, psicoeducação, etc.).
        
        Diagnóstico Base: {diagnostico}
        Metas de Tratamento: {metas}
        """

        # 2. Chamar a OpenAI
        if client:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system",
                            "content": "Você é um assistente de revisão de planos."},
                        {"role": "user", "content": prompt_texto}
                    ]
                )

                # 3. Extrair o texto da IA
                feedback = response.choices[0].message.content
                validated_data['feedback_ia'] = feedback

            except Exception as e:
                validated_data['feedback_ia'] = "Erro na comunicação com a IA."
                print(f"Erro na API da OpenAI (Plano): {e}")
        else:
            validated_data['feedback_ia'] = "Cliente OpenAI não configurado."

        return PlanoTratamento.objects.create(**validated_data)


# ------------------------------------------------------------------
# 2. DOCUMENTAÇÃO SESSÃO SERIALIZER (Lógica da IA)
# ------------------------------------------------------------------
class DocumentacaoSessaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentacaoSessao
        fields = ['id', 'paciente', 'data_sessao', 'anotacoes_brutas',
                  'resumo_ia', 'sugestao_diagnostico', 'padroes_linguagem', 'data_criacao']
        read_only_fields = ['resumo_ia', 'sugestao_diagnostico',
                            'padroes_linguagem', 'data_criacao']

    def create(self, validated_data):
        # 1. Montar a instrução para a IA
        anotacoes = validated_data.get('anotacoes_brutas')

        prompt_texto = f"""
        Você é um assistente de documentação psicológica. Analise as anotações e gere três saídas no formato JSON: um resumo conciso, sugestão de diagnóstico (CID-10 ou DSM-5) e padrões de linguagem.

        Anotações da Sessão: {anotacoes}

        Gere a resposta em um objeto JSON válido, contendo as chaves EXATAS: resumo_ia, sugestao_diagnostico, padroes_linguagem.
        """

        # 2. Chamar a OpenAI
        if client:  # Verifica se o cliente foi inicializado com sucesso
            try:
                response = client.chat.completions.create(  # ⬅️ CHAMADA CORRIGIDA
                    model="gpt-3.5-turbo-1106",
                    messages=[
                        {"role": "system",
                            "content": "Você deve responder apenas com um objeto JSON válido."},
                        {"role": "user", "content": prompt_texto}
                    ],
                    response_format={"type": "json_object"}
                )

                # 3. Extrair dados JSON
                ia_output = json.loads(response.choices[0].message.content)

                # 4. Atualizar os dados validados com o output da IA
                validated_data['resumo_ia'] = ia_output.get('resumo_ia')
                validated_data['sugestao_diagnostico'] = ia_output.get(
                    'sugestao_diagnostico')
                validated_data['padroes_linguagem'] = ia_output.get(
                    'padroes_linguagem')

            except Exception as e:
                validated_data['resumo_ia'] = "Erro na comunicação com a IA."
                raise serializers.ValidationError(
                    {"detail": f"Erro na API da OpenAI: {e}"})
        else:
            raise serializers.ValidationError(
                {"detail": "Erro de processamento: Cliente OpenAI não configurado."})

        return DocumentacaoSessao.objects.create(**validated_data)


# ------------------------------------------------------------------
# 3. TAREFA/EXERCÍCIOS SERIALIZER (Lógica da IA)
# ------------------------------------------------------------------
class TarefaExerciciosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarefaExercicios
        fields = ['id', 'paciente', 'abordagem_teorica', 'tema_principal', 'detalhes_personalizacao',
                  'exercicio_ia', 'data_criacao']
        read_only_fields = ['exercicio_ia', 'data_criacao']

    def create(self, validated_data):
        # 1. Montar a instrução para a IA
        abordagem = validated_data.get('abordagem_teorica')
        tema = validated_data.get('tema_principal')
        detalhes = validated_data.get(
            'detalhes_personalizacao', 'Não há detalhes adicionais.')

        prompt_texto = f"""
        Você é um Gerador de Tarefas Terapêuticas. Crie um exercício prático e personalizado para um paciente.

        Abordagem Teórica: {abordagem}
        Tema Principal da Tarefa: {tema}
        Detalhes de Personalização do Paciente: {detalhes}

        Crie um exercício detalhado, formatado com cabeçalhos e listas, contendo: Título, Objetivo, Passos para a execução (numerados) e O que o paciente deve observar ou anotar.
        """

        # 2. Chamar a OpenAI
        if client:  # Verifica se o cliente foi inicializado com sucesso
            try:
                response = client.chat.completions.create(  # ⬅️ CHAMADA CORRIGIDA
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Você é um gerador de tarefas. Responda apenas com o texto do exercício pronto."},
                        {"role": "user", "content": prompt_texto}
                    ]
                )

                # 3. Extrair o texto da IA
                exercicio_gerado = response.choices[0].message.content
                validated_data['exercicio_ia'] = exercicio_gerado

            except Exception as e:
                validated_data['exercicio_ia'] = "Erro na comunicação com a IA ao gerar o exercício."
                raise serializers.ValidationError(
                    {"detail": f"Erro na API da OpenAI: {e}"})
        else:
            raise serializers.ValidationError(
                {"detail": "Erro de processamento: Cliente OpenAI não configurado."})

        return TarefaExercicios.objects.create(**validated_data)


# ------------------------------------------------------------------
# 4. CONTEÚDO EDUCACIONAL SERIALIZER - VERSÃO CORRIGIDA
# ------------------------------------------------------------------
class ConteudoEducacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConteudoEducacional
        fields = ['id', 'titulo', 'tipo_conteudo', 'tema_principal', 'publico_alvo',
                  'tom_voz', 'palavras_chave', 'conteudo_gerado', 'sugestoes_titulos', 'sugestoes_imagens',
                  'hashtags', 'data_criacao', 'data_atualizacao']
        read_only_fields = ['conteudo_gerado', 'sugestoes_titulos',
                            'hashtags', 'data_criacao', 'data_atualizacao']

    
    def create(self, validated_data):
        # 1. Montar a instrução para a IA
        tipo_conteudo = validated_data.get('tipo_conteudo')
        tema_principal = validated_data.get('tema_principal')
        publico_alvo = validated_data.get('publico_alvo', 'Público geral interessado em saúde mental')
        tom_voz = validated_data.get('tom_voz', 'Profissional e acolhedor')
        palavras_chave = validated_data.get('palavras_chave', '')
        
        prompt_texto = f"""
        Você é um criador de conteúdo especializado em saúde mental. Crie um conteúdo educativo baseado nos seguintes parâmetros:

        TIPO DE CONTEÚDO: {tipo_conteudo}
        TEMA PRINCIPAL: {tema_principal}
        PÚBLICO-ALVO: {publico_alvo}
        TOM DE VOZ: {tom_voz}
        PALAVRAS-CHAVE: {palavras_chave}

        **INSTRUÇÕES ESPECÍFICAS:**
        1. CONTEÚDO PRINCIPAL: Crie um texto bem estruturado, informativo e engajador
        2. SUGESTÕES DE TÍTULOS: Forneça 3 títulos alternativos em formato de lista
        3. HASHTAGS: Sugira 5-8 hashtags relevantes separadas por vírgula
        4. SUGESTÕES DE IMAGENS: Descreva 3 tipos de imagens que combinariam com este conteúdo

        **FORMATO DA RESPOSTA (JSON OBRIGATÓRIO):**
        {{
            "conteudo_principal": "texto aqui...",
            "sugestoes_titulos": ["Título 1", "Título 2", "Título 3"],
            "hashtags": "#saudemental #ansiedade #terapia",
            "sugestoes_imagens": "1. Imagem de pessoa meditando\\n2. Infográfico sobre ansiedade\\n3. Natureza tranquila"
        }}
        """
        
        # 2. Chamar a OpenAI
        if client:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages=[
                        {"role": "system", "content": "Você deve responder APENAS com um objeto JSON válido, sem texto adicional."},
                        {"role": "user", "content": prompt_texto}
                    ],
                    response_format={"type": "json_object"}
                )
                
                # 3. Extrair dados JSON
                ia_output = json.loads(response.choices[0].message.content)
                print("=== DEBUG IA OUTPUT ===")
                print("IA OUTPUT COMPLETO:", ia_output)
                print("SUGESTÕES DE IMAGENS NO IA OUTPUT:", ia_output.get('sugestoes_imagens'))
                print("TIPO:", type(ia_output.get('sugestoes_imagens')))
                print("=======================")
                
                # 4. Atualizar os dados validados com o output da IA
                validated_data['conteudo_gerado'] = ia_output.get('conteudo_principal', '')
                validated_data['sugestoes_titulos'] = ', '.join(ia_output.get('sugestoes_titulos', []))
                validated_data['hashtags'] = ia_output.get('hashtags', '')
                
                # 5. Adicionar sugestões de imagens
                sugestoes_imagens = ia_output.get('sugestoes_imagens', '')
                validated_data['sugestoes_imagens'] = sugestoes_imagens
                
                print("=== DEBUG VALIDATED DATA ===")
                print("SUGESTÕES DE IMAGENS NO VALIDATED_DATA:", validated_data.get('sugestoes_imagens'))
                print("=======================")
                
            except Exception as e:
                print("ERRO NA IA:", e)
                validated_data['conteudo_gerado'] = "Erro na comunicação com a IA."
                raise serializers.ValidationError({"detail": f"Erro na API da OpenAI: {e}"})
        else:
            raise serializers.ValidationError({"detail": "Erro de processamento: Cliente OpenAI não configurado."})

        # 6. Criar o objeto
        conteudo = ConteudoEducacional.objects.create(**validated_data)
        
        print("=== DEBUG OBJETO CRIADO ===")
        print("SUGESTÕES DE IMAGENS NO OBJETO:", conteudo.sugestoes_imagens)
        print("OBJETO COMPLETO:", {field: getattr(conteudo, field) for field in ['id', 'titulo', 'sugestoes_imagens']})
        print("=======================")
        
        return conteudo
        
        
        # 2. Chamar a OpenAI
        if client:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages=[
                        {"role": "system", "content": "Você deve responder APENAS com um objeto JSON válido, sem texto adicional."},
                        {"role": "user", "content": prompt_texto}
                    ],
                    response_format={"type": "json_object"}
                )
                
                # 3. Extrair dados JSON
                ia_output = json.loads(response.choices[0].message.content)
                print("IA OUTPUT COMPLETO:", ia_output)  # DEBUG
                
                # 4. Atualizar os dados validados com o output da IA
                validated_data['conteudo_gerado'] = ia_output.get('conteudo_principal', '')
                validated_data['sugestoes_titulos'] = ', '.join(ia_output.get('sugestoes_titulos', []))
                validated_data['hashtags'] = ia_output.get('hashtags', '')
                
                # 5. Adicionar sugestões de imagens (garantir que existe no modelo)
                sugestoes_imagens = ia_output.get('sugestoes_imagens', '')
                print("SUGESTÕES DE IMAGENS RAW:", sugestoes_imagens)  # DEBUG
                
                # Verificar se o campo existe no modelo antes de tentar salvar
                if hasattr(ConteudoEducacional, 'sugestoes_imagens'):
                    validated_data['sugestoes_imagens'] = sugestoes_imagens
                    print("SUGESTÕES DE IMAGENS SALVAS:", validated_data['sugestoes_imagens'])  # DEBUG
                
            except Exception as e:
                print("ERRO NA IA:", e)  # DEBUG
                validated_data['conteudo_gerado'] = "Erro na comunicação com a IA."
                raise serializers.ValidationError({"detail": f"Erro na API da OpenAI: {e}"})
        else:
            raise serializers.ValidationError({"detail": "Erro de processamento: Cliente OpenAI não configurado."})

        # 6. Criar o objeto
        conteudo = ConteudoEducacional.objects.create(**validated_data)
        print("CONTEÚDO CRIADO NO BANCO:", conteudo.__dict__)  # DEBUG
        return conteudo