import streamlit as st
import pandas as pd
import uuid
from utils import (create_data)

@st.dialog("Formulário de Cadastro de Area", width="large")
def cad_novo_area_adm():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return

        
    with st.form(key="new_cad_form_area"):
        col1, col2 = st.columns(2)

        with col1:
            # Campo oculto do projeto
            cd_projeto = selected_gid

            # Gerar um novo GUID
            var_Novo_GID = uuid.uuid4()
            cd_GID = str(var_Novo_GID)
            var_tx_descricao = st.text_input("Descrição")

        with col2:
            var_vl_qtde_dias_exec = st.text_input("Qtde. dias de Execução", value="0")



        submit_button = st.form_submit_button(label="Cadastrar Area")

    if submit_button:
        new_data_area = {
            "GID":str(cd_GID),
            "CD_PROJETO": str(cd_projeto),
            "TX_DESCRICAO": str(var_tx_descricao),
            'VL_QUANTIDADE_DIAS_EXECUCAO': str(var_vl_qtde_dias_exec)
         

        }
        
        try:
            with st.spinner("Salvando informações, por favor aguarde..."):
                create_data('timecenter.TB_CADASTRO_AREA', new_data_area)
                st.success("Novo registro cadastrado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao realizar o novo registro na tabela timecenter.TB_CADASTRO_AREA: {e}")

def main():
    cad_novo_area_adm()

if __name__ == "__main__":
    main()