import streamlit as st

def visao_geral():
    st.title("🏆 Tech Challenge: Previsão do Preço do Petróleo Brent")

    st.subheader("📌 Construção e Avaliação de um Modelo de Previsão do Preço do Petróleo")

    st.markdown("---")

    # 🔹 Apresentação
    st.markdown("### **👤 Desenvolvido por:**")
    st.markdown(
        "**Carlos Pereira da Silva**  \nEngenheiro de Dados e Analista de Dados, atualmente cursando pós-graduação em Data Analytics."
    )

    # st.markdown("### **📌 Registro:**")
    # st.markdown("**RM: 123456**")

    st.markdown("---")

    # 🔹 Contexto do Problema
    st.markdown("## **O Problema**")
    st.markdown(
        """
        Fui contratado para atuar em um projeto de consultoria com o objetivo de analisar o preço do petróleo Brent.  
        O cliente solicitou um **dashboard interativo** e um **modelo preditivo** utilizando dados históricos do IPEA, que contêm apenas duas colunas: **Data** e **Preço (US$)**.

        O objetivo do projeto é:
        - 📊 **Gerar insights relevantes** sobre as variações do preço do petróleo, considerando fatores como **eventos geopolíticos, crises econômicas e demanda global por energia**.
        - 🔮 **Desenvolver um modelo de previsão** que forneça estimativas diárias do preço do petróleo com base em **séries temporais**.
        - 🚀 **Criar um MVP funcional** utilizando **Streamlit Cloud**, garantindo um fluxo otimizado para acesso e análise dos resultados.

        O desafio está em desenvolver um modelo que seja robusto o suficiente para captar as oscilações do mercado e fornecer previsões precisas.
        """
    )

    st.markdown("---")

    # 🔹 Objetivos do Projeto
    st.markdown("## **🎯 Objetivos**")
    st.markdown(
        """
        O estudo foi desenvolvido dentro do **Tech Challenge da FIAP**, com os seguintes objetivos principais:
        
        1️⃣ **Explorar os dados históricos (2005–2025):**  
           Analisar como os preços do petróleo foram impactados ao longo do tempo por diferentes cenários globais.

        2️⃣ **Construir um modelo preditivo eficiente:**  
           Aplicar técnicas de Machine Learning para gerar previsões confiáveis.

        3️⃣ **Gerar insights estratégicos:**  
           Identificar padrões e tendências que auxiliem na **tomada de decisão**.

        4️⃣ **Implementar um MVP funcional:**  
           Criar um **dashboard interativo** para visualização das análises e previsões.
        """
    )

    st.markdown("---")

    # 🔹 Introdução ao Tema
    st.markdown("## **🌎 Introdução**")
    st.markdown(
        """
        O petróleo Brent é um dos principais **indicadores econômicos globais**, impactando diretamente diversos setores.  
        Sua variação de preço é influenciada por fatores como:

        - **🌍 Eventos Geopolíticos:** Conflitos, negociações e sanções internacionais.
        - **📉 Crises Econômicas:** Recessões globais e oscilações no mercado financeiro.
        - **⚡ Demanda Global por Energia:** Mudanças no consumo e avanço de energias renováveis.

        A proposta do estudo é entender esses fatores e construir um modelo que auxilie empresas e investidores a **antecipar variações nos preços do petróleo**.
        """
    )

    st.markdown("---")

    # 🔹 Estrutura do Dashboard
    st.markdown("## **📊 Estrutura do Dashboard**")
    st.markdown(
        """
        O dashboard desenvolvido foi estruturado da seguinte forma:

        🔎 **📊 Análises Históricas:**  
        - Exploração detalhada dos dados históricos do petróleo Brent.
        - Análises sobre eventos geopolíticos e crises econômicas.

        🔮 **🤖 Modelo de Previsão:**  
        - Explicação sobre a construção do modelo de Machine Learning.
        - Avaliação da performance do modelo.

        📈 **📊 Resultados e Predições:**  
        - Visualização das previsões futuras do modelo.
        - Comparação entre os valores reais e previstos.

        🚀 **📦 Estratégia de Deploy:**  
        - Plano de deploy para produção do modelo.
        - Ferramentas utilizadas para garantir a acessibilidade e disponibilidade do serviço.
        """
    )

    st.markdown("---")

    st.success("✅ Tudo pronto! Utilize o menu lateral para navegar pelo dashboard.")