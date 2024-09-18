# forms/cadastrar_projeto.py
import streamlit as st
from utils import create_data

@st.dialog("Cadastro")
def add_projeto():
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
            create_data('timecenter.TB_PROJETO', novo_projeto)
            st.success("Projeto adicionado com sucesso!")
            st.session_state['refresh_projetos'] = True
