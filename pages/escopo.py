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
    get_nota_manutencao_geral,
    create_data,
    update_data,
    delete_data
)
import plotly.express as px

# Configurar o locale para português do Brasil
#locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def escopo_screen():
    apply_custom_style_and_header("Tela de Escopo")

    # Verifica se as informações do projeto e os dados carregados estão disponíveis
    if 'projeto_info' in st.session_state and 'project_data' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        st.markdown(f"### Projeto: {projeto_info['TX_DESCRICAO']}")
        
        # Obtendo o DataFrame de escopo específico do projeto do session_state
        df = st.session_state['project_data']['visualizar_notas_de_manutencao']

    else:
        st.error("Selecione um projeto na tela inicial.")
        return

    # Criar as abas
    tabdash, tab1, tab2, tab3, tab4 = st.tabs([
        "Dashboard",
        "Gestão das Notas e Ordens",
        "Desafio do Escopo",
        "Declaração do Escopo",
        "Gestão das Alterações do Escopo"
    ])

    with tabdash:
        st.write("Conteúdo da aba Dashboard")

    # Conteúdo da aba 1
    with tab1: 
        gestao_notas_ordens_screen(df, projeto_info)

    # Conteúdo das outras abas
    with tab2:
        st.write("Conteúdo da aba Desafio do Escopo")
    with tab3:
        st.write("Conteúdo da aba Declaração do Escopo")
    with tab4:
        st.write("Conteúdo da aba Gestão das Alterações do Escopo")

def gestao_notas_ordens_screen(df, projeto_info):
    # Verifica se o DataFrame de escopo está vazio
    if df.empty:
        st.warning("Nenhum dado foi encontrado para o projeto selecionado.")
        return
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

    # Ordenar o DataFrame pela coluna ID_NOTA_MANUTENCAO de forma decrescente
    df = df.sort_values(by='ID_NOTA_MANUTENCAO', ascending=False)

    col1, col2, col3 = st.columns([8,1,1])
    with col1:
        # Exibir as métricas com st.metric
        st.markdown("### Resumo do Projeto")
    with col2:  
        if st.button("➕ Cadastrar Nota",key="addNota"):
            cadastrar_nota_manutencao()               
    
    with col3:
        if st.button("🔄 Atualizar Dados",key="AtualizarPageNota"):
            # Obtenha o GID do projeto selecionado no session_state
            projeto_info = st.session_state.get('projeto_info', {})
            projeto_gid = projeto_info.get('GID', None)
            
            if projeto_gid:
                # Recarrega todos os DataFrames relacionados ao projeto com os dados mais recentes
                try:
                    st.session_state['project_data']['visualizar_notas_de_manutencao'] = get_vw_nota_manutencao_hh_data(projeto_gid)
                    st.session_state['project_data']['notas_de_manutencao_geral'] = get_nota_manutencao_geral(projeto_gid)
                    # Atualizar o DataFrame de exibição para refletir as novas alterações
                    df = st.session_state['project_data']['visualizar_notas_de_manutencao']
                    # Exibe uma mensagem de sucesso após a atualização
                    st.success("Dados do projeto atualizados com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar os dados: {str(e)}")
            else:
                st.error("GID do projeto não encontrado no session_state.")


    # Filtros para a tabela de dados
    with st.expander("Filtros"):
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
        
        with col1:
            nota_filter = st.multiselect("ID Nota Manutenção", options=sorted(filter(None, df['ID_NOTA_MANUTENCAO'].unique())))
        with col2:
            texto_Nota_filter = st.multiselect("Nota", options=sorted(filter(None, df['TX_NOTA'].unique())))
        with col3:
            ordem_filter = st.multiselect("Ordem", options=sorted(filter(None, df['TX_ORDEM'].unique())))
        with col4:
            tag_filter = st.multiselect("Tag", options=sorted(filter(None, df['TX_TAG'].unique())))
        with col5:
            situacao_filter = st.multiselect("Situação", options=sorted(filter(None, df['TX_SITUACAO'].unique())))
        with col6:
            # Adiciona o seletor para ordenar por VL_CUSTO_TOTAL
            custo_total_order = st.radio("Ordem Custo Total", options=["Nenhum", "Maior para Menor", "Menor para Maior"])
        with col7:
            # Adiciona o seletor para ordenar por ID_NOTA_MANUTENCAO
            id_nota_order = st.radio("Ordem ID Nota", options=["Nenhum", "Maior para Menor", "Menor para Maior"])
        with col8:
            # Opção de priorizar qual coluna ordenar primeiro
            prioridade_ordem = st.radio("Prioridade de Ordenação", options=["ID Nota", "Custo Total"])

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

        # Configurar a lista de ordenação e direções
        order_columns = []
        ascending_order = []

        # Definir a prioridade de ordenação com base na seleção do usuário
        if prioridade_ordem == "ID Nota":
            if id_nota_order != "Nenhum":
                order_columns.append("ID_NOTA_MANUTENCAO")
                ascending_order.append(id_nota_order == "Menor para Maior")
            if custo_total_order != "Nenhum":
                order_columns.append("VL_CUSTO_TOTAL")
                ascending_order.append(custo_total_order == "Menor para Maior")
        else:
            if custo_total_order != "Nenhum":
                order_columns.append("VL_CUSTO_TOTAL")
                ascending_order.append(custo_total_order == "Menor para Maior")
            if id_nota_order != "Nenhum":
                order_columns.append("ID_NOTA_MANUTENCAO")
                ascending_order.append(id_nota_order == "Menor para Maior")

        # Aplicar a ordenação no DataFrame
        if order_columns:
            df = df.sort_values(by=order_columns, ascending=ascending_order)



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

    with st.container(border=True):
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
        for index, row in df.head(10).iterrows():
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
                            st.session_state["nota_selecionada"] = row['GID_NOTA_MANUTENCAO']  # Armazena a linha selecionada no session_state
                            edit_nota_manutencao()              

                    with col_btn2:
                        if st.button("🗑️", key=f"ExcluirNota_{index}"):
                            delete_data("timecenter.TB_NOTA_MANUTENCAO", "GID", row['GID_NOTA_MANUTENCAO'])
                            st.success(f"Item excluído de ID: {row['ID']}")



def app():
    escopo_screen()
