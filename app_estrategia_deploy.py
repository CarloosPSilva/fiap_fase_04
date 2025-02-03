import streamlit as st

def detalhe_deploy():
    st.title("🚀 Deploy do Modelo no Streamlit Cloud")
    st.write("""
    Esta página documenta o processo que foi seguido para fazer o deploy do modelo de Machine Learning no **Streamlit Cloud**,
    permitindo que ele seja acessado e utilizado de qualquer lugar.
    """)

    st.subheader("📌 1. Estrutura do Projeto")
    st.write("""
    O projeto foi organizado da seguinte maneira antes do deploy:
    """)

    st.code("""
    📂 MeuProjeto/
    ├── 📄 app_main.py               # Arquivo principal do Streamlit
    ├── 📄 modelo/modelo_ml.pkl         # Modelo de Machine Learning salvo
    ├── 📄 operadoras/app.py   # Código de pré-processamento dos dados
    ├── 📂 dados/                # Pasta com datasets usados (se necessário)
    ├── 📄 requirements.txt      # Lista de dependências
    ├── 📄 .gitignore            # Arquivos que não devem ser versionados
    ├── 📄 README.md             # Documentação do projeto
    """, language="plaintext")

    st.subheader("🔄 2. Versionamento do Código no GitHub")
    st.write("""
    O código foi versionado no GitHub para permitir o deploy no Streamlit Cloud.
    Os seguintes comandos foram utilizados para subir o projeto:
    """)

    st.code("""
    # Inicializar repositório Git
    git init

    # Adicionar arquivos ao repositório
    git add .

    # Criar um commit com a versão inicial
    git commit -m "Versão inicial do projeto"

    # Conectar ao repositório remoto no GitHub (substitua pela sua URL)
    git remote add origin https://github.com/usuario/meu-repositorio.git

    # Enviar os arquivos para o GitHub
    git push -u origin main
    """, language="bash")

    st.subheader("🌐 3. Deploy no Streamlit Cloud")
    st.write("""
    O deploy foi realizado no **Streamlit Cloud**, seguindo os passos abaixo:
    """)

    st.markdown("""
    1. Acesse [Streamlit Cloud](https://streamlit.io/cloud)
    2. Faça login com a conta do **GitHub**
    3. No dashboard, clique em **"New app"**
    4. Escolha o repositório onde o código foi versionado
    5. No campo **"Main file path"**, insira `main.py`
    6. Clique em **"Deploy"** e aguarde o carregamento da aplicação
    """)

    st.subheader("⚙️ 4. Criando o `requirements.txt`")
    st.write("""
    Para garantir que todas as dependências fossem instaladas corretamente no Streamlit Cloud,
    um arquivo `requirements.txt` foi criado com os seguintes pacotes:
    """)

    st.code("""
    streamlit
    pandas
    numpy
    matplotlib
    plotly
    prophet
    xgboost
    joblib
    """, language="plaintext")

    st.write("""
    O arquivo foi gerado automaticamente com:
    """)

    st.code("""
    pip freeze > requirements.txt
    """, language="bash")

    st.subheader("🔄 5. Atualização do Modelo no Deploy")
    st.write("""
    Para atualizar o modelo de Machine Learning no Streamlit Cloud,
    o arquivo `modelo_ml.pkl` foi substituído por um novo modelo e os seguintes comandos foram usados:
    """)

    st.code("""
    # Adicionar o novo modelo ao repositório Git
    git add modelo_ml.pkl

    # Criar um commit com a atualização
    git commit -m "Atualização do modelo de Machine Learning"

    # Enviar a atualização para o GitHub
    git push origin main
    """, language="bash")

    st.write("""
    O **Streamlit Cloud** detectou automaticamente a atualização e recarregou a aplicação.
    Caso necessário, foi possível forçar a atualização clicando em **"Rerun"** no dashboard do Streamlit.
    """)


