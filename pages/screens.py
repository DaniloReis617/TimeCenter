#TimeCenter\pages\screens.py TEM AS TELAS QUE O APLICATIVO USA
import streamlit as st
import os
import pandas as pd
import numpy as np
from utils import apply_custom_style_and_header, get_db_connection, get_vw_nota_manutencao_hh_data, read_data, create_data, update_data, get_projetos_por_usuario, get_descricao_projetos, get_all_projetos, delete_data

def home_screen():
    apply_custom_style_and_header("Tela Home")
    
    st.write("Esta é a tela inicial do seu aplicativo. Você pode navegar entre as diferentes seções usando o menu à esquerda.")
    st.markdown("""
        ## Instruções
        - Use a barra lateral para navegar entre as seções.
        - Cada seção oferece diferentes funcionalidades relacionadas ao gerenciamento de projetos.
        - Clique em uma seção no menu à esquerda para começar.
    """)

    st.info("Selecione uma seção no menu para começar a explorar o aplicativo.")

def stakeholders_screen():
    apply_custom_style_and_header("Tela de Stakeholders")

        # Criar as abas
    tab1, tab2 = st.tabs(["Stakeholders", "Conteúdo de outra tela"])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Conteúdo da tela de Stakeholders")
        # Conteúdo da aba 1
    with tab2:
        st.write("Conteúdo de outra tela de Stakeholders")


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

def custos_screen():
    apply_custom_style_and_header("Tela de Custos")

    st.write("Conteúdo da tela de Custos")

    # Criar as abas
    tab1, tab2, tab3 = st.tabs(["Prévia dos Custos", "Base Orçamentária", "Gestão do Desembolso"])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Conteúdo da aba Prévia dos Custos do Projeto")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Prévia dos Custos"
    
    # Conteúdo da aba 2
    with tab2:
        st.write("Conteúdo da aba Base Orçamentária do Projeto")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Base Orçamentária"
    
    # Conteúdo da aba 3
    with tab3:
        st.write("Conteúdo da aba Gestão do Desembolso do Projeto")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Gestão do Desembolso"
    

def recursos_screen():
    apply_custom_style_and_header("Tela de Recursos")

    st.write("Conteúdo da tela de Recursos")

    # Criar as abas
    tab1, tab2, tab3 = st.tabs(["Comparativo do HH", "Levantamento do HH", "Histograma Preliminar"])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Conteúdo da aba Comparativo do HH")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Comparativo do HH"
    
    # Conteúdo da aba 2
    with tab2:
        st.write("Conteúdo da aba Levantamento do HH")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Levantamento do HH"
    
    # Conteúdo da aba 3
    with tab3:
        st.write("Conteúdo da aba Histograma Preliminar")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Histograma Preliminar"



def qualidade_screen():
    apply_custom_style_and_header("Tela de Qualidade")

    st.write("Conteúdo da tela de Qualidade")

    # Criar as abas
    tab1, tab2, tab3, tab4 = st.tabs([
        "Plano de Inspeção", 
        "Plano de Ensaios", 
        "Mapa de Juntas", 
        "Plano de Teste"
    ])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Conteúdo da aba Importação do Plano de Inspeção")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Importação do Plano de Inspeção
    
    # Conteúdo da aba 2
    with tab2:
        st.write("Conteúdo da aba Importação do Plano de Ensaios")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Importação do Plano de Ensaios
    
    # Conteúdo da aba 3
    with tab3:
        st.write("Conteúdo da aba Importação do Mapa de Juntas")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Importação do Mapa de Juntas
    
    # Conteúdo da aba 4
    with tab4:
        st.write("Conteúdo da aba Importação do Plano de Teste")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Importação do Plano de Teste



def cronogramas_screen():
    apply_custom_style_and_header("Tela de Cronogramas")

    st.write("Conteúdo da tela de Cronogramas")

    # Criar as abas
    tab1, tab2 = st.tabs([
        "Detalhamento das FT's", 
        "Auditoria dos Cronogramas"
    ])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Conteúdo da aba Detalhamento das FT's")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Detalhamento das FT's
    
    # Conteúdo da aba 2
    with tab2:
        st.write("Conteúdo da aba Auditoria dos Cronogramas")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Auditoria dos Cronogramas



def riscos_screen():
    apply_custom_style_and_header("Tela de Riscos")

    st.write("Conteúdo da tela de Riscos")

    # Criar as abas
    tab1 = st.tabs([
        "Mapeamento dos Riscos por Nota"
    ])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Conteúdo da aba Mapeamento dos Riscos por Nota")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Mapeamento dos Riscos por Nota



