import streamlit as st 
import pandas as pd
import numpy as np
import locale
import io  # Importar o módulo io
from forms.cadastrar_nota_manutencao import cadastrar_nota_manutencao
from forms.editar_nota_manutencao import edit_nota_manutencao
from utils import (
    apply_custom_style_and_header,
    get_vw_nota_manutencao_hh_data,
    create_data,
    update_data,
    delete_data
)
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import plotly.express as px

# Configurar o locale para português do Brasil
#locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def escopo_screen():
    apply_custom_style_and_header("Tela de Escopo")

    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        st.markdown(f"### Projeto: {projeto_info['TX_DESCRICAO']}")

    else:
        st.error("Selecione um projeto na tela inicial.")
        return

    # Criar as abas
    tab1, tab2, tab3, tab4 = st.tabs([
        "Gestão das Notas e Ordens",
        "Desafio do Escopo",
        "Declaração do Escopo",
        "Gestão das Alterações do Escopo"
    ])

    # Conteúdo da aba 1
    with tab1: 
        gestao_notas_ordens_screen()

    # Conteúdo das outras abas
    with tab2:
        st.write("Conteúdo da aba Desafio do Escopo")
    with tab3:
        st.write("Conteúdo da aba Declaração do Escopo")
    with tab4:
        st.write("Conteúdo da aba Gestão das Alterações do Escopo")

