
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, OrdinalEncoder
import streamlit as st


# Classes para pipeline

class DropFeatures(BaseEstimator,TransformerMixin):
    def __init__(self,feature_to_drop = ['ID_Cliente']):
        self.feature_to_drop = feature_to_drop
    def fit(self,df):
        return self
    def transform(self,df):
        if (set(self.feature_to_drop).issubset(df.columns)):
            df.drop(self.feature_to_drop,axis=1,inplace=True)
            return df
        else:
            print('Uma ou mais features não estão no DataFrame')
            return df

class OneHotEncodingNames(BaseEstimator,TransformerMixin):
    def __init__(self,OneHotEncoding = ['Estado_civil', 'Moradia', 'Categoria_de_renda', 
                                        'Ocupacao']):                                      
                                                                               
        self.OneHotEncoding = OneHotEncoding

    def fit(self,df):
        return self

    def transform(self,df):
        if (set(self.OneHotEncoding).issubset(df.columns)):
            # função para one-hot-encoding das features
            def one_hot_enc(df,OneHotEncoding):
                one_hot_enc = OneHotEncoder()
                one_hot_enc.fit(df[OneHotEncoding])
                # obtendo o resultado dos nomes das colunas
                feature_names = one_hot_enc.get_feature_names_out(OneHotEncoding)
                # mudando o array do one hot encoding para um dataframe com os nomes das colunas
                df = pd.DataFrame(one_hot_enc.transform(df[self.OneHotEncoding]).toarray(),
                                  columns= feature_names,index=df.index)
                return df

            # função para concatenar as features com aquelas que não passaram pelo one-hot-encoding
            def concat_with_rest(df,one_hot_enc_df,OneHotEncoding):              
                
                outras_features = [feature for feature in df.columns if feature not in OneHotEncoding]
                # concaternar o restante das features com as features que passaram pelo one-hot-encoding
                df_concat = pd.concat([one_hot_enc_df, df[outras_features]],axis=1)
                return df_concat

            # one hot encoded dataframe
            df_OneHotEncoding = one_hot_enc(df,self.OneHotEncoding)

            # retorna o dataframe concatenado
            df_full = concat_with_rest(df, df_OneHotEncoding,self.OneHotEncoding)
            return df_full

class OrdinalFeature(BaseEstimator,TransformerMixin):
    def __init__(self,ordinal_feature = ['Grau_escolaridade']):
        self.ordinal_feature = ordinal_feature
    def fit(self,df):
        return self
    def transform(self,df):
        if 'Grau_escolaridade' in df.columns:
            ordinal_encoder = OrdinalEncoder()
            df[self.ordinal_feature] = ordinal_encoder.fit_transform(df[self.ordinal_feature])
            return df
        else:
            print('Grau_escolaridade não está no DataFrame')
            return df

class MinMaxWithFeatNames(BaseEstimator,TransformerMixin):
    def __init__(self,min_max_scaler_ft = ['Idade', 'Rendimento_anual', 'Tamanho_familia', 'Anos_empregado']):
        self.min_max_scaler_ft = min_max_scaler_ft
    def fit(self,df):
        return self
    def transform(self,df):
        if (set(self.min_max_scaler_ft).issubset(df.columns)):
            min_max_enc = MinMaxScaler()
            df[self.min_max_scaler_ft] = min_max_enc.fit_transform(df[self.min_max_scaler_ft])
            return df
        else:
            print('Uma ou mais features não estão no DataFrame')
            return df
        
        
def style():
    st.markdown(
        """
        <style>
        /* Sidebar com fundo cinza escuro */
        [data-testid="stSidebar"] {
            display: flex;
            background-color: #3A3A3A !important; /* Cinza chumbo */
            color: white !important;
            flex-direction: column;
            align-items: center;
        }

        /* Classe exclusiva para o menu de navegação */
        .menu-navegacao {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px; /* Espaçamento inferior */
            padding: 10px;
            background-color: #2C2C2C; /* Cor de fundo */
            border-radius: 5px;
            color: white;
            width: 90%;
        }

        /* Ajuste no dropdown do menu lateral */
        div[data-testid="stSidebar"] select {
            background-color: #FFFFFF;
            color: #333333;
            font-weight: bold;
            border-radius: 5px;
            border: 2px solid #D7263D;  /* Aumenta a borda do menu */
        }

        /* Hover no menu lateral */
        div[data-testid="stSidebar"] select:hover {
            background-color: #8B0000 !important;  /* Vermelho escuro no hover */
            color: white !important;
        }

        /* Hover nos itens do menu lateral */
        div[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] div:hover {
            background-color: #444444 !important; /* Cinza escuro no hover */
            color: white !important;
            border-radius: 5px;
        }

        /* Ajuste no título principal */
        .stApp h1 {
            color: #D7263D;
            margin-top: 30px; /* Empurra o título um pouco para baixo */
            text-align: center;
        }

        /* Ajuste no subtítulo */
        .stApp h2, .stApp h3 {
            margin-top: 20px; /* Adiciona espaçamento para evitar sobreposição */
        }

        /* Botões estilizados */
        .stButton>button {
            background-color: #D7263D;
            color: white;
            border-radius: 10px;
            font-weight: bold;
            transition: 0.3s;
            padding: 8px 15px;
            border: none;
        }

        /* Efeito hover nos botões */
        .stButton>button:hover {
            background-color: #C00021; /* Vermelho mais escuro no hover */
            color: white;
            transform: scale(1.05); /* Efeito de leve crescimento */
        }

        /* Ajustar a cor do texto no corpo da tabela */
        .stDataFrame div[data-testid="stVerticalBlock"] div {
            color: white !important;
            font-size: 14px !important;
            font-weight: bold !important;
        }
        
        /* Ajustar a cor do cabeçalho da tabela */
        .stDataFrame [data-testid="stTable"] thead tr th {
            background-color: #660000 !important; /* Vermelho escuro da FIAP */
            color: white !important;
            font-weight: bold !important;
            text-align: center !important;
            padding: 10px !important;
        }

        /* Ajustar a cor do fundo da tabela */
        .stDataFrame {
            background-color: rgba(0, 0, 0, 0.9) !important;
        }

        /* Ajustar a cor do fundo das células */
        .stDataFrame td {
            background-color: rgba(0, 0, 0, 0.8) !important;
            color: white !important;
            text-align: center !important;
            font-weight: bold !important;
        }
        /* Ajusta a cor e tamanho dos valores das métricas */
        div[data-testid="stMetricValue"] {
            font-size: 50px !important;  /* Aumenta a fonte */
            font-weight: bold !important;
            color: #D7263D !important;  /* Vermelho FIAP */
        }

        /* Ajusta o tamanho do texto das labels das métricas */
        div[data-testid="stMetricLabel"] {
            font-size: 18px !important;
            font-weight: bold !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )