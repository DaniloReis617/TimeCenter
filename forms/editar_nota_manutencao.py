import streamlit as st
import pandas as pd
from utils import (update_data, read_data,
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

# Função para carregar os dados com base no GID_PROJETO
@st.cache_data
def load_data(selected_gid):
    df = read_data("timecenter.TB_NOTA_MANUTENCAO")

    if df is None or df.empty:
        return pd.DataFrame()

    df = df[df['CD_PROJETO'] == selected_gid]
    df['ID'] = df['ID'].astype(int)
    df = df.sort_values(by='ID', ascending=False)
    
    return df

@st.dialog("Editar Nota", width="large")
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

    # Filtrar valores None da coluna TX_NOTA
    df = df[df['TX_NOTA'].notna()]

    # Seleção do TX_NOTA
    st.subheader("Selecione a Nota de Manutenção para Editar")
    tx_nota_selected = st.multiselect("Nota de Manutenção", options=sorted(df['TX_NOTA']), key="filtertxnota")

    # Carregar os dados da nota selecionada
    nota_data = df[df['TX_NOTA'].isin(tx_nota_selected)]

    # Criar as abas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Editar Notas e Ordens",
        "Informativo",
        "Material",
        "Recurso",
        "Apoio"
    ])

    # Conteúdo da aba 1
    with tab1: 

        if not nota_data.empty:
            nota_data = nota_data.iloc[0]
            
            # Formulário de edição
            with st.form(key="edit_nota_form"):
                col1, col2 = st.columns(2)

                with col1:
                    #cd_projeto = selected_gid

                    # Mostrar o ID da nota
                    st.text_input("ID da Nota", value=nota_data['ID'], disabled=True)

                    dt_data_row = nota_data.get('DT_NOTA', None)
                    if pd.isnull(dt_data_row) or isinstance(dt_data_row, str):
                        dt_data = st.date_input("Data da Nota", value=pd.to_datetime('today').date())
                    else:
                        dt_data = st.date_input("Data da Nota", value=pd.to_datetime(dt_data_row).date())

                    # Novo campo para DT_HR_CADASTRO
                    dt_hr_cadastro_row = nota_data.get('DT_HR_CADASTRO', None)
                    if pd.isnull(dt_hr_cadastro_row) or isinstance(dt_hr_cadastro_row, str):
                        dt_hr_cadastro = st.date_input("Data de Cadastro", value=pd.to_datetime('today').date(), disabled=True)
                    else:
                        dt_hr_cadastro = st.date_input("Data de Cadastro", value=pd.to_datetime(dt_hr_cadastro_row).date(), disabled=True)
                    
                    
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
                        dt_hr_alteracao = st.date_input("Data de Alteração", value=pd.to_datetime('today').date(), disabled=True)
                    else:
                        dt_hr_alteracao = st.date_input("Data de Alteração", value=pd.to_datetime(dt_hr_alteracao_row).date(), disabled=True)

                    # Serviços
                    servicos_df = get_servicos_projeto(selected_gid)
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
                    situacao_motivo_df = get_situacao_motivo_projeto(selected_gid)
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
                    setores_solicitantes_df = get_setor_solicitante_projeto(selected_gid)
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
                    setores_responsaveis_df = get_setor_responsavel_projeto(selected_gid)
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
                    familias_equipamentos_df = get_familia_equipamentos_projeto(selected_gid)
                    if familias_equipamentos_df.empty:
                        st.selectbox("Família de Equipamentos", options=[])
                        cd_familia_equipamentos = None
                    else:
                        familia_equipamentos_map = dict(zip(familias_equipamentos_df['TX_DESCRICAO'], familias_equipamentos_df['GID']))
                        familia_atual = familias_equipamentos_df.loc[familias_equipamentos_df['GID'] == nota_data.get('CD_FAMILIA_EQUIPAMENTOS', ''), 'TX_DESCRICAO'].values
                        familia_atual = familia_atual[0] if len(familia_atual) > 0 else None
                        familia_equipamentos_selecionada = st.selectbox("Família de Equipamentos", options=list(familia_equipamentos_map.keys()), index=list(familia_equipamentos_map.keys()).index(familia_atual) if familia_atual else 0)
                        cd_familia_equipamentos = familia_equipamentos_map[familia_equipamentos_selecionada]

                    plantas_df = get_plantas_projeto(selected_gid)
                    if plantas_df.empty:
                        st.selectbox("Código da Planta", options=[])
                        cd_planta = None
                    else:
                        planta_map = dict(zip(plantas_df['TX_DESCRICAO'], plantas_df['GID']))
                        planta_atual = plantas_df.loc[plantas_df['GID'] == nota_data.get('CD_PLANTA', ''), 'TX_DESCRICAO'].values
                        planta_atual = planta_atual[0] if len(planta_atual) > 0 else None
                        planta_selecionada = st.selectbox("Código da Planta", options=list(planta_map.keys()), index=list(planta_map.keys()).index(planta_atual) if planta_atual else 0)
                        cd_planta = planta_map[planta_selecionada]

                    especialidades_df = get_especialidades_projeto(selected_gid)
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

                with col2:
                    areas_df = get_areas_projeto(selected_gid)
                    if areas_df.empty:
                        st.selectbox("Código da Área", options=[])
                        cd_area = None
                    else:
                        area_map = dict(zip(areas_df['TX_DESCRICAO'], areas_df['GID']))
                        area_atual = areas_df.loc[areas_df['GID'] == nota_data.get('CD_AREA', ''), 'TX_DESCRICAO'].values
                        area_atual = area_atual[0] if len(area_atual) > 0 else None
                        area_selecionada = st.selectbox("Código da Área", options=list(area_map.keys()), index=list(area_map.keys()).index(area_atual) if area_atual else 0)
                        cd_area = area_map[area_selecionada]

                    sistemas_operacionais_df = get_sistemas_operacionais_projeto(selected_gid)
                    if sistemas_operacionais_df.empty:
                        st.selectbox("Sistema Operacional 1", options=[])
                        cd_sistema_operacional_1 = None
                        cd_sistema_operacional_2 = None
                    else:
                        sistema_operacional_map = dict(zip(sistemas_operacionais_df['TX_DESCRICAO'], sistemas_operacionais_df['GID']))
                        sistema_operacional_atual_1 = sistemas_operacionais_df.loc[sistemas_operacionais_df['GID'] == nota_data.get('CD_SISTEMA_OPERACIONAL_1', ''), 'TX_DESCRICAO'].values
                        sistema_operacional_atual_1 = sistema_operacional_atual_1[0] if len(sistema_operacional_atual_1) > 0 else None
                        sistema_operacional_selecionado_1 = st.selectbox("Sistema Operacional 1", options=list(sistema_operacional_map.keys()), index=list(sistema_operacional_map.keys()).index(sistema_operacional_atual_1) if sistema_operacional_atual_1 else 0)
                        cd_sistema_operacional_1 = sistema_operacional_map[sistema_operacional_selecionado_1]

                        sistema_operacional_atual_2 = sistemas_operacionais_df.loc[sistemas_operacionais_df['GID'] == nota_data.get('CD_SISTEMA_OPERACIONAL_2', ''), 'TX_DESCRICAO'].values
                        sistema_operacional_atual_2 = sistema_operacional_atual_2[0] if len(sistema_operacional_atual_2) > 0 else None
                        sistema_operacional_selecionado_2 = st.selectbox("Sistema Operacional 2", options=list(sistema_operacional_map.keys()), index=list(sistema_operacional_map.keys()).index(sistema_operacional_atual_2) if sistema_operacional_atual_2 else 0)
                        cd_sistema_operacional_2 = sistema_operacional_map[sistema_operacional_selecionado_2]

                # Seção Escopo e Situação
                st.header("Escopo e Situação")
                col1, col2 = st.columns(2)
                with col1:
                    escopo_origem_df = get_escopo_origem_projeto(selected_gid)
                    if escopo_origem_df.empty:
                        st.selectbox("Origem do Escopo", options=[])
                        cd_escopo_origem = None
                    else:
                        escopo_origem_map = dict(zip(escopo_origem_df['TX_DESCRICAO'], escopo_origem_df['GID']))
                        escopo_origem_atual = escopo_origem_df.loc[escopo_origem_df['GID'] == nota_data.get('CD_ESCOPO_ORIGEM', ''), 'TX_DESCRICAO'].values
                        escopo_origem_atual = escopo_origem_atual[0] if len(escopo_origem_atual) > 0 else None
                        escopo_origem_selecionado = st.selectbox("Origem do Escopo", options=list(escopo_origem_map.keys()), index=list(escopo_origem_map.keys()).index(escopo_origem_atual) if escopo_origem_atual else 0)
                        cd_escopo_origem = escopo_origem_map[escopo_origem_selecionado]

                    escopo_tipo_df = get_escopo_tipo_projeto(selected_gid)
                    if escopo_tipo_df.empty:
                        st.selectbox("Tipo de Escopo", options=[])
                        cd_escopo_tipo = None
                    else:
                        escopo_tipo_map = dict(zip(escopo_tipo_df['TX_DESCRICAO'], escopo_tipo_df['GID']))
                        escopo_tipo_atual = escopo_tipo_df.loc[escopo_tipo_df['GID'] == nota_data.get('CD_ESCOPO_TIPO', ''), 'TX_DESCRICAO'].values
                        escopo_tipo_atual = escopo_tipo_atual[0] if len(escopo_tipo_atual) > 0 else None
                        escopo_tipo_selecionado = st.selectbox("Tipo de Escopo", options=list(escopo_tipo_map.keys()), index=list(escopo_tipo_map.keys()).index(escopo_tipo_atual) if escopo_tipo_atual else 0)
                        cd_escopo_tipo = escopo_tipo_map[escopo_tipo_selecionado]

                    tx_equipamento_mestre = st.text_input("Equipamento Mestre", nota_data.get('TX_EQUIPAMENTO_MESTRE', ''))

                with col2:
                    fl_nmp = st.selectbox("Nota Manutenção Parada?", ["Sim", "Não"], index=0 if nota_data.get('FL_NMP', 'Não') == 'Sim' else 1)
                    fl_ase = st.selectbox("Tem Autorização de Serviço Extra?", ["Sim", "Não"], index=0 if nota_data.get('FL_ASE', 'Não') == 'Sim' else 1)
                    tx_ase = st.text_input("Autorização Serviço Extra", nota_data.get('TX_ASE', ''))

                # Seção Executantes
                st.header("Executantes")
                col1, col2 = st.columns(2)
                with col1:
                    executantes_df = get_executantes_projeto(selected_gid)
                    if executantes_df.empty:
                        st.selectbox("Código do Executante 1", options=[])
                        cd_executante_1 = None
                    else:
                        executante_map = dict(zip(executantes_df['TX_DESCRICAO'], executantes_df['GID']))
                        executante_atual_1 = executantes_df.loc[executantes_df['GID'] == nota_data.get('CD_EXECUTANTE_1', ''), 'TX_DESCRICAO'].values
                        executante_atual_1 = executante_atual_1[0] if len(executante_atual_1) > 0 else None
                        executante_1_selecionado = st.selectbox("Código do Executante 1", options=list(executante_map.keys()), index=list(executante_map.keys()).index(executante_atual_1) if executante_atual_1 else 0)
                        cd_executante_1 = executante_map[executante_1_selecionado]

                with col2:
                    if executantes_df.empty:
                        st.selectbox("Código do Executante 2", options=[])
                        cd_executante_2 = None
                    else:
                        executante_atual_2 = executantes_df.loc[executantes_df['GID'] == nota_data.get('CD_EXECUTANTE_2', ''), 'TX_DESCRICAO'].values
                        executante_atual_2 = executante_atual_2[0] if len(executante_atual_2) > 0 else None
                        executante_2_selecionado = st.selectbox("Código do Executante 2", options=list(executante_map.keys()), index=list(executante_map.keys()).index(executante_atual_2) if executante_atual_2 else 0)
                        cd_executante_2 = executante_map[executante_2_selecionado]

                # Seção Observações
                st.header("Observações")
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
                    #"CD_PROJETO": str(cd_projeto),
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
                updated_data = convert_to_native_types(updated_data)

                try:
                    update_data('timecenter.TB_NOTA_MANUTENCAO', 'ID', int(nota_data['ID']), updated_data)
                    st.success("Nota atualizada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar a nota: {e}")

    # Conteúdo das outras abas
    with tab2:
        st.write("LANÇAMENTO DE NOTAS DE MANUTENÇÃO (INFORMATIVO) - ADMINISTRAÇÃO")
    with tab3:
        st.write("LANÇAMENTO DE NOTAS DE MANUTENÇÃO (MATERIAL) - MANUTENÇÃO")
    with tab4:
        st.write("LANÇAMENTO DE NOTAS DE MANUTENÇÃO (RECURSO) - ADMINISTRAÇÃO")
    with tab5:
        st.write("LANÇAMENTO DE NOTAS DE MANUTENÇÃO (APOIO) - ADMINISTRAÇÃO")

# Função principal
def main():
    edit_nota_manutencao()

if __name__ == "__main__":
    main()