def aquisicoes_screen():
    apply_custom_style_and_header("Tela de Aquisições")

    st.write("Conteúdo da tela de Aquisições")

    # Criar as abas
    tab1, tab2 = st.tabs([
        "Plano de Contratação", 
        "Lista de Materiais e Equipamentos"
    ])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Conteúdo da aba Plano de Contratação")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Plano de Contratação
    
    # Conteúdo da aba 2
    with tab2:
        st.write("Conteúdo da aba Lista de Materiais e Equipamentos")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Lista de Materiais e Equipamentos



def integracao_screen():
    apply_custom_style_and_header("Tela de Integração")

    st.write("Conteúdo da tela de Integração")

    # Criar as abas
    tab1, tab2, tab3 = st.tabs([
        "Dashboards", 
        "Auditoria das Fases do Projeto", 
        "Timeline da Parada"
    ])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Conteúdo da aba Dashboards")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Dashboards
    
    # Conteúdo da aba 2
    with tab2:
        st.write("Conteúdo da aba Auditoria das Fases do Projeto")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Auditoria das Fases do Projeto
    
    # Conteúdo da aba 3
    with tab3:
        st.write("Conteúdo da aba Timeline da Parada")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Timeline da Parada

def adm_screen():
    apply_custom_style_and_header("Tela de Administração")

    conn = get_db_connection()

    if conn:
        usuarios_df = read_data(conn, "timecenter.TB_USUARIO")

        if usuarios_df.empty:
            st.warning("Nenhum usuário encontrado.")
        else:
            # Criar as abas
            tab1, tab2 = st.tabs([
                "Dashboards de Usuários", 
                "Lista de Projetos por Usuário"
            ])
            
            # Mapeamentos para os campos NR_NIVEL e FL_STATUS
            nivel_mapping = {1: "Visualizador", 2: "Gestor", 4: "Administrador", 8: "Super Usuário"}
            status_mapping = {"A": "Ativo", "I": "Inativo"}

            # Adiciona as colunas mapeadas ao DataFrame de usuários
            usuarios_df['NR_NIVEL_MAPPED'] = usuarios_df['NR_NIVEL'].map(nivel_mapping)
            usuarios_df['FL_STATUS_MAPPED'] = usuarios_df['FL_STATUS'].map(status_mapping)

            # Variáveis de controle para exibir os contêineres
            if 'show_dashboard' not in st.session_state:
                st.session_state['show_dashboard'] = True
            if 'show_cadastro' not in st.session_state:
                st.session_state['show_cadastro'] = False
            if 'show_edicao' not in st.session_state:
                st.session_state['show_edicao'] = False

            # Função para controlar a visibilidade dos contêineres
            def reset_view():
                st.session_state['show_dashboard'] = True
                st.session_state['show_cadastro'] = False
                st.session_state['show_edicao'] = False

            # Conteúdo da aba 1 - Dashboards de Usuários
            with tab1:
                col1, col2, col3 = st.columns([6, 2, 2])
                with col1:
                    st.header("Dashboard de Usuários")
                
                # Botões que alternam entre os formulários e a tabela
                with col2:
                    if st.button("Cadastro de Novos Usuários"):
                        st.session_state['show_cadastro'] = True
                        st.session_state['show_edicao'] = False
                        st.session_state['show_dashboard'] = False
                with col3:
                    if st.button("Edição de Usuários"):
                        st.session_state['show_edicao'] = True
                        st.session_state['show_cadastro'] = False
                        st.session_state['show_dashboard'] = False

                # Mostrar a tabela de usuários
                if st.session_state['show_dashboard']:
                    with st.container():
                        st.subheader("Lista de Usuários")
                        st.dataframe(usuarios_df[['ID', 'TX_LOGIN', 'FL_STATUS_MAPPED', 'NR_NIVEL_MAPPED']], use_container_width=True, hide_index=True)

                # Mostrar o formulário de cadastro
                if st.session_state['show_cadastro']:
                    with st.container():
                        col1, col2 = st.columns([8, 2])
                        with col1:                        
                            st.subheader("Cadastro de Novo Usuário")
                        with col2:    
                            if st.button("Voltar para a Tabela"):
                                reset_view()

                        with st.form(key="form_novo_usuario_cadastro"):
                            novo_login = st.text_input("Login", key="novo_login_dialog")
                            novo_nivel = st.selectbox("Nível de Acesso", ["Visualizador", "Gestor", "Administrador", "Super Usuário"], key="novo_nivel_dialog")
                            novo_status = st.selectbox("Status", ["Ativo", "Inativo"], key="novo_status_dialog")
                            submit_button = st.form_submit_button("Cadastrar")
                            
                            if submit_button:
                                nivel_reverso_mapping = {"Visualizador": 1, "Gestor": 2, "Administrador": 4, "Super Usuário": 8}
                                status_reverso_mapping = {"Ativo": "A", "Inativo": "I"}
                                
                                novo_usuario = {
                                    "TX_LOGIN": novo_login,
                                    "NR_NIVEL": nivel_reverso_mapping[novo_nivel],
                                    "FL_STATUS": status_reverso_mapping[novo_status]
                                }

                                create_data(conn, "timecenter.TB_USUARIO", novo_usuario)
                                st.success(f"Usuário {novo_login} cadastrado com sucesso!")
                                reset_view()

                # Mostrar o formulário de edição
                if st.session_state['show_edicao']:
                    with st.container():
                        col1, col2 = st.columns([8, 2])
                        with col1:                        
                            st.subheader("Edição de Usuários")
                        with col2:    
                            if st.button("Voltar para a Tabela"):
                                reset_view()
                        
                        usuario_selecionado = st.selectbox("Selecione um usuário", usuarios_df['TX_LOGIN'], key="edicao_usuario_dialog")
                        usuario_info = usuarios_df[usuarios_df['TX_LOGIN'] == usuario_selecionado].iloc[0]
                        nivel_atual = nivel_mapping.get(usuario_info['NR_NIVEL'], "Perfil Desconhecido")
                        status_atual = status_mapping.get(usuario_info['FL_STATUS'], "Status Desconhecido")
                        
                        with st.form(key=f"form_editar_usuario_dialog_{usuario_selecionado}"):
                            login = st.text_input("Login", value=usuario_info['TX_LOGIN'], key="edicao_login_dialog")
                            nivel = st.selectbox("Nível de Acesso", ["Visualizador", "Gestor", "Administrador", "Super Usuário"], index=["Visualizador", "Gestor", "Administrador", "Super Usuário"].index(nivel_atual), key="edicao_nivel_dialog")
                            status = st.selectbox("Status", ["Ativo", "Inativo"], index=["Ativo", "Inativo"].index(status_atual), key="edicao_status_dialog")
                            submit_button = st.form_submit_button("Atualizar")
                            
                            if submit_button:
                                nivel_reverso_mapping = {"Visualizador": 1, "Gestor": 2, "Administrador": 4, "Super Usuário": 8}
                                status_reverso_mapping = {"Ativo": "A", "Inativo": "I"}
                                
                                dados_atualizados = {
                                    "TX_LOGIN": login,
                                    "NR_NIVEL": nivel_reverso_mapping[nivel],
                                    "FL_STATUS": status_reverso_mapping[status]
                                }
                                update_data(conn, "timecenter.TB_USUARIO", "TX_LOGIN", usuario_info['TX_LOGIN'], dados_atualizados)
                                st.success(f"Usuário {login} atualizado com sucesso!")
                                reset_view()

            # Conteúdo da aba 2 - Projetos por Usuário
            with tab2:
                # Controle de exibição dos contêineres
                if 'show_projetos_dashboard' not in st.session_state:
                    st.session_state['show_projetos_dashboard'] = True
                if 'show_projetos_cadastro' not in st.session_state:
                    st.session_state['show_projetos_cadastro'] = False

                # Função para resetar a visualização
                def reset_projetos_view():
                    st.session_state['show_projetos_dashboard'] = True
                    st.session_state['show_projetos_cadastro'] = False

                col1, col2 = st.columns([6, 6])
                with col1:
                    st.subheader("Projetos por Usuário")
                
                # Botão para alternar entre cadastro e visualização
                with col2:
                    if st.button("Cadastro de Projetos", key="projeto_cadastro"):
                        st.session_state['show_projetos_cadastro'] = True
                        st.session_state['show_projetos_dashboard'] = False

                # Mostrar a tabela de projetos
                if st.session_state['show_projetos_dashboard']:
                    usuario_selecionado_projeto = st.selectbox(
                        "Selecione um usuário", 
                        usuarios_df['TX_LOGIN'], 
                        key="projeto_usuario"
                    )
                    usuario_info_projeto = usuarios_df[usuarios_df['TX_LOGIN'] == usuario_selecionado_projeto].iloc[0]
                    
                    projetos_df = get_projetos_por_usuario(conn, usuario_info_projeto['GID'])

                    if not projetos_df.empty:
                        cd_projetos_list = projetos_df['CD_PROJETO'].unique().tolist()
                        if cd_projetos_list:
                            projetos_desc_df = get_descricao_projetos(conn, cd_projetos_list)

                            # Fazer o merge das descrições com os projetos
                            projetos_df = projetos_df.merge(projetos_desc_df, left_on='CD_PROJETO', right_on='GID', how='left')

                            st.subheader(f"Projetos associados ao usuário {usuario_selecionado_projeto}")
                            st.dataframe(projetos_df[['CD_PROJETO', 'TX_DESCRICAO']], use_container_width=True, hide_index=True)

                            # Adicionar a funcionalidade de exclusão
                            projeto_para_excluir = st.selectbox(
                                "Selecione um projeto para excluir", 
                                projetos_df['TX_DESCRICAO'], 
                                key=f"exclusao_projeto_{usuario_selecionado_projeto}"
                            )
                            projeto_info = projetos_df[projetos_df['TX_DESCRICAO'] == projeto_para_excluir].iloc[0]
                            
                            if st.button("Excluir Projeto"):
                                delete_data(conn, "timecenter.TB_USUARIO_PROJETO", "CD_PROJETO", projeto_info['CD_PROJETO'])
                                st.success(f"Projeto {projeto_para_excluir} excluído com sucesso!")
                                reset_projetos_view()

                    else:
                        st.warning(f"Este usuário ({usuario_selecionado_projeto}) não tem acesso a nenhum projeto.")

                # Formulário de cadastro de projetos na tabela TB_USUARIO_PROJETO
                if st.session_state['show_projetos_cadastro']:
                    with st.container():
                        col1, col2 = st.columns([8, 2])
                        with col1:                        
                            st.subheader("Cadastro de Projeto para o Usuário")
                        with col2:    
                            if st.button("Voltar para Tabela"):
                                reset_projetos_view()

                        # Formulário de cadastro
                        with st.form(key="form_cadastro_projeto_usuario"):
                            # Selecionar o usuário para cadastro
                            usuario_selecionado_cadastro = st.selectbox(
                                "Selecione um usuário para cadastrar um projeto", 
                                usuarios_df['TX_LOGIN'], 
                                key="cadastro_usuario"
                            )
                            usuario_info_cadastro = usuarios_df[usuarios_df['TX_LOGIN'] == usuario_selecionado_cadastro].iloc[0]

                            # Mostrar o ID do usuário selecionado (somente visualização)
                            st.text_input("ID do Usuário", value=usuario_info_cadastro['GID'], key="cadastro_cd_usuario", disabled=True)

                            # Selecionar o projeto pela descrição (TX_DESCRICAO), mas armazenar o GID (ID do projeto)
                            projetos_desc_df = get_all_projetos(conn)  # Função que obtém todos os projetos
                            projeto_selecionado = st.selectbox(
                                "Selecione um projeto", 
                                projetos_desc_df['TX_DESCRICAO'], 
                                key="cadastro_projeto"
                            )
                            cd_projeto = projetos_desc_df.loc[projetos_desc_df['TX_DESCRICAO'] == projeto_selecionado, 'GID'].iloc[0]

                            nivel_acesso = st.selectbox("Nível de Acesso", ["Visualizador", "Gestor", "Administrador", "Super Usuário"], key="cadastro_nivel_acesso")
                            status_projeto = st.selectbox("Status no Projeto", ["Ativo", "Inativo"], key="cadastro_status_projeto")
                            submit_button = st.form_submit_button("Cadastrar Projeto para Usuário")

                            if submit_button:
                                # Mapear nível e status para os valores esperados
                                nivel_reverso_mapping = {"Visualizador": 1, "Gestor": 2, "Administrador": 4, "Super Usuário": 8}
                                status_reverso_mapping = {"Ativo": "A", "Inativo": "I"}

                                novo_projeto_usuario = {
                                    "CD_PROJETO": cd_projeto,  # Salvar o ID do projeto
                                    "CD_USUARIO": usuario_info_cadastro['GID'],  # Adiciona o ID do usuário no cadastro
                                    "NR_NIVEL": nivel_reverso_mapping[nivel_acesso],
                                    "FL_STATUS": status_reverso_mapping[status_projeto]
                                }

                                # Função para cadastrar o projeto para o usuário na tabela TB_USUARIO_PROJETO
                                create_data(conn, "timecenter.TB_USUARIO_PROJETO", novo_projeto_usuario)
                                st.success(f"Projeto {projeto_selecionado} cadastrado com sucesso para o usuário {usuario_selecionado_cadastro}!")
                                reset_projetos_view()