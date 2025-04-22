from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
import re

# Create your models here.
class DadosAcoes(models.Model):
    #index = models.IntegerField(primary_key=True, serialize=False)
    id = models.AutoField(primary_key=True)
    index = models.BigIntegerField()
    data_pregao = models.DateField()
    preco_max = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    preco_min = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    preco_abertura = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    preco_fechamento = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    vol_negocios = models.BigIntegerField(
        validators=[MinValueValidator(0)]
    )
    #preco_fechamento_ajustado = models.FloatField()
    sigla_acao = models.CharField(
        max_length=4,
        validators=[
            RegexValidator(
                regex='^[A-Z]{4}$',
                message='Sigla deve conter exatamente 4 letras maiúsculas'
            )
        ]
    )
    dividendos = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    desdobramento = models.FloatField(null=True, blank=True)
    

    class Meta:
        db_table = 'dados_acoes'
        indexes = [
            models.Index(fields=['data_pregao', 'sigla_acao']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(preco_max__gte=models.F('preco_min')),
                name='preco_max_maior_que_min'
            ),
            models.CheckConstraint(
                check=models.Q(preco_max__gte=models.F('preco_abertura')),
                name='preco_max_maior_que_abertura'
            ),
            models.CheckConstraint(
                check=models.Q(preco_max__gte=models.F('preco_fechamento')),
                name='preco_max_maior_que_fechamento'
            ),
            models.CheckConstraint(
                check=models.Q(preco_min__lte=models.F('preco_abertura')),
                name='preco_min_menor_que_abertura'
            ),
            models.CheckConstraint(
                check=models.Q(preco_min__lte=models.F('preco_fechamento')),
                name='preco_min_menor_que_fechamento'
            ),
        ]

   #def __str__(self):
   #    return f"{self.sigla_acao} - {self.data_pregao}"

    def clean(self):
        # Validações adicionais
        if self.preco_max < self.preco_min:
            raise ValidationError('Preço máximo não pode ser menor que o preço mínimo')
        
        if self.preco_max < self.preco_abertura or self.preco_max < self.preco_fechamento:
            raise ValidationError('Preço máximo deve ser maior ou igual aos outros preços')
        
        if self.preco_min > self.preco_abertura or self.preco_min > self.preco_fechamento:
            raise ValidationError('Preço mínimo deve ser menor ou igual aos outros preços')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
