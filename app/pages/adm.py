import streamlit as st
import os
import pandas as pd
import numpy as np
from utils import apply_custom_style_and_header, get_db_connection, get_vw_nota_manutencao_hh_data, read_data, create_data, update_data, get_projetos_por_usuario, get_descricao_projetos, get_all_projetos, delete_data

def adm_screen():
    apply_custom_style_and_header("Tela de Administração")

    conn = get_db_connection()

    if conn:
        usuarios_df = read_data(conn, "timecenter.TB_USUARIO")

        if usuarios_df.empty:
            st.warning("Nenhum usuário encontrado.")
        else:
            # Criar as abas
            tab1, tab2, tab3 = st.tabs([
                "Dashboards de Usuários", 
                "Projetos por Usuário",
                "Projetos"
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
                                key="cadastro_projeto_por_usuário"
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

            with tab3:
                st.subheader("Gestão de Projetos")
                
                projetos_df = get_all_projetos(conn)

                if not projetos_df.empty:
                    # Mostrar seleção de projetos
                    projeto_selecionado = st.selectbox(
                        "Selecione um projeto para visualizar detalhes", 
                        projetos_df['TX_DESCRICAO'],
                        placeholder="Escolha um Projeto",
                        key="cadastro_projeto"
                    )
                    
                    # Obter GID do projeto selecionado
                    gid_selecionado = projetos_df.loc[projetos_df['TX_DESCRICAO'] == projeto_selecionado, 'GID'].iloc[0]

                    # Este exemplo apenas filtra o DataFrame original, mas você pode fazer mais operações conforme necessário
                    projetos_df_Filtrado = projetos_df[projetos_df['GID'] == gid_selecionado]
                    # Convertendo a coluna ID para texto
                    projetos_df_Filtrado['ID'] = projetos_df_Filtrado['ID'].astype(str)
                    # Convertendo as colunas de data para o formato dd/mm/aaaa
                    projetos_df_Filtrado['DT_INICIO'] = pd.to_datetime(projetos_df_Filtrado['DT_INICIO']).dt.strftime('%d/%m/%Y')
                    projetos_df_Filtrado['DT_TERMINO'] = pd.to_datetime(projetos_df_Filtrado['DT_TERMINO']).dt.strftime('%d/%m/%Y')
                    # Substituindo 'A' por 'Ativo' e 'I' por 'Inativo'
                    projetos_df_Filtrado['FL_STATUS'] = projetos_df_Filtrado['FL_STATUS'].replace({'A': 'Ativo', 'I': 'Inativo'})
                    # Reorganizando as colunas para que FL_STATUS seja a última
                    projetos_df_Filtrado_Reordenado = projetos_df_Filtrado[['ID', 'GID', 'TX_DESCRICAO', 'DT_INICIO', 'DT_TERMINO', 'FL_STATUS']]

                    def color_status(val):
                        if val == "Ativo":
                            color = '#d4edda'  # Verde fraco
                        elif val == "Inativo":
                            color = '#f8d7da'  # Vermelho fraco
                        else:
                            color = ''
                        return f'background-color: {color}'

                    styled_df = projetos_df_Filtrado_Reordenado.style.map(color_status, subset=['FL_STATUS'])


                    # Exibir a tabela de dados com colunas formatadas, ícones e índice oculto
                    st.dataframe(styled_df,use_container_width=True,hide_index=True)

                    action = st.radio("Escolha a ação:", ('Adicionar', 'Editar', 'Excluir'), horizontal=True)

                    if action == 'Adicionar':
                        with st.form("form_add_project"):
                            nova_descricao = st.text_input("Descrição do Projeto")
                            nova_data_inicio = st.date_input("Data de Início")
                            nova_data_termino = st.date_input("Data de Término")
                            novo_status = st.selectbox("Status do Projeto", ['A', 'I'], format_func=lambda x: 'Ativo' if x == 'A' else 'Inativo')
                            submit_button = st.form_submit_button("Adicionar Projeto")
                            
                            if submit_button:
                                novo_projeto = {
                                    'TX_DESCRICAO': nova_descricao,
                                    'DT_INICIO': nova_data_inicio,
                                    'DT_TERMINO': nova_data_termino,
                                    'FL_STATUS': novo_status
                                }
                                create_data(conn, 'timecenter.TB_PROJETO', novo_projeto)
                                st.success("Projeto adicionado com sucesso!")
                                projetos_df = get_all_projetos(conn)

                    elif action == 'Editar':
                        projeto_to_edit = st.selectbox("Selecione o Projeto para Editar:", projetos_df['TX_DESCRICAO'])
                        projeto_info = projetos_df[projetos_df['TX_DESCRICAO'] == projeto_to_edit].iloc[0]
                        def setup_status(projeto_info):
                            status_map = {'A': 'Ativo', 'I': 'Inativo'}
                            # Assegurar que o status no projeto_info está mapeado corretamente
                            mapped_status = status_map.get(projeto_info['FL_STATUS'], 'Ativo')  # Default to 'Ativo' if not found
                            return st.selectbox(
                                "Status do Projeto",
                                ['Ativo', 'Inativo'],
                                index=['Ativo', 'Inativo'].index(mapped_status)
                            )

                        with st.form("form_edit_project"):
                            edit_descricao = st.text_input("Descrição do Projeto", value=projeto_info['TX_DESCRICAO'])
                            edit_data_inicio = st.date_input("Data de Início", value=pd.to_datetime(projeto_info['DT_INICIO']))
                            edit_data_termino = st.date_input("Data de Término", value=pd.to_datetime(projeto_info['DT_TERMINO']))
                            
                            # Mapeie os status para a forma completa antes de passar para o selectbox
                            status_map = {'A': 'Ativo', 'I': 'Inativo'}
                            projeto_info['FL_STATUS'] = status_map[projeto_info['FL_STATUS']]

                            edit_status = st.selectbox(
                                "Status do Projeto",
                                ['Ativo', 'Inativo'],
                                index=['Ativo', 'Inativo'].index(projeto_info['FL_STATUS'])
)

                            submit_button = st.form_submit_button("Atualizar Projeto")
                            
                            if submit_button:
                                updated_project = {
                                    'TX_DESCRICAO': edit_descricao,
                                    'DT_INICIO': edit_data_inicio,
                                    'DT_TERMINO': edit_data_termino,
                                    'FL_STATUS': edit_status
                                }
                                update_data(conn, 'timecenter.TB_PROJETO', 'GID', projeto_info['GID'], updated_project)
                                st.success("Projeto atualizado com sucesso!")
                                projetos_df = get_all_projetos(conn)

                    elif action == 'Excluir':
                        projeto_to_delete = st.selectbox("Selecione o Projeto para Excluir:", projetos_df['TX_DESCRICAO'])
                        if st.button("Excluir Projeto"):
                            projeto_info = projetos_df[projetos_df['TX_DESCRICAO'] == projeto_to_delete].iloc[0]
                            delete_data(conn, 'timecenter.TB_PROJETO', 'GID', projeto_info['GID'])
                            st.success(f"Projeto {projeto_to_delete} excluído com sucesso!")
                            projetos_df = get_all_projetos(conn)
                else:
                    st.error("Não há projetos disponíveis.")

def app():
    adm_screen()