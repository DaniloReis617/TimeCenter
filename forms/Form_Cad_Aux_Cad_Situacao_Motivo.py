import streamlit as st
import pandas as pd
import uuid
from utils import (create_data)

@st.dialog("Formulário de Cadastro de Situação Motivo - Manutenção", width="large")
def cad_novo_situacao_motivo_adm():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return

        
    with st.form(key="new_cad_form_situacao_motivo"):

        # Campo oculto do projeto
        cd_projeto = selected_gid
        # Gerar um novo GUID
        var_Novo_GID = uuid.uuid4()
        cd_GID = str(var_Novo_GID)
        var_tx_descricao = st.text_input("Descrição")


        submit_button = st.form_submit_button(label="Cadastrar Situação Motivo")

    if submit_button:
        new_data_situacao_motivo = {
            "GID":str(cd_GID),
            "CD_PROJETO": str(cd_projeto),
            "TX_DESCRICAO": str(var_tx_descricao)        
        }
        
        try:
            with st.spinner("Salvando informações, por favor aguarde..."):
                create_data('timecenter.TB_CADASTRO_SITUACAO_MOTIVO ', new_data_situacao_motivo)
                st.success("Novo registro cadastrada com sucesso!")
        except Exception as e:
            st.error(f"Erro ao realizar o novo registro na tabela timecenter.TB_CADASTRO_SITUACAO_MOTIVO : {e}")

def main():
    cad_novo_situacao_motivo_adm()

if __name__ == "__main__":
    main()