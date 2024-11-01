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

        with col2:
            areas_df = project_data['areas']
            if areas_df.empty:
                st.selectbox("Código da Área", options=[])
                cd_area = None
            else:
                area_map = dict(zip(areas_df['TX_DESCRICAO'], areas_df['GID']))
                area_atual = areas_df.loc[areas_df['GID'] == nota_data.get('CD_AREA', ''), 'TX_DESCRICAO'].values
                area_atual = area_atual[0] if len(area_atual) > 0 else None
                area_selecionada = st.selectbox("Código da Área", options=list(area_map.keys()), index=list(area_map.keys()).index(area_atual) if area_atual else 0)
                cd_area = area_map[area_selecionada]

            sistemas_operacionais_df = project_data['sistemas_operacionais']
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
            escopo_origem_df = project_data['escopo_origem']
            if escopo_origem_df.empty:
                st.selectbox("Origem do Escopo", options=[])
                cd_escopo_origem = None
            else:
                escopo_origem_map = dict(zip(escopo_origem_df['TX_DESCRICAO'], escopo_origem_df['GID']))
                escopo_origem_atual = escopo_origem_df.loc[escopo_origem_df['GID'] == nota_data.get('CD_ESCOPO_ORIGEM', ''), 'TX_DESCRICAO'].values
                escopo_origem_atual = escopo_origem_atual[0] if len(escopo_origem_atual) > 0 else None
                escopo_origem_selecionado = st.selectbox("Origem do Escopo", options=list(escopo_origem_map.keys()), index=list(escopo_origem_map.keys()).index(escopo_origem_atual) if escopo_origem_atual else 0)
                cd_escopo_origem = escopo_origem_map[escopo_origem_selecionado]

            escopo_tipo_df = project_data['escopo_tipo']
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
            executantes_df = project_data['executantes']
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
            with st.spinner("Salvando informações, por favor aguarde..."):
                update_data('timecenter.TB_NOTA_MANUTENCAO', 'ID', int(nota_data['ID']), updated_data)
                st.success("Nota atualizada com sucesso!")

        except Exception as e:
            st.error(f"Erro ao atualizar a nota: {e}")


