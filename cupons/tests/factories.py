import factory
from cupons.models import Cliente, Cupom, Consumo
from datetime import datetime, timedelta

class ClienteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cliente

    nome = factory.Sequence(lambda n: f"cliente{n}")
    email = factory.Sequence(lambda n: f"cliente{n}@example.com")

class CupomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cupom

    codigo = factory.Sequence(lambda n: f"CODE{n}")
    data_expiracao = datetime.now() + timedelta(days=30)
    max_usos = 10
    valor_minimo_compra = 100.00
    tipo_desconto = 'PERCENTUAL'
    valor_desconto = 10.00

class ConsumoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Consumo

    cliente = factory.SubFactory(ClienteFactory)
    cupom = factory.SubFactory(CupomFactory)
    valor_compra = 150.00
