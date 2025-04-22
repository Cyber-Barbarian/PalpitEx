import pandas as pd 
import yfinance as yf
import matplotlib.pyplot as plt
import glob
import os
from datetime import datetime
from ..models import DadosAcoes
from django.db.models import Q

def historic_data(tickers = ['PETR3.SA', 'PETR4.SA', 'USIM5.SA', 'VALE3.SA']):
    # vOHLC - Open, High, Low, Close + Adj Close + Volume , neste caso). Que significam o preço de abertura, 
    #o preço máximo no dia, o preço mínimo no dia, o preço de fechamento do dia, o preço ajustado por eventos corporativos 
    #e o volume de contratos negociados no dia (seguindo a ordem do dataframe).
    #teste
    #tickers = ['PETR3.SA', 'PETR4.SA']
    print("tickers: ", tickers)

    #tickers = ['RRRP3.SA', 'ALPA4.SA', 'ABEV3.SA', 'AMER3.SA', 'ARZZ3.SA', 'ASAI3.SA', 'AZUL4.SA', 'B3SA3.SA', 'BPAN4.SA', 'BBSE3.SA', 
    #'BRML3.SA', 'BBDC3.SA', 'BBDC4.SA', 'BRAP4.SA', 'BBAS3.SA', 'BRKM5.SA', 'BRFS3.SA', 'BPAC11.SA', 'CRFB3.SA', 'CCRO3.SA', 
    #'CMIG4.SA', 'CIEL3.SA', 'COGN3.SA', 'CPLE6.SA', 'CSAN3.SA', 'CPFE3.SA', 'CMIN3.SA', 'CVCB3.SA', 'CYRE3.SA', 'DXCO3.SA', 
    #'ECOR3.SA', 'ELET3.SA', 'ELET6.SA', 'EMBR3.SA', 'ENBR3.SA', 'ENGI11.SA', 'ENEV3.SA', 'EGIE3.SA', 'EQTL3.SA', 'EZTC3.SA', 
    #'FLRY3.SA', 'GGBR4.SA', 'GOAU4.SA', 'GOLL4.SA', 'NTCO3.SA', 'SOMA3.SA', 'HAPV3.SA', 'HYPE3.SA', 'IGTI11.SA', 'IRBR3.SA', 
    #'ITSA4.SA', 'ITUB4.SA', 'JBSS3.SA', 'KLBN11.SA', 'RENT3.SA', 'LWSA3.SA', 'LREN3.SA', 'MGLU3.SA', 'MRFG3.SA', 'CASH3.SA', 
    #'BEEF3.SA', 'MRVE3.SA', 'MULT3.SA', 'PCAR3.SA', 'PETR3.SA', 'PETR4.SA', 'PRIO3.SA', 'PETZ3.SA', 'POSI3.SA', 'QUAL3.SA', 
    #'RADL3.SA', 'RAIZ4.SA', 'RDOR3.SA', 'RAIL3.SA', 'SBSP3.SA', 'SANB11.SA', 'SMTO3.SA', 'CSNA3.SA', 'SLCE3.SA', 'SULA11.SA', 
    #'SUZB3.SA', 'TAEE11.SA', 'VIVT3.SA', 'TIMS3.SA', 'TOTS3.SA', 'UGPA3.SA', 'USIM5.SA', 'VALE3.SA', 'VIIA3.SA', 'VBBR3.SA', 
    #'WEGE3.SA', 'YDUQ3.SA']

    def get_stock_data(tickers, start_date='2024-01-01', end_date='2025-01-01'):
        try:
            df_list = []
            for ticker in tickers:
                stock = yf.Ticker(ticker)
                df = stock.history(start=start_date, end=end_date)
                df['ticker'] = ticker
                df_list.append(df)

            df_cotacoes = pd.concat(df_list)
            return df_cotacoes
        except Exception as e:
            print(f"Erro ao obter dados: {str(e)}")
            return None

    # Obtendo os dados
    df_cotacoes = get_stock_data(tickers)
    df_cotacoes['data_pregao'] = df_cotacoes.index

    
    df_cotacoes= df_cotacoes.reset_index().drop('Date', axis=1)
    df_cotacoes['index'] = df_cotacoes.index
    
    
    if df_cotacoes is not None:
        # Renomeando as colunas
        df_cotacoes = df_cotacoes.rename(columns={
            "index": "index", 
            "High": "preco_max", 
            "Low": "preco_min",
            "Open": "preco_abertura",
            "Close": "preco_fechamento",
            "Volume": "vol_negocios",
            #"Adj Close": "preco_fechamento_ajustado",
            "ticker": "sigla_acao", 
            "Dividends": "dividendos", 
            "Stock Splits": "desdobramento"
        })

        df_cotacoes = df_cotacoes.sort_values(by=['sigla_acao', 'data_pregao'])
        print("verificação inicial")
        print(list(df_cotacoes.columns))
        print(df_cotacoes.head(20))
        


        
        # Truncando a tabela antes de inserir novos dados
        print("\nLimpando a tabela DadosAcoes...")
        DadosAcoes.objects.all().delete()
        # Reset the auto-increment counter
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'dados_acoes'")
        print("Tabela DadosAcoes limpa com sucesso!")

        # Salvando no banco de dados
        print("\nSalvando dados no banco de dados...")
        for _, row in df_cotacoes.iterrows():
            DadosAcoes.objects.create(
                index=row['index'],
                data_pregao=row['data_pregao'].date(),
                preco_max=row['preco_max'],
                preco_min=row['preco_min'],
                preco_abertura=row['preco_abertura'],
                preco_fechamento=row['preco_fechamento'],
                vol_negocios=row['vol_negocios'],
                #preco_fechamento_ajustado=row['preco_fechamento_ajustado'],
                sigla_acao=row['sigla_acao'],
                dividendos=row['dividendos'],
                desdobramento=row['desdobramento']
            )
        print("Dados salvos com sucesso!")

        # Consultando as 20 primeiras linhas do banco de dados
        print("\nPrimeiras 20 linhas dos dados (consultando o banco de dados):")
        dados_banco = DadosAcoes.objects.all().order_by('sigla_acao', 'data_pregao')[:20]
        
        # Formatando a saída
        print("\n{:<10} {:<12} {:<10} {:<10} {:<10} {:<10} {:<15} {:<10}".format(
            "Index", "Data", "Ação", "Abertura", "Máximo", "Mínimo", "Fechamento", "Volume"
        ))
        print("-" * 80)
        
        for dado in dados_banco:
            print("{:<10} {:<12} {:<10} {:<10.2f} {:<10.2f} {:<10.2f} {:<15.2f} {:<10}".format(
                dado.index,
                dado.data_pregao.strftime('%Y-%m-%d'),
                dado.sigla_acao,
                dado.preco_abertura,
                dado.preco_max,
                dado.preco_min,
                dado.preco_fechamento,
                dado.vol_negocios
            ))
    else:
        print("Não foi possível obter os dados das ações.")

    return df_cotacoes

#historic_data()