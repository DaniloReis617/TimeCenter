import streamlit as st 
import os
import pandas as pd
import numpy as np
from utils import apply_custom_style_and_header, get_db_connection, get_vw_nota_manutencao_hh_data, read_data, create_data, update_data, get_projetos_por_usuario, get_descricao_projetos, get_all_projetos, delete_data

def escopo_screen():
    apply_custom_style_and_header("Tela de Escopo")
    
    # Criar as abas
    tab1, tab2, tab3, tab4 = st.tabs(["Gestão das Notas e Ordens", "Desafio do Escopo", "Declaração do Escopo", "Gestão das Alterações do Escopo"])
    
    # Conteúdo da aba 1
    with tab1:
        gestao_notas_ordens_screen()

    # Conteúdo das outras abas (implementação pode ser adicionada conforme necessário)
    with tab2:
        st.write("Conteúdo da aba Desafio do Escopo")
        
    with tab3:
        st.write("Conteúdo da aba Declaração do Escopo")
        
    with tab4:
        st.write("Conteúdo da aba Gestão das Alterações do Escopo")

def gestao_notas_ordens_screen():
    conn = get_db_connection()
    
    if conn:
        # Carregar os projetos e criar o filtro de seleção
        projetos_df = read_data(conn, "timecenter.TB_PROJETO")
        projetos = projetos_df['TX_DESCRICAO'].tolist()
        
        selected_project = st.selectbox("Selecione o Projeto", projetos)
        
        if selected_project:
            selected_gid = projetos_df.loc[projetos_df['TX_DESCRICAO'] == selected_project, 'GID'].iloc[0]
            st.session_state['selected_gid'] = selected_gid
        else:
            st.session_state['selected_gid'] = None
            st.warning("Selecione um projeto para continuar.")
            return

        try:
            # Obter os dados da tabela VW_NOTA_MANUTENCAO_HH e filtrar pelo GID do projeto selecionado
            df = get_vw_nota_manutencao_hh_data(conn)
            df = df[df['GID_PROJETO'] == st.session_state['selected_gid']]  # Filtrar pelo GID_PROJETO
            
            if df.empty:
                st.warning("Nenhum dado foi encontrado para o projeto selecionado.")
                return
            
            # Remover a coluna GID_PROJETO antes de exibir a tabela
            df = df.drop(columns=['GID_PROJETO'])
            
            # Limpeza e tratamento das colunas
            df['VL_HH_TOTAL'] = df['VL_HH_TOTAL'].apply(lambda x: int(float(str(x).replace(',', '').strip())) if pd.notnull(x) else 0)

            # Função para limpar e formatar o valor para BRL
            def format_to_brl(value):
                value = str(value).replace(' ', '').replace(',', '.').strip()  # Remover espaços e converter vírgulas
                try:
                    value = float(value)
                    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                except ValueError:
                    return "R$ 0,00"  # Valor padrão em caso de erro de conversão

            # Aplicar a função de formatação à coluna de custo total
            df['VL_CUSTO_TOTAL'] = df['VL_CUSTO_TOTAL'].apply(format_to_brl)

            # Remover o .0 convertendo a coluna para string e removendo o .0
            df['ID_NOTA_MANUTENCAO'] = df['ID_NOTA_MANUTENCAO'].astype(int)

            # Converter todas as colunas para texto
            df = df.astype(str)

            # Criar filtros com valores distintos e não nulos, permitindo pesquisa
            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
            with col1:
                nota_filter = st.multiselect("ID Nota Manutenção", options=sorted(df['ID_NOTA_MANUTENCAO'].unique()))
            with col2:
                tx_nota_filter = st.multiselect("Nota", options=sorted(df['TX_NOTA'].unique()))
            with col3:
                ordem_filter = st.multiselect("Ordem", options=sorted(df['TX_ORDEM'].unique()))
            with col4:
                tag_filter = st.multiselect("Tag", options=sorted(df['TX_TAG'].unique()))
            with col5:
                solicitante_filter = st.multiselect("Solicitante", options=sorted(df['TX_NOME_SOLICITANTE'].unique()))
            with col6:
                descricao_filter = st.multiselect("Descrição", options=sorted(df['TX_DESCRICAO_SERVICO'].unique()))
            with col7:
                situacao_filter = st.multiselect("Situação", options=sorted(df['TX_SITUACAO'].unique()))

            # Aplicar os filtros
            if nota_filter:
                df = df[df['ID_NOTA_MANUTENCAO'].isin(nota_filter)]
            if tx_nota_filter:
                df = df[df['TX_NOTA'].isin(tx_nota_filter)]
            if ordem_filter:
                df = df[df['TX_ORDEM'].isin(ordem_filter)]
            if tag_filter:
                df = df[df['TX_TAG'].isin(tag_filter)]
            if solicitante_filter:
                df = df[df['TX_NOME_SOLICITANTE'].isin(solicitante_filter)]
            if descricao_filter:
                df = df[df['TX_DESCRICAO_SERVICO'].isin(descricao_filter)]
            if situacao_filter:
                df = df[df['TX_SITUACAO'].isin(situacao_filter)]

            # Aplicar cores na coluna TX_SITUACAO
            def apply_color(val):
                if val == "Aprovada":
                    return 'background-color: #d4edda;'  # Verde fraco
                elif val == "Pendente":
                    return 'background-color: #fff3cd;'  # Amarelo fraco
                elif val == "Reprovada":
                    return 'background-color: #f8d7da;'  # Vermelho fraco
                else:
                    return ''

            styled_df = df.style.applymap(apply_color, subset=['TX_SITUACAO'])

            # Calcular as métricas
            total_notas = len(df['ID_NOTA_MANUTENCAO'])
            total_ordens = len(df['TX_ORDEM'].dropna())  # Exclui valores nulos
            total_hh = df['VL_HH_TOTAL'].astype(float).sum()
            custo_total = df['VL_CUSTO_TOTAL'].str.replace('R$', '').str.replace('.', '').str.replace(',', '.').astype(float).sum()
            
            with st.container(border=True):
                # Exibir as métricas
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"<div style='text-align: center'><p style='font-size: 32px; line-height: 0.9'><b>Total de Notas</b><br>{total_notas}</p></div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div style='text-align: center'><p style='font-size: 32px; line-height: 0.9'><b>Total de Ordens</b><br>{total_ordens}</p></div>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<div style='text-align: center'><p style='font-size: 32px; line-height: 0.9'><b>Total de HH</b><br>{total_hh}</p></div>", unsafe_allow_html=True)
                with col4:
                    st.markdown(f"<div style='text-align: center'><p style='font-size: 32px; line-height: 0.9'><b>Custo Total</b><br>R${custo_total:,.2f}</p></div>", unsafe_allow_html=True)

            # Exibir a tabela de dados com colunas formatadas, ícones e índice oculto
            st.dataframe(styled_df,use_container_width=True,hide_index=True)

        except Exception as e:
            st.error(f"Erro ao ler dados: {e}")
    else:
        st.error("Erro ao conectar ao banco de dados")

def app():
    escopo_screen()