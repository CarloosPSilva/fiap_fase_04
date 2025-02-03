import streamlit as st


def detalhe_previsao():
    st.title("📊 Detalhe do Modelo de Previsão")
    st.write(
        """
    **Detalhamento do modelo de Machine Learning utilizado para prever o preço do petróleo Brent.**
    """
    )

    st.markdown("---")
    st.header("📏 Métricas de Desempenho")
    st.write(
        """
    Abaixo estão as métricas de desempenho do modelo ajustado:
    """
    )

    # Valores das métricas
    rmse_ajustado = 5.346641716678905
    mae_ajustado = 2.7844824427972106
    mape_ajustado = 5.854750854854621

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="RMSE", value=f"{rmse_ajustado:.2f}")
    with col2:
        st.metric(label="MAE", value=f"{mae_ajustado:.2f}")
    with col3:
        st.metric(label="MAPE", value=f"{mape_ajustado:.2f}%")
    st.markdown("---")

    st.header("🎯 Analise do Modelo")
    st.write(
        """
    O preço do petróleo Brent é altamente volátil e influenciado por diversos fatores, como:
    - 🌍 Geopolítica global
    - 📈 Demanda e oferta
    - 💰 Fatores econômicos
    - 🛢️ Eventos climáticos e desastres naturais

    Para auxiliar na tomada de decisões, desenvolvemos um modelo de previsão que combina técnicas de **Machine Learning** e **Análise de Séries Temporais**.
    """
    )

    st.markdown("---")

    st.header("⚙️ Como o Modelo Funciona")
    st.write(
        """
    O modelo utiliza uma abordagem híbrida, combinando duas técnicas principais:
    """
    )

    st.subheader("1. Prophet (Facebook)")
    st.write(
        """
    - **Prophet** é uma ferramenta de previsão de séries temporais desenvolvida pelo Facebook.
    - Ele é capaz de capturar tendências, sazonalidades e feriados automaticamente.
    - No nosso modelo, o Prophet é usado para gerar uma previsão inicial do preço do petróleo.
    """
    )

    st.subheader("2. XGBoost (Extreme Gradient Boosting)")
    st.write(
        """
    - **XGBoost** é um algoritmo de Machine Learning baseado em árvores de decisão.
    - Ele é usado para corrigir os resíduos (erros) da previsão do Prophet.
    - Isso melhora a precisão do modelo, especialmente em cenários complexos.
    """
    )

    st.markdown("---")

    st.header("📂 Fluxo do Modelo")
    st.write(
        """
    O modelo segue os seguintes passos:
    """
    )

    st.subheader("1. Pré-processamento dos Dados")
    st.write(
        """
    - 📅 Criação de features de calendário (ano, mês, dia, dia da semana).
    - 📊 Cálculo da média móvel de 12 meses como baseline.
    - 🧹 Tratamento de valores ausentes e outliers.
    """
    )

    st.subheader("2. Treinamento do Prophet")
    st.write(
        """
    - O Prophet é treinado com os dados históricos de preço do petróleo.
    - Ele gera previsões iniciais e intervalos de confiança.
    """
    )

    st.subheader("3. Cálculo dos Resíduos")
    st.write(
        """
    - Os resíduos (diferença entre o valor real e a previsão do Prophet) são calculados.
    - Esses resíduos são usados como alvo para o modelo XGBoost.
    """
    )

    st.subheader("4. Treinamento do XGBoost")
    st.write(
        """
    - O XGBoost é treinado para prever os resíduos com base em features como:
        - Lags dos resíduos (valores passados).
        - Features de calendário.
    """
    )

    st.subheader("5. Previsão Final")
    st.write(
        """
    - A previsão final é a soma da previsão do Prophet e da correção feita pelo XGBoost.
    - Isso resulta em uma previsão mais precisa e robusta.
    """
    )

    st.markdown("---")

    st.header("🚀 Como Usar o Modelo")
    st.write(
        """
    - O modelo pode ser usado para prever o preço do petróleo Brent em datas futuras.
    - Basta carregar os dados históricos e executar o pipeline de previsão.
    - As previsões são salvas em um arquivo CSV para análise posterior.
    """
    )

    st.markdown("---")

    st.header("🎉 Conclusão")
    st.write(
        """
    Este modelo combina a robustez do Prophet para capturar padrões temporais com a capacidade do XGBoost de corrigir erros.
    O resultado é uma previsão mais precisa e confiável, que pode ser usada para auxiliar na tomada de decisões estratégicas.
    """
    )


if __name__ == "__main__":
    detalhe_previsao()
