import streamlit as st 
import pandas as pd
import numpy as np
import locale
import io  # Importar o módulo io
from utils import apply_custom_style_and_header, read_data, create_data, update_data
from forms.Form_Cad_Aux_Cad_Apoio import cad_novo_apoio_adm
from forms.Form_Cad_Aux_Cad_Area import cad_novo_area_adm
from forms.Form_Cad_Aux_Cad_Despesa import cad_novo_despesa_adm
from forms.Form_Cad_Aux_Cad_Escopo_Origem import cad_novo_escopo_origem_adm
from forms.Form_Cad_Aux_Cad_Escopo_Tipo import cad_novo_escopo_tipo_adm
from forms.Form_Cad_Aux_Cad_Especialidade import cad_novo_especialidade_adm
from forms.Form_Cad_Aux_Cad_Executante import cad_novo_executante_adm
from forms.Form_Cad_Aux_Cad_Familia_Equipamentos import cad_novo_familia_equip_adm
from forms.Form_Cad_Aux_Cad_Informativo import cad_novo_informativo_adm
from forms.Form_Cad_Aux_Cad_Planta import cad_novo_planta_adm
from forms.Form_Cad_Aux_Cad_Recurso import cad_novo_recurso_adm
from forms.Form_Cad_Aux_Cad_Servico import cad_novo_servico_adm
from forms.Form_Cad_Aux_Cad_Setor_Responsavel import cad_novo_setor_responsavel_adm
from forms.Form_Cad_Aux_Cad_Setor_Solicitante import cad_novo_setor_solicitante_adm
from forms.Form_Cad_Aux_Cad_Sistema_Operacional import cad_novo_sistema_operacional_adm
from forms.Form_Cad_Aux_Cad_Situacao_Motivo import cad_novo_situacao_motivo_adm
from forms.Form_Cad_Lancamento_Despesa import cad_novo_lancamento_despesa_adm
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
                    # Criar as abas
                    tab1, tab2 = st.tabs([
                        "Lista de Despesas",
                        "Lançamento de Despesas - Administração"
                    ])

                    # Conteúdo da aba 1
                    with tab1: 
                        show_DESPESA()

                    # Conteúdo da aba 1
                    with tab2: 
                        show_Lancamento_de_Despesas()

                elif opcao_selecionada == "Sist. Operacional":
                    show_SISTEMA_OPERACIONAL()
                elif opcao_selecionada == "Situação Motivo":
                    show_SITUACAO_MOTIVO()
                elif opcao_selecionada == "Setor Solicitante":
                    show_SETOR_SOLICITANTE()
                elif opcao_selecionada == "Setor Responsável":
                    show_SETOR_RESPONSAVEL()
                elif opcao_selecionada == "Serviço":
                    show_SERVICO()
                elif opcao_selecionada == "Recurso":
                    show_RECURSO()
                elif opcao_selecionada == "Planta":
                    show_PLANTA()
                elif opcao_selecionada == "Informativo":
                    show_INFORMATIVO()
                elif opcao_selecionada == "Família Equipamentos":
                    show_Familia_Equipamentos()
                elif opcao_selecionada == "Executante":
                    show_Executante()
                elif opcao_selecionada == "Especialidade":
                    show_Especialidade()
                elif opcao_selecionada == "Escopo Tipo":
                    show_Escopo_Tipo()
                elif opcao_selecionada == "Escopo Origem":
                    show_Escopo_Origem()
                elif opcao_selecionada == "Área":
                    show_Area()
                elif opcao_selecionada == "Apoio":
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

    collayoutapoio1, collayoutapoio2 = st.columns([8, 2])
    with collayoutapoio1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Apoio - Administração")

    with collayoutapoio2:
        if st.button("➕ Cadastrar Apoio",key="addApoio"):
            cad_novo_apoio_adm()


    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição',
        'TX_TIPO':'Tipo',
        'VL_VALOR_CUSTO': 'Valor',
        'VL_PERCENTUAL_CUSTO': 'Percentual'
    })
    st.dataframe(df[['ID', 'Descrição', 'Tipo', 'Valor', 'Percentual']], use_container_width=True, hide_index=True)

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

    # Converter a coluna VL_QUANTIDADE_DIAS_EXECUCAO para int
    df['VL_QUANTIDADE_DIAS_EXECUCAO'] = df['VL_QUANTIDADE_DIAS_EXECUCAO'].astype(int)

    # Formatar a coluna VL_QUANTIDADE_DIAS_EXECUCAO para exibir como número inteiro
    df['VL_QUANTIDADE_DIAS_EXECUCAO'] = df['VL_QUANTIDADE_DIAS_EXECUCAO'].apply(lambda x: f"{x:,}".replace(",", "."))

    # Converter a coluna ID para int
    df['ID'] = df['ID'].astype(int)

    # Filtros para a tabela de dados
    with st.expander("Filtros"):
        col1, col2 = st.columns(2)
        with col1:
            ID_filter_Area = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_Area = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_Area:
            df = df[df['ID'].isin(ID_filter_Area)]
        if descricao_filter_Area:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_Area)]

    collayoutarea1, collayoutarea2 = st.columns([8, 2])
    with collayoutarea1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Area - Administração")

    with collayoutarea2:
        if st.button("➕ Cadastrar area",key="addarea"):
            cad_novo_area_adm()


    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição',
        'VL_QUANTIDADE_DIAS_EXECUCAO':'QTD.Dias'
    })
    st.dataframe(df[['ID', 'Descrição', 'QTD.Dias']], use_container_width=True, hide_index=True)

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
            ID_filter_Escopo_Origem = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_Escopo_Origem = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_Escopo_Origem:
            df = df[df['ID'].isin(ID_filter_Escopo_Origem)]
        if descricao_filter_Escopo_Origem:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_Escopo_Origem)]

    collayoutescopo_origem1, collayoutescopo_origem2 = st.columns([8, 2])
    with collayoutescopo_origem1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Escopo de Origem - Administração")

    with collayoutescopo_origem2:
        if st.button("➕ Cadastrar Escopo de Origem",key="addescopo_origem"):
            cad_novo_escopo_origem_adm()  


    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição'
    })
    st.dataframe(df[['ID', 'Descrição']], use_container_width=True, hide_index=True)

