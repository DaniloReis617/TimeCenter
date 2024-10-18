import streamlit as st
import pandas as pd
import uuid
from utils import (create_data)

tblTipoApoio = pd.DataFrame([
	{ "Tipo": "Acesso"},
	{ "Tipo": "Alpinismo"},
	{ "Tipo": "Automação"},
	{ "Tipo": "Calibração de Válvulas"},
	{ "Tipo": "Civil"},
	{ "Tipo": "Espaço Confinado"},
	{ "Tipo": "Espoletamento"},
	{ "Tipo": "Fabricação"},
	{ "Tipo": "Hidrojato"},
	{ "Tipo": "Inspeção (ENDs)"},
	{ "Tipo": "Inspeção (Ensaios Especiais)"},
	{ "Tipo": "Isolamento"},
	{ "Tipo": "Manutenção Externa"},
	{ "Tipo": "Máquina de Carga Horizontal"},
	{ "Tipo": "Máquina de Carga Vertical"},
	{ "Tipo": "Outros"},
	{ "Tipo": "Pintura"},
	{ "Tipo": "Retubagem"},
	{ "Tipo": "Usinagem"}
])

@st.dialog("Formulário de Cadastro de Apoio", width="large")
def cad_novo_apoio_adm():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return

        
    with st.form(key="new_cad_form_apoio"):
        col1, col2 = st.columns(2)

        with col1:
            # Campo oculto do projeto
            cd_projeto = selected_gid

            # Gerar um novo GUID
            var_Novo_GID = uuid.uuid4()
            cd_GID = str(var_Novo_GID)
            var_tx_descricao = st.text_input("Descrição")
            var_tx_tipo = st.selectbox("Tipo:", tblTipoApoio['Tipo'].unique())

        with col2:
            var_vl_valor_custo = st.text_input("Valor de Custo (R$)", value="0.00")
            var_vl_percentual_custo = st.text_input("Perc. de Custo (%)", value="0.00")


        submit_button = st.form_submit_button(label="Cadastrar Apoio")

    if submit_button:
        new_data_apoio = {
            "GID":str(cd_GID),
            "CD_PROJETO": str(cd_projeto),
            "TX_DESCRICAO": str(var_tx_descricao),
            "TX_TIPO": str(var_tx_tipo),
            'VL_VALOR_CUSTO': str(var_vl_valor_custo),
            'VL_PERCENTUAL_CUSTO': str(var_vl_percentual_custo)            
        }
        
        try:
            with st.spinner("Salvando informações, por favor aguarde..."):
                create_data('timecenter.TB_CADASTRO_APOIO', new_data_apoio)
                st.success("Novo registro cadastrado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao realizar o novo registro na tabela timecenter.TB_CADASTRO_APOIO: {e}")

def main():
    cad_novo_apoio_adm()

if __name__ == "__main__":
    main()