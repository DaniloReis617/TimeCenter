# forms/editar_nota_manutencao.py
import streamlit as st
import pandas as pd
import uuid
from utils import update_data, read_data, create_data, convert_to_native_types

# Função para carregar ou atualizar tabelas específicas
def load_or_refresh_data(table_name, session_key):
    if session_key not in st.session_state:
        st.session_state[session_key] = read_data(table_name)
    return st.session_state[session_key]

# Definir função para limpar o cache de dados específico no st.session_state
def clear_cache(*keys):
    """Remove as entradas de cache para as tabelas especificadas no st.session_state."""
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]

def show_edit_nota_form(project_data, nota_data):
    """Exibe o formulário para editar informações principais da nota de manutenção."""
    # Formulário de edição
    with st.form(key="edit_nota_form", enter_to_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            #cd_projeto = selected_gid

            # Mostrar o ID da nota
            #txt_GID = var_Novo_GID_Nota_Manutencao

            # Mostrar o ID da nota
            txt_ID = st.text_input("ID da Nota", value=nota_data['ID'], disabled=True)

            dt_data_row = nota_data.get('DT_NOTA', None)
            if pd.isnull(dt_data_row) or isinstance(dt_data_row, str):
                dt_data = st.date_input("Data da Nota", value=pd.to_datetime('today').date())
            else:
                dt_data = st.date_input("Data da Nota", value=pd.to_datetime(dt_data_row).date())

            # Novo campo para DT_HR_CADASTRO
            dt_hr_cadastro_row = nota_data.get('DT_HR_CADASTRO', None)
            if pd.isnull(dt_hr_cadastro_row) or isinstance(dt_hr_cadastro_row, str):
                dt_hr_cadastro = pd.to_datetime('today').date()
            else:
                dt_hr_cadastro = pd.to_datetime(dt_hr_cadastro_row).date()
            
            
            situacao_map = {'P': 'Pendente', 'A': 'Aprovado', 'R': 'Reprovado'}
            reverse_situacao_map = {v: k for k, v in situacao_map.items()}
            situacao_atual = situacao_map.get(nota_data.get('FL_SITUACAO', 'P'), 'Pendente')
            fl_situacao_nota = st.selectbox("Situação da Nota", options=list(situacao_map.values()), index=list(situacao_map.values()).index(situacao_atual))
            fl_situacao_nota = reverse_situacao_map[fl_situacao_nota]

            tx_nota = st.text_input("Nota", nota_data.get('TX_NOTA', ''))
            tx_ordem = st.text_input("Ordem", nota_data.get('TX_ORDEM', ''))
            tx_tag = st.text_input("Tag", nota_data.get('TX_TAG', ''))
            tx_tag_linha = st.text_input("Tag da Linha", nota_data.get('TX_TAG_LINHA', ''))

        with col2:
            # Novo campo para DT_HR_ALTERACAO
            dt_hr_alteracao_row = nota_data.get('DT_HR_ALTERACAO', None)
            if pd.isnull(dt_hr_alteracao_row) or isinstance(dt_hr_alteracao_row, str):
                dt_hr_alteracao = pd.to_datetime('today').date()
            else:
                dt_hr_alteracao = pd.to_datetime(dt_hr_alteracao_row).date()

            # Serviços
            servicos_df = project_data['servicos']
            if servicos_df.empty:
                st.selectbox("Código do Serviço", options=[])
                cd_servico = None
                tx_descricao_servico = None
            else:
                servico_map = dict(zip(servicos_df['TX_DESCRICAO'], servicos_df['GID']))
                descricao_atual = servicos_df.loc[servicos_df['GID'] == nota_data.get('CD_SERVICO', ''), 'TX_DESCRICAO'].values
                descricao_atual = descricao_atual[0] if len(descricao_atual) > 0 else None
                descricao_servico_selecionada = st.selectbox("Código do Serviço", options=list(servico_map.keys()), index=list(servico_map.keys()).index(descricao_atual) if descricao_atual else 0)
                cd_servico = servico_map[descricao_servico_selecionada]
                tx_descricao_servico = st.text_area("Descrição do Serviço", nota_data.get('TX_DESCRICAO_SERVICO', ''), height=150)

            # Motivos de Situação
            situacao_motivo_df = project_data['situacao_motivo']
            if situacao_motivo_df.empty:
                st.selectbox("Motivo da Situação", options=[])
                cd_situacao_motivo = None
            else:
                situacao_motivo_map = dict(zip(situacao_motivo_df['TX_DESCRICAO'], situacao_motivo_df['GID']))
                motivo_atual = situacao_motivo_df.loc[situacao_motivo_df['GID'] == nota_data.get('CD_SITUACAO_MOTIVO', ''), 'TX_DESCRICAO'].values
                motivo_atual = motivo_atual[0] if len(motivo_atual) > 0 else None
                motivo_situacao_selecionado = st.selectbox("Motivo da Situação", options=list(situacao_motivo_map.keys()), index=list(situacao_motivo_map.keys()).index(motivo_atual) if motivo_atual else 0)
                cd_situacao_motivo = situacao_motivo_map[motivo_situacao_selecionado]

        # Seção Solicitante e Responsável
        st.header("Solicitante e Responsável")
        col1, col2 = st.columns(2)
        with col1:
            setores_solicitantes_df = project_data['setor_solicitante']
            if setores_solicitantes_df.empty:
                st.selectbox("Setor Solicitante", options=[])
                cd_setor_solicitante = None
            else:
                setor_solicitante_map = dict(zip(setores_solicitantes_df['TX_DESCRICAO'], setores_solicitantes_df['GID']))
                setor_atual = setores_solicitantes_df.loc[setores_solicitantes_df['GID'] == nota_data.get('CD_SETOR_SOLICITANTE', ''), 'TX_DESCRICAO'].values
                setor_atual = setor_atual[0] if len(setor_atual) > 0 else None
                setor_solicitante_selecionado = st.selectbox("Setor Solicitante", options=list(setor_solicitante_map.keys()), index=list(setor_solicitante_map.keys()).index(setor_atual) if setor_atual else 0)
                cd_setor_solicitante = setor_solicitante_map[setor_solicitante_selecionado]
            tx_nome_solicitante = st.text_input("Nome do Solicitante", nota_data.get('TX_NOME_SOLICITANTE', ''))

        with col2:
            setores_responsaveis_df = project_data['setor_responsavel']
            if setores_responsaveis_df.empty:
                st.selectbox("Setor Responsável", options=[])
                cd_setor_responsavel = None
            else:
                setor_responsavel_map = dict(zip(setores_responsaveis_df['TX_DESCRICAO'], setores_responsaveis_df['GID']))
                setor_responsavel_atual = setores_responsaveis_df.loc[setores_responsaveis_df['GID'] == nota_data.get('CD_SETOR_RESPONSAVEL', ''), 'TX_DESCRICAO'].values
                setor_responsavel_atual = setor_responsavel_atual[0] if len(setor_responsavel_atual) > 0 else None
                setor_responsavel_selecionado = st.selectbox("Setor Responsável", options=list(setor_responsavel_map.keys()), index=list(setor_responsavel_map.keys()).index(setor_responsavel_atual) if setor_responsavel_atual else 0)
                cd_setor_responsavel = setor_responsavel_map[setor_responsavel_selecionado]

        # Seção Detalhes Técnicos
        st.header("Detalhes Técnicos")
        col1, col2 = st.columns(2)
        with col1:
            familias_equipamentos_df = project_data['familia_equipamentos']
            if familias_equipamentos_df.empty:
                st.selectbox("Família de Equipamentos", options=[])
                cd_familia_equipamentos = None
            else:
                familia_equipamentos_map = dict(zip(familias_equipamentos_df['TX_DESCRICAO'], familias_equipamentos_df['GID']))
                familia_atual = familias_equipamentos_df.loc[familias_equipamentos_df['GID'] == nota_data.get('CD_FAMILIA_EQUIPAMENTOS', ''), 'TX_DESCRICAO'].values
                familia_atual = familia_atual[0] if len(familia_atual) > 0 else None
                familia_equipamentos_selecionada = st.selectbox("Família de Equipamentos", options=list(familia_equipamentos_map.keys()), index=list(familia_equipamentos_map.keys()).index(familia_atual) if familia_atual else 0)
                cd_familia_equipamentos = familia_equipamentos_map[familia_equipamentos_selecionada]

            plantas_df = project_data['plantas']
            if plantas_df.empty:
                st.selectbox("Código da Planta", options=[])
                cd_planta = None
            else:
                planta_map = dict(zip(plantas_df['TX_DESCRICAO'], plantas_df['GID']))
                planta_atual = plantas_df.loc[plantas_df['GID'] == nota_data.get('CD_PLANTA', ''), 'TX_DESCRICAO'].values
                planta_atual = planta_atual[0] if len(planta_atual) > 0 else None
                planta_selecionada = st.selectbox("Código da Planta", options=list(planta_map.keys()), index=list(planta_map.keys()).index(planta_atual) if planta_atual else 0)
                cd_planta = planta_map[planta_selecionada]

            especialidades_df = project_data['especialidades']
            if especialidades_df.empty:
                st.selectbox("Código da Especialidade", options=[])
                cd_especialidade = None
            else:
                especialidade_map = dict(zip(especialidades_df['TX_DESCRICAO'], especialidades_df['GID']))
                especialidade_atual = especialidades_df.loc[especialidades_df['GID'] == nota_data.get('CD_ESPECIALIDADE', ''), 'TX_DESCRICAO'].values
                especialidade_atual = especialidade_atual[0] if len(especialidade_atual) > 0 else None
                especialidade_selecionada = st.selectbox("Código da Especialidade", options=list(especialidade_map.keys()), index=list(especialidade_map.keys()).index(especialidade_atual) if especialidade_atual else 0)
                cd_especialidade = especialidade_map[especialidade_selecionada]
                
            tx_rec_inspecao = st.text_input("Recomendação de Inspeção", nota_data.get('TX_REC_INSPECAO', ''))
            tx_liberavel_em_rotina = st.text_input("Liberável em Rotina", nota_data.get('TX_LIBERAVEL_EM_ROTINA', ''))
                            
        with col2:
            tx_periodo_de_manutencao = st.text_input("Período de Manutenção < 5 dias ?", nota_data.get('[TX_PERIODO_DE_MANUTENCAO_MENOR_QUE_5_DIAS]', ''))
            tx_equipamento_reserva_sistby_pass = st.text_input("Equipamento Reserva ou Sistema By-Pass", nota_data.get('TX_EQUIPTO_RESERVA_OU_SISTBY_PASS', ''))
            tx_critico = st.text_input("Crítico", nota_data.get('TX_CRITICO', ''))
            tx_oportunidade = st.text_input("Oprtunidade", nota_data.get('TX_OPORTUNIDADE', ''))                                                            

        tx_observacao = st.text_area("Observação Adicional", nota_data.get('TX_OBSERVACAO', ''), height=100)

        submit_button = st.form_submit_button(label="Atualizar Nota")

    # Atualizar dados no banco de dados
    if submit_button:
        updated_data = {
            #"CD_PROJETO": str(cd_projeto),
            #"GID":str(txt_GID) if txt_GID else None,
            "ID":str(txt_ID) if txt_ID else None,
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
            "CD_ESPECIALIDADE": str(cd_especialidade) if cd_especialidade else None,
            "CD_SITUACAO_MOTIVO": str(cd_situacao_motivo) if cd_situacao_motivo else None,
            "TX_REC_INSPECAO": str(tx_rec_inspecao) if tx_rec_inspecao else None,
            "TX_LIBERAVEL_EM_ROTINA": str(tx_liberavel_em_rotina) if tx_liberavel_em_rotina else None,
            "TX_PERIODO_DE_MANUTENCAO_MENOR_QUE_5_DIAS": str(tx_periodo_de_manutencao) if tx_periodo_de_manutencao else None,
            "TX_EQUIPTO_RESERVA_OU_SISTBY_PASS": str(tx_equipamento_reserva_sistby_pass) if tx_equipamento_reserva_sistby_pass else None,
            "TX_CRITICO": str(tx_critico) if tx_critico else None,
            "TX_OPORTUNIDADE": str(tx_oportunidade) if tx_oportunidade else None,                                                            
            "TX_OBSERVACAO": str(tx_observacao) if tx_observacao else None
        }

        # Aplique a conversão de tipos antes de atualizar
        updated_data = convert_to_native_types(updated_data)

        try:
            with st.spinner("Salvando informações, por favor aguarde..."):
                update_data('timecenter.TB_NOTA_MANUTENCAO', 'ID', int(nota_data['ID']), updated_data)
                st.success("Nota atualizada com sucesso!")
                
        except Exception as e:
            st.error(f"Erro ao atualizar a nota: {e}")

            
@st.dialog("Editar Nota", width="large")
def edit_nota_manutencao_desafio():
    if 'project_data' in st.session_state and 'nota_selecionada' in st.session_state:
        project_data = st.session_state['project_data']
        gid_nota = st.session_state['nota_selecionada']
        notas_df = project_data['notas_de_manutencao_geral']
        nota_data = notas_df[notas_df['GID'] == gid_nota].iloc[0] if gid_nota else None

        if nota_data is None:
            st.warning("Nota não encontrada.")
            return

        show_edit_nota_form(project_data, nota_data)

def main():
    edit_nota_manutencao_desafio()

if __name__ == "__main__":
    main()