def show_Escopo_Tipo():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_ESCOPO_TIPO")

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
            ID_filter_Escopo_Tipo = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_Escopo_Tipo = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_Escopo_Tipo:
            df = df[df['ID'].isin(ID_filter_Escopo_Tipo)]
        if descricao_filter_Escopo_Tipo:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_Escopo_Tipo)]

    collayout_escopo_tipo1, collayout_escopo_tipo2 = st.columns([8, 2])
    with collayout_escopo_tipo1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Tipo de Escopo - Administração")

    with collayout_escopo_tipo2:
        if st.button("➕ Cadastrar Tipo de Escopo",key="add_escopo_tipo"):
            cad_novo_escopo_tipo_adm() 


    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição'
    })
    st.dataframe(df[['ID', 'Descrição']], use_container_width=True, hide_index=True)

def show_Especialidade():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_ESPECIALIDADE")

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
            ID_filter_Especialidade = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_Especialidade = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_Especialidade:
            df = df[df['ID'].isin(ID_filter_Especialidade)]
        if descricao_filter_Especialidade:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_Especialidade)]

    collayout_especialidade1, collayout_especialidade2 = st.columns([8, 2])
    with collayout_especialidade1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Especialidade - Administração")

    with collayout_especialidade2:
        if st.button("➕ Cadastrar Especialidade",key="add_especialidade"):
            cad_novo_especialidade_adm() 


    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição'
    })
    st.dataframe(df[['ID', 'Descrição']], use_container_width=True, hide_index=True)

def show_Executante():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_EXECUTANTE")

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
            ID_filter_Executante = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_Executante = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_Executante:
            df = df[df['ID'].isin(ID_filter_Executante)]
        if descricao_filter_Executante:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_Executante)]

    collayout_executante1, collayout_executante2 = st.columns([8, 2])
    with collayout_executante1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Executante - Administração")

    with collayout_executante2:
        if st.button("➕ Cadastrar Executante",key="add_executante"):
            cad_novo_executante_adm()


    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição'
    })
    st.dataframe(df[['ID', 'Descrição']], use_container_width=True, hide_index=True)

