import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


def analises_historicas(df):
    st.title("📊 Dashboard Interativo: Preço do Petróleo Brent")
    st.write(
        """
    Este dashboard apresenta uma análise detalhada da variação do preço do petróleo Brent ao longo do tempo.
    Explore os gráficos interativos e descubra como eventos geopolíticos, crises econômicas e a demanda global por energia impactaram os preços.
    """
    )
    st.markdown("---")

    # 1. Evolução do preço ao longo do tempo com eventos geopolíticos
    st.header("🌍 Evolução do Preço com Eventos Geopolíticos")
    st.write(
        """
    O preço do petróleo é altamente sensível a eventos geopolíticos. Este gráfico mostra a evolução do preço do Brent, destacando:
    - **Crise Financeira de 2008**: A queda drástica no preço devido à recessão global.
    - **Pandemia de COVID-19 (2020)**: A queda histórica nos preços devido à redução da demanda global.
    - **Guerra na Ucrânia (2022)**: Aumento nos preços devido à incerteza no fornecimento.
    """
    )

    fig1 = px.line(
        df,
        x="Data",
        y="Preço (US$)",
        title="Evolução do Preço do Petróleo Brent com Eventos Geopolíticos",
        color_discrete_sequence=["#D7263D"],
    )

    eventos = {
        "2008-09-15": ("Crise Financeira 2008", "yellow"),
        "2020-03-01": ("COVID-19", "blue"),
        "2022-02-24": ("Guerra Ucrânia", "green"),
    }

    for data, (texto, cor) in eventos.items():
        fig1.add_vline(x=pd.Timestamp(data), line_dash="dash", line_color=cor)
        fig1.add_annotation(
            x=pd.Timestamp(data),
            y=df["Preço (US$)"].max(),
            text=texto,
            showarrow=True,
            arrowhead=2,
            font=dict(color=cor),
        )

    fig1.update_layout(
        xaxis_title="Ano",
        yaxis_title="Preço (US$)",
        hovermode="x unified",
        template="plotly_dark",
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.write(
        """
    **Insights:**
    - A **Crise Financeira de 2008** causou uma queda abrupta no preço do petróleo, refletindo a recessão global.
    - Durante a **Pandemia de COVID-19**, o preço caiu drasticamente devido à redução da demanda por combustíveis.
    - A **Guerra na Ucrânia** em 2022 levou a um aumento nos preços, refletindo incertezas no fornecimento global.
    """
    )
    st.markdown("---")

    # 2. Variação percentual mensal do preço
    st.header("📈 Variação Percentual Mensal")

    df["Variação (%)"] = df["Preço (US$)"].pct_change() * 100

    # Criando o gráfico
    fig2 = px.line(
        df,
        x="Data",
        y="Variação (%)",
        title="Variação Percentual Mensal do Preço do Petróleo",
        line_shape="spline",
        template="plotly_dark",
        color_discrete_sequence=["#D7263D"],  # Vermelho FIAP
    )

    fig2.add_hline(y=0, line_dash="dash", line_color="gray")

    # Ajustando layout para melhor visualização
    fig2.update_layout(
        xaxis_title="Ano", yaxis_title="Variação (%)", hovermode="x unified"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.write(
        """
    **Insights:**
    - A volatilidade do preço do petróleo é evidente, com picos e quedas significativos ao longo do tempo.
    - Períodos de alta volatilidade estão frequentemente associados a eventos globais, como crises econômicas e conflitos geopolíticos.
    - A linha tracejada em 0% ajuda a identificar períodos de aumento ou queda nos preços.
    """
    )
    st.markdown("---")

    # 3. Preço médio anual com destaques para crises
    st.header("📉 Preço Médio Anual com Destaque para Crises")

    df["Ano"] = df["Data"].dt.year

    # Calcular o preço médio por ano
    df_media_anual = df.groupby("Ano")["Preço (US$)"].mean().reset_index()

    # Criar o gráfico de barras
    fig3 = px.bar(
        df_media_anual,
        x="Ano",
        y="Preço (US$)",
        title="Preço Médio Anual do Petróleo com Destaque para Crises",
        color_discrete_sequence=["#D7263D"],  # Cor das barras
    )

    eventos = {
        2008: ("Crise Financeira 2008", "#FFD700"),  # Amarelo
        2020: ("COVID-19", "#1E90FF"),  # Azul
        2022: ("Guerra Ucrânia", "#32CD32"),  # Verde
    }

    for ano, (evento, cor) in eventos.items():
        fig3.add_vline(x=ano, line_dash="dash", line_color=cor)
        fig3.add_annotation(
            x=ano,
            y=df_media_anual["Preço (US$)"].max()
            * 1.05,  # Ajusta a posição para melhor visibilidade
            text=evento,
            showarrow=True,
            arrowhead=2,
            font=dict(color=cor, size=12),
        )

    fig3.update_layout(
        xaxis_title="Ano", yaxis_title="Preço Médio (US$)", template="plotly_dark"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.write(
        """
    **Insights:**
    - O preço médio anual mostra tendências de longo prazo, destacando os impactos de crises econômicas e eventos globais.
    - A **Crise Financeira de 2008** resultou em uma queda significativa no preço médio.
    - A **Pandemia de COVID-19** causou uma redução drástica no preço médio em 2020.
    - A **Guerra na Ucrânia** em 2022 levou a um aumento no preço médio devido à incerteza no fornecimento.
    """
    )
    st.markdown("---")

    # 4. Impacto da Crise Financeira de 2008
    st.header("📊 Impacto da Crise Financeira de 2008")

    # Filtrar os dados entre 2007 e 2009
    df_crise_2008 = df[(df["Data"] >= "2007-01-01") & (df["Data"] <= "2009-12-31")]

    fig4 = px.line(
        df_crise_2008,
        x="Data",
        y="Preço (US$)",
        title="Preço do Petróleo Antes e Após a Crise de 2008",
        color_discrete_sequence=["#D7263D"],
    )

    # Adicionar linha vertical e anotação para a crise de 2008
    fig4.add_vline(
        x=pd.Timestamp("2008-09-15"), line_dash="dash", line_color="#FFD700"
    )  # Amarelo
    fig4.add_annotation(
        x=pd.Timestamp("2008-09-15"),
        y=df_crise_2008["Preço (US$)"].max() * 1.05,
        text="Crise 2008",
        showarrow=True,
        arrowhead=2,
        font=dict(color="#FFD700", size=12),
    )

    fig4.update_layout(
        xaxis_title="Ano", yaxis_title="Preço (US$)", template="plotly_dark"
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.write(
        """
    **Insights:**
    - A **Crise Financeira de 2008** causou uma queda abrupta no preço do petróleo, refletindo a recessão global.
    - Antes da crise, os preços estavam em alta, mas caíram drasticamente após setembro de 2008.
    - Este gráfico mostra o impacto imediato e duradouro da crise no mercado de petróleo.
    """
    )
    st.markdown("---")

    # 5. Distribuição dos preços
    st.header("📊 Distribuição dos Preços")
    fig5 = px.histogram(
        df,
        x="Preço (US$)",
        nbins=30,
        title="Distribuição dos Preços do Petróleo Brent",
        color_discrete_sequence=["#D7263D"],
    )
    fig5.update_layout(
        xaxis_title="Preço (US$)", yaxis_title="Frequência", template="plotly_dark"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.write(
        """
    **Insights:**
    - A distribuição dos preços mostra que a maioria dos valores está concentrada em uma faixa específica.
    - Picos de frequência indicam preços mais comuns, enquanto caudas longas refletem períodos de alta volatilidade.
    - Este gráfico ajuda a entender a dispersão dos preços ao longo do tempo.
    """
    )
    st.markdown("---")


# Exemplo de uso
if __name__ == "__main__":
    df = pd.read_csv("dados_petroleo_brent_2005_2025.csv")
