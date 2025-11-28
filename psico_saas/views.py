from django.shortcuts import render
from rest_framework import viewsets 
from .models import PlanoTratamento # <-- AQUI ESTÁ O PRÓXIMO PONTO DE FALHA
from .serializers import PlanoTratamentoSerializer 

class PlanoTratamentoViewSet(viewsets.ModelViewSet):
    '''
    Endpoint da API que permite criar, visualizar, atualizar e deleter planos de tratamento
    '''
    # CORREÇÃO: Usar get_queryset() para ADIAR a query do banco de dados 
    def get_queryset(self):
        # Esta função só executa quando o servidor já está a funcionar
        return PlanoTratamento.objects.all().order_by('-data_criacao')
        
    serializer_class = PlanoTratamentoSerializer