def show_informativo_tab(project_data, nota_data):
    # Criar as abas
    tabinformativo1, tabinformativo2 = st.tabs([
        "Lista de Dados Informativos",
        "Cadastrar Informativo"
    ])

    with tabinformativo1:
        # Limpar cache e recarregar dados
        clear_cache("informativo_data")
        st.write("LANÇAMENTO DE NOTAS DE MANUTENÇÃO (INFORMATIVO) - ADMINISTRAÇÃO")
        # Carregar dados da tabela INFORMATIVO
        df_INFORMATIVO = load_or_refresh_data("timecenter.TB_NOTA_MANUTENCAO_INFORMATIVO", "informativo_data")

        if df_INFORMATIVO is None or df_INFORMATIVO.empty:
            st.warning("Nenhum informativo encontrado para a nota selecionada.")
            return

        # Verifique se 'GID' contém mais de um valor
        if isinstance(nota_data['GID'], pd.Series):
            # Se 'GID' for uma série (pode conter mais de um valor)
            df_INFORMATIVO = df_INFORMATIVO[df_INFORMATIVO['CD_NOTA_MANUTENCAO'].isin(nota_data['GID'])]
        else:
            # Se 'GID' for um valor único (string ou número)
            df_INFORMATIVO = df_INFORMATIVO[df_INFORMATIVO['CD_NOTA_MANUTENCAO'] == nota_data['GID']]

        # Carregar os dados de timecenter.TB_CADASTRO_INFORMATIVO para mapear os códigos
        df_cadastro_INFORMATIVO = read_data("timecenter.TB_CADASTRO_INFORMATIVO")

        if df_cadastro_INFORMATIVO is not None and not df_cadastro_INFORMATIVO.empty:
            # Fazer a junção com base no campo CD_DESPESA
            df_INFORMATIVO = pd.merge(df_INFORMATIVO, df_cadastro_INFORMATIVO[['GID', 'TX_DESCRICAO']], 
                                    left_on='CD_INFORMATIVO', right_on='GID', how='left')
            
            # Substituir a coluna CD_DESPESA por TX_DESCRICAO
            df_INFORMATIVO['CD_INFORMATIVO'] = df_INFORMATIVO['TX_DESCRICAO']

        # Renomear as colunas
        df_INFORMATIVO = df_INFORMATIVO.rename(columns={
            'TX_DESCRICAO': 'Descrição'
        })

        # Exibir o DataFrame formatado
        st.dataframe(df_INFORMATIVO[['Descrição']], use_container_width=True, hide_index=True)

    with tabinformativo2:
        st.write("FORMULÁRIO DE CADASTRO DE NOTAS DE MANUTENÇÃO (INFORMATIVO) - ADMINISTRAÇÃO")
        var_Novo_GID_Nota_Informativo = str(uuid.uuid4())
        with st.form(key="new_nota_informativo", clear_on_submit=True, enter_to_submit=False):
            nota_informativo_df = project_data['informativo']
            nota_informativo_map = dict(zip(nota_informativo_df['TX_DESCRICAO'], nota_informativo_df['GID'])) if not nota_informativo_df.empty else {}
            nota_informativo_selecionado = st.selectbox("Descrição", options=list(nota_informativo_map.keys()) or [''])
            cd_nota_informativo = nota_informativo_map.get(nota_informativo_selecionado, None)
            cd_GID_informativo = var_Novo_GID_Nota_Informativo
            cd_nota_manutencao_informativo = nota_data['GID']
            
            submit_button = st.form_submit_button("Salvar Nota Informativo")
            
            if submit_button:
                nova_nota_informativo = {
                    'CD_INFORMATIVO': cd_nota_informativo,
                    'GID': cd_GID_informativo,
                    'CD_NOTA_MANUTENCAO': cd_nota_manutencao_informativo,

                }
                try:
                    with st.spinner("Salvando informações, por favor aguarde..."):
                        create_data('timecenter.TB_NOTA_MANUTENCAO_INFORMATIVO', nova_nota_informativo)
                        st.success("Nova Nota de Informativo cadastrada com sucesso!")
                        
                        # Limpar cache e recarregar dados
                        clear_cache("informativo_data")

                except Exception as e:
                    st.error(f"Erro ao cadastrar informativo: {e}")

