import streamlit as st
import pandas as pd
import uuid
from utils import (create_data, get_lancamento_despesas)

@st.dialog("Formulário de Cadastro de Lançamento de Nota", width="large")
def cad_novo_lancamento_despesa_adm():
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
            df_lancamento_df = get_lancamento_despesas(selected_gid)
            df_lancamento_map = dict(zip(df_lancamento_df['TX_DESCRICAO'], df_lancamento_df['GID'])) if not df_lancamento_df.empty else {}
            df_lancamento_selecionado = st.selectbox("Tipo de Escopo", options=list(df_lancamento_map.keys()) or [''])
            var_cd_despesa = df_lancamento_map.get(df_lancamento_selecionado, None)
            dt_data_lancamento = st.date_input("Data da Nota", value=pd.to_datetime('today').date())

        with col2:
            var_vl_valor_custo = st.text_input("Valor de Custo (R$)", value="0.00")
            var_tx_observacao = st.text_area("Observação Adicional", "", height=100)            



        submit_button = st.form_submit_button(label="Cadastro de Lançamento de Nota")

    if submit_button:
        new_data_lancamento_despesa = {
            "GID":str(cd_GID),
            "CD_PROJETO": str(cd_projeto),
            "CD_DESPESA": str(var_cd_despesa),
            "DT_LANCAMENTO": str(dt_data_lancamento),
            'VL_VALOR_CUSTO': str(var_vl_valor_custo),
            'TX_OBSERVACAO': str(var_tx_observacao)            
        }
        
        try:
            with st.spinner("Salvando informações, por favor aguarde..."):
                create_data('timecenter.TB_LANCAMENTO_DESPESA', new_data_lancamento_despesa)
                st.success("Novo registro cadastrado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao realizar o novo registro na tabela timecenter.TB_LANCAMENTO_DESPESA: {e}")

def main():
    cad_novo_lancamento_despesa_adm()

if __name__ == "__main__":
    main()