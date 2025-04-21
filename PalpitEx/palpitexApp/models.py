from django.db import models

# Create your models here.
class StockData(models.Model):
    index = models.AutoField(primary_key=True)
    data_pregao = models.DateField()
    preco_max = models.DecimalField(max_digits=10, decimal_places=6)
    preco_min = models.DecimalField(max_digits=10, decimal_places=6)
    preco_abertura = models.DecimalField(max_digits=10, decimal_places=6)
    preco_fechamento = models.DecimalField(max_digits=10, decimal_places=6)
    vol_negocios = models.IntegerField()
    preco_fechamento_ajustado = models.DecimalField(max_digits=10, decimal_places=6)
    sigla_acao = models.CharField(max_length=10)