def show_material_tab(project_data, nota_data):
    # Criar as abas
    tabmaterial1, tabmaterial2 = st.tabs([
        "Lista de Dados Materiais",
        "Cadastrar Material"
    ])

    with tabmaterial1:
        # Limpar cache e recarregar dados
        clear_cache("material_data")
        st.write("LANÇAMENTO DE NOTAS DE MANUTENÇÃO (MATERIAL) - MANUTENÇÃO")
        df_MATERIAL = load_or_refresh_data("timecenter.TB_NOTA_MANUTENCAO_MATERIAL", "material_data")

        if df_MATERIAL is None or df_MATERIAL.empty:
            st.warning("Nenhum MATERIAL encontrado para a nota selecionada.")
            return

        # Verifique se 'GID' contém mais de um valor
        if isinstance(nota_data['GID'], pd.Series):
            # Se 'GID' for uma série (pode conter mais de um valor)
            df_MATERIAL = df_MATERIAL[df_MATERIAL['CD_NOTA_MANUTENCAO'].isin(nota_data['GID'])]
        else:
            # Se 'GID' for um valor único (string ou número)
            df_MATERIAL = df_MATERIAL[df_MATERIAL['CD_NOTA_MANUTENCAO'] == nota_data['GID']]

        # Renomear as colunas
        df_MATERIAL = df_MATERIAL.rename(columns={
            'TX_IDENTIFICADOR': 'ID',
            'TX_DESCRICAO': 'Descrição',
            'VL_QUANTIDADE': 'Quantidade',
            'VL_CUSTO_TOTAL': 'Custo Total',
            'TX_NUMERO_RC': 'Número RC',
            'DT_PEDIDO':'Data Pedido',
            'TX_NUMERO_PEDIDO':'Número Pedido'
        })

        # Formatar a coluna Data (DT_LANCAMENTO) para o formato dd/mm/aaaa
        df_MATERIAL['Data Pedido'] = pd.to_datetime(df_MATERIAL['Data Pedido'], errors='coerce').dt.strftime('%d/%m/%Y')

        # Exibir o DataFrame formatado
        st.dataframe(df_MATERIAL[['ID', 'Descrição', 'Quantidade', 'Custo Total', 'Número RC', 'Data Pedido', 'Número Pedido']], 
                    use_container_width=True, hide_index=True)
        
    with tabmaterial2:
        st.write("FORMULÁRIO DE CADASTRO DE NOTAS DE MANUTENÇÃO (MATERIAL) - MANUTENÇÃO")
        var_Novo_GID_Nota_Material = str(uuid.uuid4())
        with st.form(key="new_nota_material", clear_on_submit=True, enter_to_submit=False):

            collayout_material1, collayout_material2, collayout_material3, collayout_material4 = st.columns(4)
            with collayout_material1:
                var_cd_gid_material = var_Novo_GID_Nota_Material
                var_TX_IDENTIFICADOR_material = st.text_input("Identificador")
                var_CD_NOTA_MANUTENCAO_material = nota_data['GID']
                var_TX_DESCRICAO_material = st.text_input("Descrição")

            with collayout_material2: 
                var_VL_QUANTIDADE_material = st.text_input("Quantidade", value="0.00")
                if not var_VL_QUANTIDADE_material.isdigit():
                    st.warning("A quantidade deve ser um número.")       

            with collayout_material3:            
                var_VL_CUSTO_TOTAL_material = st.text_input("Custo Total", value="0.00")
                if not var_VL_CUSTO_TOTAL_material.isdigit():
                    st.warning("O custo total deve ser um número.")
            with collayout_material4:
                var_TX_NUMERO_RC_material = st.text_input("Número da RC") 
                var_DT_PEDIDO_material = st.date_input("Data do Pedido", value=pd.to_datetime('today').date())
                var_TX_NUMERO_PEDIDO_material = st.text_input("Número do Pedido")
            
            submit_button = st.form_submit_button("Salvar Nota material")
            
            if submit_button:
                nova_nota_material = {
                    'GID': var_cd_gid_material,
                    'TX_IDENTIFICADOR': var_TX_IDENTIFICADOR_material,
                    'CD_NOTA_MANUTENCAO': var_CD_NOTA_MANUTENCAO_material,
                    'TX_DESCRICAO': var_TX_DESCRICAO_material,
                    'VL_QUANTIDADE': var_VL_QUANTIDADE_material,
                    'VL_CUSTO_TOTAL': var_VL_CUSTO_TOTAL_material,
                    'TX_NUMERO_RC': var_TX_NUMERO_RC_material,
                    'DT_PEDIDO': var_DT_PEDIDO_material,
                    'TX_NUMERO_PEDIDO': var_TX_NUMERO_PEDIDO_material               

                }                   
                try:
                    with st.spinner("Salvando informações, por favor aguarde..."):
                        create_data('timecenter.TB_NOTA_MANUTENCAO_material', nova_nota_material)
                        st.success("Nova Nota de material cadastrada com sucesso!")
                        
                        # Limpar cache e recarregar dados
                        clear_cache("material_data")

                except Exception as e:
                    st.error(f"Erro ao cadastrar informativo: {e}")

