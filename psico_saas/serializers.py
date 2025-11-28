from rest_framework import serializers 
from .models import PlanoTratamento


class PlanoTratamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoTratamento 
        fields = '__all__'
        read_only_fields = ('data_criacao', 'feedback_ia')