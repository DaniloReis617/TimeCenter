# forms/cadastrar_projeto_por_usuario.py
import streamlit as st
from utils import create_data, get_all_projetos

def add_projeto_usuario(conn, usuarios_df):
    # Selecionar o usuário para cadastro
    usuario_selecionado_cadastro = st.selectbox(
        "Selecione um usuário para cadastrar um projeto", 
        usuarios_df['TX_LOGIN'], 
        key="cadastro_usuario_projeto"
    )
    usuario_info_cadastro = usuarios_df[usuarios_df['TX_LOGIN'] == usuario_selecionado_cadastro].iloc[0]

    # Mostrar o ID do usuário selecionado (somente visualização)
    st.text_input("ID do Usuário", value=usuario_info_cadastro['GID'], key="cadastro_cd_usuario", disabled=True)

    # Selecionar o projeto pela descrição (TX_DESCRICAO), mas armazenar o GID (ID do projeto)
    projetos_desc_df = get_all_projetos(conn)  # Função que obtém todos os projetos
    projeto_selecionado = st.selectbox(
        "Selecione um projeto", 
        projetos_desc_df['TX_DESCRICAO'], 
        key="cadastro_projeto_usuario"
    )
    cd_projeto = projetos_desc_df.loc[projetos_desc_df['TX_DESCRICAO'] == projeto_selecionado, 'GID'].iloc[0]

    nivel_acesso = st.selectbox("Nível de Acesso", ["Visualizador", "Gestor", "Administrador", "Super Usuário"], key="cadastro_nivel_acesso_usuario")
    status_projeto = st.selectbox("Status no Projeto", ["Ativo", "Inativo"], key="cadastro_status_projeto_usuario")
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
        st.session_state['show_projetos_dashboard'] = True
        st.session_state['show_projetos_cadastro'] = False
