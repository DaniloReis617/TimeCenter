import streamlit as st 
import pandas as pd
import numpy as np
import locale
import io  # Importar o módulo io
from utils import apply_custom_style_and_header, read_data, create_data, update_data
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import plotly.express as px

def Cadastro_Auxiliar_screen():
    apply_custom_style_and_header("Cadastro Auxiliar")

    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        st.write(f"Exibindo dados para o projeto {projeto_info['TX_DESCRICAO']}")
    else:
        st.error("Selecione um projeto na tela inicial.")

    # Container maior que pega a tela inteira
    with st.container():
        # Criando duas colunas dentro do container
        col1, col2 = st.columns([1, 3])  # Coluna 1 menor e coluna 2 maior
        
        # Primeiro container dentro da primeira coluna para o rádio
        with col1:
            with st.container():
                st.subheader("Selecione a Opção")

                # Opções de cadastro
                cadastro_opcoes = [
                    "Apoio",
                    "Área",
                    "Escopo Origem",
                    "Escopo Tipo",
                    "Especialidade",
                    "Executante",
                    "Família Equipamentos",
                    "Informativo",
                    "Planta",
                    "Recurso",
                    "Serviço",
                    "Setor Responsável",
                    "Setor Solicitante",
                    "Situação Motivo",
                    "Sist. Operacional",
                    "Despesa"
                ]
                
                # Botão de seleção de rádio para escolher a ação
                opcao_selecionada = st.radio("Cadastro Auxiliar:", cadastro_opcoes)

        # Segundo container na segunda coluna para mostrar o resultado
        with col2:
            with st.container():
                st.subheader("Resultado da Seleção")

                # Lógica de navegação com base na opção selecionada
                if opcao_selecionada == "Despesa":
                    st.write("Acessando tela de Cadastro de Despesa")
                elif opcao_selecionada == "Sist. Operacional":
                    st.write("Acessando tela de Cadastro de Sistema Operacional")
                elif opcao_selecionada == "Situação Motivo":
                    st.write("Acessando tela de Cadastro de Situação Motivo")
                elif opcao_selecionada == "Setor Solicitante":
                    st.write("Acessando tela de Cadastro de Setor Solicitante")
                elif opcao_selecionada == "Setor Responsável":
                    st.write("Acessando tela de Cadastro de Setor Responsável")
                elif opcao_selecionada == "Serviço":
                    st.write("Acessando tela de Cadastro de Serviço")
                elif opcao_selecionada == "Recurso":
                    st.write("Acessando tela de Cadastro de Recurso")
                elif opcao_selecionada == "Planta":
                    st.write("Acessando tela de Cadastro de Planta")
                elif opcao_selecionada == "Informativo":
                    st.write("Acessando tela de Cadastro de Informativo")
                elif opcao_selecionada == "Família Equipamentos":
                    st.write("Acessando tela de Cadastro de Família de Equipamentos")
                elif opcao_selecionada == "Executante":
                    st.write("Acessando tela de Cadastro de Executante")
                elif opcao_selecionada == "Especialidade":
                    st.write("Acessando tela de Cadastro de Especialidade")
                elif opcao_selecionada == "Escopo Tipo":
                    st.write("Acessando tela de Cadastro de Escopo Tipo")
                elif opcao_selecionada == "Escopo Origem":
                    st.write("Acessando tela de Cadastro de Escopo Origem")
                    show_Escopo_Origem()
                elif opcao_selecionada == "Área":
                    st.write("Acessando tela de Cadastro de Área")
                    show_Area()
                elif opcao_selecionada == "Apoio":
                    st.write("Acessando tela de Cadastro de Apoio")
                    show_Apoio()


