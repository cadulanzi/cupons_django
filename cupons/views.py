from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime
from cupons.models import Cliente, Consumo, Cupom
from decimal import Decimal
from cupons.serializers import ClienteSerializer, ConsumoSerializer, CupomSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    """Exibindo todos os clientes"""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class CuponsViewSet(viewsets.ModelViewSet):
    """Exibindo todos os cupons"""
    queryset = Cupom.objects.all()
    serializer_class = CupomSerializer

class ConsumoViewSet(viewsets.ModelViewSet):
    """Exibindo todos os consumos"""
    queryset = Consumo.objects.all()
    serializer_class = ConsumoSerializer

    def listAll(self, request, *args, **kwargs):
        """Listando todos os consumos"""
        consumos = Consumo.objects.all()
        serializer = ConsumoSerializer(consumos, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """Listando os consumos"""
        cliente_id = request.query_params.get("cliente_id", None)
        if cliente_id:
            consumos = Consumo.objects.filter(cliente_id=cliente_id)
        else:
            consumos = Consumo.objects.all()
        serializer = ConsumoSerializer(consumos, many=True)
        return Response(serializer.data)
    
    def listByCupom(self, request, *args, **kwargs):
        """Listando os consumos"""
        cupom_code = kwargs.get("cupom")
        
        if not cupom_code:
            return Response({"erro": "Cupom não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

        cupom_instance = get_object_or_404(Cupom, codigo=cupom_code)
        consumos = Consumo.objects.filter(cupom=cupom_instance)
        serializer = ConsumoSerializer(consumos, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        cupom_codigo = request.data.get("cupom", "").strip().upper()
        valor_compra = Decimal(request.data.get("valor_compra", 0))
        cliente_id = request.data.get("cliente_id")

        # 1. Validar se o cupom existe
        try:
            cupom = Cupom.objects.get(codigo=cupom_codigo)
        except Cupom.DoesNotExist:
            return Response({"erro": f"Cupom '{cupom_codigo}' não encontrado."}, status=status.HTTP_400_BAD_REQUEST)


        # 2. Verificar data de expiração
        if timezone.now() > cupom.data_expiracao:

            return Response({"erro": "Cupom expirado."}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Verificar número de utilizações
        usos = Consumo.objects.filter(cupom=cupom).count()
        if usos >= cupom.max_usos:
            return Response({"erro": "Cupom atingiu o número máximo de utilizações."}, status=status.HTTP_400_BAD_REQUEST)

        # 4. Checar o valor da compra
        if valor_compra < cupom.valor_minimo_compra:
            return Response({"erro": "Valor da compra é inferior ao necessário para utilizar o cupom."}, status=status.HTTP_400_BAD_REQUEST)

        # 5. Verificar se é a primeira compra do cliente com aquele cupom
        if cupom.primeira_compra and Consumo.objects.filter(cliente_id=cliente_id, cupom=cupom).exists():
            return Response({"erro": "Cupom válido apenas para a primeira compra."}, status=status.HTTP_400_BAD_REQUEST)

        # Aplicar o desconto usando o método do modelo Cupom
        desconto = cupom.calcular_desconto(valor_compra)
        
        valor_final = valor_compra - desconto


        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            return Response({"erro": "Cliente não encontrado."}, status=status.HTTP_400_BAD_REQUEST)
        # Salvando o consumo
        consumo = Consumo(cupom=cupom, cliente_id=cliente, valor_compra=valor_compra, desconto_aplicado=desconto)
        consumo.save()

        # Retornando a resposta
        return Response({
            "valor_desconto": desconto,
            "valor_final": valor_final,
            "codigo_cupom": cupom_codigo
        }, status=status.HTTP_201_CREATED)