from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.conf import settings
from .models import DadosAcao
from django.db.models import Q
from datetime import datetime
import yfinance as yf
import json
import logging
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

# Configurar logger
logger = logging.getLogger(__name__)

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
    return render(request, 'index.html')

def extract_data(request):
    try:
        dados = DadosAcao.objects.all().order_by('-data_pregao')
        siglas = DadosAcao.objects.values_list('sigla_acao', flat=True).distinct().order_by('sigla_acao')
        return render(request, 'extract_data.html', {
            'dados': dados,
            'siglas': siglas
        })
    except Exception as e:
        logger.error(f"Erro ao extrair dados: {str(e)}")
        return render(request, 'extract_data.html', {
            'error': 'Erro ao carregar dados. Por favor, tente novamente mais tarde.'
        })

def transform_data(request):
    return render(request, 'transform_data.html')

def load_historic_data(request):
    # Lógica para carregar dados históricos
    #historic_data()  # ou qualquer outra lógica que você queira executar
    dados = DadosAcoes.objects.all().order_by('data_pregao')
    return render(request, 'extract_data.html', {'dados': dados})

@require_http_methods(["POST"])
def carregar_dados_historicos(request):
    # Rate limiting
    client_ip = request.META.get('REMOTE_ADDR')
    cache_key = f'data_load_{client_ip}'
    if cache.get(cache_key):
        return JsonResponse({
            'error': 'Muitas requisições. Por favor, aguarde alguns minutos.'
        }, status=429)

    try:
        data = json.loads(request.body)
        sigla_acao = data.get('sigla_acao', '').strip().upper()

        # Validação da sigla
        if not sigla_acao or not re.match(r'^[A-Z]{4}$', sigla_acao):
            return JsonResponse({
                'error': 'Sigla da ação inválida'
            }, status=400)

        # Verificar cache
        cache_key = f'stock_data_{sigla_acao}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return JsonResponse({'message': 'Dados já existem para esta ação'})

        # Verificar se já existem dados
        if DadosAcao.objects.filter(sigla_acao=sigla_acao).exists():
            cache.set(cache_key, True, timeout=3600)  # Cache por 1 hora
            return JsonResponse({'message': 'Dados já existem para esta ação'})

        # Baixar dados históricos com timeout
        try:
            acao = yf.Ticker(f"{sigla_acao}.SA")
            dados_historicos = acao.history(period="max", timeout=10)
        except Exception as e:
            logger.error(f"Erro ao baixar dados do yfinance: {str(e)}")
            return JsonResponse({
                'error': 'Erro ao obter dados da ação. Por favor, tente novamente mais tarde.'
            }, status=500)

        # Validar dados antes de salvar
        if dados_historicos.empty:
            return JsonResponse({
                'error': 'Nenhum dado encontrado para esta ação'
            }, status=404)

        # Converter e validar dados
        for index, row in dados_historicos.iterrows():
            try:
                DadosAcao.objects.create(
                    data_pregao=index.date(),
                    preco_abertura=float(row['Open']),
                    preco_max=float(row['High']),
                    preco_min=float(row['Low']),
                    preco_fechamento=float(row['Close']),
                    vol_negocios=int(row['Volume']),
                    dividendos=float(row.get('Dividends', 0)),
                    sigla_acao=sigla_acao
                )
            except (ValueError, TypeError) as e:
                logger.error(f"Erro ao salvar dados: {str(e)}")
                continue

        # Configurar cache
        cache.set(cache_key, True, timeout=3600)
        cache.set(f'data_load_{client_ip}', True, timeout=300)  # 5 minutos de rate limit

        return JsonResponse({'message': 'Dados carregados com sucesso'})

    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Formato de dados inválido'
        }, status=400)
    except Exception as e:
        logger.error(f"Erro não tratado: {str(e)}")
        return JsonResponse({
            'error': 'Erro interno do servidor'
        }, status=500)


