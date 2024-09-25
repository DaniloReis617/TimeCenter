# forms/cadastrar_projeto.py
import streamlit as st
from utils import create_data

@st.dialog("Cadastro")
def add_projeto():
    with st.form("form_add_project"):
        nova_descricao = st.text_input("Descrição do Projeto")
        nova_data_inicio = st.date_input("Data de Início")
        nova_data_termino = st.date_input("Data de Término")
        novo_orcamento = st.text_input("Orçamento (R$)", value="0.00")  # Campo de orçamento
        novo_percentual_contingencia = st.text_input("Contingência (%)", value="0.00")  # Campo de contingência
        novo_status = st.selectbox("Status do Projeto", ['A', 'I'], format_func=lambda x: 'Ativo' if x == 'A' else 'Inativo')
        novas_informacoes = st.text_area("Informações Adicionais")
        
        submit_button = st.form_submit_button("Adicionar Projeto")
        
        if submit_button:
            novo_projeto = {
                'TX_DESCRICAO': nova_descricao,
                'DT_INICIO': nova_data_inicio,
                'DT_TERMINO': nova_data_termino,
                'VL_VALOR_ORCAMENTO': float(novo_orcamento.replace(",", ".")),
                'VL_PERCENTUAL_CONTINGENCIA': float(novo_percentual_contingencia.replace(",", ".")),
                'FL_STATUS': novo_status,
                'TX_INFORMACAO': novas_informacoes
            }
            create_data('timecenter.TB_PROJETO', novo_projeto)
            st.success("Projeto adicionado com sucesso!")
            st.session_state['refresh_projetos'] = True
