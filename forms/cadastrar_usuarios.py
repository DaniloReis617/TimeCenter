# forms/cadastrar_usuario.py
import streamlit as st
import uuid
from utils import create_data

@st.dialog("Cadastro")
def add_usuario():
    nivel_reverso_mapping = {"Visualizador": 1, "Gestor": 2, "Administrador": 4, "Super Usuário": 8}
    status_reverso_mapping = {"Ativo": "A", "Inativo": "I"}
               
    st.subheader("Cadastro de Novo Usuário")

    with st.form(key="form_novo_usuario_cadastro", clear_on_submit=True, enter_to_submit=False):
        var_Novo_GID = uuid.uuid4()
        cd_GID = str(var_Novo_GID)
        novo_login = st.text_input("Login", key="novo_login_dialog")
        novo_nivel = st.selectbox("Nível de Acesso", ["Visualizador", "Gestor", "Administrador", "Super Usuário"], key="novo_nivel_dialog")
        novo_status = st.selectbox("Status", ["Ativo", "Inativo"], key="novo_status_dialog")
        submit_button = st.form_submit_button("Cadastrar")
        
        if submit_button:
            novo_usuario = {
                "GID":str(cd_GID),
                "TX_LOGIN": novo_login,
                "NR_NIVEL": nivel_reverso_mapping[novo_nivel],
                "FL_STATUS": status_reverso_mapping[novo_status]
            }
            with st.spinner("Salvando informações, por favor aguarde..."):
                create_data("timecenter.TB_USUARIO", novo_usuario)
                st.success(f"Usuário {novo_login} cadastrado com sucesso!")
