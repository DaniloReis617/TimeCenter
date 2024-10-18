import streamlit as st
from utils import update_data, read_data

@st.dialog("Editar")
def edit_usuario():
    st.subheader("Edição de Usuários")

    usuarios_df = read_data("timecenter.TB_USUARIO")
    nivel_mapping = {1: "Visualizador", 2: "Gestor", 4: "Administrador", 8: "Super Usuário"}
    status_mapping = {"A": "Ativo", "I": "Inativo"}
    
    usuario_selecionado = st.selectbox("Selecione um usuário", usuarios_df['TX_LOGIN'], key="edicao_usuario_dialog")
    
    if usuario_selecionado:
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
                with st.spinner("Salvando informações, por favor aguarde..."):
                    update_data("timecenter.TB_USUARIO", "TX_LOGIN", usuario_info['TX_LOGIN'], dados_atualizados)
                    st.success(f"Usuário {login} atualizado com sucesso!")

