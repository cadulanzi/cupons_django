import pytest
from rest_framework import serializers
from cupons.serializers import ClienteSerializer, CupomSerializer, ConsumoSerializer
from .factories import ClienteFactory, CupomFactory, ConsumoFactory

@pytest.mark.django_db
def test_cliente_serializer():
    cliente = ClienteFactory()
    serializer = ClienteSerializer(cliente)
    
    assert serializer.data['nome'] == cliente.nome

@pytest.mark.django_db
def test_cupom_serializer():
    cupom = CupomFactory()
    serializer = CupomSerializer(cupom)
    
    assert serializer.data['codigo'] == cupom.codigo
    assert serializer.data['tipo_desconto'] == cupom.tipo_desconto
    assert float(serializer.data['valor_desconto']) == cupom.valor_desconto

@pytest.mark.django_db
def test_consumo_serializer():
    consumo = ConsumoFactory()
    serializer = ConsumoSerializer(consumo)
    
    assert serializer.data['cliente']['nome'] == consumo.cliente.nome
    assert serializer.data['cupom']['codigo'] == consumo.cupom.codigo
    assert float(serializer.data['valor_compra']) == consumo.valor_compra


@pytest.mark.django_db
def test_consumo_serializer_validate_valor_compra():
    serializer = ConsumoSerializer(data={'valor_compra': -100})

    with pytest.raises(serializers.ValidationError) as e:
        serializer.is_valid(raise_exception=True)

    assert 'O valor da compra deve ser positivo.' in str(e.value)
