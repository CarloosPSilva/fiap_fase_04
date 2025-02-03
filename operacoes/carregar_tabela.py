import requests
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

def carregar_base_dados():
    url = "http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view"

    try:
        # Tenta acessar a API e carregar os dados
        response = requests.get(url, timeout=10)  # Timeout de 10 segundos para evitar travamento

        if response.status_code == 200:
            # st.success("Página acessada com sucesso.")
            soup = BeautifulSoup(response.content, "html.parser")

            # Procurar a tabela na página
            table = soup.find("table", {"class": "dxgvTable"})

            if table:
                # st.success("Tabela encontrada, iniciando o carregamento...")
                df = pd.read_html(str(table))[0]
                df.columns = ["Data", "Preço (US$)"]

                # Processamento dos dados
                df = df[df["Data"].str.match(r"\d{2}/\d{2}/\d{4}", na=False)]
                df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y", errors="coerce")
                df["Preço (US$)"] = df["Preço (US$)"].str.replace(",", ".").astype(float) / 100

                # Filtrar período de 2005 a 2025
                df = df[(df["Data"] >= "2005-01-01") & (df["Data"] <= "2025-12-31")]
                df.reset_index(drop=True, inplace=True)

                return df

            else:
                raise ValueError("Tabela não encontrada na página.")

        else:
            raise ConnectionError(f"Erro ao acessar a página. Código: {response.status_code}")

    except Exception as e:
        # Se ocorrer um erro, tenta carregar o arquivo local
        st.error(f"Erro ao acessar a API: {e}")
        try:
            df = pd.read_csv("dados/dados_petroleo_brent_2005_2025.csv")
            st.warning("Carregando dados do arquivo local.")
            return df
        except FileNotFoundError:
            st.error("Erro: O arquivo local não foi encontrado.")
            return None

# # Executar a função
# df = acessando_base_dados()

# # Exibir as primeiras linhas do DataFrame
# if df is not None:
#     print(df.head())  # ✅ Correto