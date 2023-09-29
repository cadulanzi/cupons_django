from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .factories import ClienteFactory, CupomFactory, ConsumoFactory
from datetime import datetime, timedelta

class TestConsumoApi(APITestCase):

    def setUp(self):
        self.cliente = ClienteFactory()
        self.cupom = CupomFactory()
        self.consumo = ConsumoFactory(cliente=self.cliente, cupom=self.cupom)
        self.url = reverse('consumos-list')

    def test_invalid_cupom(self):
        data = {"cupom": "INVALID", "valor_compra": 150.00, "cliente": self.cliente.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expired_cupom(self):
        expired_cupom = CupomFactory(data_expiracao=datetime.now() - timedelta(days=1))
        data = {"cupom": expired_cupom.codigo, "valor_compra": 150.00, "cliente": self.cliente.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_max_usos_cupom(self):
        max_uso_cupom = CupomFactory(max_usos=1)
        ConsumoFactory(cupom=max_uso_cupom)  # Já utilizamos uma vez

        data = {"cupom": max_uso_cupom.codigo, "valor_compra": 150.00, "cliente": self.cliente.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valor_compra_inferior(self):
        data = {"cupom": self.cupom.codigo, "valor_compra": 50.00, "cliente": self.cliente.id}  # valor abaixo do necessário
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cupom_primeira_compra(self):
        first_time_cupom = CupomFactory(primeira_compra=True)
        ConsumoFactory(cliente=self.cliente, cupom=first_time_cupom)  # Já utilizamos uma vez

        data = {"cupom": first_time_cupom.codigo, "valor_compra": 150.00, "cliente": self.cliente.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filtragem_cliente(self):
        another_cliente = ClienteFactory()
        another_consumo = ConsumoFactory(cliente=another_cliente, cupom=self.cupom)

        # Filtrando consumos por nosso cliente original
        response = self.client.get(self.url, {"cliente": self.cliente.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(response.data[0]['cliente']['id'], self.cliente.id)

        # Filtrando consumos pelo outro cliente
        response = self.client.get(self.url, {"cliente": another_cliente.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[1]['cliente']['id'], another_cliente.id)

    def test_filtragem_cupom(self):
        another_cupom = CupomFactory()
        another_consumo = ConsumoFactory(cliente=self.cliente, cupom=another_cupom)

        # Filtrando consumos pelo nosso cupom original
        response = self.client.get(self.url, {"cupom": self.cupom.codigo})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['cupom']['codigo'], self.cupom.codigo)

        # Filtrando consumos pelo outro cupom
        response = self.client.get(self.url, {"cupom": another_cupom.codigo})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[1]['cupom']['codigo'], another_cupom.codigo)

    def test_desconto_percentual(self):
        cupom = CupomFactory(tipo_desconto='PERCENTUAL', valor_desconto=10.00)
        data = {"cupom": cupom.codigo, "valor_compra": 150.00, "cliente_id": self.cliente.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['valor_desconto'], 15.00)
