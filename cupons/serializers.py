from rest_framework import serializers
from .models import Cliente, Cupom, Consumo

class ClienteSerializer(serializers.ModelSerializer):
    """Serializa informações de um Cliente."""
    
    class Meta:
        model = Cliente
        fields = '__all__'

class CupomSerializer(serializers.ModelSerializer):
    """Serializa informações de um Cupom."""
    
    class Meta:
        model = Cupom
        fields = '__all__'

class ConsumoSerializer(serializers.ModelSerializer): 
    """Serializa informações de um Consumo. 
    Inclui desconto aplicado e data/hora do uso como campos somente leitura."""
    
    cliente = ClienteSerializer(read_only=True)
    cupom = CupomSerializer(read_only=True)

    class Meta:
        model = Consumo
        fields = '__all__'
        read_only_fields = ('desconto_aplicado', 'data_hora_uso')

    def validate_valor_compra(self, value):
        """Valida se o valor da compra é positivo."""
        
        if value <= 0:
            raise serializers.ValidationError("O valor da compra deve ser positivo.")
        return value
