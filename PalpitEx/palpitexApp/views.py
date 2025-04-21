from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .ETL.meu_codigo_teste import soma

def minha_view(request):
    resultado = soma(3, 4)
    return HttpResponse(f"O resultado da soma é: {resultado}")