def show_Familia_Equipamentos():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_FAMILIA_EQUIPAMENTOS")

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
            ID_filter_Familia_Equipamentos = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_Familia_Equipamentos = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_Familia_Equipamentos:
            df = df[df['ID'].isin(ID_filter_Familia_Equipamentos)]
        if descricao_filter_Familia_Equipamentos:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_Familia_Equipamentos)]

    collayout_familia_equipamento1, collayout_familia_equipamento2 = st.columns([8, 2])
    with collayout_familia_equipamento1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Familia Equipamentos - Administração")

    with collayout_familia_equipamento2:
        if st.button("➕ Cadastrar Familia Equipamentos",key="add_familia_equipamento"):
            cad_novo_familia_equip_adm()


    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição'
    })
    st.dataframe(df[['ID', 'Descrição']], use_container_width=True, hide_index=True)

def show_INFORMATIVO():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_INFORMATIVO")

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
            ID_filter_INFORMATIVO = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_INFORMATIVO = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_INFORMATIVO:
            df = df[df['ID'].isin(ID_filter_INFORMATIVO)]
        if descricao_filter_INFORMATIVO:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_INFORMATIVO)]

    collayout_informativo1, collayout_informativo2 = st.columns([8, 2])
    with collayout_informativo1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Informativo - Administração")

    with collayout_informativo2:
        if st.button("➕ Cadastrar Informativo",key="add_informativo"):
            cad_novo_informativo_adm()

    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição'
    })
    st.dataframe(df[['ID', 'Descrição']], use_container_width=True, hide_index=True)

def show_PLANTA():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_PLANTA")

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
            ID_filter_PLANTA = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_PLANTA = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_PLANTA:
            df = df[df['ID'].isin(ID_filter_PLANTA)]
        if descricao_filter_PLANTA:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_PLANTA)]

    collayout_planta1, collayout_planta2 = st.columns([8, 2])
    with collayout_planta1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Planta - Administração")

    with collayout_planta2:
        if st.button("➕ Cadastrar Planta",key="add_planta"):
            cad_novo_planta_adm()


    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição'
    })
    st.dataframe(df[['ID', 'Descrição']], use_container_width=True, hide_index=True)

def show_RECURSO():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_RECURSO")

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

    # Converter a coluna ID para int
    df['ID'] = df['ID'].astype(int)

    # Filtros para a tabela de dados
    with st.expander("Filtros"):
        col1, col2 = st.columns(2)
        with col1:
            ID_filter_RECURSO = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_RECURSO = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_RECURSO:
            df = df[df['ID'].isin(ID_filter_RECURSO)]
        if descricao_filter_RECURSO:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_RECURSO)]

    collayout_recurso1, collayout_recurso2 = st.columns([8, 2])
    with collayout_recurso1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Recurso - Administração")

    with collayout_recurso2:
        if st.button("➕ Cadastrar Recurso",key="add_recurso"):
            cad_novo_recurso_adm()

    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição',
        'VL_VALOR_CUSTO':'Valor'
    })
    st.dataframe(df[['ID', 'Descrição', 'Valor']], use_container_width=True, hide_index=True)

def show_SERVICO():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_SERVICO")

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
            ID_filter_SERVICO = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_SERVICO = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_SERVICO:
            df = df[df['ID'].isin(ID_filter_SERVICO)]
        if descricao_filter_SERVICO:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_SERVICO)]

    collayout_servico1, collayout_servico2 = st.columns([8, 2])
    with collayout_servico1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Serviços - Administração")

    with collayout_servico2:
        if st.button("➕ Cadastrar Serviços",key="add_servico"):
            cad_novo_servico_adm()

    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição'
    })
    st.dataframe(df[['ID', 'Descrição']], use_container_width=True, hide_index=True)

def show_SETOR_RESPONSAVEL():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_SETOR_RESPONSAVEL")

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
            ID_filter_SETOR_RESPONSAVEL = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_SETOR_RESPONSAVEL = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_SETOR_RESPONSAVEL:
            df = df[df['ID'].isin(ID_filter_SETOR_RESPONSAVEL)]
        if descricao_filter_SETOR_RESPONSAVEL:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_SETOR_RESPONSAVEL)]

    collayout_setor_responsavel1, collayout_setor_responsavel2 = st.columns([8, 2])
    with collayout_setor_responsavel1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Setor Responsável - Administração")

    with collayout_setor_responsavel2:
        if st.button("➕ Cadastrar Setor Responsável",key="add_setor_responsavel"):
            cad_novo_setor_responsavel_adm()

    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição'
    })
    st.dataframe(df[['ID', 'Descrição']], use_container_width=True, hide_index=True)

