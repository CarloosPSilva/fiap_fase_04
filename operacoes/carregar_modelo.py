import pandas as pd
from prophet import Prophet
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from operacoes.carregar_tabela import carregar_base_dados
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date
import os
import joblib
import streamlit as st


@st.cache_data
# Função para carregar os dados e treinar os modelos
def carregar_e_treinar_modelos():
    try:
        # Tenta carregar os dados do arquivo local
        df = pd.read_csv("dados/dados_petroleo_brent_2005_2025.csv")
        # st.success("✅ Dados carregados com sucesso do arquivo local.")
    
    except FileNotFoundError:
        st.warning("⚠️ Arquivo local não encontrado. Tentando carregar da base de dados online...")
        try:
            df = carregar_base_dados()
            # st.success("✅ Dados carregados com sucesso da base de dados online.")
        except Exception as e:
            st.error(f"❌ Erro ao carregar os dados online: {e}")
            return None, None, None, None, None

    # Verificar colunas esperadas
    if "Data" not in df.columns or "Preço (US$)" not in df.columns:
        st.error("O arquivo CSV deve conter as colunas 'Data' e 'Preço (US$)'.")
        return None, None, None, None, None

    # Converter colunas para os tipos corretos
    df["ds"] = pd.to_datetime(df["Data"], errors="coerce")  # Converte para datetime
    df["y"] = pd.to_numeric(df["Preço (US$)"], errors="coerce")  # Converte para numérico

    # Verificar valores ausentes
    if df["ds"].isnull().any() or df["y"].isnull().any():
        st.warning("⚠️ Atenção: Há valores ausentes nas colunas 'Data' ou 'Preço (US$)'. Preenchendo valores ausentes...")
        df["ds"].fillna(method="ffill", inplace=True)  # Preenche datas ausentes
        df["y"].fillna(method="ffill", inplace=True)  # Preenche preços ausentes

    # Ordenar os dados corretamente
    df = df.sort_values(by="ds").reset_index(drop=True)

    # Verificar e remover duplicatas na coluna 'ds' (Data)
    if df.duplicated(subset=["ds"]).any():
        st.warning("⚠️ Atenção: Há duplicatas na coluna 'Data'. Removendo duplicatas...")
        df = df.drop_duplicates(subset=["ds"])

    # Treinar o modelo Prophet
    prophet = Prophet()
    prophet.fit(df[["ds", "y"]])  # Usando apenas as colunas 'ds' e 'y'

    # Definir a data final desejada (31 de dezembro de 2026)
    data_final_desejada = pd.to_datetime("2026-12-31")

    # Calcular o número de dias até a data final desejada
    ultima_data_df = df["ds"].max()
    dias_ate_2026 = (data_final_desejada - ultima_data_df).days

    # Criar previsões do Prophet até o final de 2026
    future = prophet.make_future_dataframe(periods=dias_ate_2026)  # Previsão até 31 de dezembro de 2026
    prophet_future = prophet.predict(future)

    # Mesclar previsões do Prophet com o DataFrame original
    df = df.merge(prophet_future[["ds", "yhat", "yhat_lower", "yhat_upper"]], on="ds", how="left")

    # Verificar duplicatas após a mesclagem
    if df.duplicated(subset=["ds"]).any():
        st.warning("⚠️ Atenção: Há duplicatas após a mesclagem. Removendo duplicatas...")
        df = df.drop_duplicates(subset=["ds"])

    # Renomear as colunas de forma clara e estruturada
    df.rename(columns={"ds": "Data", "y": "Preço Real", "yhat": "US$ Preço Previsto", "yhat_lower": "Intervalo Inferior", "yhat_upper": "Intervalo Superior"}, inplace=True)

    # Remover colunas duplicadas após a renomeação
    df = df.loc[:, ~df.columns.duplicated()]

    # Calcular resíduos (erros) do Prophet
    df["Resíduo"] = df["Preço Real"] - df["US$ Preço Previsto"]

    # Criar features para o modelo XGBoost
    for i in range(1, 8):  # Criar lags de 1 a 7 dias
        df[f"Resíduo_Lag_{i}"] = df["Resíduo"].shift(i)

    # Remover linhas com valores ausentes gerados pelos lags
    df.dropna(inplace=True)

    # Dividir os dados em treino e teste
    train_size = int(len(df) * 0.8)  # 80% para treino, 20% para teste
    train = df.iloc[:train_size]
    test = df.iloc[train_size:]

    # Definir features e target para o XGBoost
    features = [f"Resíduo_Lag_{i}" for i in range(1, 8)]  # Usar os lags como features
    X_train, y_train = train[features], train["Resíduo"]
    X_test, y_test = test[features], test["Resíduo"]

    # Treinar o modelo XGBoost
    model_xgb = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1, random_state=42)
    model_xgb.fit(X_train, y_train)

    # Definir o diretório onde os modelos serão salvos
    modelo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modelo"))

    # Criar diretório caso não exista
    if not os.path.exists(modelo_dir):
        os.makedirs(modelo_dir)

    # Caminhos completos para os arquivos de modelo
    modelo_prophet_path = os.path.join(modelo_dir, "modelo_prophet.pkl")
    modelo_xgb_path = os.path.join(modelo_dir, "modelo_xgboost.pkl")

    # Salvar os modelos treinados
    joblib.dump(prophet, modelo_prophet_path)
    joblib.dump(model_xgb, modelo_xgb_path)
    print(f"✅ Modelos salvos com sucesso em: {modelo_dir}")

    return df, prophet, model_xgb, test, prophet_future


