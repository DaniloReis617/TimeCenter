# forms/cadastrar_projeto.py
import streamlit as st
import uuid
from utils import create_data

@st.dialog("Cadastro")
def add_empresa():
    with st.form("form_add_empresas", clear_on_submit=True, enter_to_submit=False):
        
        nova_descricao = st.text_input("Descrição do Projeto")
    
        submit_button = st.form_submit_button("Adicionar Empresa")
    
    if submit_button:
        nova_empresa = {
            "GID_EMPRESA":str(uuid.uuid4()),                
            'TX_NOME_EMPRESA': nova_descricao
        }
        with st.spinner("Salvando informações, por favor aguarde..."):
            create_data('timecenter.TB_EMPRESAS', nova_empresa)
            st.success("Projeto adicionado com sucesso!")
            st.session_state['refresh_projetos'] = True
