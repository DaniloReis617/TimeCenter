import streamlit as st
import pandas as pd
from utils import apply_custom_style_and_header, get_db_connection, read_data, create_data, update_data, get_all_projetos, get_projetos_por_usuario, get_descricao_projetos
from forms.cadastrar_usuarios import add_usuario
from forms.editar_usuario import edit_usuario
from forms.cadastrar_projetos import add_projeto
from forms.editar_projeto import edit_projeto
from forms.cadastrar_usuarios_por_projetos import add_projeto_usuario
from forms.editar_usuarios_por_projetos import editar_projeto_usuario

def adm_screen():
    apply_custom_style_and_header("Tela de Administração")

    # Conectar ao banco de dados
    conn = get_db_connection()

    if conn:
        # Criar as abas
        tab1, tab2, tab3 = st.tabs([
            "Dashboards de Usuários", 
            "Projetos por Usuário", 
            "Gestão de Projetos"
        ])
        
        # Conteúdo da aba 1
        with tab1:
            col1, col2, col3 = st.columns([8,1,1])
            with col1:
                st.header("Dashboard de Usuários")
            with col2:
                if st.button("➕👤 Novo",key="adduser"):
                    add_usuario()
            with col3:
                if st.button("✏️👤 Editar",key="edituser"):
                    edit_usuario()

            show_user_dashboard()
        
        # Conteúdo da aba 2
        with tab2:
            col1, col2, col3 = st.columns([8,1,1])
            with col1:
                st.header("Gestão de Usuários por Projetos")
            with col2:
                if st.button("➕👤 Novo",key="addUserProj"):
                    add_projeto_usuario()
            with col3:
                if st.button("✏️👤 Editar",key="editUserProj"):
                    editar_projeto_usuario()
            show_projetos_por_usuario()
        
        # Conteúdo da aba 3
        with tab3:
            col1, col2, col3 = st.columns([8,1,1])
            with col1:
                st.header("Gestão de Projetos")
            with col2:
                if st.button("➕👤 Novo",key="addproj"):
                    add_projeto()
            with col3:
                if st.button("✏️👤 Editar",key="editproj"):
                    edit_projeto()
            show_gestao_projetos()

def show_user_dashboard():
    usuarios_df = read_data("timecenter.TB_USUARIO")

    if usuarios_df.empty:
        st.warning("Nenhum usuário encontrado.")
        return

    # Mapeamento de campos
    nivel_mapping = {1: "Visualizador", 2: "Gestor", 4: "Administrador", 8: "Super Usuário"}
    status_mapping = {"A": "Ativo", "I": "Inativo"}
    
    usuarios_df['NR_NIVEL_MAPPED'] = usuarios_df['NR_NIVEL'].map(nivel_mapping)
    usuarios_df['FL_STATUS_MAPPED'] = usuarios_df['FL_STATUS'].map(status_mapping)

    st.subheader("Lista de Usuários")
    st.dataframe(usuarios_df[['ID', 'TX_LOGIN', 'FL_STATUS_MAPPED', 'NR_NIVEL_MAPPED']], use_container_width=True, hide_index=True)

def show_projetos_por_usuario():
    st.subheader("Projetos por Usuário")

    # Carregar os usuários
    usuarios_df = read_data("timecenter.TB_USUARIO")

    # Selecionar um usuário (com opção de não selecionar nenhum)
    usuario_selecionado = st.selectbox("Selecione um usuário (ou deixe em branco para ver todos)", [""] + usuarios_df['TX_LOGIN'].tolist())

    if usuario_selecionado:
        # Se um usuário for selecionado, filtrar os projetos desse usuário
        usuario_info = usuarios_df[usuarios_df['TX_LOGIN'] == usuario_selecionado].iloc[0]
        projetos_df = get_projetos_por_usuario(usuario_info['GID'])
        if projetos_df.empty:
            st.warning(f"Este usuário ({usuario_selecionado}) não tem projetos.")
            return
        # Obter descrições dos projetos
        projetos_desc_df = get_descricao_projetos(projetos_df['CD_PROJETO'].unique().tolist())
        projetos_df = projetos_df.merge(projetos_desc_df, left_on='CD_PROJETO', right_on='GID')
    else:
        # Se nenhum usuário for selecionado, mostrar todos os projetos
        projetos_df = get_all_projetos()
        if projetos_df.empty:
            st.error("Não há projetos disponíveis.")
            return

    # Exibir a tabela de projetos
    st.dataframe(projetos_df[['TX_DESCRICAO']], use_container_width=True, hide_index=True)

def show_gestao_projetos():
    st.subheader("Lista de Projetos")

    projetos_df = get_all_projetos()
    if projetos_df.empty:
        st.error("Não há projetos disponíveis.")
        return
    
    status_mapping = {"A": "Ativo", "I": "Inativo"}
    
    # Mapeamento do status
    projetos_df['FL_STATUS_MAPPED'] = projetos_df['FL_STATUS'].map(status_mapping)
    
    # Formatação das colunas de data
    projetos_df['DT_INICIO'] = pd.to_datetime(projetos_df['DT_INICIO']).dt.strftime('%d/%m/%Y')
    projetos_df['DT_TERMINO'] = pd.to_datetime(projetos_df['DT_TERMINO']).dt.strftime('%d/%m/%Y')

    st.dataframe(projetos_df[['ID', 'TX_DESCRICAO', 'FL_STATUS_MAPPED', 'DT_INICIO', 'DT_TERMINO']], use_container_width=True, hide_index=True)


def app():
    adm_screen()