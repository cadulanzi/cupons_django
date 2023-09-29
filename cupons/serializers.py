from rest_framework import serializers
from .models import Cliente, Cupom, Consumo

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class CupomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupom
        fields = '__all__'

class ConsumoSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Consumo
        fields = '__all__'
        read_only_fields = ('desconto_aplicado', 'data_hora_uso')