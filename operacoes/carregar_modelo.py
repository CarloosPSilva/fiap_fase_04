import pandas as pd
from prophet import Prophet
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date

import streamlit as st
@st.cache_data
# Função para carregar os dados e treinar os modelos
def carregar_e_treinar_modelos():
    try:
        df = pd.read_csv("dados/dados_petroleo_brent_2005_2025.csv")
        print("Arquivo carregado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        raise

    # Verificar colunas esperadas
    if "Data" not in df.columns or "Preço (US$)" not in df.columns:
        st.error("O arquivo CSV deve conter as colunas 'Data' e 'Preço (US$)'.")
        return None, None, None

    # Converter colunas para os tipos corretos
    df["ds"] = pd.to_datetime(df["Data"], errors="coerce")  # Converte para datetime
    df["y"] = pd.to_numeric(
        df["Preço (US$)"], errors="coerce"
    )  # Converte para numérico

    # Verificar valores ausentes
    if df["ds"].isnull().any() or df["y"].isnull().any():
        st.warning(
            "Atenção: Há valores ausentes nas colunas 'Data' ou 'Preço (US$)'. Preenchendo valores ausentes..."
        )
        df["ds"].fillna(method="ffill", inplace=True)  # Preenche datas ausentes
        df["y"].fillna(method="ffill", inplace=True)  # Preenche preços ausentes

    # Ordenar os dados corretamente
    df = df.sort_values(by="ds").reset_index(drop=True)

    # Verificar e remover duplicatas na coluna 'ds' (Data)
    if df.duplicated(subset=["ds"]).any():
        st.warning("Atenção: Há duplicatas na coluna 'Data'. Removendo duplicatas...")
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
    future = prophet.make_future_dataframe(
        periods=dias_ate_2026
    )  # Previsão até 31 de dezembro de 2026
    prophet_future = prophet.predict(future)

    # Mesclar previsões do Prophet com o DataFrame original
    df = df.merge(
        prophet_future[["ds", "yhat", "yhat_lower", "yhat_upper"]], on="ds", how="left"
    )

    # Verificar duplicatas após a mesclagem
    if df.duplicated(subset=["ds"]).any():
        st.warning("Atenção: Há duplicatas após a mesclagem. Removendo duplicatas...")
        df = df.drop_duplicates(subset=["ds"])

    # Renomear as colunas de forma clara e estruturada
    mapeamento_colunas = {
        "ds": "Data",
        "y": "Preço Real",
        "yhat": "Preço Previsto",
        "yhat_lower": "Intervalo Inferior",
        "yhat_upper": "Intervalo Superior",
    }

    df.rename(columns=mapeamento_colunas, inplace=True)

    # Remover colunas duplicadas após a renomeação
    df = df.loc[:, ~df.columns.duplicated()]

    # Calcular resíduos (erros) do Prophet
    df["Resíduo"] = df["Preço Real"] - df["Preço Previsto"]

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
    X_train = train[features]
    y_train = train["Resíduo"]
    X_test = test[features]
    y_test = test["Resíduo"]

    # Treinar o modelo XGBoost
    model_xgb = xgb.XGBRegressor(
        objective="reg:squarederror",
        n_estimators=100,
        learning_rate=0.1,
        random_state=42,
    )
    model_xgb.fit(X_train, y_train)

    # Salvar os modelos treinados
    joblib.dump(prophet, "modelo/modelo_prophet.pkl")  # Salvar o modelo Prophet
    joblib.dump(model_xgb, "modelo/modelo_xgboost.pkl")   # Salvar o modelo XGBoost
    # st.success("Modelos salvos com sucesso!")

    return df, prophet, model_xgb, test, prophet_future


# Função para criar tabela de previsões


def criar_tabela_previsoes(data_inicio, dias_futuros, df_inicial):
    """
    Função para criar uma tabela de previsões a partir de uma data específica.
    :param data_inicio: Data inicial no formato 'YYYY-MM-DD'.
    :param dias_futuros: Número de dias para prever no futuro.
    :param df_inicial: DataFrame inicial com os dados históricos.
    :return: DataFrame com as previsões.
    """
    # Carregar os modelos salvos
    prophet = joblib.load("modelo/modelo_prophet.pkl")
    model_xgb = joblib.load("modelo/modelo_xgboost.pkl")

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
    future_df["Preço Previsto Ajustado"] = future_df["yhat"] + residuo_previsto
    future_df["Preço Previsto Ajustado Inferior"] = (
        future_df["yhat_lower"] + residuo_previsto
    )
    future_df["Preço Previsto Ajustado Superior"] = (
        future_df["yhat_upper"] + residuo_previsto
    )

    # Renomear colunas
    future_df.rename(
        columns={
            "ds": "Data",
            "Preço Previsto Ajustado": "Preço Previsto",
            "Preço Previsto Ajustado Inferior": "Intervalo Inferior (95%)",
            "Preço Previsto Ajustado Superior": "Intervalo Superior (95%)",
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
            "Preço Previsto",
            "Intervalo Inferior (95%)",
            "Intervalo Superior (95%)",
        ]
    ]

    return tabela_previsoes