# Função para criar tabela de previsões


def criar_tabela_previsoes(data_inicio, dias_futuros, df_inicial):
    """
    Função para criar uma tabela de previsões a partir de uma data específica.
    :param data_inicio: Data inicial no formato 'YYYY-MM-DD'.
    :param dias_futuros: Número de dias para prever no futuro.
    :param df_inicial: DataFrame inicial com os dados históricos.
    :return: DataFrame com as previsões.
    # Obter o diretório do script atual"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modelo"))


    modelo_prophet_path = os.path.join(base_dir, "modelo_prophet.pkl")
    modelo_xgb_path = os.path.join(base_dir, "modelo_xgboost.pkl")


    # Carregar os modelos salvos
    # Carregar os modelos
    prophet = joblib.load(modelo_prophet_path)
    model_xgb = joblib.load(modelo_xgb_path)

    # Criar DataFrame com as datas futuras
    datas_futuras = pd.date_range(start=data_inicio, periods=dias_futuros, freq="D")
    future_df = pd.DataFrame({"ds": datas_futuras})

    # Fazer previsões com o Prophet
    prophet_future = prophet.predict(future_df)

    # Mesclar previsões do Prophet com o DataFrame futuro
    future_df = future_df.merge(
        prophet_future[["ds", "yhat", "yhat_lower", "yhat_upper"]], on="ds", how="left"
    )

    # Calcular resíduos previstos pelo XGBoost
    ultimos_residuos = df_inicial["Resíduo"].tail(7).values
    if len(ultimos_residuos) < 7:
        raise ValueError("Não há dados históricos suficientes para prever o resíduo.")

    # Criar features para o XGBoost
    features_xgb = {f"Resíduo_Lag_{i+1}": ultimos_residuos[-(i + 1)] for i in range(7)}
    features_xgb = pd.DataFrame([features_xgb])

    # Prever o resíduo com o XGBoost
    residuo_previsto = model_xgb.predict(features_xgb)[0]

    # Ajustar as previsões do Prophet com o resíduo previsto
    future_df["US$ Preço Previsto Ajustado"] = future_df["yhat"] + residuo_previsto
    future_df["US$ Preço Previsto Ajustado Inferior"] = (
        future_df["yhat_lower"] + residuo_previsto
    )
    future_df["US$ Preço Previsto Ajustado Superior"] = (
        future_df["yhat_upper"] + residuo_previsto
    )

    # Renomear colunas
    future_df.rename(
        columns={
            "ds": "Data",
            "US$ Preço Previsto Ajustado": "US$ Preço Previsto",
            "US$ Preço Previsto Ajustado Inferior": "US$ Estimativa de Preço Mínima",
            "US$ Preço Previsto Ajustado Superior": "US$ Estimativa de Preço Máxima",
        },
        inplace=True,
    )

    # Formatar a coluna "Data" para o padrão brasileiro (dia/mês/ano)
    future_df["Data"] = future_df["Data"].dt.strftime("%Y/%m/%d")

    # Arredondar os valores para 2 casas decimais
    future_df = future_df.round(2)

    # Selecionar colunas relevantes
    tabela_previsoes = future_df[
        [
            "Data",
            "US$ Preço Previsto",
            "US$ Estimativa de Preço Mínima",
            "US$ Estimativa de Preço Máxima",
        ]
    ]

    return tabela_previsoes