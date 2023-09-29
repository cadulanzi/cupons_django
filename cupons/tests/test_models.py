from django.test import TestCase
from cupons.models import Cliente, Cupom, Consumo

class ClienteModelTest(TestCase):

    def test_create_and_retrieve_cliente(self):
        cliente = Cliente.objects.create(nome="John Doe", email="john.doe@example.com")
        saved_cliente = Cliente.objects.first()
        self.assertEqual(saved_cliente, cliente)

