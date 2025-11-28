import os
from rest_framework import serializers
from .models import PlanoTratamento
from openai import OpenAI # Importar a classe OpenAI

'''class PlanoTratamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoTratamento
        fields = '__all__'
        read_only_fields = ['feedback_ia', 'data_criacao']
        
    def gerar_prompt(self, valid_data):
        """Função para construir o prompt com base nos dados do plano."""
        # Coloque a sua lógica de criação de prompt aqui, usando valid_data
        # Exemplo:
        return f"""
        Você é um revisor de plano de tratamento especializado em TCC.
        Diagnóstico: {valid_data['diagnostico_base']}
        Metas a Longo Prazo: {valid_data['metas_longo_prazo']}
        Metas a Curto Prazo: {valid_data['metas_curto_prazo']}
        Técnicas/Abordagem: {valid_data['tecnicas_abordagem']}
        
        Sua tarefa é revisar este plano. Se ele estiver conciso, devolva 'OK'. Se precisar de ajustes ou for muito vago, devolva um feedback estruturado e construtivo.
        """

    def create(self, validated_data):
        # 1. INICIALIZAÇÃO DA API (CORREÇÃO CRÍTICA):
        # Mova a inicialização para DENTRO do método para garantir que a 
        # OPENAI_API_KEY do Railway é lida.
        try:
            chave_api = os.environ.get('OPENAI_API_KEY')
            if not chave_api:
                # Se a chave não for encontrada (o que causava o crash)
                raise ValueError("OPENAI_API_KEY não configurada no ambiente.")
                
            client = OpenAI(api_key=chave_api)

            # 2. Geração do Prompt e Chamada da API
            prompt = self.gerar_prompt(validated_data)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo", # Use o modelo que desejar
                messages=[
                    {"role": "system", "content": "Você é um revisor de planos de tratamento."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # 3. Extrair o Feedback
            feedback_ia = response.choices[0].message.content
            
        except ValueError as e:
            # Captura a exceção se a chave não for encontrada
            feedback_ia = f"ERRO INTERNO: Falha na API da IA. Detalhe: {e}"
        except Exception as e:
            # Captura qualquer outro erro da API
            feedback_ia = f"ERRO NA CHAMADA DA API. Detalhe: {e}"

        # 4. Salvar o Plano com o Feedback
        return PlanoTratamento.objects.create(
            **validated_data, 
            feedback_ia=feedback_ia
        )'''
        
        
# psico_saas/serializers.py

import os
from rest_framework import serializers
from .models import PlanoTratamento
# Mantenha a importação da OpenAI, mesmo que não seja usada
from openai import OpenAI 

class PlanoTratamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoTratamento
        fields = '__all__'
        read_only_fields = ['feedback_ia', 'data_criacao']
        
    def gerar_prompt(self, valid_data):
        # Mantenha esta função, mas ela não será chamada
        pass 

    def create(self, validated_data):
        # CÓDIGO TEMPORÁRIO DE TESTE: IGNORAR A CHAMADA DA API
        
        # 1. Simula o feedback da IA
        feedback_ia_teste = "TESTE DE DEPLOY: A API Gunicorn carregou com sucesso. O erro não está no startup."

        # 2. Salva o Plano no PostgreSQL (sem chamar a API externa)
        return PlanoTratamento.objects.create(
            **validated_data, 
            feedback_ia=feedback_ia_teste
        )