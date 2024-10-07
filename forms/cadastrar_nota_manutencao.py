import streamlit as st
import pandas as pd
from utils import (create_data, read_data, 
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

@st.cache_data
def load_data(selected_gid):
    df = read_data("timecenter.TB_NOTA_MANUTENCAO")

    if df is None or df.empty:
        return pd.DataFrame()

    df = df[df['CD_PROJETO'] == selected_gid]
    df['ID'] = df['ID'].astype(int)
    df = df.sort_values(by='ID', ascending=False)
    
    return df

@st.dialog("Cadastrar Nova Nota", width="large")
def cadastrar_nota_manutencao():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return

    st.write(f"Cadastrando nova nota para o projeto: {selected_gid}")
        
    with st.form(key="new_nota_form"):
        col1, col2 = st.columns(2)

        with col1:
            cd_projeto = selected_gid



            dt_data = st.date_input("Data da Nota", value=pd.to_datetime('today').date())

            situacao_map = {'P': 'Pendente', 'A': 'Aprovado', 'R': 'Reprovado'}
            situacao_nota = st.selectbox("Situação da Nota", options=list(situacao_map.values()))
            fl_situacao_nota = {v: k for k, v in situacao_map.items()}[situacao_nota]

            tx_nota = st.text_input("Nota", "")
            tx_ordem = st.text_input("Ordem", "")
            tx_tag = st.text_input("Tag", "")
            tx_tag_linha = st.text_input("Tag da Linha", "")

        with col2:
            servicos_df = get_servicos_projeto(selected_gid)

            if servicos_df.empty:
                st.warning("Nenhum serviço encontrado para este projeto.")
                cd_servico = None
                tx_descricao_servico = None
            else:
                servico_map = dict(zip(servicos_df['TX_DESCRICAO'], servicos_df['GID']))
                
                descricao_servico_selecionada = st.selectbox("Código do Serviço", options=list(servico_map.keys()))
                cd_servico = servico_map[descricao_servico_selecionada]
                tx_descricao_servico = st.text_area("Descrição do Serviço", "", height=150)

            situacao_motivo_df = get_situacao_motivo_projeto(selected_gid)

            if situacao_motivo_df.empty:
                st.warning("Nenhum motivo de situação encontrado para este projeto.")
                cd_situacao_motivo = None
            else:
                situacao_motivo_map = dict(zip(situacao_motivo_df['TX_DESCRICAO'], situacao_motivo_df['GID']))
                motivo_situacao_selecionado = st.selectbox("Motivo da Situação", options=list(situacao_motivo_map.keys()))
                cd_situacao_motivo = situacao_motivo_map[motivo_situacao_selecionado]

        st.header("Solicitante e Responsável")
        col1, col2 = st.columns(2)
        with col1:
            setores_solicitantes_df = get_setor_solicitante_projeto(selected_gid)

            if setores_solicitantes_df.empty:
                st.warning("Nenhum setor solicitante encontrado para este projeto.")
                cd_setor_solicitante = None
            else:
                setor_solicitante_map = dict(zip(setores_solicitantes_df['TX_DESCRICAO'], setores_solicitantes_df['GID']))
                setor_solicitante_selecionado = st.selectbox("Setor Solicitante", options=list(setor_solicitante_map.keys()))
                cd_setor_solicitante = setor_solicitante_map[setor_solicitante_selecionado]
            
            tx_nome_solicitante = st.text_input("Nome do Solicitante", "")

        with col2:
            setores_responsaveis_df = get_setor_responsavel_projeto(selected_gid)

            if setores_responsaveis_df.empty:
                st.warning("Nenhum setor responsável encontrado para este projeto.")
                cd_setor_responsavel = None
            else:
                setor_responsavel_map = dict(zip(setores_responsaveis_df['TX_DESCRICAO'], setores_responsaveis_df['GID']))
                setor_responsavel_selecionado = st.selectbox("Setor Responsável", options=list(setor_responsavel_map.keys()))
                cd_setor_responsavel = setor_responsavel_map[setor_responsavel_selecionado]

        st.header("Detalhes Técnicos")
        col1, col2 = st.columns(2)
        with col1:
            familias_equipamentos_df = get_familia_equipamentos_projeto(selected_gid)

            if familias_equipamentos_df.empty:
                st.warning("Nenhuma família de equipamentos encontrada para este projeto.")
                cd_familia_equipamentos = None
            else:
                familia_equipamentos_map = dict(zip(familias_equipamentos_df['TX_DESCRICAO'], familias_equipamentos_df['GID']))
                familia_equipamentos_selecionada = st.selectbox("Família de Equipamentos", options=list(familia_equipamentos_map.keys()))
                cd_familia_equipamentos = familia_equipamentos_map[familia_equipamentos_selecionada]

            plantas_df = get_plantas_projeto(selected_gid)

            if plantas_df.empty:
                st.warning("Nenhuma planta encontrada para este projeto.")
                cd_planta = None
            else:
                planta_map = dict(zip(plantas_df['TX_DESCRICAO'], plantas_df['GID']))
                planta_selecionada = st.selectbox("Código da Planta", options=list(planta_map.keys()))
                cd_planta = planta_map[planta_selecionada]

            especialidades_df = get_especialidades_projeto(selected_gid)

            if especialidades_df.empty:
                st.warning("Nenhuma especialidade encontrada para este projeto.")
                cd_especialidade = None
            else:
                especialidade_map = dict(zip(especialidades_df['TX_DESCRICAO'], especialidades_df['GID']))
                especialidade_selecionada = st.selectbox("Código da Especialidade", options=list(especialidade_map.keys()))
                cd_especialidade = especialidade_map[especialidade_selecionada]

            tx_rec_inspecao = st.text_input("Recomendação de Inspeção", "")

        with col2:
            areas_df = get_areas_projeto(selected_gid)

            if areas_df.empty:
                st.warning("Nenhuma área encontrada para este projeto.")
                cd_area = None
            else:
                area_map = dict(zip(areas_df['TX_DESCRICAO'], areas_df['GID']))
                area_selecionada = st.selectbox("Código da Área", options=list(area_map.keys()))
                cd_area = area_map[area_selecionada]

            sistemas_operacionais_df = get_sistemas_operacionais_projeto(selected_gid)

            if sistemas_operacionais_df.empty:
                st.warning("Nenhum sistema operacional encontrado para este projeto.")
                cd_sistema_operacional_1 = None
                cd_sistema_operacional_2 = None
            else:
                sistema_operacional_map = dict(zip(sistemas_operacionais_df['TX_DESCRICAO'], sistemas_operacionais_df['GID']))

                sistema_operacional_selecionado_1 = st.selectbox("Sistema Operacional 1", options=list(sistema_operacional_map.keys()))
                cd_sistema_operacional_1 = sistema_operacional_map[sistema_operacional_selecionado_1]

                sistema_operacional_selecionado_2 = st.selectbox("Sistema Operacional 2", options=list(sistema_operacional_map.keys()))
                cd_sistema_operacional_2 = sistema_operacional_map[sistema_operacional_selecionado_2]

        st.header("Escopo e Situação")
        col1, col2 = st.columns(2)
        with col1:
            escopo_origem_df = get_escopo_origem_projeto(selected_gid)

            if escopo_origem_df.empty:
                st.warning("Nenhuma origem de escopo encontrada para este projeto.")
                cd_escopo_origem = None
            else:
                escopo_origem_map = dict(zip(escopo_origem_df['TX_DESCRICAO'], escopo_origem_df['GID']))
                escopo_origem_selecionado = st.selectbox("Origem do Escopo", options=list(escopo_origem_map.keys()))
                cd_escopo_origem = escopo_origem_map[escopo_origem_selecionado]

            escopo_tipo_df = get_escopo_tipo_projeto(selected_gid)

            if escopo_tipo_df.empty:
                st.warning("Nenhum tipo de escopo encontrado para este projeto.")
                cd_escopo_tipo = None
            else:
                escopo_tipo_map = dict(zip(escopo_tipo_df['TX_DESCRICAO'], escopo_tipo_df['GID']))
                escopo_tipo_selecionado = st.selectbox("Tipo de Escopo", options=list(escopo_tipo_map.keys()))
                cd_escopo_tipo = escopo_tipo_map[escopo_tipo_selecionado]

            tx_equipamento_mestre = st.text_input("Equipamento Mestre", "")

        with col2:
            fl_nmp = st.selectbox("Nota Manutenção Parada?", ["Sim", "Não"])
            fl_ase = st.selectbox("Tem Autorização de Serviço Extra?", ["Sim", "Não"])
            tx_ase = st.text_input("Autorização Serviço Extra", "")

        st.header("Executantes")
        col1, col2 = st.columns(2)
        with col1:
            executantes_df = get_executantes_projeto(selected_gid)

            if executantes_df.empty:
                st.warning("Nenhum executante encontrado para este projeto.")
                cd_executante_1 = None
            else:
                executante_map = dict(zip(executantes_df['TX_DESCRICAO'], executantes_df['GID']))
                executante_1_selecionado = st.selectbox("Código do Executante 1", options=list(executante_map.keys()))
                cd_executante_1 = executante_map[executante_1_selecionado]

        with col2:
            if executantes_df.empty:
                st.warning("Nenhum executante encontrado para este projeto.")
                cd_executante_2 = None
            else:
                executante_2_selecionado = st.selectbox("Código do Executante 2", options=list(executante_map.keys()))
                cd_executante_2 = executante_map[executante_2_selecionado]

        st.header("Observações")
        dt_atualizacao = st.date_input("Data de Atualização", value=pd.to_datetime('today').date())
        tx_observacao = st.text_area("Observação Adicional", "", height=100)

        submit_button = st.form_submit_button(label="Cadastrar Nota")

    if submit_button:
        new_data = {
            "CD_PROJETO": cd_projeto,
            "DT_NOTA": dt_data,
            "FL_SITUACAO": fl_situacao_nota,
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
        
        try:
            create_data('timecenter.TB_NOTA_MANUTENCAO', new_data)
        except Exception as e:
            st.error(f"Erro ao realizar o novo registro na tabela timecenter.TB_NOTA_MANUTENCAO: {e}")
        st.success("Nota cadastrada com sucesso!")

def main():
    cadastrar_nota_manutencao()

if __name__ == "__main__":
    main()
