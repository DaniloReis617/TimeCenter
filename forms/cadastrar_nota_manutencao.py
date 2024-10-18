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

@st.cache_data
def load_data(selected_gid):
    df = read_data("timecenter.TB_NOTA_MANUTENCAO")

    if df is None or df.empty:
        return pd.DataFrame()

    df = df[df['CD_PROJETO'] == selected_gid]
    df['ID'] = df['ID'].astype(int)
    df = df.sort_values(by='ID', ascending=False)
    
    return df

@st.cache_data
def load_all_notas():
    """Carregar todas as notas da tabela para verificação de duplicidade"""
    df = read_data("timecenter.TB_NOTA_MANUTENCAO")
    if df is None or df.empty:
        return pd.DataFrame()
    return df['TX_NOTA']

@st.dialog("Cadastrar Nova Nota", width="large")
def cadastrar_nota_manutencao():
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return

    # Carregar as notas existentes para verificação
    notas_existentes = load_all_notas()

    # Carregar os dados existentes para calcular o próximo ID
    df_notas = load_data(selected_gid)
    if df_notas.empty:
        novo_id = 1  # Começa em 1 se não houver notas
    else:
        novo_id = df_notas['ID'].max() + 1  # Incrementa o ID
        
    with st.form(key="new_nota_form"):
        col1, col2 = st.columns(2)

        with col1:
            # Campo oculto do projeto
            cd_projeto = selected_gid

            # Gerar um novo GUID
            var_Novo_GID = uuid.uuid4()
            cd_GID = st.text_input("GID", value=str(var_Novo_GID), disabled=True)

            # Campo do ID gerado automaticamente
            tx_ID = st.text_input("ID", value=str(novo_id), disabled=True)

            dt_data = st.date_input("Data da Nota", value=pd.to_datetime('today').date())

            # Novo campo para DT_HR_CADASTRO
            dt_hr_cadastro = st.date_input("Data de Cadastro", value=pd.to_datetime('today').date(), disabled=True)


            situacao_map = {'P': 'Pendente', 'A': 'Aprovado', 'R': 'Reprovado'}
            situacao_nota = st.selectbox("Situação da Nota", options=list(situacao_map.values()))
            fl_situacao_nota = {v: k for k, v in situacao_map.items()}[situacao_nota]

            # Entrada de Nota com verificação de duplicidade
            tx_nota = st.text_input("Nota", "")

            # Verificação de duplicidade em tempo real
            nota_existente = tx_nota in notas_existentes.values
            if nota_existente:
                st.error(f"A nota '{tx_nota}' já existe. Por favor, insira uma nova nota.")

            
            tx_ordem = st.text_input("Ordem", "")
            tx_tag = st.text_input("Tag", "")
            tx_tag_linha = st.text_input("Tag da Linha", "")

        with col2:

            dt_hr_alteracao = st.date_input("Data de Alteração", value=pd.to_datetime('today').date(), disabled=True)
            
            servicos_df = get_servicos_projeto(selected_gid)
            servico_map = dict(zip(servicos_df['TX_DESCRICAO'], servicos_df['GID'])) if not servicos_df.empty else {}
            
            descricao_servico_selecionada = st.selectbox("Código do Serviço", options=list(servico_map.keys()) or [''])
            cd_servico = servico_map.get(descricao_servico_selecionada, None)
            tx_descricao_servico = st.text_area("Descrição do Serviço", "", height=150)

            situacao_motivo_df = get_situacao_motivo_projeto(selected_gid)
            situacao_motivo_map = dict(zip(situacao_motivo_df['TX_DESCRICAO'], situacao_motivo_df['GID'])) if not situacao_motivo_df.empty else {}
            
            motivo_situacao_selecionado = st.selectbox("Motivo da Situação", options=list(situacao_motivo_map.keys()) or [''])
            cd_situacao_motivo = situacao_motivo_map.get(motivo_situacao_selecionado, None)

        st.header("Solicitante e Responsável")
        col1, col2 = st.columns(2)
        with col1:
            setores_solicitantes_df = get_setor_solicitante_projeto(selected_gid)
            setor_solicitante_map = dict(zip(setores_solicitantes_df['TX_DESCRICAO'], setores_solicitantes_df['GID'])) if not setores_solicitantes_df.empty else {}
            
            setor_solicitante_selecionado = st.selectbox("Setor Solicitante", options=list(setor_solicitante_map.keys()) or [''])
            cd_setor_solicitante = setor_solicitante_map.get(setor_solicitante_selecionado, None)
            
            tx_nome_solicitante = st.text_input("Nome do Solicitante", "")

        with col2:
            setores_responsaveis_df = get_setor_responsavel_projeto(selected_gid)
            setor_responsavel_map = dict(zip(setores_responsaveis_df['TX_DESCRICAO'], setores_responsaveis_df['GID'])) if not setores_responsaveis_df.empty else {}

            setor_responsavel_selecionado = st.selectbox("Setor Responsável", options=list(setor_responsavel_map.keys()) or [''])
            cd_setor_responsavel = setor_responsavel_map.get(setor_responsavel_selecionado, None)

        st.header("Detalhes Técnicos")
        col1, col2 = st.columns(2)
        with col1:
            familias_equipamentos_df = get_familia_equipamentos_projeto(selected_gid)
            familia_equipamentos_map = dict(zip(familias_equipamentos_df['TX_DESCRICAO'], familias_equipamentos_df['GID'])) if not familias_equipamentos_df.empty else {}

            familia_equipamentos_selecionada = st.selectbox("Família de Equipamentos", options=list(familia_equipamentos_map.keys()) or [''])
            cd_familia_equipamentos = familia_equipamentos_map.get(familia_equipamentos_selecionada, None)

            plantas_df = get_plantas_projeto(selected_gid)
            planta_map = dict(zip(plantas_df['TX_DESCRICAO'], plantas_df['GID'])) if not plantas_df.empty else {}

            planta_selecionada = st.selectbox("Código da Planta", options=list(planta_map.keys()) or [''])
            cd_planta = planta_map.get(planta_selecionada, None)

            especialidades_df = get_especialidades_projeto(selected_gid)
            especialidade_map = dict(zip(especialidades_df['TX_DESCRICAO'], especialidades_df['GID'])) if not especialidades_df.empty else {}

            especialidade_selecionada = st.selectbox("Código da Especialidade", options=list(especialidade_map.keys()) or [''])
            cd_especialidade = especialidade_map.get(especialidade_selecionada, None)

            tx_rec_inspecao = st.text_input("Recomendação de Inspeção", "")

        with col2:
            areas_df = get_areas_projeto(selected_gid)
            area_map = dict(zip(areas_df['TX_DESCRICAO'], areas_df['GID'])) if not areas_df.empty else {}

            area_selecionada = st.selectbox("Código da Área", options=list(area_map.keys()) or [''])
            cd_area = area_map.get(area_selecionada, None)

            sistemas_operacionais_df = get_sistemas_operacionais_projeto(selected_gid)
            sistema_operacional_map = dict(zip(sistemas_operacionais_df['TX_DESCRICAO'], sistemas_operacionais_df['GID'])) if not sistemas_operacionais_df.empty else {}

            sistema_operacional_selecionado_1 = st.selectbox("Sistema Operacional 1", options=list(sistema_operacional_map.keys()) or [''])
            cd_sistema_operacional_1 = sistema_operacional_map.get(sistema_operacional_selecionado_1, None)

            sistema_operacional_selecionado_2 = st.selectbox("Sistema Operacional 2", options=list(sistema_operacional_map.keys()) or [''])
            cd_sistema_operacional_2 = sistema_operacional_map.get(sistema_operacional_selecionado_2, None)

        st.header("Escopo e Situação")
        col1, col2 = st.columns(2)
        with col1:
            escopo_origem_df = get_escopo_origem_projeto(selected_gid)
            escopo_origem_map = dict(zip(escopo_origem_df['TX_DESCRICAO'], escopo_origem_df['GID'])) if not escopo_origem_df.empty else {}

            escopo_origem_selecionado = st.selectbox("Origem do Escopo", options=list(escopo_origem_map.keys()) or [''])
            cd_escopo_origem = escopo_origem_map.get(escopo_origem_selecionado, None)

            escopo_tipo_df = get_escopo_tipo_projeto(selected_gid)
            escopo_tipo_map = dict(zip(escopo_tipo_df['TX_DESCRICAO'], escopo_tipo_df['GID'])) if not escopo_tipo_df.empty else {}

            escopo_tipo_selecionado = st.selectbox("Tipo de Escopo", options=list(escopo_tipo_map.keys()) or [''])
            cd_escopo_tipo = escopo_tipo_map.get(escopo_tipo_selecionado, None)

            tx_equipamento_mestre = st.text_input("Equipamento Mestre", "")

        with col2:
            fl_nmp = st.selectbox("Nota Manutenção Parada?", ["Sim", "Não"])
            fl_ase = st.selectbox("Tem Autorização de Serviço Extra?", ["Sim", "Não"])
            tx_ase = st.text_input("Autorização Serviço Extra", "")

        st.header("Executantes")
        col1, col2 = st.columns(2)
        with col1:
            executantes_df = get_executantes_projeto(selected_gid)
            executante_map = dict(zip(executantes_df['TX_DESCRICAO'], executantes_df['GID'])) if not executantes_df.empty else {}

            executante_1_selecionado = st.selectbox("Código do Executante 1", options=list(executante_map.keys()) or [''])
            cd_executante_1 = executante_map.get(executante_1_selecionado, None)

        with col2:
            executante_2_selecionado = st.selectbox("Código do Executante 2", options=list(executante_map.keys()) or [''])
            cd_executante_2 = executante_map.get(executante_2_selecionado, None)

        st.header("Observações")
        dt_atualizacao = st.date_input("Data de Atualização", value=pd.to_datetime('today').date())
        tx_observacao = st.text_area("Observação Adicional", "", height=100)

        submit_button = st.form_submit_button(label="Cadastrar Nota")

    if submit_button:
        new_data = {
            "ID": tx_ID,
            "GID":str(cd_GID),
            "CD_PROJETO": str(cd_projeto),
            "DT_NOTA": dt_data.strftime('%Y-%m-%d'),
            "DT_HR_CADASTRO": dt_hr_cadastro.strftime('%Y-%m-%d %H:%M:%S'),
            "DT_HR_ALTERACAO": dt_hr_alteracao.strftime('%Y-%m-%d %H:%M:%S'),
            "FL_SITUACAO": fl_situacao_nota,
            "TX_NOTA": str(tx_nota) if tx_nota else None,
            "TX_ORDEM": str(tx_ordem) if tx_ordem else None,
            "TX_TAG": str(tx_tag) if tx_tag else None,
            "TX_TAG_LINHA": str(tx_tag_linha) if tx_tag_linha else None,
            "CD_SERVICO": str(cd_servico) if cd_servico else None,
            "TX_DESCRICAO_SERVICO": str(tx_descricao_servico) if tx_descricao_servico else None,
            "CD_SETOR_SOLICITANTE": str(cd_setor_solicitante) if cd_setor_solicitante else None,
            "TX_NOME_SOLICITANTE": str(tx_nome_solicitante) if tx_nome_solicitante else None,
            "CD_SETOR_RESPONSAVEL": str(cd_setor_responsavel) if cd_setor_responsavel else None,
            "CD_FAMILIA_EQUIPAMENTOS": str(cd_familia_equipamentos) if cd_familia_equipamentos else None,
            "CD_PLANTA": str(cd_planta) if cd_planta else None,
            "CD_AREA": str(cd_area) if cd_area else None,
            "CD_ESPECIALIDADE": str(cd_especialidade) if cd_especialidade else None,
            "CD_SISTEMA_OPERACIONAL_1": str(cd_sistema_operacional_1) if cd_sistema_operacional_1 else None,
            "CD_SISTEMA_OPERACIONAL_2": str(cd_sistema_operacional_2) if cd_sistema_operacional_2 else None,
            "TX_EQUIPAMENTO_MESTRE": str(tx_equipamento_mestre) if tx_equipamento_mestre else None,
            "CD_ESCOPO_ORIGEM": str(cd_escopo_origem) if cd_escopo_origem else None,
            "CD_ESCOPO_TIPO": str(cd_escopo_tipo) if cd_escopo_tipo else None,
            "CD_SITUACAO_MOTIVO": str(cd_situacao_motivo) if cd_situacao_motivo else None,
            "TX_REC_INSPECAO": str(tx_rec_inspecao) if tx_rec_inspecao else None,
            "FL_NMP": fl_nmp[0],  # char(1)
            "FL_ASE": fl_ase[0],  # char(1)
            "TX_ASE": str(tx_ase) if tx_ase else None,
            "CD_EXECUTANTE_1": str(cd_executante_1) if cd_executante_1 else None,
            "CD_EXECUTANTE_2": str(cd_executante_2) if cd_executante_2 else None,
            "DT_ATUALIZACAO": dt_atualizacao.strftime('%Y-%m-%d'),
            "TX_OBSERVACAO": str(tx_observacao) if tx_observacao else None
        }

        # Aplique a conversão de tipos antes de atualizar
        new_data = convert_to_native_types(new_data)
        
        try:
            with st.spinner("Salvando informações, por favor aguarde..."):
                create_data('timecenter.TB_NOTA_MANUTENCAO', new_data)
                st.success("Nota cadastrada com sucesso!")
        except Exception as e:
            st.error(f"Erro ao realizar o novo registro na tabela timecenter.TB_NOTA_MANUTENCAO: {e}")

def main():
    cadastrar_nota_manutencao()

if __name__ == "__main__":
    main()
