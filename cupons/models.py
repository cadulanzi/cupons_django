from django.db import models
from decimal import Decimal

PERCENTUAL = 'PERCENTUAL'
VALOR_FIXO = 'VALOR_FIXO'
TIPO_DESCONTO_CHOICES = [(PERCENTUAL, 'Percentual'), (VALOR_FIXO, 'Valor Fixo')]

class Cliente(models.Model):
    """Representa um cliente no sistema."""
    
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Cupom(models.Model):
    """Representa um cupom de desconto no sistema."""

    codigo = models.CharField(max_length=50, unique=True, db_index=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_expiracao = models.DateTimeField()
    max_usos = models.PositiveIntegerField()
    valor_minimo_compra = models.DecimalField(max_digits=7, decimal_places=2)
    tipo_desconto = models.CharField(choices=TIPO_DESCONTO_CHOICES, max_length=10)
    valor_desconto = models.DecimalField(max_digits=7, decimal_places=2)
    primeira_compra = models.BooleanField(default=False)

    def calcular_desconto(self, valor_compra):
        """Calcula o desconto baseado no tipo e valor do cupom."""
        
        valor_compra = Decimal(valor_compra)
        if self.tipo_desconto == PERCENTUAL:
            return valor_compra * (self.valor_desconto / Decimal(100))
        elif self.tipo_desconto == VALOR_FIXO:
            return min(self.valor_desconto, valor_compra)
        else:
            raise ValueError("Tipo de desconto inválido.")
        
    def save(self, *args, **kwargs):
        """Salva o cupom após converter o código para maiúsculas."""
        
        self.codigo = self.codigo.upper()
        super(Cupom, self).save(*args, **kwargs)

    def __str__(self):
       return self.codigo


class Consumo(models.Model):
    """Representa o consumo/usagem de um cupom por um cliente."""
    
    cupom = models.ForeignKey(Cupom, on_delete=models.CASCADE, db_index=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_index=True)
    valor_compra = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    desconto_aplicado = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    data_hora_uso = models.DateTimeField(auto_now_add=True)
