from django.shortcuts import render
from rest_framework import viewsets 
from .models import PlanoTratamento 
from .serializers import PlanoTratamentoSerializer 


class PlanoTratamentoViewSet(viewsets.ModelViewSet):
    '''
    Endpoint da API que permite criar, visualizar, atualizar e deleter planos de tratamento
    '''
    # REMOVIDA: queryset = PlanoTratamento.objects.all().order_by('-data_criacao')
    
    # CORREÇÃO: Usar get_queryset() para ADIAR a query do banco de dados 
    # até que o servidor esteja completamente ativo e o Gunicorn esteja pronto.
    def get_queryset(self):
        return PlanoTratamento.objects.all().order_by('-data_criacao')
        
    serializer_class = PlanoTratamentoSerializer

