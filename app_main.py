import streamlit as st
from PIL import Image
import pandas as pd
from operacoes.app_estrategia_deploy import detalhe_deploy
from operacoes.app_modelo_previsao import modelo_de_previsao
from operacoes.app_visao_geral import visao_geral
from operacoes.carregar_tabela import carregar_base_dados
from operacoes.utils import style
from operacoes.app_detalhe_previsao import detalhe_previsao
from operacoes.app_analise_historica import analises_historicas


st.set_page_config(
    page_title="Dashboard - Análise e Previsão do Petróleo Brent",
    layout="wide",
    menu_items={"About": "Desenvolvido por Carlos Silva"},
)

# style()

img = Image.open("imagens/tx1.png")


largura_original, altura_original = img.size

nova_altura = 150


nova_largura = int((nova_altura / altura_original) * largura_original)

# Redimensionar a imagem
img_resized = img.resize((nova_largura, nova_altura))


st.sidebar.image(img_resized)

st.sidebar.markdown("## **MENU NAVEGAÇÃO**")

menu = [
    "🏠 Visão Geral",
    "📊 Análises Históricas",
    "🤖 Modelo de Previsão",
    "📈 Resultados e Predições",
    "🚀 Estratégia de Deploy",
]
choice = st.sidebar.selectbox("", menu)

st.sidebar.markdown("---")
st.sidebar.image("imagens/rb_50948.png")


# Menu de navegação
if choice == "🏠 Visão Geral":
    visao_geral()

elif choice == "📊 Análises Históricas":
    df = carregar_base_dados()
    # df = pd.read_csv("dados/dados_petroleo_brent_2005_2025.csv")
    analises_historicas(df)

elif choice == "🤖 Informações do Modelo":
    detalhe_previsao()

elif choice == "📈 Resultados e Predições":
    modelo_de_previsao()

elif choice == "🚀 Estratégia de Deploy":
    detalhe_deploy()


st.sidebar.markdown("---")
st.sidebar.markdown("**Desenvolvido por Carlos Pereira Silva**")

