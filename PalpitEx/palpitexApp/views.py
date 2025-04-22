from django.shortcuts import render

import pandas as pd 
import pandas_datareader
from pandas_datareader import data as web 
import matplotlib.pyplot as plt
import glob
import os

# Create your views here.

from django.http import HttpResponse
from .ETL.meu_codigo_teste import soma
from .ETL.etl import *
from .models import DadosAcoes
from .ETL.etl import historic_data

def minha_view(request):
    resultado = soma(3, 4)
    return HttpResponse(f"O resultado da soma é: {resultado}")

def index(request):
    nome_usuario = "Palhaço Pirulito"

    return render(request, 'index.html', {
        'nome_usuario': nome_usuario})


def extract_data(request):
    # Buscar as 50 primeiras linhas da tabela DadosAcoes

    dados = DadosAcoes.objects.all().order_by('data_pregao')[:50]
    return render(request, 'extract_data.html', {'dados': dados})

def transform_data(request):
    return render(request, 'transform_data.html')

def load_historic_data(request):
    # Lógica para carregar dados históricos
    historic_data()  # ou qualquer outra lógica que você queira executar
    return render(request, 'extract_data.html', {})


