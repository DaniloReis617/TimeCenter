import streamlit as st
import pandas as pd
import uuid
from utils import (create_data, convert_to_native_types,get_nota_manutencao_geral)

@st.dialog("Cadastrar Nova Nota", width="large")
def cadastrar_nota_manutencao():
    # Verifique se os dados do projeto foram carregados em st.session_state
    if 'projeto_info' not in st.session_state:
        st.warning("Selecione um projeto na tela inicial.")
        return

    # Recupera o ID do projeto e dados de notas do session_state
    projeto_info = st.session_state['projeto_info']
    selected_gid = projeto_info['GID']
    project_data = st.session_state.get("project_data", {})

    # Usar dados de notas já carregados em `st.session_state['notas_data']`
    df_notas = st.session_state['project_data']['notas_de_manutencao_geral']
    
    # Carregar o próximo ID de nota
    novo_id = 1 if df_notas.empty else df_notas['ID'].max() + 1

    # Recuperar dados do projeto já carregados em `home`
    project_data = st.session_state.get("project_data", {})

    with st.form(key="new_nota_form", clear_on_submit=True, enter_to_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            # Campos e inputs do formulário
            cd_projeto = selected_gid
            var_Novo_GID = uuid.uuid4()
            cd_GID = str(var_Novo_GID)
            tx_ID = st.text_input("ID", value=str(novo_id), disabled=True)
            dt_data = st.date_input("Data da Nota", value=pd.to_datetime('today').date())
            dt_hr_cadastro = pd.to_datetime('today').date()
            situacao_map = {'P': 'Pendente', 'A': 'Aprovado', 'R': 'Reprovado'}
            situacao_nota = st.selectbox("Situação da Nota", options=list(situacao_map.values()))
            fl_situacao_nota = {v: k for k, v in situacao_map.items()}[situacao_nota]
            tx_nota = st.text_input("Nota", "")

            tx_ordem = st.text_input("Ordem", "")
            tx_tag = st.text_input("Tag", "")
            tx_tag_linha = st.text_input("Tag da Linha", "")

        with col2:
            dt_hr_alteracao = pd.to_datetime('today').date()

            # Serviço (verificar se o DataFrame tem dados)
            if not project_data.get("servicos", pd.DataFrame()).empty:
                descricao_servico_selecionada = st.selectbox(
                    "Código do Serviço", options=list(project_data["servicos"]["TX_DESCRICAO"].values)
                )
                cd_servico = project_data["servicos"].loc[project_data["servicos"]["TX_DESCRICAO"] == descricao_servico_selecionada, 'GID'].values[0]
            else:
                descricao_servico_selecionada = st.selectbox("Código do Serviço", options=['Nenhum serviço disponível'])
                cd_servico = None

            tx_descricao_servico = st.text_area("Descrição do Serviço", "", height=150)

            # Motivo da Situação
            if not project_data.get("situacao_motivo", pd.DataFrame()).empty:
                motivo_situacao_selecionado = st.selectbox(
                    "Motivo da Situação", options=list(project_data["situacao_motivo"]["TX_DESCRICAO"].values)
                )
                cd_situacao_motivo = project_data["situacao_motivo"].loc[project_data["situacao_motivo"]["TX_DESCRICAO"] == motivo_situacao_selecionado, 'GID'].values[0]
            else:
                motivo_situacao_selecionado = st.selectbox("Motivo da Situação", options=['Nenhum motivo disponível'])
                cd_situacao_motivo = None

        st.header("Solicitante e Responsável")
        col1, col2 = st.columns(2)
        with col1:
            # Setor Solicitante
            if not project_data.get("setor_solicitante", pd.DataFrame()).empty:
                setor_solicitante_selecionado = st.selectbox(
                    "Setor Solicitante", options=list(project_data["setor_solicitante"]["TX_DESCRICAO"].values)
                )
                cd_setor_solicitante = project_data["setor_solicitante"].loc[
                    project_data["setor_solicitante"]["TX_DESCRICAO"] == setor_solicitante_selecionado, 'GID'].values[0]
            else:
                setor_solicitante_selecionado = st.selectbox("Setor Solicitante", options=['Nenhum setor disponível'])
                cd_setor_solicitante = None

            tx_nome_solicitante = st.text_input("Nome do Solicitante", "")

        with col2:
            # Setor Responsável
            if not project_data.get("setor_responsavel", pd.DataFrame()).empty:
                setor_responsavel_selecionado = st.selectbox(
                    "Setor Responsável", options=list(project_data["setor_responsavel"]["TX_DESCRICAO"].values)
                )
                cd_setor_responsavel = project_data["setor_responsavel"].loc[
                    project_data["setor_responsavel"]["TX_DESCRICAO"] == setor_responsavel_selecionado, 'GID'].values[0]
            else:
                setor_responsavel_selecionado = st.selectbox("Setor Responsável", options=['Nenhum setor disponível'])
                cd_setor_responsavel = None

        st.header("Detalhes Técnicos")
        col1, col2 = st.columns(2)
        with col1:
            # Família de Equipamentos
            if not project_data.get("familia_equipamentos", pd.DataFrame()).empty:
                familia_equipamentos_selecionada = st.selectbox(
                    "Família de Equipamentos", options=list(project_data["familia_equipamentos"]["TX_DESCRICAO"].values)
                )
                cd_familia_equipamentos = project_data["familia_equipamentos"].loc[
                    project_data["familia_equipamentos"]["TX_DESCRICAO"] == familia_equipamentos_selecionada, 'GID'].values[0]
            else:
                familia_equipamentos_selecionada = st.selectbox("Família de Equipamentos", options=['Nenhuma família disponível'])
                cd_familia_equipamentos = None

            # Planta
            if not project_data.get("familia_equipamentos", pd.DataFrame()).empty:
                planta_selecionada = st.selectbox(
                    "Código da Planta", options=list(project_data["plantas"]["TX_DESCRICAO"].values)
                )
                cd_planta = project_data["plantas"].loc[
                    project_data["plantas"]["TX_DESCRICAO"] == planta_selecionada, 'GID'].values[0]
            else:
                planta_selecionada = st.selectbox("Código da Planta", options=['Nenhuma planta disponível'])
                cd_planta = None

            # Especialidade
            if not project_data.get("especialidades", pd.DataFrame()).empty:
                especialidade_selecionada = st.selectbox(
                    "Código da Especialidade", options=list(project_data["especialidades"]["TX_DESCRICAO"].values)
                )
                cd_especialidade = project_data["especialidades"].loc[
                    project_data["especialidades"]["TX_DESCRICAO"] == especialidade_selecionada, 'GID'].values[0]
            else:
                especialidade_selecionada = st.selectbox("Código da Especialidade", options=['Nenhuma especialidade disponível'])
                cd_especialidade = None

            tx_rec_inspecao = st.text_input("Recomendação de Inspeção", "")

        with col2:
            # Área
            if not project_data.get("areas", pd.DataFrame()).empty:
                area_selecionada = st.selectbox(
                    "Código da Área", options=list(project_data["areas"]["TX_DESCRICAO"].values)
                )
                cd_area = project_data["areas"].loc[project_data["areas"]["TX_DESCRICAO"] == area_selecionada, 'GID'].values[0]
            else:
                area_selecionada = st.selectbox("Código da Área", options=['Nenhuma área disponível'])
                cd_area = None

            # Sistemas Operacionais
            if not project_data.get("sistemas_operacionais", pd.DataFrame()).empty:
                sistema_operacional_selecionado_1 = st.selectbox(
                    "Sistema Operacional 1", options=list(project_data["sistemas_operacionais"]["TX_DESCRICAO"].values)
                )
                cd_sistema_operacional_1 = project_data["sistemas_operacionais"].loc[
                    project_data["sistemas_operacionais"]["TX_DESCRICAO"] == sistema_operacional_selecionado_1, 'GID'].values[0]
            else:
                sistema_operacional_selecionado_1 = st.selectbox("Sistema Operacional 1", options=['Nenhum sistema disponível'])
                cd_sistema_operacional_1 = None

            if not project_data.get("sistemas_operacionais", pd.DataFrame()).empty:
                sistema_operacional_selecionado_2 = st.selectbox(
                    "Sistema Operacional 2", options=list(project_data["sistemas_operacionais"]["TX_DESCRICAO"].values)
                )
                cd_sistema_operacional_2 = project_data["sistemas_operacionais"].loc[
                    project_data["sistemas_operacionais"]["TX_DESCRICAO"] == sistema_operacional_selecionado_2, 'GID'].values[0]
            else:
                sistema_operacional_selecionado_2 = st.selectbox("Sistema Operacional 2", options=['Nenhum sistema disponível'])
                cd_sistema_operacional_2 = None

        st.header("Escopo e Situação")
        col1, col2 = st.columns(2)
        with col1:
            # Origem do Escopo
            if not project_data.get("escopo_origem", pd.DataFrame()).empty:
                escopo_origem_selecionado = st.selectbox(
                    "Origem do Escopo", options=list(project_data["escopo_origem"]["TX_DESCRICAO"].values)
                )
                cd_escopo_origem = project_data["escopo_origem"].loc[
                    project_data["escopo_origem"]["TX_DESCRICAO"] == escopo_origem_selecionado, 'GID'].values[0]
            else:
                escopo_origem_selecionado = st.selectbox("Origem do Escopo", options=['Nenhuma origem disponível'])
                cd_escopo_origem = None

            # Tipo de Escopo
            if not project_data.get("escopo_origem", pd.DataFrame()).empty:
                escopo_tipo_selecionado = st.selectbox(
                    "Tipo de Escopo", options=list(project_data["escopo_tipo"]["TX_DESCRICAO"].values)
                )
                cd_escopo_tipo = project_data["escopo_tipo"].loc[
                    project_data["escopo_tipo"]["TX_DESCRICAO"] == escopo_tipo_selecionado, 'GID'].values[0]
            else:
                escopo_tipo_selecionado = st.selectbox("Tipo de Escopo", options=['Nenhum tipo disponível'])
                cd_escopo_tipo = None

            tx_equipamento_mestre = st.text_input("Equipamento Mestre", "")

        with col2:
            fl_nmp = st.selectbox("Nota Manutenção Parada?", ["Sim", "Não"])
            fl_ase = st.selectbox("Tem Autorização de Serviço Extra?", ["Sim", "Não"])
            tx_ase = st.text_input("Autorização Serviço Extra", "")

        st.header("Executantes")
        col1, col2 = st.columns(2)
        with col1:
            # Executante 1
            if not project_data.get("executantes", pd.DataFrame()).empty:
                executante_1_selecionado = st.selectbox(
                    "Código do Executante 1", options=list(project_data["executantes"]["TX_DESCRICAO"].values)
                )
                cd_executante_1 = project_data["executantes"].loc[
                    project_data["executantes"]["TX_DESCRICAO"] == executante_1_selecionado, 'GID'].values[0]
            else:
                executante_1_selecionado = st.selectbox("Código do Executante 1", options=['Nenhum executante disponível'])
                cd_executante_1 = None

        with col2:
            # Executante 2
            if not project_data.get("executantes", pd.DataFrame()).empty:
                executante_2_selecionado = st.selectbox(
                    "Código do Executante 2", options=list(project_data["executantes"]["TX_DESCRICAO"].values)
                )
                cd_executante_2 = project_data["executantes"].loc[
                    project_data["executantes"]["TX_DESCRICAO"] == executante_2_selecionado, 'GID'].values[0]
            else:
                executante_2_selecionado = st.selectbox("Código do Executante 2", options=['Nenhum executante disponível'])
                cd_executante_2 = None

        st.header("Observações")
        dt_atualizacao = st.date_input("Data de Atualização", value=pd.to_datetime('today').date())
        tx_observacao = st.text_area("Observação Adicional", "", height=100)

        submit_button = st.form_submit_button(label="Cadastrar Nota")

    if submit_button:
        # Verificação se a nota já existe
        if tx_nota in df_notas['TX_NOTA'].values:
            st.error(f"A nota '{tx_nota}' já existe. Por favor, insira uma nova.")
        else:
            new_data = {
                "ID": tx_ID,
                "GID": str(cd_GID),
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
