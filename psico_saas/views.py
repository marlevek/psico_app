from django.shortcuts import render
from rest_framework import viewsets 
from .models import PlanoTratamento 
from .serializers import PlanoTratamentoSerializer 

class PlanoTratamentoViewSet(viewsets.ModelViewSet):
    '''
    Endpoint da API que permite criar, visualizar, atualizar e deleter planos de tratamento
    '''
    queryset = PlanoTratamento.objects.all().order_by('-data_criacao')
    serializer_class = PlanoTratamentoSerializer 

