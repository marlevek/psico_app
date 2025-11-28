from django.shortcuts import render
from rest_framework import viewsets 
from rest_framework.permissions import IsAuthenticated # ⬅️ Novo Import
from rest_framework.authentication import TokenAuthentication # ⬅️ Novo Import
from .models import PlanoTratamento 
from .serializers import PlanoTratamentoSerializer 


class PlanoTratamentoViewSet(viewsets.ModelViewSet):
    '''
    Endpoint da API que permite criar, visualizar, atualizar e deletar planos de tratamento
    '''
    authentication_classes = [TokenAuthentication]
    
    permission_classes = [IsAuthenticated]
    
       
    def get_queryset(self):
        # Método opcional para customizações
        return PlanoTratamento.objects.filter(usuario=self.request.user).order_by('-data_criacao')
        
    serializer_class = PlanoTratamentoSerializer
