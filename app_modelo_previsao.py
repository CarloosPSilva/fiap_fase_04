import streamlit as st
from datetime import datetime, date
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from modelo.carregar_modelo import carregar_e_treinar_modelos, criar_tabela_previsoes


def modelo_de_previsao():
    st.title("🛢️ Projeções do Preço do Petróleo 🔮")
    st.write(
        "Explore as previsões do modelo para o preço do petróleo Brent nos próximos dias e anos, com análise detalhada das tendências."
    )

    # Carregar e treinar os modelos
    df, prophet, model_xgb, test, prophet_future = carregar_e_treinar_modelos()

    # Converter as colunas para datetime
    df["Data"] = pd.to_datetime(df["Data"])
    prophet_future["ds"] = pd.to_datetime(prophet_future["ds"])

    ultima_data_real = df["Data"].max()
    future_df = prophet_future[prophet_future["ds"] > ultima_data_real][
        ["ds", "yhat"]
    ].rename(columns={"ds": "Data", "yhat": "Preço Previsto"})

    df_completo = pd.concat([df, future_df]).reset_index(drop=True)

    if "data_inicio" not in st.session_state:
        st.session_state["data_inicio"] = date.today()

    if "dias_futuros" not in st.session_state:
        st.session_state["dias_futuros"] = 30

    anos_marcados = list(range(2005, 2027))

    st.write("### Gráfico de Preço Real vs. Preço Previsto")
    fig1 = px.line(
        df_completo,
        x="Data",
        y=["Preço Real", "Preço Previsto"],
        labels={"value": "Preço (US$)", "variable": "Legenda"},
        title="Preço Real vs. Preço Previsto",
        color_discrete_map={
            "Preço Real": "#D7263D",
            "Preço Previsto": "blue",
        },
    )

    fig1.update_layout(
        xaxis_title="Data",
        yaxis_title="Preço (US$)",
        legend_title="Legenda",
        hovermode="x unified",
        xaxis=dict(
            tickmode="array",
            tickvals=pd.to_datetime([f"{ano}-01-01" for ano in anos_marcados]),
            tickformat="%Y",
        ),
    )

    st.plotly_chart(fig1)

    data_limite = date(2026, 12, 31)

    data_inicio = st.date_input(
        "📅 Selecione a data inicial para as previsões:",
        min_value=date.today(),
        max_value=data_limite,
        value=st.session_state["data_inicio"],
    )

    st.session_state["data_inicio"] = data_inicio
    
    dias_maximos = (data_limite - data_inicio).days

    dias_futuros = st.number_input(
        "Número de dias para prever:",
        min_value=1,
        max_value=dias_maximos,
        value=st.session_state["dias_futuros"],
    )


    st.session_state["dias_futuros"] = dias_futuros
    
    if dias_futuros > dias_maximos:
        st.warning(f"O número máximo de dias permitido é {dias_maximos}. Selecione um valor dentro do limite.")

    try:
        tabela_previsoes = criar_tabela_previsoes(
            data_inicio.strftime("%Y-%m-%d"), dias_futuros, df
        )
        st.write("### Tabela de Previsões Futuras")
        st.dataframe(tabela_previsoes, height=400, use_container_width=True)

        st.write("### Gráfico de Previsões Futuras")
        fig2 = go.Figure()
        fig2.add_trace(
            go.Scatter(
                x=tabela_previsoes["Data"],
                y=tabela_previsoes["Preço Previsto"],
                mode="lines",
                name="Preço Previsto",
                line=dict(color="blue", width=2),
            )
        )
        fig2.add_trace(
            go.Scatter(
                x=tabela_previsoes["Data"],
                y=tabela_previsoes["Intervalo Superior (95%)"],
                fill=None,
                mode="lines",
                line=dict(width=0),
                showlegend=False,
            )
        )
        fig2.add_trace(
            go.Scatter(
                x=tabela_previsoes["Data"],
                y=tabela_previsoes["Intervalo Inferior (95%)"],
                fill="tonexty",
                mode="lines",
                line=dict(width=0),
                name="Intervalo de Confiança (95%)",
                fillcolor="rgba(128, 128, 128, 0.3)",
            )
        )
        fig2.update_layout(
            title="Previsões Futuras do Preço do Petróleo",
            xaxis_title="Data",
            yaxis_title="Preço (US$)",
            hovermode="x unified",
        )
        st.plotly_chart(fig2)
    except Exception as e:
        st.error(f"Erro ao criar previsões: {e}")


# Executar a função principal
if __name__ == "__main__":
    modelo_de_previsao()
