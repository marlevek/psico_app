from django.shortcuts import render
from rest_framework import viewsets 
from .models import PlanoTratamento 
from .serializers import PlanoTratamentoSerializer 


class PlanoTratamentoViewSet(viewsets.ModelViewSet):
    '''
    Endpoint da API que permite criar, visualizar, atualizar e deletar planos de tratamento
    '''
    #queryset = PlanoTratamento.objects.all()  # ⬅️ ADICIONE ESTA LINHA
    serializer_class = PlanoTratamentoSerializer
    
    def get_queryset(self):
        # Método opcional para customizações
        return PlanoTratamento.objects.all().order_by('-data_criacao')
        
   