def show_SETOR_SOLICITANTE():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_SETOR_SOLICITANTE")

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
            ID_filter_SETOR_SOLICITANTE = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_SETOR_SOLICITANTE = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_SETOR_SOLICITANTE:
            df = df[df['ID'].isin(ID_filter_SETOR_SOLICITANTE)]
        if descricao_filter_SETOR_SOLICITANTE:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_SETOR_SOLICITANTE)]

    collayout_setor_solicitante1, collayout_setor_solicitante2 = st.columns([8, 2])
    with collayout_setor_solicitante1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Setor Solicitante - Administração")

    with collayout_setor_solicitante2:
        if st.button("➕ Cadastrar Setor Solicitante",key="add_setor_solicitante"):
            cad_novo_setor_solicitante_adm()

    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição'
    })
    # Exibir o DataFrame formatado
    st.subheader("Cadastro de Setor Solicitante - Administração")
    st.dataframe(df[['ID', 'Descrição']], use_container_width=True, hide_index=True)

def show_SITUACAO_MOTIVO():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_SITUACAO_MOTIVO")

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
            ID_filter_SITUACAO_MOTIVO = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_SITUACAO_MOTIVO = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_SITUACAO_MOTIVO:
            df = df[df['ID'].isin(ID_filter_SITUACAO_MOTIVO)]
        if descricao_filter_SITUACAO_MOTIVO:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_SITUACAO_MOTIVO)]

    collayout_situacao_motivo1, collayout_situacao_motivo2 = st.columns([8, 2])
    with collayout_situacao_motivo1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Situação Motivo - Administração")

    with collayout_situacao_motivo2:
        if st.button("➕ Cadastrar Situação Motivo",key="add_situacao_motivo"):
            cad_novo_situacao_motivo_adm()

    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição'
    })

    st.dataframe(df[['ID', 'Descrição']], use_container_width=True, hide_index=True)

def show_SISTEMA_OPERACIONAL():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_SISTEMA_OPERACIONAL")

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
            ID_filter_SISTEMA_OPERACIONAL = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_SISTEMA_OPERACIONAL = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_SISTEMA_OPERACIONAL:
            df = df[df['ID'].isin(ID_filter_SISTEMA_OPERACIONAL)]
        if descricao_filter_SISTEMA_OPERACIONAL:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_SISTEMA_OPERACIONAL)]

    collayout_sistema_operacional1, collayout_sistema_operacional2 = st.columns([8, 2])
    with collayout_sistema_operacional1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Sistema Operacional - Administração")

    with collayout_sistema_operacional2:
        if st.button("➕ Cadastrar Sistema Operacional",key="add_sistema_operacional"):
            cad_novo_sistema_operacional_adm()

    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição'
    })
    st.dataframe(df[['ID', 'Descrição']], use_container_width=True, hide_index=True)

def show_DESPESA():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    df = read_data("timecenter.TB_CADASTRO_DESPESA")

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
            ID_filter_DESPESA = st.multiselect("ID", options=sorted(df['ID'].unique()))
        with col2:
            descricao_filter_DESPESA = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO'].unique()))

        # Aplicar os filtros
        if ID_filter_DESPESA:
            df = df[df['ID'].isin(ID_filter_DESPESA)]
        if descricao_filter_DESPESA:
            df = df[df['TX_DESCRICAO'].isin(descricao_filter_DESPESA)]

    collayout_despesa1, collayout_despesa2 = st.columns([8, 2])
    with collayout_despesa1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Despesa - Administração")

    with collayout_despesa2:
        if st.button("➕ Cadastrar Despesa",key="add_despesa"):
            cad_novo_despesa_adm()

    # Renomear as colunas
    df = df.rename(columns={
        'ID': 'ID',
        'TX_DESCRICAO': 'Descrição'
    })
    st.dataframe(df[['ID', 'Descrição']], use_container_width=True, hide_index=True)

