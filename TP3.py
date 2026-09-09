import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import re

# Exercício 1
st.write("# Análise de Dados com Streamlit")

st.write("""O motivo da escolha deste dataset A escolha deste dataset baseia-se na relevância 
econômica do turismo para a cidade do Rio de Janeiro. A base de dados oferece métricas claras e 
contínuas (diária média, gasto médio e permanência) distribuídas ao longo de vários meses e anos. 
Isso o torna ideal para a construção de um dashboard interativo no Streamlit, pois permite a exploração 
de sazonalidades, identificando como o comportamento do turista muda em meses de alta 
temporada (como janeiro e fevereiro) comparado ao resto do ano.""")

st.write("""O objetivo principal é desenvolver um painel de inteligência de negócios (dashboard)
interativo que permita ao usuário explorar o histórico financeiro e de ocupação do turismo hoteleiro 
carioca entre 1997 e 2002. A aplicação visa facilitar a visualização da flutuação de preços e do 
tempo de estadia dos visitantes, extraindo insights sobre quais meses atraem turistas que gastam 
mais ou que ficam por mais dias.""")

st.write("## Funcionalidades e Vizualizações que serão implementadas:")
st.write("""* Gráficos de barra usando matplotlib e seaborn para mostrar a distribuição de preços médios por mês e ano.
* Gráficos de linha usando plotly para visualizar a evolução do gasto médio e da permanência ao longo do tempo.
* Filtros interativos para selecionar anos específicos, permitindo uma análise detalhada de períodos específicos.
* Comparação entre diferentes métricas (diária média, gasto médio e permanência) para identificar correlações e tendências.""")


# Exercício 2
st.write("Insira o arquivo para análise:")
arquivo = st.file_uploader('Escolha um arquivo', type=['csv','xlsx', 'xls'])

