import streamlit as st
import pandas as pd
from utils import (update_data, read_data, 
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
    # Converter a coluna ID_NOTA_MANUTENCAO para int
    df['ID'] = df['ID'].astype(int)
    # Ordenar o DataFrame pela coluna ID_NOTA_MANUTENCAO de forma decrescente
    df = df.sort_values(by='ID', ascending=False)

    #df['VL_HH_TOTAL'] = pd.to_numeric(df['VL_HH_TOTAL'], errors='coerce').fillna(0.0)
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
    id_nota_selected = st.multiselect("ID Nota Manutenção", options=sorted(df['ID'].unique()),key="filteridnota")

    # Carregar os dados da nota selecionada
    nota_data = df[df['ID'].isin(id_nota_selected)]

    if not nota_data.empty:
        nota_data = nota_data.iloc[0]

        st.write(f"Editando Nota: {id_nota_selected}")
        
        # Formulário de edição
        with st.form(key="edit_nota_form"):
            col1, col2 = st.columns(2)

            with col1:
                cd_projeto = st.text_input("Código do Projeto", nota_data.get('CD_PROJETO', ''))

                # Converter a data de atualização para garantir que seja uma data válida
                dt_data_row = nota_data.get('DT_NOTA', None)
                if pd.isnull(dt_data_row) or isinstance(dt_data_row, str):
                    dt_data = st.date_input("Data da Nota", value=pd.to_datetime('today').date())
                else:
                    dt_data = st.date_input("Data da Nota", value=pd.to_datetime(dt_data_row).date())
                
                # Mapeamento de valores para a situação da nota
                situacao_map = {'P': 'Pendente', 'A': 'Aprovado', 'R': 'Reprovado'}
                reverse_situacao_map = {v: k for k, v in situacao_map.items()}

                # Obter a situação atual da nota e exibir na caixa de seleção
                situacao_atual = situacao_map.get(nota_data.get('FL_SITUACAO', 'P'), 'Pendente')
                fl_situacao_nota = st.selectbox("Situação da Nota", options=list(situacao_map.values()), index=list(situacao_map.values()).index(situacao_atual))
                
                # Converter de volta para o valor original ('P', 'A', 'R') para salvar no banco de dados
                fl_situacao_nota = reverse_situacao_map[fl_situacao_nota]

                tx_nota = st.text_input("Nota", nota_data.get('TX_NOTA', ''))
                tx_ordem = st.text_input("Ordem", nota_data.get('TX_ORDEM', ''))
                tx_tag = st.text_input("Tag", nota_data.get('TX_TAG', ''))
                tx_tag_linha = st.text_input("Tag da Linha", nota_data.get('TX_TAG_LINHA', ''))

            with col2:
                # Carregar os serviços disponíveis para o projeto atual
                servicos_df = get_servicos_projeto(selected_gid)

                # Verificar se há dados retornados
                if servicos_df.empty:
                    st.warning("Nenhum serviço encontrado para este projeto.")
                    cd_servico = None
                    tx_descricao_servico = None
                else:
                    # Mapear descrições para os GIDs
                    servico_map = dict(zip(servicos_df['TX_DESCRICAO'], servicos_df['GID']))
                    
                    # Obter a descrição atual com base no GID da nota
                    descricao_atual = servicos_df.loc[servicos_df['GID'] == nota_data.get('CD_SERVICO', ''), 'TX_DESCRICAO'].values
                    descricao_atual = descricao_atual[0] if len(descricao_atual) > 0 else None

                    # Criar a caixa de seleção (selectbox) para exibir as descrições
                    descricao_servico_selecionada = st.selectbox(
                        "Código do Serviço",
                        options=list(servico_map.keys()),
                        index=list(servico_map.keys()).index(descricao_atual) if descricao_atual else 0
                    )
                    
                    # Obter o GID correspondente à descrição selecionada
                    cd_servico = servico_map[descricao_servico_selecionada]
                    
                    # Campo de texto para a descrição do serviço selecionado
                    tx_descricao_servico = st.text_area("Descrição do Serviço", nota_data.get('TX_DESCRICAO_SERVICO', ''), height=150)

                # Carregar os motivos de situação para o projeto atual
                situacao_motivo_df = get_situacao_motivo_projeto(selected_gid)

                if situacao_motivo_df.empty:
                    st.warning("Nenhum motivo de situação encontrado para este projeto.")
                    cd_situacao_motivo = None
                else:
                    # Mapear descrições de motivos para os GIDs
                    situacao_motivo_map = dict(zip(situacao_motivo_df['TX_DESCRICAO'], situacao_motivo_df['GID']))

                    # Obter a descrição atual com base no GID da nota
                    motivo_atual = situacao_motivo_df.loc[situacao_motivo_df['GID'] == nota_data.get('CD_SITUACAO_MOTIVO', ''), 'TX_DESCRICAO'].values
                    motivo_atual = motivo_atual[0] if len(motivo_atual) > 0 else None

                    # Criar a caixa de seleção (selectbox) para exibir os motivos de situação
                    motivo_situacao_selecionado = st.selectbox(
                        "Motivo da Situação",
                        options=list(situacao_motivo_map.keys()),
                        index=list(situacao_motivo_map.keys()).index(motivo_atual) if motivo_atual else 0
                    )

                    # Obter o GID correspondente ao motivo selecionado
                    cd_situacao_motivo = situacao_motivo_map[motivo_situacao_selecionado]

            # Seção Solicitante e Responsável
            st.header("Solicitante e Responsável")
            col1, col2 = st.columns(2)
            with col1:
                # Carregar os setores solicitantes disponíveis para o projeto atual
                setores_solicitantes_df = get_setor_solicitante_projeto(selected_gid)

                if setores_solicitantes_df.empty:
                    st.warning("Nenhum setor solicitante encontrado para este projeto.")
                    cd_setor_solicitante = None
                else:
                    # Mapear descrições para os GIDs
                    setor_solicitante_map = dict(zip(setores_solicitantes_df['TX_DESCRICAO'], setores_solicitantes_df['GID']))

                    # Obter a descrição atual com base no GID do setor solicitante
                    setor_atual = setores_solicitantes_df.loc[setores_solicitantes_df['GID'] == nota_data.get('CD_SETOR_SOLICITANTE', ''), 'TX_DESCRICAO'].values
                    setor_atual = setor_atual[0] if len(setor_atual) > 0 else None

                    # Criar a caixa de seleção (selectbox) para exibir os setores solicitantes
                    setor_solicitante_selecionado = st.selectbox(
                        "Setor Solicitante",
                        options=list(setor_solicitante_map.keys()),
                        index=list(setor_solicitante_map.keys()).index(setor_atual) if setor_atual else 0
                    )

                    # Obter o GID correspondente ao setor selecionado
                    cd_setor_solicitante = setor_solicitante_map[setor_solicitante_selecionado]
                
                # Campo de texto para o nome do solicitante
                tx_nome_solicitante = st.text_input("Nome do Solicitante", nota_data.get('TX_NOME_SOLICITANTE', ''))

            with col2:
                # Carregar os setores responsáveis disponíveis para o projeto atual
                setores_responsaveis_df = get_setor_responsavel_projeto(selected_gid)

                if setores_responsaveis_df.empty:
                    st.warning("Nenhum setor responsável encontrado para este projeto.")
                    cd_setor_responsavel = None
                else:
                    # Mapear descrições para os GIDs
                    setor_responsavel_map = dict(zip(setores_responsaveis_df['TX_DESCRICAO'], setores_responsaveis_df['GID']))

                    # Obter a descrição atual com base no GID do setor responsável
                    setor_responsavel_atual = setores_responsaveis_df.loc[setores_responsaveis_df['GID'] == nota_data.get('CD_SETOR_RESPONSAVEL', ''), 'TX_DESCRICAO'].values
                    setor_responsavel_atual = setor_responsavel_atual[0] if len(setor_responsavel_atual) > 0 else None

                    # Criar a caixa de seleção (selectbox) para exibir os setores responsáveis
                    setor_responsavel_selecionado = st.selectbox(
                        "Setor Responsável",
                        options=list(setor_responsavel_map.keys()),
                        index=list(setor_responsavel_map.keys()).index(setor_responsavel_atual) if setor_responsavel_atual else 0
                    )

                    # Obter o GID correspondente ao setor selecionado
                    cd_setor_responsavel = setor_responsavel_map[setor_responsavel_selecionado]

            # Seção Detalhes Técnicos
            st.header("Detalhes Técnicos")
            col1, col2 = st.columns(2)
            with col1:
                # Carregar as famílias de equipamentos disponíveis para o projeto atual
                familias_equipamentos_df = get_familia_equipamentos_projeto(selected_gid)

                if familias_equipamentos_df.empty:
                    st.warning("Nenhuma família de equipamentos encontrada para este projeto.")
                    cd_familia_equipamentos = None
                else:
                    # Mapear descrições para os GIDs
                    familia_equipamentos_map = dict(zip(familias_equipamentos_df['TX_DESCRICAO'], familias_equipamentos_df['GID']))

                    # Obter a descrição atual com base no GID da família de equipamentos
                    familia_atual = familias_equipamentos_df.loc[familias_equipamentos_df['GID'] == nota_data.get('CD_FAMILIA_EQUIPAMENTOS', ''), 'TX_DESCRICAO'].values
                    familia_atual = familia_atual[0] if len(familia_atual) > 0 else None

                    # Criar a caixa de seleção (selectbox) para exibir as famílias de equipamentos
                    familia_equipamentos_selecionada = st.selectbox(
                        "Família de Equipamentos",
                        options=list(familia_equipamentos_map.keys()),
                        index=list(familia_equipamentos_map.keys()).index(familia_atual) if familia_atual else 0
                    )

                    # Obter o GID correspondente à família de equipamentos selecionada
                    cd_familia_equipamentos = familia_equipamentos_map[familia_equipamentos_selecionada]

                # Carregar as plantas disponíveis para o projeto atual
                plantas_df = get_plantas_projeto(selected_gid)

                if plantas_df.empty:
                    st.warning("Nenhuma planta encontrada para este projeto.")
                    cd_planta = None
                else:
                    # Mapear descrições para os GIDs
                    planta_map = dict(zip(plantas_df['TX_DESCRICAO'], plantas_df['GID']))

                    # Obter a descrição atual com base no GID da planta
                    planta_atual = plantas_df.loc[plantas_df['GID'] == nota_data.get('CD_PLANTA', ''), 'TX_DESCRICAO'].values
                    planta_atual = planta_atual[0] if len(planta_atual) > 0 else None

                    # Criar a caixa de seleção (selectbox) para exibir as plantas
                    planta_selecionada = st.selectbox(
                        "Código da Planta",
                        options=list(planta_map.keys()),
                        index=list(planta_map.keys()).index(planta_atual) if planta_atual else 0
                    )

                    # Obter o GID correspondente à planta selecionada
                    cd_planta = planta_map[planta_selecionada]

                # Carregar as especialidades disponíveis para o projeto atual
                especialidades_df = get_especialidades_projeto(selected_gid)

                if especialidades_df.empty:
                    st.warning("Nenhuma especialidade encontrada para este projeto.")
                    cd_especialidade = None
                else:
                    # Mapear descrições para os GIDs
                    especialidade_map = dict(zip(especialidades_df['TX_DESCRICAO'], especialidades_df['GID']))

                    # Obter a descrição atual com base no GID da especialidade
                    especialidade_atual = especialidades_df.loc[especialidades_df['GID'] == nota_data.get('CD_ESPECIALIDADE', ''), 'TX_DESCRICAO'].values
                    especialidade_atual = especialidade_atual[0] if len(especialidade_atual) > 0 else None

                    # Criar a caixa de seleção (selectbox) para exibir as especialidades
                    especialidade_selecionada = st.selectbox(
                        "Código da Especialidade",
                        options=list(especialidade_map.keys()),
                        index=list(especialidade_map.keys()).index(especialidade_atual) if especialidade_atual else 0
                    )

                    # Obter o GID correspondente à especialidade selecionada
                    cd_especialidade = especialidade_map[especialidade_selecionada]

                # Outros campos
                tx_rec_inspecao = st.text_input("Recomendação de Inspeção", nota_data.get('TX_REC_INSPECAO', ''))

            with col2:
                # Carregar as áreas disponíveis para o projeto atual
                areas_df = get_areas_projeto(selected_gid)

                if areas_df.empty:
                    st.warning("Nenhuma área encontrada para este projeto.")
                    cd_area = None
                else:
                    # Mapear descrições para os GIDs
                    area_map = dict(zip(areas_df['TX_DESCRICAO'], areas_df['GID']))

                    # Obter a descrição atual com base no GID da área
                    area_atual = areas_df.loc[areas_df['GID'] == nota_data.get('CD_AREA', ''), 'TX_DESCRICAO'].values
                    area_atual = area_atual[0] if len(area_atual) > 0 else None

                    # Criar a caixa de seleção (selectbox) para exibir as áreas
                    area_selecionada = st.selectbox(
                        "Código da Área",
                        options=list(area_map.keys()),
                        index=list(area_map.keys()).index(area_atual) if area_atual else 0
                    )

                    # Obter o GID correspondente à área selecionada
                    cd_area = area_map[area_selecionada]

                # Carregar os sistemas operacionais disponíveis para o projeto atual
                sistemas_operacionais_df = get_sistemas_operacionais_projeto(selected_gid)

                if sistemas_operacionais_df.empty:
                    st.warning("Nenhum sistema operacional encontrado para este projeto.")
                    cd_sistema_operacional_1 = None
                    cd_sistema_operacional_2 = None
                else:
                    # Mapear descrições para os GIDs
                    sistema_operacional_map = dict(zip(sistemas_operacionais_df['TX_DESCRICAO'], sistemas_operacionais_df['GID']))

                    # Obter a descrição atual com base no GID do sistema operacional 1
                    sistema_operacional_atual_1 = sistemas_operacionais_df.loc[sistemas_operacionais_df['GID'] == nota_data.get('CD_SISTEMA_OPERACIONAL_1', ''), 'TX_DESCRICAO'].values
                    sistema_operacional_atual_1 = sistema_operacional_atual_1[0] if len(sistema_operacional_atual_1) > 0 else None

                    # Criar a caixa de seleção (selectbox) para exibir os sistemas operacionais 1
                    sistema_operacional_selecionado_1 = st.selectbox(
                        "Sistema Operacional 1",
                        options=list(sistema_operacional_map.keys()),
                        index=list(sistema_operacional_map.keys()).index(sistema_operacional_atual_1) if sistema_operacional_atual_1 else 0
                    )

                    # Obter o GID correspondente ao sistema operacional selecionado 1
                    cd_sistema_operacional_1 = sistema_operacional_map[sistema_operacional_selecionado_1]

                    # Obter a descrição atual com base no GID do sistema operacional 2
                    sistema_operacional_atual_2 = sistemas_operacionais_df.loc[sistemas_operacionais_df['GID'] == nota_data.get('CD_SISTEMA_OPERACIONAL_2', ''), 'TX_DESCRICAO'].values
                    sistema_operacional_atual_2 = sistema_operacional_atual_2[0] if len(sistema_operacional_atual_2) > 0 else None

                    # Criar a caixa de seleção (selectbox) para exibir os sistemas operacionais 2
                    sistema_operacional_selecionado_2 = st.selectbox(
                        "Sistema Operacional 2",
                        options=list(sistema_operacional_map.keys()),
                        index=list(sistema_operacional_map.keys()).index(sistema_operacional_atual_2) if sistema_operacional_atual_2 else 0
                    )

                    # Obter o GID correspondente ao sistema operacional selecionado 2
                    cd_sistema_operacional_2 = sistema_operacional_map[sistema_operacional_selecionado_2]


            # Seção Escopo e Situação
            st.header("Escopo e Situação")
            col1, col2 = st.columns(2)
            with col1:
                # Carregar as origens de escopo disponíveis para o projeto atual
                escopo_origem_df = get_escopo_origem_projeto(selected_gid)

                if escopo_origem_df.empty:
                    st.warning("Nenhuma origem de escopo encontrada para este projeto.")
                    cd_escopo_origem = None
                else:
                    # Mapear descrições para os GIDs
                    escopo_origem_map = dict(zip(escopo_origem_df['TX_DESCRICAO'], escopo_origem_df['GID']))

                    # Obter a descrição atual com base no GID da origem do escopo
                    escopo_origem_atual = escopo_origem_df.loc[escopo_origem_df['GID'] == nota_data.get('CD_ESCOPO_ORIGEM', ''), 'TX_DESCRICAO'].values
                    escopo_origem_atual = escopo_origem_atual[0] if len(escopo_origem_atual) > 0 else None

                    # Criar a caixa de seleção (selectbox) para exibir as origens de escopo
                    escopo_origem_selecionado = st.selectbox(
                        "Origem do Escopo",
                        options=list(escopo_origem_map.keys()),
                        index=list(escopo_origem_map.keys()).index(escopo_origem_atual) if escopo_origem_atual else 0
                    )

                    # Obter o GID correspondente à origem de escopo selecionada
                    cd_escopo_origem = escopo_origem_map[escopo_origem_selecionado]

                # Carregar os tipos de escopo disponíveis para o projeto atual
                escopo_tipo_df = get_escopo_tipo_projeto(selected_gid)

                if escopo_tipo_df.empty:
                    st.warning("Nenhum tipo de escopo encontrado para este projeto.")
                    cd_escopo_tipo = None
                else:
                    # Mapear descrições para os GIDs
                    escopo_tipo_map = dict(zip(escopo_tipo_df['TX_DESCRICAO'], escopo_tipo_df['GID']))

                    # Obter a descrição atual com base no GID do tipo de escopo
                    escopo_tipo_atual = escopo_tipo_df.loc[escopo_tipo_df['GID'] == nota_data.get('CD_ESCOPO_TIPO', ''), 'TX_DESCRICAO'].values
                    escopo_tipo_atual = escopo_tipo_atual[0] if len(escopo_tipo_atual) > 0 else None

                    # Criar a caixa de seleção (selectbox) para exibir os tipos de escopo
                    escopo_tipo_selecionado = st.selectbox(
                        "Tipo de Escopo",
                        options=list(escopo_tipo_map.keys()),
                        index=list(escopo_tipo_map.keys()).index(escopo_tipo_atual) if escopo_tipo_atual else 0
                    )

                    # Obter o GID correspondente ao tipo de escopo selecionado
                    cd_escopo_tipo = escopo_tipo_map[escopo_tipo_selecionado]

                # Outros campos
                tx_equipamento_mestre = st.text_input("Equipamento Mestre", nota_data.get('TX_EQUIPAMENTO_MESTRE', ''))

            with col2:
                fl_nmp = st.selectbox("Nota Manutenção Parada?", ["Sim", "Não"], index=0 if nota_data.get('FL_NMP', 'Não') == 'Sim' else 1)
                fl_ase = st.selectbox("Tem Autorização de Serviço Extra?", ["Sim", "Não"], index=0 if nota_data.get('FL_ASE', 'Não') == 'Sim' else 1)
                tx_ase = st.text_input("Autorização Serviço Extra", nota_data.get('TX_ASE', ''))

            # Seção 5: Executantes
            st.header("Executantes")
            col1, col2 = st.columns(2)
            with col1:
                # Carregar os executantes disponíveis para o projeto atual
                executantes_df = get_executantes_projeto(selected_gid)

                if executantes_df.empty:
                    st.warning("Nenhum executante encontrado para este projeto.")
                    cd_executante_1 = None
                else:
                    # Mapear descrições para os GIDs
                    executante_map = dict(zip(executantes_df['TX_DESCRICAO'], executantes_df['GID']))

                    # Obter a descrição atual com base no GID do executante
                    executante_atual_1 = executantes_df.loc[executantes_df['GID'] == nota_data.get('CD_EXECUTANTE_1', ''), 'TX_DESCRICAO'].values
                    executante_atual_1 = executante_atual_1[0] if len(executante_atual_1) > 0 else None

                    # Criar a caixa de seleção (selectbox) para exibir os executantes
                    executante_1_selecionado = st.selectbox(
                        "Código do Executante 1",
                        options=list(executante_map.keys()),
                        index=list(executante_map.keys()).index(executante_atual_1) if executante_atual_1 else 0
                    )

                    # Obter o GID correspondente ao executante selecionado
                    cd_executante_1 = executante_map[executante_1_selecionado]

            with col2:
                if executantes_df.empty:
                    st.warning("Nenhum executante encontrado para este projeto.")
                    cd_executante_2 = None
                else:
                    # Obter a descrição atual com base no GID do executante 2
                    executante_atual_2 = executantes_df.loc[executantes_df['GID'] == nota_data.get('CD_EXECUTANTE_2', ''), 'TX_DESCRICAO'].values
                    executante_atual_2 = executante_atual_2[0] if len(executante_atual_2) > 0 else None

                    # Criar a caixa de seleção (selectbox) para exibir os executantes
                    executante_2_selecionado = st.selectbox(
                        "Código do Executante 2",
                        options=list(executante_map.keys()),
                        index=list(executante_map.keys()).index(executante_atual_2) if executante_atual_2 else 0
                    )

                    # Obter o GID correspondente ao executante selecionado
                    cd_executante_2 = executante_map[executante_2_selecionado]

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
                "DT_NOTA": dt_data,
                "FL_SITUACAO":fl_situacao_nota,
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
