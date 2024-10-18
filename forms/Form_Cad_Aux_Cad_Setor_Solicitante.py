import streamlit as st
import pandas as pd
import uuid
from utils import (create_data, read_data,
                   convert_to_native_types, 
                   get_servicos_projeto, 
                   get_situacao_motivo_projeto, 
                   get_setor_solicitante_projeto, 
                   get_setor_responsavel_projeto, 
                   get_familia_equipamentos_projeto,
                   get_plantas_projeto,
                   get_especialidades_projeto,
                   get_areas_projeto,
                   get_sistemas_operacionais_projeto,
                   get_escopo_origem_projeto,
                   get_escopo_tipo_projeto,
                   get_executantes_projeto
)

@st.dialog("Formulário de Cadastro de Setor Solicitante - Manutenção", width="large")
def cad_novo_setor_solicitante_adm():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return

        
    with st.form(key="new_cad_form_setor_solicitante"):

        # Campo oculto do projeto
        cd_projeto = selected_gid
        # Gerar um novo GUID
        var_Novo_GID = uuid.uuid4()
        cd_GID = str(var_Novo_GID)
        var_tx_descricao = st.text_input("Descrição")


        submit_button = st.form_submit_button(label="Cadastrar Setor Solicitante")

    if submit_button:
        new_data_setor_solicitante = {
            "GID":str(cd_GID),
            "CD_PROJETO": str(cd_projeto),
            "TX_DESCRICAO": str(var_tx_descricao)        
        }
        
        try:
            with st.spinner("Salvando informações, por favor aguarde..."):
                create_data('timecenter.TB_CADASTRO_SETOR_SOLICITANTE ', new_data_setor_solicitante)
                st.success("Novo registro cadastrada com sucesso!")
        except Exception as e:
            st.error(f"Erro ao realizar o novo registro na tabela timecenter.TB_CADASTRO_SETOR_SOLICITANTE : {e}")

def main():
    cad_novo_setor_solicitante_adm()

if __name__ == "__main__":
    main()