def show_Apoio():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_APOIO")

    if df is None or df.empty:
        return pd.DataFrame()  # Retorna um DataFrame vazio

    # Filtrar o DataFrame pelo projeto selecionado
    df = df[df['CD_PROJETO'] == selected_gid]

    # Converter a coluna VL_VALOR_CUSTO para float
    df['VL_VALOR_CUSTO'] = pd.to_numeric(df['VL_VALOR_CUSTO'], errors='coerce').fillna(0.0)

    # Tratar a coluna VL_VALOR_CUSTO
    # Verificar se a coluna é do tipo string
    if df['VL_VALOR_CUSTO'].dtype == 'object':
        # Remover 'R$' e espaços, e converter para float
        df['VL_VALOR_CUSTO'] = df['VL_VALOR_CUSTO'].str.replace('R$', '').str.replace(' ', '').str.replace('.', '').str.replace(',', '.').astype(float)

    # Garantir que a coluna é float
    df['VL_VALOR_CUSTO'] = df['VL_VALOR_CUSTO'].astype(float)

    # Formatar a coluna VL_VALOR_CUSTO como BRL
    df['VL_VALOR_CUSTO'] = df['VL_VALOR_CUSTO'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # Converter a coluna VL_PERCENTUAL_CUSTO para float
    df['VL_PERCENTUAL_CUSTO'] = pd.to_numeric(df['VL_PERCENTUAL_CUSTO'], errors='coerce').fillna(0.0)

    # Formatar a coluna VL_PERCENTUAL_CUSTO como percentual
    df['VL_PERCENTUAL_CUSTO'] = df['VL_PERCENTUAL_CUSTO'].apply(lambda x: f"{x:.2f}%")

    # Converter a coluna ID para int
    df['ID'] = df['ID'].astype(int)

    # Filtros para a tabela de dados
    with st.expander("Filtros"):
        col1, col2, col3 = st.columns(3)
        with col1:
            ID_filter = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))
        with col3:
            Tipo_filter = st.multiselect("Tipo", options=sorted(df['TX_TIPO'].unique()))

        # Aplicar os filtros
        if ID_filter:
            df = df[df['ID'].isin(ID_filter)]
        if descricao_filter:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter)]
        if Tipo_filter:
            df = df[df['TX_TIPO'].isin(Tipo_filter)]

    # Exibir o DataFrame formatado
    st.subheader("Cadastro de Apoio - Administração")
    st.dataframe(df[['ID', 'TX_DESCRICAO', 'TX_TIPO', 'VL_VALOR_CUSTO', 'VL_PERCENTUAL_CUSTO']], use_container_width=True, hide_index=True)

def show_Area():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_AREA")

    if df is None or df.empty:
        return pd.DataFrame()  # Retorna um DataFrame vazio

    # Filtrar o DataFrame pelo projeto selecionado
    df = df[df['CD_PROJETO'] == selected_gid]

    # Converter a coluna VL_VALOR_CUSTO para float
    df['VL_QUANTIDADE_DIAS_EXECUCAO'] = pd.to_numeric(df['VL_QUANTIDADE_DIAS_EXECUCAO'], errors='coerce').fillna(0.0)

    # Tratar a coluna VL_QUANTIDADE_DIAS_EXECUCAO
    # Verificar se a coluna é do tipo string
    if df['VL_QUANTIDADE_DIAS_EXECUCAO'].dtype == 'object':
        # Remover 'R$' e espaços, e converter para float
        df['VL_QUANTIDADE_DIAS_EXECUCAO'] = df['VL_QUANTIDADE_DIAS_EXECUCAO'].str.replace('R$', '').str.replace(' ', '').str.replace('.', '').str.replace(',', '.').astype(float)

    # Garantir que a coluna é float
    df['VL_QUANTIDADE_DIAS_EXECUCAO'] = df['VL_QUANTIDADE_DIAS_EXECUCAO'].astype(float)

    # Formatar a coluna VL_QUANTIDADE_DIAS_EXECUCAO como BRL
    df['VL_QUANTIDADE_DIAS_EXECUCAO'] = df['VL_QUANTIDADE_DIAS_EXECUCAO'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # Converter a coluna ID para int
    df['ID'] = df['ID'].astype(int)

    # Filtros para a tabela de dados
    with st.expander("Filtros"):
        col1, col2 = st.columns(2)
        with col1:
            ID_filter = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter:
            df = df[df['ID'].isin(ID_filter)]
        if descricao_filter:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter)]

    # Exibir o DataFrame formatado
    st.subheader("Cadastro de Area - Administração")
    st.dataframe(df[['ID', 'TX_DESCRICAO', 'VL_QUANTIDADE_DIAS_EXECUCAO']], use_container_width=True, hide_index=True)

def show_Escopo_Origem():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_ESCOPO_ORIGEM")

    if df is None or df.empty:
        return pd.DataFrame()  # Retorna um DataFrame vazio

    # Filtrar o DataFrame pelo projeto selecionado
    df = df[df['CD_PROJETO'] == selected_gid]

    # Converter a coluna ID para int
    df['ID'] = df['ID'].astype(int)

    # Filtros para a tabela de dados
    with st.expander("Filtros"):
        col1, col2 = st.columns(2)
        with col1:
            ID_filter = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter:
            df = df[df['ID'].isin(ID_filter)]
        if descricao_filter:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter)]

    # Exibir o DataFrame formatado
    st.subheader("Cadastro de Escopo de Origem - Administração")
    st.dataframe(df[['ID', 'TX_DESCRICAO']], use_container_width=True, hide_index=True)

# Função principal do aplicativo
def app():
    Cadastro_Auxiliar_screen()

if __name__ == "__main__":
    app()
