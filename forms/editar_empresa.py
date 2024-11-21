import streamlit as st
import pandas as pd
from utils import update_data, read_data

@st.dialog("Editar")
def edit_empresa():
    st.subheader("Edição de empresa")
    empresa_df = read_data("timecenter.TB_EMPRESAS")
    empresa_selecionado = st.selectbox("Selecione uma empresa", empresa_df['TX_NOME_EMPRESA'], key="edicao_empresa_dialog")
    
    if empresa_selecionado:
        empresa_info = empresa_df[empresa_df['TX_NOME_EMPRESA'] == empresa_selecionado].iloc[0]
        
        with st.form(key=f"form_editar_empresa_dialog_{empresa_selecionado}", enter_to_submit=False):

            edit_descricao = st.text_input("Descrição do empresa", value=empresa_info['TX_NOME_EMPRESA'])

            submit_button = st.form_submit_button("Atualizar empresa")
        
        if submit_button:
            updated_empresa = {
                'TX_NOME_EMPRESA': edit_descricao
            }
            with st.spinner("Salvando informações, por favor aguarde..."):
                update_data('timecenter.TB_empresa', 'GID_EMPRESA', empresa_info['GID_EMPRESA'], updated_empresa)
                st.success("Empresa atualizado com sucesso!")
                st.session_state['refresh_projetos'] = True

