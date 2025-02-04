import streamlit as st
from PIL import Image
import pandas as pd
import threading

from operacoes.app_estrategia_deploy import detalhe_deploy
from operacoes.app_modelo_previsao import modelo_de_previsao
from operacoes.carregar_tabela import carregar_base_dados
from operacoes.utils import style
from operacoes.app_detalhe_previsao import detalhe_previsao
from operacoes.app_analise_historica import analises_historicas


st.set_page_config(
    page_title="Dashboard - Análise e Previsão do Petróleo Brent",
    layout="wide",
    menu_items={"About": "Desenvolvido por Carlos Silva"},
)

style()

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

# 🔹 Inicializa a Previsão Automaticamente (Assíncrono)
def carregar_modelo():
    with st.spinner("🔄 Carregando modelo de previsão... Isso pode levar alguns segundos."):
        if "previsao_carregada" not in st.session_state:
            modelo_de_previsao()
            st.session_state["previsao_carregada"] = True

# 🔹 Inicia a carga do modelo em paralelo
if "previsao_carregada" not in st.session_state:
    threading.Thread(target=carregar_modelo).start()


# Menu de navegação
if choice == "🏠 Visão Geral":
    st.markdown("# **Tech Challenge: Previsão do Preço do Petróleo Brent**")

    st.markdown(
        "### **Construção e Avaliação de um Modelo de Previsão do Preço do Petróleo**"
    )

    st.markdown("---")

    st.markdown("### **Elaborado por:**")
    st.markdown(
        "**Carlos Pereira da Silva**  \nEngenheiro de Dados e Analista de Dados, atualmente cursando pós-graduação em Data Analytics."
    )

    st.markdown("### **Registro:**")
    st.markdown("**RM: 123456**")

    st.markdown("---")

    st.markdown(
        """
    Este estudo foi desenvolvido como parte do Tech Challenge da **FIAP**, na quarta fase do curso de pós-graduação em **Data Analytics**, 
    com o objetivo de:
    """
    )

    st.markdown(
        """
    1. **Analisar os dados históricos do preço do petróleo Brent (2005–2025):**  
       Explorando como eventos históricos, econômicos e geopolíticos influenciaram o preço do petróleo.
    
    2. **Construir e avaliar um modelo preditivo:**  
       Aplicando técnicas de Machine Learning para prever o preço do petróleo com base em séries temporais.
    
    3. **Gerar insights relevantes:**  
       Identificando padrões e tendências que possam apoiar tomadas de decisões estratégicas em cenários globais.
    """
    )

    st.markdown("---")

    st.markdown("## **Introdução**")
    st.markdown(
        """
    O preço do petróleo Brent é um dos principais indicadores da economia global, impactando decisões estratégicas em diversos setores. 
    Sua variação é influenciada por fatores como:
    
    - **Eventos Geopolíticos:** Conflitos e negociações internacionais.
    - **Crises Econômicas:** Recessões globais e choques financeiros.
    - **Demanda Energética:** Mudanças no consumo global de energia, incluindo avanços em energias renováveis.
    
    Este trabalho busca entender esses impactos e fornecer previsões futuras que possam auxiliar em decisões estratégicas.
    """
    )

    st.markdown("---")


elif choice == "📊 Análises Históricas":
    df = carregar_base_dados()
    analises_historicas(df)

elif choice == "🤖 Modelo de Previsão":
    detalhe_previsao()

elif choice == "📈 Resultados e Predições":
    modelo_de_previsao()

elif choice == "🚀 Estratégia de Deploy":
    detalhe_deploy()


# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown("**Desenvolvido por Carlos Pereira Silva**")
