from django.db import models
from decimal import Decimal

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Cupom(models.Model):
    codigo = models.CharField(max_length=50, unique=True, db_index=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_expiracao = models.DateTimeField()
    max_usos = models.PositiveIntegerField()
    valor_minimo_compra = models.DecimalField(max_digits=7, decimal_places=2)
    TIPO_DESCONTO_CHOICES = [('PERCENTUAL', 'Percentual'), ('VALOR_FIXO', 'Valor Fixo')]
    tipo_desconto = models.CharField(choices=TIPO_DESCONTO_CHOICES, max_length=10)
    valor_desconto = models.DecimalField(max_digits=7, decimal_places=2)
    primeira_compra = models.BooleanField(default=False)

    def calcular_desconto(self, valor_compra):
        valor_compra = Decimal(valor_compra)
        if self.tipo_desconto == 'PERCENTUAL':
            return valor_compra * (self.valor_desconto / Decimal('100.0'))
        else:
            return min(self.valor_desconto, valor_compra)
        
    def save(self, *args, **kwargs):
        self.codigo = self.codigo.upper()
        super(Cupom, self).save(*args, **kwargs)

    
    def __str__(self):
       return self.codigo


class Consumo(models.Model):
    cupom = models.ForeignKey(Cupom, on_delete=models.CASCADE, db_index=True)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_index=True)
    valor_compra = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    desconto_aplicado = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    data_hora_uso = models.DateTimeField(auto_now_add=True)