def show_recurso_tab(project_data, nota_data):
    # Criar as abas
    tabrecurso1, tabrecurso2 = st.tabs([
        "Lista de Dados Recursos",
        "Cadastrar Recursos"
    ])

    with tabrecurso1:
        # Limpar cache e recarregar dados
        clear_cache("recurso_data")
        st.write("LANÇAMENTO DE NOTAS DE MANUTENÇÃO (RECURSO) - ADMINISTRAÇÃO")
        df_RECURSO = load_or_refresh_data("timecenter.TB_NOTA_MANUTENCAO_RECURSO", "recurso_data")

        if df_RECURSO is None or df_RECURSO.empty:
            st.warning("Nenhum RECURSO encontrado para a nota selecionada.")
            return

        # Verifique se 'GID' contém mais de um valor
        if isinstance(nota_data['GID'], pd.Series):
            # Se 'GID' for uma série (pode conter mais de um valor)
            df_RECURSO = df_RECURSO[df_RECURSO['CD_NOTA_MANUTENCAO'].isin(nota_data['GID'])]
        else:
            # Se 'GID' for um valor único (string ou número)
            df_RECURSO = df_RECURSO[df_RECURSO['CD_NOTA_MANUTENCAO'] == nota_data['GID']]

        # Carregar os dados de timecenter.TB_CADASTRO_RECURSO para mapear os códigos
        df_CADASTRO_RECURSO = read_data("timecenter.TB_CADASTRO_RECURSO")

        if df_CADASTRO_RECURSO is not None and not df_CADASTRO_RECURSO.empty:
            # Fazer a junção com base no campo CD_DESPESA
            df_RECURSO = pd.merge(df_RECURSO, df_CADASTRO_RECURSO[['GID', 'TX_DESCRICAO']], 
                                    left_on='CD_RECURSO', right_on='GID', how='left')
            
            # Substituir a coluna CD_DESPESA por TX_DESCRICAO
            df_RECURSO['CD_RECURSO'] = df_RECURSO['TX_DESCRICAO']

                # Adicionar a nova coluna 'HH' como o produto de 'VL_QUANTIDADE' e 'VL_DURACAO'
        df_RECURSO['HH'] = df_RECURSO['VL_QUANTIDADE'] * df_RECURSO['VL_DURACAO']
        
        # Formatar a coluna 'HH' no formato brasileiro #.###0,00
        df_RECURSO['HH'] = df_RECURSO['HH'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        # Formatar a coluna 'HH' no formato brasileiro #.###0,00
        df_RECURSO['VL_QUANTIDADE'] = df_RECURSO['VL_QUANTIDADE'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        df_RECURSO['VL_DURACAO'] = df_RECURSO['VL_DURACAO'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        df_RECURSO['VL_VALOR_CUSTO'] = df_RECURSO['VL_VALOR_CUSTO'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        df_RECURSO['VL_CUSTO_TOTAL'] = df_RECURSO['VL_CUSTO_TOTAL'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        # Renomear as colunas
        df_RECURSO = df_RECURSO.rename(columns={
            'TX_DESCRICAO': 'Descrição',
            'VL_QUANTIDADE': 'Quantidade',
            'VL_DURACAO': 'Duração',
            'VL_VALOR_CUSTO': 'Custo (R$)',
            'VL_CUSTO_TOTAL': 'Custo Total'
        })

        # Exibir o DataFrame formatado
        st.dataframe(df_RECURSO[['Descrição', 'Quantidade', 'Duração', 'HH', 'Custo (R$)', 'Custo Total']], 
                    use_container_width=True, hide_index=True)
        
    with tabrecurso2:
        st.write("FORMULÁRIO DE CADASTRO DE NOTAS DE MANUTENÇÃO (RECURSO) - ADMINISTRAÇÃO")
        var_Novo_GID_Nota_Recurso = str(uuid.uuid4())
        with st.form(key="new_nota_recurso", clear_on_submit=True, enter_to_submit=False):

            collayout_recurso1, collayout_recurso2, collayout_recurso3, collayout_recurso4 = st.columns(4)
            with collayout_recurso1:
                # Função para carregar os dados dos recursos do projeto
                nota_recurso_df = project_data['recurso']
                nota_recurso_map = dict(zip(nota_recurso_df['TX_DESCRICAO'], nota_recurso_df['GID'])) if not nota_recurso_df.empty else {}
                # Selecionar o código do recurso
                nota_recurso_selecionado = st.selectbox("Cód. Recurso", options=list(nota_recurso_map.keys()) or [''])
                var_cd_nota_recurso = nota_recurso_map.get(nota_recurso_selecionado, None)
                # Inicializar valores padrão
                var_vl_valor_custo_recurso = 0.0
                var_vl_quantidade_recurso = 0.0
                var_vl_duracao_recurso = 0.0
                var_vl_custo_total_recurso = 0.0

                # Carregar o valor do recurso selecionado
                if nota_recurso_selecionado:
                    # Acessar os dados do recurso selecionado
                    recurso_selecionado_data = nota_recurso_df[nota_recurso_df['TX_DESCRICAO'] == nota_recurso_selecionado]
                    
                    # Se o recurso foi encontrado, carregar o valor de custo
                    if not recurso_selecionado_data.empty:
                        var_vl_valor_custo_recurso = recurso_selecionado_data.iloc[0]['VL_VALOR_CUSTO']

                # Exibir os campos com os valores calculados
                var_GID_recurso = var_Novo_GID_Nota_Recurso
                var_cd_nota_manutencao_recurso = nota_data['GID']

            with collayout_recurso2:
                # Campo de Quantidade
                var_vl_quantidade_recurso = st.text_input("Quantidade", value=str(var_vl_quantidade_recurso))
                if not var_vl_quantidade_recurso.isdigit():
                    st.warning("A quantidade deve ser um número.")
                    var_vl_quantidade_recurso = 0.0  # Valor padrão se não for um número

            with collayout_recurso3:
                # Campo de Duração (horas)
                var_vl_duracao_recurso = st.text_input("Duração (h)", value=str(var_vl_duracao_recurso))
                if not var_vl_duracao_recurso.isdigit():
                    st.warning("A duração deve ser um número.")
                    var_vl_duracao_recurso = 0.0  # Valor padrão se não for um número

            with collayout_recurso4:
                # Campo de Valor de Custo (preenchido automaticamente com o valor do recurso selecionado)
                var_vl_valor_custo_recurso = st.text_input("Valor de Custo (R$)", value=str(var_vl_valor_custo_recurso))

                # Calcular o valor total com base em quantidade, duração e valor de custo
                try:
                    var_vl_quantidade_recurso = float(var_vl_quantidade_recurso)
                    var_vl_duracao_recurso = float(var_vl_duracao_recurso)
                    var_vl_valor_custo_recurso = float(var_vl_valor_custo_recurso)

                    # Cálculo do valor total
                    var_vl_custo_total_recurso = var_vl_quantidade_recurso * var_vl_duracao_recurso * var_vl_valor_custo_recurso

                except ValueError:
                    st.warning("Por favor, insira valores válidos para quantidade, duração e valor de custo.")
                    var_vl_custo_total_recurso = 0.0  # Valor padrão se houver erro

                # Exibir o resultado do cálculo
                st.text_input("Valor Total (R$)", value=f"{var_vl_custo_total_recurso:.2f}", disabled=True)                
            
            submit_button = st.form_submit_button("Salvar Nota Recurso")
            
            if submit_button:
                nova_nota_recurso = {
                    'GID': var_GID_recurso,
                    'CD_NOTA_MANUTENCAO': var_cd_nota_manutencao_recurso,
                    'CD_RECURSO': var_cd_nota_recurso,
                    'VL_QUANTIDADE': var_vl_quantidade_recurso,
                    'VL_DURACAO': var_vl_duracao_recurso,
                    'VL_VALOR_CUSTO': var_vl_valor_custo_recurso,
                    'VL_CUSTO_TOTAL': var_vl_custo_total_recurso

                }                    
                try:
                    with st.spinner("Salvando informações, por favor aguarde..."):
                        create_data('timecenter.TB_NOTA_MANUTENCAO_RECURSO', nova_nota_recurso)
                        st.success("Nova nota de recurso cadastrada com sucesso!")
                        # Limpar cache e recarregar dados
                        clear_cache("recurso_data")

                except Exception as e:
                    st.error(f"Erro ao cadastrar informativo: {e}")

def show_apoio_tab(project_data, nota_data):
    # Criar as abas
    tabapoio1, tabapoio2 = st.tabs([
        "Lista de Dados Apoio",
        "Cadastrar Apoio"
    ])

    with tabapoio1:
        # Limpar cache e recarregar dados
        clear_cache("apoio_data")
        st.write("LANÇAMENTO DE NOTAS DE MANUTENÇÃO (APOIO) - ADMINISTRAÇÃO")
        df_APOIO = load_or_refresh_data("timecenter.TB_NOTA_MANUTENCAO_APOIO", "apoio_data")

        if df_APOIO is None or df_APOIO.empty:
            st.warning("Nenhum APOIO encontrado para a nota selecionada.")
            return

        # Verifique se 'GID' contém mais de um valor
        if isinstance(nota_data['GID'], pd.Series):
            # Se 'GID' for uma série (pode conter mais de um valor)
            df_APOIO = df_APOIO[df_APOIO['CD_NOTA_MANUTENCAO'].isin(nota_data['GID'])]
        else:
            # Se 'GID' for um valor único (string ou número)
            df_APOIO = df_APOIO[df_APOIO['CD_NOTA_MANUTENCAO'] == nota_data['GID']]

        # Carregar os dados de timecenter.TB_CADASTRO_APOIO para mapear os códigos
        df_CADASTRO_APOIO = read_data("timecenter.TB_CADASTRO_APOIO")

        if df_CADASTRO_APOIO is not None and not df_CADASTRO_APOIO.empty:
            # Fazer a junção com base no campo CD_DESPESA
            df_APOIO = pd.merge(df_APOIO, df_CADASTRO_APOIO[['GID', 'TX_DESCRICAO']], 
                                    left_on='CD_APOIO', right_on='GID', how='left')
            
            # Substituir a coluna CD_DESPESA por TX_DESCRICAO
            df_APOIO['CD_APOIO'] = df_APOIO['TX_DESCRICAO']

        # Formatar a coluna 'HH' no formato brasileiro #.###0,00
        df_APOIO['VL_QUANTIDADE'] = df_APOIO['VL_QUANTIDADE'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        # Formatar a coluna 'VL_PERCENTUAL_CUSTO' no formato percentual
        df_APOIO['VL_PERCENTUAL_CUSTO'] = df_APOIO['VL_PERCENTUAL_CUSTO'].apply(
            lambda x: f"{x * 100:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        df_APOIO['VL_VALOR_CUSTO'] = df_APOIO['VL_VALOR_CUSTO'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        df_APOIO['VL_CUSTO_TOTAL'] = df_APOIO['VL_CUSTO_TOTAL'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        # Renomear as colunas
        df_APOIO = df_APOIO.rename(columns={
            'TX_DESCRICAO': 'Descrição',
            'VL_QUANTIDADE': 'Quantidade',
            'VL_VALOR_CUSTO': 'Custo (R$)',
            'VL_PERCENTUAL_CUSTO': 'Custo (%)',
            'VL_CUSTO_TOTAL': 'Custo Total'
        })

        # Exibir o DataFrame formatado
        st.dataframe(df_APOIO[['Descrição', 'Quantidade', 'Custo (R$)', 'Custo (%)', 'Custo Total']], 
                    use_container_width=True, hide_index=True)

    with tabapoio2:
        st.write("FORMULÁRIO DE CADASTRO DE NOTAS DE MANUTENÇÃO (APOIO) - ADMINISTRAÇÃO")
        var_Novo_GID_Nota_Apoio = str(uuid.uuid4())
        with st.form(key="new_nota_apoio", clear_on_submit=True, enter_to_submit=False):

            collayout_apoio1, collayout_apoio2 = st.columns(2)
            with collayout_apoio1:
                # Função para carregar os dados dos apoios do projeto
                nota_apoio_df = project_data['apoio']
                nota_apoio_map = dict(zip(nota_apoio_df['TX_DESCRICAO'], nota_apoio_df['GID'])) if not nota_apoio_df.empty else {}
                # Selecionar o código de apoio
                nota_apoio_selecionado = st.selectbox("Cód. Apoio", options=list(nota_apoio_map.keys()) or [''])
                var_cd_apoio = nota_apoio_map.get(nota_apoio_selecionado, None)

                # Inicializar variáveis
                var_vl_valor_custo_apoio = 0.00
                var_vl_percentual_custo_apoio = 0.00
                var_vl_quantidade_apoio = 0.00
                var_vl_custo_total_apoio = 0.00

                # Carregar o valor do apoio selecionado
                if nota_apoio_selecionado:
                    # Acessar os dados do apoio selecionado
                    apoio_selecionado_data = nota_apoio_df[nota_apoio_df['TX_DESCRICAO'] == nota_apoio_selecionado]
                    
                    # Se o apoio foi encontrado, carregar o valor de custo e o percentual de custo
                    if not apoio_selecionado_data.empty:
                        var_vl_valor_custo_apoio = apoio_selecionado_data.iloc[0]['VL_VALOR_CUSTO']
                        var_vl_percentual_custo_apoio = apoio_selecionado_data.iloc[0]['VL_PERCENTUAL_CUSTO']

                # Exibir os campos com os valores preenchidos
                var_GID_apoio = var_Novo_GID_Nota_Apoio
                var_cd_nota_manutencao_apoio = nota_data['GID']

                # Campo de Quantidade
                var_vl_quantidade_apoio = st.text_input("Quantidade", value=str(var_vl_quantidade_apoio))
                if not var_vl_quantidade_apoio.isdigit():
                    st.warning("A quantidade deve ser um número.")
                    var_vl_quantidade_apoio = 0.00  # Valor padrão se não for um número
            with collayout_apoio2:
                # Campo de Valor de Custo (preenchido automaticamente com o valor do apoio selecionado)
                var_vl_valor_custo_apoio = st.text_input("Valor de Custo (R$)", value=f"{var_vl_valor_custo_apoio:.2f}", disabled=True)

                # Campo de Percentual de Custo (preenchido automaticamente com o percentual de custo)
                var_vl_percentual_custo_apoio = st.text_input("Percentual de Custo (%)", value=f"{var_vl_percentual_custo_apoio:.2f}", disabled=True)

                # Calcular o valor total com base em quantidade e valor de custo
                try:
                    var_vl_quantidade_apoio = float(var_vl_quantidade_apoio)
                    var_vl_valor_custo_apoio = float(var_vl_valor_custo_apoio)

                    # Cálculo do valor total
                    var_vl_custo_total_apoio = var_vl_quantidade_apoio * var_vl_valor_custo_apoio

                except ValueError:
                    st.warning("Por favor, insira valores válidos para quantidade e valor de custo.")
                    var_vl_custo_total_apoio = 0.00  # Valor padrão se houver erro

                # Exibir o resultado do cálculo
                st.text_input("Valor Total (R$)", value=f"{var_vl_custo_total_apoio:.2f}", disabled=True)               
            
            submit_button = st.form_submit_button("Salvar Nota Apoio")
            
            if submit_button:
                nova_nota_apoio = {
                    'GID': var_GID_apoio,
                    'CD_NOTA_MANUTENCAO': var_cd_nota_manutencao_apoio,
                    'CD_APOIO': var_cd_apoio,
                    'VL_QUANTIDADE': var_vl_quantidade_apoio,
                    'VL_VALOR_CUSTO': var_vl_valor_custo_apoio,
                    'VL_CUSTO_TOTAL': var_vl_custo_total_apoio,
                    'VL_PERCENTUAL_CUSTO': var_vl_percentual_custo_apoio

                }
                with st.spinner("Salvando informações, por favor aguarde..."):
                    create_data('timecenter.TB_NOTA_MANUTENCAO_APOIO', nova_nota_apoio)
                    st.success("Nova nota de recurso cadastrada com sucesso!")
                    
                try:
                    with st.spinner("Salvando informações, por favor aguarde..."):
                        create_data('timecenter.TB_NOTA_MANUTENCAO_APOIO', nova_nota_apoio)
                        st.success("Nova nota de recurso cadastrada com sucesso!")
                        
                        # Limpar cache e recarregar dados
                        clear_cache("apoio_data")

                except Exception as e:
                    st.error(f"Erro ao cadastrar informativo: {e}")
            
@st.dialog("Editar Nota", width="large")
def edit_nota_manutencao():
    if 'project_data' in st.session_state and 'nota_selecionada' in st.session_state:
        project_data = st.session_state['project_data']
        gid_nota = st.session_state['nota_selecionada']
        notas_df = project_data['notas_de_manutencao_geral']
        nota_data = notas_df[notas_df['GID'] == gid_nota].iloc[0] if gid_nota else None

        if nota_data is None:
            st.warning("Nota não encontrada.")
            return

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Editar Notas e Ordens", "Informativo", "Material", "Recurso", "Apoio"
        ])

        with tab1:
            show_edit_nota_form(project_data, nota_data)
        with tab2:
            show_informativo_tab(project_data, nota_data)
        with tab3:
            show_material_tab(project_data, nota_data)
        with tab4:
            show_recurso_tab(project_data, nota_data)
        with tab5:
            show_apoio_tab(project_data, nota_data)

def main():
    edit_nota_manutencao()

if __name__ == "__main__":
    main()
