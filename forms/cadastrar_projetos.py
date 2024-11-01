# forms/cadastrar_projeto.py
import streamlit as st
import uuid
from utils import create_data

@st.dialog("Cadastro")
def add_projeto():
    with st.form("form_add_project", clear_on_submit=True, enter_to_submit=False):
        collayout_cad_proj1, collayout_cad_proj2 = st.columns(2)
        with collayout_cad_proj1:
            var_Novo_GID = uuid.uuid4()
            cd_GID = str(var_Novo_GID)
            nova_descricao = st.text_input("Descrição do Projeto")
            nova_data_inicio = st.date_input("Data de Início")
            nova_data_termino = st.date_input("Data de Término")
            novo_orcamento = st.text_input("Orçamento (R$)", value="0.00")  # Campo de orçamento
            
        with collayout_cad_proj2:
            novo_percentual_contingencia = st.text_input("Contingência (%)", value="0.00")  # Campo de contingência
            novo_status = st.selectbox("Status do Projeto", ['A', 'I'], format_func=lambda x: 'Ativo' if x == 'A' else 'Inativo')
            novas_informacoes = st.text_area("Informações Adicionais")
        
        submit_button = st.form_submit_button("Adicionar Projeto")
        
        if submit_button:
            novo_projeto = {
                "GID":str(cd_GID),                
                'TX_DESCRICAO': nova_descricao,
                'DT_INICIO': nova_data_inicio,
                'DT_TERMINO': nova_data_termino,
                'VL_VALOR_ORCAMENTO': float(novo_orcamento.replace(",", ".")),
                'VL_PERCENTUAL_CONTINGENCIA': float(novo_percentual_contingencia.replace(",", ".")),
                'FL_STATUS': novo_status,
                'TX_INFORMACAO': novas_informacoes
            }
            with st.spinner("Salvando informações, por favor aguarde..."):
                create_data('timecenter.TB_PROJETO', novo_projeto)
                st.success("Projeto adicionado com sucesso!")
                st.session_state['refresh_projetos'] = True