def show_Lancamento_de_Despesas():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return
    
    # Carregar os dados de timecenter.TB_LANCAMENTO_DESPESA
    df_lancamento = read_data("timecenter.TB_LANCAMENTO_DESPESA")

    if df_lancamento is None or df_lancamento.empty:
        return pd.DataFrame()  # Retorna um DataFrame vazio

    # Filtrar o DataFrame pelo projeto selecionado
    df_lancamento = df_lancamento[df_lancamento['CD_PROJETO'] == selected_gid]

    # Converter a coluna VL_VALOR_CUSTO para float
    df_lancamento['VL_VALOR_CUSTO'] = pd.to_numeric(df_lancamento['VL_VALOR_CUSTO'], errors='coerce').fillna(0.0)

    # Garantir que a coluna VL_VALOR_CUSTO é float
    df_lancamento['VL_VALOR_CUSTO'] = df_lancamento['VL_VALOR_CUSTO'].astype(float)

    # Formatar a coluna VL_VALOR_CUSTO como BRL
    df_lancamento['VL_VALOR_CUSTO'] = df_lancamento['VL_VALOR_CUSTO'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # Converter a coluna ID para int
    df_lancamento['ID'] = df_lancamento['ID'].astype(int)

    # Carregar os dados de timecenter.TB_CADASTRO_DESPESA para mapear os códigos
    df_cadastro_despesa = read_data("timecenter.TB_CADASTRO_DESPESA")

    if df_cadastro_despesa is not None and not df_cadastro_despesa.empty:
        # Fazer a junção com base no campo CD_DESPESA
        df_lancamento = pd.merge(df_lancamento, df_cadastro_despesa[['GID', 'TX_DESCRICAO']], 
                                 left_on='CD_DESPESA', right_on='GID', how='left')

        # Substituir a coluna CD_DESPESA por TX_DESCRICAO
        df_lancamento['CD_DESPESA'] = df_lancamento['TX_DESCRICAO']

    # Renomear as colunas
    df_lancamento = df_lancamento.rename(columns={
        'ID': 'ID',
        'DT_LANCAMENTO': 'Data',
        'TX_DESCRICAO': 'Despesa',
        'VL_VALOR_CUSTO': 'Valor',
        'TX_OBSERVACAO': 'Observação'
    })

    # Formatar a coluna Data (DT_LANCAMENTO) para o formato dd/mm/aaaa
    df_lancamento['Data'] = pd.to_datetime(df_lancamento['Data'], errors='coerce').dt.strftime('%d/%m/%Y')

    # Filtros para a tabela de dados
    with st.expander("Filtros"):
        col1, col2, col3 = st.columns(3)
        with col1:
            ID_filter_Lancamento_de_Despesas = st.multiselect("ID", options=sorted(df_lancamento['ID'].unique()), key="rowID")

        with col2:
            descricao_filter_Lancamento_de_Despesas = st.multiselect("Descrição", options=sorted(df_lancamento['Despesa'].unique()), key="rowdescricao")

        with col3:
            data_filter_Lancamento_de_Despesas = st.multiselect("Data", options=sorted(df_lancamento['Data'].unique()), key="rowdate")


        # Aplicar os filtros
        if ID_filter_Lancamento_de_Despesas:
            df_lancamento = df_lancamento[df_lancamento['ID'].isin(ID_filter_Lancamento_de_Despesas)]
        if descricao_filter_Lancamento_de_Despesas:
            df_lancamento = df_lancamento[df_lancamento['Despesa'].isin(descricao_filter_Lancamento_de_Despesas)]
        if data_filter_Lancamento_de_Despesas:
            df_lancamento = df_lancamento[df_lancamento['Data'].isin(descricao_filter_Lancamento_de_Despesas)]

    collayout_lancamento_despesa1, collayout_lancamento_despesa2 = st.columns([8, 2])
    with collayout_lancamento_despesa1:
        # Exibir o DataFrame formatado
        st.subheader("Cadastro de Lançamentos de Despesas - Administração")

    with collayout_lancamento_despesa2:
        if st.button("➕ Cadastrar Lançamentos de Despesas",key="add_lancamento_despesa"):
            cad_novo_lancamento_despesa_adm()

    # Exibir o DataFrame formatado
    st.subheader("Lançamento de Despesas - Administração")
    st.dataframe(df_lancamento[['ID', 'Data', 'Despesa', 'Valor', 'Observação']], 
                 use_container_width=True, hide_index=True)


# Função principal do aplicativo
def app():
    Cadastro_Auxiliar_screen()

if __name__ == "__main__":
    app()