if arquivo:  
    st.write('Nome do arquivo:', arquivo.name)
    st.write('Tipo do arquivo:', arquivo.type)
    st.write('Tamanho do arquivo:', arquivo.size, 'bytes')

    df = pd.read_excel(arquivo)

    # Processamento/Tratamento dos Dados
    linhas_tratadas = []
    ano_atual = None

    meses_validos = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    for _, linha in df.iterrows():
        primeira_celula = (str(linha.iloc[0]).strip() if pd.notna(linha.iloc[0]) else "")
        
        # Identifica se a linha indica a mudança de Ano 
        if "Média" in primeira_celula:
            busca_ano = re.search(r'\d{4}', primeira_celula)
            if busca_ano:
                ano_atual = int(busca_ano.group(0))
            continue
            
        # Identifica se a linha é um Mês válido e extrai os valores das colunas
        if primeira_celula in meses_validos and ano_atual is not None:
            def para_float(valor):
                try:
                    return float(valor)
                except (ValueError, TypeError):
                    return None

            linhas_tratadas.append({
                "Ano": ano_atual,
                "Mês": primeira_celula,
                "Diária Média (R$)": para_float(linha.iloc[1]),
                "Gasto Médio (R$)": para_float(linha.iloc[2]),
                "Permanência Média (dias)": para_float(linha.iloc[3])
            })
    # 3. Criação do DataFrame limpo e estruturado
    df_limpo = pd.DataFrame(linhas_tratadas)



    # Exercício 3
    st.sidebar.header("Filtros e Configurações")

    # DROPDOWN (Selectbox): Filtrar por Ano
    anos_disponiveis = ["Todos"] + sorted(df_limpo["Ano"].unique().tolist())
    ano_selecionado = st.sidebar.selectbox("1. Selecione o Ano:", anos_disponiveis)

    # RADIO BUTTON: Escolher a Ordenação dos Dados
    ordem_selecionada = st.sidebar.radio(
        "2. Ordenar Diária Média por:",
        options=["Padrão (Cronológica)", "Crescente", "Decrescente"]
    )

    # CHECKBOX: Ocultar dados nulos
    ocultar_nulos = st.sidebar.checkbox("3. Ocultar meses sem informação de Gasto Médio")


    # Exercício 4
    # APLICAÇÃO DOS FILTROS NO DATAFRAME
    df_filtrado = df_limpo.copy()

    # Aplica o Filtro 1 (Dropdown)
    if ano_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Ano"] == ano_selecionado]

    # Aplica o Filtro 2 (Checkbox)
    if ocultar_nulos:
        df_filtrado = df_filtrado.dropna(subset=["Gasto Médio (R$)"])

    # Aplica o Filtro 3 (Radio)
    if ordem_selecionada == "Crescente":
        df_filtrado = df_filtrado.sort_values(by="Diária Média (R$)", ascending=True)
    elif ordem_selecionada == "Decrescente":
        df_filtrado = df_filtrado.sort_values(by="Diária Média (R$)", ascending=False)

    # 5. EXIBIÇÃO DA TABELA FILTRADA
    st.subheader("Tabela de Dados Filtrada")
    st.write(f"Exibindo **{len(df_filtrado)}** registros:")
    st.dataframe(df_filtrado, use_container_width=True)


    # Exercício 5
    st.header("Download de arquivos:")
    st.text("Escolha os dados para baixar:")
    st.download_button("df_filtrado", df_filtrado.to_csv(), file_name='df_filtrado.csv')


    # Exercício 6
    st.header("Barra de Progresso")
    barra = st.progress(0.2, "Progresso", 100)
    i = 0
    for i in range(1, 101, 5):
        time.sleep(0.1)
        barra.progress(i, f"Processando {i}...", 100)
    st.text("Após barra de progressão")

    st.header("Spinner")
    with st.spinner(text="Processando...", show_time=True, 
    width=300):
        time.sleep(3)
    st.text("Após spinner")


    # Exercício 7
    #st.title ("Personalização")
    cor_fundo = st.sidebar.color_picker("Escolha a cor de fundo", "#FFFFFF")
    cor_fonte = st.sidebar.color_picker("Escolha a cor da fonte", "#000000")

    estilo_customizado = f"""
    <style>
    .stApp {{
        background-color: {cor_fundo};
        color: {cor_fonte};
    }}
    /* Garante que títulos e textos comuns respeitem a cor escolhida */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp p, .stApp span, .stApp label {{
        color: {cor_fonte} !important;
    }}
    </style>
    """
    st.markdown(estilo_customizado, unsafe_allow_html=True)


    # Exercício 8
    @st.cache_data(show_spinner=False)
    def carregar_e_tratar_dados(file):
        """
        Função com cache para ler e tratar a planilha apenas uma vez, 
        otimizando a performance em interações futuras.
        """
        df = pd.read_excel(file)

        linhas_tratadas = []
        ano_atual = None

        meses_validos = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

        for _, linha in df.iterrows():
            primeira_celula = (str(linha.iloc[0]).strip() if pd.notna(linha.iloc[0]) else "")
        
            # Identifica se a linha indica a mudança de Ano 
            if "Média" in primeira_celula:
                busca_ano = re.search(r'\d{4}', primeira_celula)
            if busca_ano:
                ano_atual = int(busca_ano.group(0))
            continue
            
        # Identifica se a linha é um Mês válido e extrai os valores das colunas
            if primeira_celula in meses_validos and ano_atual is not None:
                def para_float(valor):
                    try:
                        return float(valor)
                    except (ValueError, TypeError):
                        return None

                linhas_tratadas.append({
                    "Ano": ano_atual,
                    "Mês": primeira_celula,
                    "Diária Média (R$)": para_float(linha.iloc[1]),
                    "Gasto Médio (R$)": para_float(linha.iloc[2]),
                    "Permanência Média (dias)": para_float(linha.iloc[3])
                    })

        return pd.DataFrame(linhas_tratadas)


    # Exercício 9
    st.sidebar.header("Filtros e Configurações (Persistentes)")

    # Inicialização das chaves no Session State
    if "ano_sel" not in st.session_state:
        st.session_state.ano_sel = "Todos"
    if "ordem_sel" not in st.session_state:
        st.session_state.ordem_sel = "Padrão (Cronológica)"
    if "ocultar_nulos_sel" not in st.session_state:
        st.session_state.ocultar_nulos_sel = False

    # Componentes mapeados diretamente para o Session State
    anos_disponiveis = ["Todos"] + sorted(df_limpo["Ano"].unique().tolist())
    
    st.sidebar.selectbox("1. Selecione o Ano:", anos_disponiveis, key="ano_sel")
    st.sidebar.radio(
        "2. Ordenar Diária Média por:",
        options=["Padrão (Cronológica)", "Crescente", "Decrescente"],
        key="ordem_sel"
    )
    st.sidebar.checkbox("3. Ocultar meses sem informação de Gasto Médio", key="ocultar_nulos_sel")


    # =========================================================================
    # APLICAÇÃO DOS FILTROS USANDO O SESSION STATE
    # =========================================================================
    df_filtrado = df_limpo.copy()

    # Filtro de Ano
    if st.session_state.ano_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Ano"] == st.session_state.ano_sel]

    # Filtro de Nulos
    if st.session_state.ocultar_nulos_sel:
        df_filtrado = df_filtrado.dropna(subset=["Gasto Médio (R$)"])

    # Ordenação
    if st.session_state.ordem_sel == "Crescente":
        df_filtrado = df_filtrado.sort_values(by="Diária Média (R$)", ascending=True)
    elif st.session_state.ordem_sel == "Decrescente":
        df_filtrado = df_filtrado.sort_values(by="Diária Média (R$)", ascending=False)


    # =========================================================================
    # EXERCÍCIO 12: EXIBIR MÉTRICAS BÁSICAS
    # =========================================================================
    st.subheader("Métricas Principais")
    
    m1, m2, m3, m4 = st.columns(4)
    
    total_registros = len(df_filtrado)
    media_diaria = df_filtrado["Diária Média (R$)"].mean()
    max_gasto = df_filtrado["Gasto Médio (R$)"].max()
    media_permanencia = df_filtrado["Permanência Média (dias)"].mean()

    m1.metric("Total de Registros", f"{total_registros}")
    m2.metric("Diária Média", f"R$ {media_diaria:.2f}" if pd.notna(media_diaria) else "N/A")
    m3.metric("Maior Gasto Diário", f"R$ {max_gasto:.2f}" if pd.notna(max_gasto) else "N/A")
    m4.metric("Permanência Média", f"{media_permanencia:.2f} dias" if pd.notna(media_permanencia) else "N/A")

    st.markdown("---")

    # =========================================================================
    # EXIBIÇÃO DA TABELA FILTRADA
    # =========================================================================
    st.subheader("Tabela de Dados Filtrada")
    st.dataframe(df_filtrado, use_container_width=True)

    # EXERCÍCIO 5: DOWNLOAD
    st.download_button(
        label="Baixar Tabela Filtrada (CSV)", 
        data=df_filtrado.to_csv(index=False).encode('utf-8'), 
        file_name='df_filtrado.csv',
        mime='text/csv'
    )

    st.markdown("---")

    # =========================================================================
    # EXERCÍCIO 10: VISUALIZAÇÕES DE DADOS - GRÁFICOS SIMPLES
    # =========================================================================
    st.header("Exercício 10: Visualizações de Dados - Gráficos Simples")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Evolução da Diária Média")
        fig_line = px.line(
            df_filtrado, 
            x="Mês", 
            y="Diária Média (R$)", 
            color="Ano" if st.session_state.ano_sel == "Todos" else None,
            markers=True,
            title="Diária Média por Mês"
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        st.subheader("Gasto Médio por Mês")
        fig_bar = px.bar(
            df_filtrado, 
            x="Mês", 
            y="Gasto Médio (R$)", 
            color="Ano" if st.session_state.ano_sel == "Todos" else None,
            barmode="group",
            title="Gasto Médio do Visitante"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Distribuição da Permanência Média")
    fig_pie = px.pie(
        df_filtrado, 
        names="Mês", 
        values="Permanência Média (dias)",
        title="Proporção da Permanência Média ao longo do período"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # =========================================================================
    # EXERCÍCIO 11: VISUALIZAÇÕES DE DADOS - GRÁFICOS AVANÇADOS
    # =========================================================================
    st.header("Visualizações de Dados - Gráficos Avançados")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Histograma: Distribuição das Diárias")
        fig_hist = px.histogram(
            df_filtrado, 
            x="Diária Média (R$)", 
            nbins=15, 
            marginal="box",
            title="Distribuição e Frequência do Valor das Diárias",
            color_discrete_sequence=['#636EFA']
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col4:
        st.subheader("Scatter Plot: Diária Média vs Permanência")
        df_scatter = df_filtrado.dropna(
            subset=[
            "Diária Média (R$)",
            "Permanência Média (dias)",
            "Gasto Médio (R$)"
          ]
      )

        fig_scatter = px.scatter(
            df_scatter,
            x="Diária Média (R$)",
            y="Permanência Média (dias)",
            size="Gasto Médio (R$)",color="Mês",
            hover_name="Mês",
            title="Relação entre Valor da Diária e Dias de Permanência"
            )

        st.plotly_chart(fig_scatter, use_container_width=True)