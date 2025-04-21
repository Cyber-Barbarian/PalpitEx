from django.db import models

# Create your models here.
class DadosAcoes(models.Model):
    index = models.IntegerField(primary_key=True, serialize=False)
    #index = models.BigIntegerField()
    data_pregao = models.DateField()
    preco_max = models.FloatField()
    preco_min = models.FloatField()
    preco_abertura = models.FloatField()
    preco_fechamento = models.FloatField()
    vol_negocios = models.BigIntegerField()
    #preco_fechamento_ajustado = models.FloatField()
    sigla_acao = models.CharField(max_length=10)
    dividendos = models.FloatField(null=True, blank=True)
    desdobramento = models.FloatField(null=True, blank=True)

    #class Meta:
    #    db_table = 'dados_acoes'
    #    indexes = [
    #        models.Index(fields=['data_pregao', 'sigla_acao']),
    #    ]

   #def __str__(self):
   #    return f"{self.sigla_acao} - {self.data_pregao}"
