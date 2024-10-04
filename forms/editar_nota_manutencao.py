import streamlit as st
import pandas as pd
from utils import get_vw_nota_manutencao_hh_data, update_data

# Função para carregar os dados com base no GID_PROJETO
@st.cache_data
def load_data(selected_gid):
    df = get_vw_nota_manutencao_hh_data()

    if df is None or df.empty:
        return pd.DataFrame()

    df = df[df['GID_PROJETO'] == selected_gid]
    # Converter a coluna ID_NOTA_MANUTENCAO para int
    df['ID_NOTA_MANUTENCAO'] = df['ID_NOTA_MANUTENCAO'].astype(int)
    # Ordenar o DataFrame pela coluna ID_NOTA_MANUTENCAO de forma decrescente
    df = df.sort_values(by='ID_NOTA_MANUTENCAO', ascending=False)

    df['VL_HH_TOTAL'] = pd.to_numeric(df['VL_HH_TOTAL'], errors='coerce').fillna(0.0)
    df['VL_CUSTO_TOTAL'] = pd.to_numeric(df['VL_CUSTO_TOTAL'], errors='coerce').fillna(0.0)
    
    return df
@st.dialog("Editar Nota",width="large")
def edit_nota_manutencao():
    # Verifica se o projeto foi selecionado
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return

    # Carregar os dados associados ao projeto
    df = load_data(selected_gid)

    if df.empty:
        st.warning("Nenhuma nota encontrada para o projeto selecionado.")
        return

    # Seleção do ID_NOTA_MANUTENCAO
    st.subheader("Selecione a Nota de Manutenção para Editar")
    id_nota_selected = st.multiselect("ID Nota Manutenção", options=sorted(df['ID_NOTA_MANUTENCAO'].unique()),key="filteridnota")

    # Carregar os dados da nota selecionada
    nota_data = df[df['ID_NOTA_MANUTENCAO'].isin(id_nota_selected)]

    if not nota_data.empty:
        nota_data = nota_data.iloc[0]

        st.write(f"Editando Nota: {id_nota_selected}")
        
        # Formulário de edição
        with st.form(key="edit_nota_form"):
            col1, col2 = st.columns(2)

            with col1:
                cd_projeto = st.text_input("Código do Projeto", nota_data.get('CD_PROJETO', ''))
                tx_nota = st.text_input("Nota", nota_data.get('TX_NOTA', ''))
                tx_ordem = st.text_input("Ordem", nota_data.get('TX_ORDEM', ''))
                tx_tag = st.text_input("Tag", nota_data.get('TX_TAG', ''))
                tx_tag_linha = st.text_input("Tag da Linha", nota_data.get('TX_TAG_LINHA', ''))
            with col2:
                cd_servico = st.text_input("Código do Serviço", nota_data.get('CD_SERVICO', ''))
                tx_descricao_servico = st.text_area("Descrição do Serviço", nota_data.get('TX_DESCRICAO_SERVICO', ''), height=150)

            # Seção Solicitante e Responsável
            st.header("Solicitante e Responsável")
            col1, col2 = st.columns(2)
            with col1:
                cd_setor_solicitante = st.text_input("Setor Solicitante", nota_data.get('CD_SETOR_SOLICITANTE', ''))
                tx_nome_solicitante = st.text_input("Nome do Solicitante", nota_data.get('TX_NOME_SOLICITANTE', ''))
            with col2:
                cd_setor_responsavel = st.text_input("Setor Responsável", nota_data.get('CD_SETOR_RESPONSAVEL', ''))

            # Seção Detalhes Técnicos
            st.header("Detalhes Técnicos")
            col1, col2 = st.columns(2)
            with col1:
                cd_familia_equipamentos = st.text_input("Família de Equipamentos", nota_data.get('CD_FAMILIA_EQUIPAMENTOS', ''))
                cd_planta = st.text_input("Código da Planta", nota_data.get('CD_PLANTA', ''))
                cd_area = st.text_input("Código da Área", nota_data.get('CD_AREA', ''))
                cd_especialidade = st.text_input("Código da Especialidade", nota_data.get('CD_ESPECIALIDADE', ''))
            with col2:
                cd_sistema_operacional_1 = st.text_input("Sistema Operacional 1", nota_data.get('CD_SISTEMA_OPERACIONAL_1', ''))
                cd_sistema_operacional_2 = st.text_input("Sistema Operacional 2", nota_data.get('CD_SISTEMA_OPERACIONAL_2', ''))
                tx_equipamento_mestre = st.text_input("Equipamento Mestre", nota_data.get('TX_EQUIPAMENTO_MESTRE', ''))

            # Seção Escopo e Situação
            st.header("Escopo e Situação")
            col1, col2 = st.columns(2)
            with col1:
                cd_escopo_origem = st.text_input("Origem do Escopo", nota_data.get('CD_ESCOPO_ORIGEM', ''))
                cd_escopo_tipo = st.text_input("Tipo de Escopo", nota_data.get('CD_ESCOPO_TIPO', ''))
                cd_situacao_motivo = st.text_input("Motivo da Situação", nota_data.get('CD_SITUACAO_MOTIVO', ''))
                tx_rec_inspecao = st.text_input("Recomendação de Inspeção", nota_data.get('TX_REC_INSPECAO', ''))
            with col2:
                fl_nmp = st.selectbox("Nota Manutenção Parada?", ["Sim", "Não"], index=0 if nota_data.get('FL_NMP', 'Não') == 'Sim' else 1)
                fl_ase = st.selectbox("Tem Autorização de Serviço Extra?", ["Sim", "Não"], index=0 if nota_data.get('FL_ASE', 'Não') == 'Sim' else 1)
                tx_ase = st.text_input("Autorização Serviço Extra", nota_data.get('TX_ASE', ''))

            # Seção 5: Executantes
            st.header("Executantes")
            col1, col2 = st.columns(2)
            with col1:
                cd_executante_1 = st.text_input("Código do Executante 1", nota_data.get('CD_EXECUTANTE_1', ''))
            with col2:
                cd_executante_2 = st.text_input("Código do Executante 2", nota_data.get('CD_EXECUTANTE_2', ''))



            # Seção Observações
            st.header("Observações")
            # Converter a data de atualização para garantir que seja uma data válida
            dt_atualizacao_raw = nota_data.get('DT_ATUALIZACAO', None)
            if pd.isnull(dt_atualizacao_raw) or isinstance(dt_atualizacao_raw, str):
                dt_atualizacao = st.date_input("Data de Atualização", value=pd.to_datetime('today').date())
            else:
                dt_atualizacao = st.date_input("Data de Atualização", value=pd.to_datetime(dt_atualizacao_raw).date())

            tx_observacao = st.text_area("Observação Adicional", nota_data.get('TX_OBSERVACAO', ''), height=100)

            submit_button = st.form_submit_button(label="Atualizar Nota")

        # Atualizar dados no banco de dados
        if submit_button:
            updated_data = {
                "CD_PROJETO": cd_projeto,
                "TX_NOTA": tx_nota,
                "TX_ORDEM": tx_ordem,
                "TX_TAG": tx_tag,
                "TX_TAG_LINHA": tx_tag_linha,
                "CD_SERVICO": cd_servico,
                "TX_DESCRICAO_SERVICO": tx_descricao_servico,
                "CD_SETOR_SOLICITANTE": cd_setor_solicitante,
                "TX_NOME_SOLICITANTE": tx_nome_solicitante,
                "CD_SETOR_RESPONSAVEL": cd_setor_responsavel,
                "CD_FAMILIA_EQUIPAMENTOS": cd_familia_equipamentos,
                "CD_PLANTA": cd_planta,
                "CD_AREA": cd_area,
                "CD_ESPECIALIDADE": cd_especialidade,
                "CD_SISTEMA_OPERACIONAL_1": cd_sistema_operacional_1,
                "CD_SISTEMA_OPERACIONAL_2": cd_sistema_operacional_2,
                "TX_EQUIPAMENTO_MESTRE": tx_equipamento_mestre,
                "CD_ESCOPO_ORIGEM": cd_escopo_origem,
                "CD_ESCOPO_TIPO": cd_escopo_tipo,
                "CD_SITUACAO_MOTIVO": cd_situacao_motivo,
                "TX_REC_INSPECAO": tx_rec_inspecao,
                "FL_NMP": fl_nmp,
                "FL_ASE": fl_ase,
                "TX_ASE": tx_ase,
                "CD_EXECUTANTE_1": cd_executante_1,
                "CD_EXECUTANTE_2": cd_executante_2,
                "DT_ATUALIZACAO": dt_atualizacao,
                "TX_OBSERVACAO": tx_observacao
            }
            
            update_data('timecenter.TB_NOTA_MANUTENCAO', 'ID_NOTA_MANUTENCAO', id_nota_selected, updated_data)
            st.success("Nota atualizada com sucesso!")

# Função principal
def main():
    edit_nota_manutencao()

if __name__ == "__main__":
    main()