@st.cache_data
def load_tela_escopo_data(selected_gid):
    # Obter os dados da tabela
    df = get_vw_nota_manutencao_hh_data()

    if df is None or df.empty:
        return pd.DataFrame()  # Retorna um DataFrame vazio

    df = df[df['GID_PROJETO'] == selected_gid]

    if df.empty:
        return df

    # Remover as colunas 'GID_PROJETO' e 'TX_NOME_SOLICITANTE' em uma única operação
    df = df.drop(columns=['TX_NOME_SOLICITANTE'])

    # Converter a coluna VL_HH_TOTAL para float
    df['VL_HH_TOTAL'] = pd.to_numeric(df['VL_HH_TOTAL'], errors='coerce').fillna(0.0)

    # Tratar a coluna VL_CUSTO_TOTAL
    # Verificar se a coluna é do tipo string
    if df['VL_CUSTO_TOTAL'].dtype == 'object':
        # Remover 'R$' e espaços, e converter para float usando locale
        df['VL_CUSTO_TOTAL'] = df['VL_CUSTO_TOTAL'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    else:
        # Se já for numérico, garantir que é float
        df['VL_CUSTO_TOTAL'] = df['VL_CUSTO_TOTAL'].astype(float)

    # Converter a coluna ID_NOTA_MANUTENCAO para int
    df['ID_NOTA_MANUTENCAO'] = df['ID_NOTA_MANUTENCAO'].astype(int)

    # Converter colunas categóricas para string
    categorical_cols = ['TX_NOTA', 'TX_ORDEM', 'TX_TAG', 'TX_FAMILIA_EQUIPAMENTOS', 'TX_DESCRICAO_SERVICO', 'TX_ESCOPO_TIPO', 'TX_SITUACAO']
    df[categorical_cols] = df[categorical_cols].astype(str)

    return df

def exibir_detalhes_da_linha(row):
    """Exibe os detalhes de uma linha selecionada."""
    st.subheader("Detalhes da Nota Selecionada")
    st.write(row)

def gestao_notas_ordens_screen():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return

    try:
        df = load_tela_escopo_data(selected_gid)

        if df.empty:
            st.warning("Nenhum dado foi encontrado para o projeto selecionado.")
            return

        # Ordenar o DataFrame pela coluna ID_NOTA_MANUTENCAO de forma decrescente
        df = df.sort_values(by='ID_NOTA_MANUTENCAO', ascending=False)

        col1, col2, col3, col4 = st.columns([7,1,1,1])
        with col1:
            # Exibir as métricas com st.metric
            st.markdown("### Resumo do Projeto")
        with col2:  
            if st.button("➕ Cadastrar Nota",key="addNota"):
                cadastrar_nota_manutencao()               
        
        with col3:
            if st.button("✏️ Editar Nota",key="EditNota"):
                edit_nota_manutencao()              

        with col4:
            if st.button("🔄 Atualizar Dados",key="AtualizarPageNota"):
                # Invalida o cache e recarrega os dados
                load_tela_escopo_data.clear()
                load_tela_escopo_data(selected_gid)

        # Filtros para a tabela de dados
        with st.expander("Filtros"):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                nota_filter = st.multiselect("ID Nota Manutenção", options=sorted(df['ID_NOTA_MANUTENCAO'].unique()))
            with col2:
                texto_Nota_filter = st.multiselect("Nota", options=sorted(df['TX_NOTA'].unique()))
            with col3:
                ordem_filter = st.multiselect("Ordem", options=sorted(df['TX_ORDEM'].unique()))
            with col4:
                tag_filter = st.multiselect("Tag", options=sorted(df['TX_TAG'].unique()))
            with col5:
                situacao_filter = st.multiselect("Situação", options=sorted(df['TX_SITUACAO'].unique()))

            # Aplicar os filtros
            if nota_filter:
                df = df[df['ID_NOTA_MANUTENCAO'].isin(nota_filter)]
            if texto_Nota_filter:
                df = df[df['TX_NOTA'].isin(texto_Nota_filter)]
            if ordem_filter:
                df = df[df['TX_ORDEM'].isin(ordem_filter)]
            if tag_filter:
                df = df[df['TX_TAG'].isin(tag_filter)]
            if situacao_filter:
                df = df[df['TX_SITUACAO'].isin(situacao_filter)]

        # Calcular as métricas
        total_notas = len(df['ID_NOTA_MANUTENCAO'].unique())
        total_ordens = len(df['TX_ORDEM'].dropna().unique())
        total_hh = df['VL_HH_TOTAL'].sum()
        custo_total = df['VL_CUSTO_TOTAL'].sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total de Notas", f"{total_notas}")
        col2.metric("Total de Ordens", f"{total_ordens}")
        col3.metric("Total de HH", f"{total_hh}")
        col4.metric("Custo Total", f"R$ {custo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        # Renomear as colunas
        df = df.rename(columns={
            'ID_NOTA_MANUTENCAO': 'ID',
            'TX_NOTA': 'NOTA',
            'TX_ORDEM':'ORDEM',
            'TX_TAG':'TAG',
            'TX_FAMILIA_EQUIPAMENTOS':'FAMILIA DE EQUIP.',
            'TX_DESCRICAO_SERVICO':'SERVIÇO',
            'VL_HH_TOTAL':'HH',
            'VL_CUSTO_TOTAL':'VALOR TOTAL',
            'TX_ESCOPO_TIPO':'TIPO ESCOPO',
            'TX_SITUACAO':'SITUAÇÃO'
        })

        # Garantir que as colunas 'HH' e 'VALOR TOTAL' são numéricas para formatação
        df['HH'] = pd.to_numeric(df['HH'], errors='coerce').fillna(0.0)
        df['VALOR TOTAL'] = pd.to_numeric(df['VALOR TOTAL'], errors='coerce').fillna(0.0)


        # Filtrar somente as colunas renomeadas
        df_renomeado = df[['ID', 'NOTA', 'ORDEM', 'TAG', 'FAMILIA DE EQUIP.', 'SERVIÇO', 'HH', 'VALOR TOTAL', 'TIPO ESCOPO', 'SITUAÇÃO']]

        # Limitar o número de registros para melhorar o desempenho
        max_rows = 1000
        if len(df_renomeado) > max_rows:
            st.warning(f"O conjunto de dados é grande ({len(df_renomeado)} registros). Exibindo os primeiros {max_rows} registros.")
            df_display = df_renomeado.head(max_rows)
        else:
            df_display = df_renomeado

        # Garantir que a coluna ID seja exibida como string, sem formatação extra
        df_display['ID'] = df_display['ID'].astype(str)

        df_display['HH'] = df_display['HH'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        # Formatar a coluna VALOR TOTAL para exibir com "R$"
        df_display['VALOR TOTAL'] = df_display['VALOR TOTAL'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        # Exibir a tabela com cabeçalhos e botões
        col_id, col_nota, col_ordem, col_tag, col_familia, col_servico, col_hh, col_valor, col_escopo, col_situacao, col_acao = st.columns(
            [0.5, 1, 1, 1, 1.5, 2, 0.5, 1, 1, 1, 1]
        )
        
        col_id.markdown("**ID**")
        col_nota.markdown("**NOTA**")
        col_ordem.markdown("**ORDEM**")
        col_tag.markdown("**TAG**")
        col_familia.markdown("**FAMÍLIA DE EQUIP.**")
        col_servico.markdown("**SERVIÇO**")
        col_hh.markdown("**HH**")
        col_valor.markdown("**VALOR TOTAL**")
        col_escopo.markdown("**TIPO ESCOPO**")
        col_situacao.markdown("**SITUAÇÃO**")
        col_acao.markdown("**Ações**")

        # Exibir cada linha
        for index, row in df.head(15).iterrows():
            with st.container():
                col_id, col_nota, col_ordem, col_tag, col_familia, col_servico, col_hh, col_valor, col_escopo, col_situacao, col_acao = st.columns(
                    [0.5, 1, 1, 1, 1.5, 2, 0.5, 1, 1, 1, 1]
                )
                col_id.write(row['ID'])
                col_nota.write(row['NOTA'])
                col_ordem.write(row['ORDEM'])
                col_tag.write(row['TAG'])
                col_familia.write(row['FAMILIA DE EQUIP.'])
                col_servico.write(row['SERVIÇO'])
                col_hh.write(row['HH'])
                col_valor.write(row['VALOR TOTAL'])
                col_escopo.write(row['TIPO ESCOPO'])
                col_situacao.write(row['SITUAÇÃO'])

                # Botões de ação
                with col_acao:
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button("✏️", key=f"EditNota_{index}"):
                            st.session_state["linha_selecionada"] = row  # Armazena a linha selecionada no session_state
                    with col_btn2:
                        if st.button("🗑️", key=f"ExcluirNota_{index}"):
                            delete_data(row['ID'])

        # Exibir detalhes da linha selecionada, se houver
        if "linha_selecionada" in st.session_state:
            exibir_detalhes_da_linha(st.session_state["linha_selecionada"])

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar os dados. Por favor, tente novamente mais tarde. Erro: {e}")

def app():
    escopo_screen()
