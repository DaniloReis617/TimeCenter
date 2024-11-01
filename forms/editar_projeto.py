import streamlit as st
import pandas as pd
from utils import update_data, read_data

@st.dialog("Editar")
def edit_projeto():
    st.subheader("Edição de Projetos")
    projetos_df = read_data("timecenter.TB_PROJETO")
    projeto_selecionado = st.selectbox("Selecione um projeto", projetos_df['TX_DESCRICAO'], key="edicao_projeto_dialog")
    
    if projeto_selecionado:
        projeto_info = projetos_df[projetos_df['TX_DESCRICAO'] == projeto_selecionado].iloc[0]
        
        with st.form(key=f"form_editar_projeto_dialog_{projeto_selecionado}", enter_to_submit=False):
            collayout_edit_proj1, collayout_edit_proj2 = st.columns(2)
            with collayout_edit_proj1:
                edit_descricao = st.text_input("Descrição do Projeto", value=projeto_info['TX_DESCRICAO'])
                edit_data_inicio = st.date_input("Data de Início", value=pd.to_datetime(projeto_info['DT_INICIO']))
                edit_data_termino = st.date_input("Data de Término", value=pd.to_datetime(projeto_info['DT_TERMINO']))
            with collayout_edit_proj2:
                edit_orcamnto = st.text_input("Orçamento do Projeto", value=projeto_info['VL_VALOR_ORCAMENTO'])
                edit_contigencia = st.text_input("Contingência do Projeto", value=projeto_info['VL_PERCENTUAL_CONTINGENCIA'])
                edit_informacoes = st.text_area("Informações do Projeto", value=projeto_info['TX_INFORMACAO'], height=100)
                
                # Mapeie os status para a forma completa antes de passar para o selectbox
                status_map = {'A': 'Ativo', 'I': 'Inativo'}
                projeto_info['FL_STATUS'] = status_map.get(projeto_info['FL_STATUS'], 'Ativo')

                edit_status = st.selectbox(
                    "Status do Projeto",
                    ['Ativo', 'Inativo'],
                    index=['Ativo', 'Inativo'].index(projeto_info['FL_STATUS'])
                )

            submit_button = st.form_submit_button("Atualizar Projeto")
            
            if submit_button:
                # Mapear o status para 'A' ou 'I'
                status_reverso_mapping = {'Ativo': 'A', 'Inativo': 'I'}
                updated_project = {
                    'TX_DESCRICAO': edit_descricao,
                    'DT_INICIO': edit_data_inicio,
                    'DT_TERMINO': edit_data_termino,
                    'VL_VALOR_ORCAMENTO': edit_orcamnto,
                    'VL_PERCENTUAL_CONTINGENCIA': edit_contigencia,
                    'FL_STATUS': status_reverso_mapping[edit_status],
                    'TX_INFORMACAO': edit_informacoes
                }
                with st.spinner("Salvando informações, por favor aguarde..."):
                    update_data('timecenter.TB_PROJETO', 'GID', projeto_info['GID'], updated_project)
                    st.success("Projeto atualizado com sucesso!")
                    st.session_state['refresh_projetos'] = True

