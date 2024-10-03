import streamlit as st
from utils import get_distinct_values, update_data, read_data

@st.dialog("Cadastrar Nova Nota")
def edit_nota_manutencao():
    # Verifica se o projeto foi selecionado e se há informação do projeto no estado da sessão
    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        selected_gid = projeto_info['GID']
    else:
        st.warning("Selecione um projeto na tela inicial.")
        return

    # Carregar as notas associadas ao projeto
    notas = get_distinct_values(f"timecenter.TB_NOTA_MANUTENCAO WHERE GID_PROJETO = {selected_gid}", 'TX_NOTA')
    
    # Seção: Escolha da Nota
    st.subheader("Selecione a Nota, Ordem e Tag")
    col1, col2, col3 = st.columns(3)
    
    # Inicializar listas vazias para ordens e tags
    ordens = []
    tags = []
    nota_data = None  # Inicializar nota_data como None

    # Seleção da Nota
    with col1:
        tx_nota_selected = st.selectbox("Nota", notas)
    
    # Filtrar ordens com base na nota selecionada
    if tx_nota_selected:
        ordens = get_distinct_values(f"timecenter.TB_NOTA_MANUTENCAO WHERE TX_NOTA = '{tx_nota_selected}' AND GID_PROJETO = {selected_gid}", 'TX_ORDEM')
    
    # Seleção da Ordem
    with col2:
        tx_ordem_selected = st.selectbox("Ordem", ordens if ordens else ["Nenhuma ordem disponível"])
    
    # Filtrar tags com base na ordem selecionada
    if tx_ordem_selected and tx_ordem_selected != "Nenhuma ordem disponível":
        tags = get_distinct_values(f"timecenter.TB_NOTA_MANUTENCAO WHERE TX_NOTA = '{tx_nota_selected}' AND TX_ORDEM = '{tx_ordem_selected}' AND GID_PROJETO = {selected_gid}", 'TX_TAG')
    
    # Seleção da Tag
    with col3:
        tx_tag_selected = st.selectbox("Tag", tags if tags else ["Nenhuma tag disponível"])

    # Carregar os dados da tabela com base nas seleções
    if tx_tag_selected and tx_tag_selected != "Nenhuma tag disponível":
        filter_condition = f"TX_NOTA = '{tx_nota_selected}' AND TX_ORDEM = '{tx_ordem_selected}' AND TX_TAG = '{tx_tag_selected}' AND GID_PROJETO = {selected_gid}"
        nota_data = read_data('timecenter.TB_NOTA_MANUTENCAO', filter_condition)
    
    # Verificar se nota_data foi carregado corretamente
    if nota_data is not None and not nota_data.empty:
        st.write(f"Editando dados para Nota: {tx_nota_selected}, Ordem: {tx_ordem_selected}, Tag: {tx_tag_selected}")
        
        # Formulário para edição dos dados
        with st.form(key="edit_nota_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                cd_projeto = st.text_input("Código do Projeto", nota_data['CD_PROJETO'].iloc[0])
                tx_nota = st.text_input("Descrição da Nota", nota_data['TX_NOTA'].iloc[0])
                tx_ordem = st.text_input("Ordem", nota_data['TX_ORDEM'].iloc[0])
                tx_tag = st.text_input("Tag", nota_data['TX_TAG'].iloc[0])
                tx_tag_linha = st.text_input("Tag da Linha", nota_data['TX_TAG_LINHA'].iloc[0])
            with col2:
                cd_servico = st.text_input("Código do Serviço", nota_data['CD_SERVICO'].iloc[0])
                tx_descricao_servico = st.text_area("Descrição do Serviço", nota_data['TX_DESCRICAO_SERVICO'].iloc[0], height=150)

            # Seção 2: Solicitante e Responsável
            st.header("Solicitante e Responsável")
            col1, col2 = st.columns(2)
            with col1:
                cd_setor_solicitante = st.text_input("Código do Setor Solicitante", nota_data['CD_SETOR_SOLICITANTE'].iloc[0])
                tx_nome_solicitante = st.text_input("Nome do Solicitante", nota_data['TX_NOME_SOLICITANTE'].iloc[0])
            with col2:
                cd_setor_responsavel = st.text_input("Código do Setor Responsável", nota_data['CD_SETOR_RESPONSAVEL'].iloc[0])

            # Seção 3: Detalhes Técnicos
            st.header("Detalhes Técnicos")
            col1, col2 = st.columns(2)
            with col1:
                cd_familia_equipamentos = st.text_input("Família de Equipamentos", nota_data['CD_FAMILIA_EQUIPAMENTOS'].iloc[0])
                cd_planta = st.text_input("Código da Planta", nota_data['CD_PLANTA'].iloc[0])
                cd_area = st.text_input("Código da Área", nota_data['CD_AREA'].iloc[0])
                cd_especialidade = st.text_input("Código da Especialidade", nota_data['CD_ESPECIALIDADE'].iloc[0])
            with col2:
                cd_sistema_operacional_1 = st.text_input("Sistema Operacional 1", nota_data['CD_SISTEMA_OPERACIONAL_1'].iloc[0])
                cd_sistema_operacional_2 = st.text_input("Sistema Operacional 2", nota_data['CD_SISTEMA_OPERACIONAL_2'].iloc[0])
                tx_equipamento_mestre = st.text_input("Equipamento Mestre", nota_data['TX_EQUIPAMENTO_MESTRE'].iloc[0])

            # Seção 4: Escopo e Situação
            st.header("Escopo e Situação")
            col1, col2 = st.columns(2)
            with col1:
                cd_escopo_origem = st.text_input("Origem do Escopo", nota_data['CD_ESCOPO_ORIGEM'].iloc[0])
                cd_escopo_tipo = st.text_input("Tipo de Escopo", nota_data['CD_ESCOPO_TIPO'].iloc[0])
                cd_situacao_motivo = st.text_input("Motivo da Situação", nota_data['CD_SITUACAO_MOTIVO'].iloc[0])
                tx_rec_inspecao = st.text_input("Recomendação de Inspeção", nota_data['TX_REC_INSPECAO'].iloc[0])
            with col2:
                fl_nmp = st.selectbox("Tem Nota Manut. Parada?", ["Sim", "Não"], index=0 if nota_data['FL_NMP'].iloc[0] == 'Sim' else 1)
                fl_ase = st.selectbox("Tem Autorização de Serviço Extra?", ["Sim", "Não"], index=0 if nota_data['FL_ASE'].iloc[0] == 'Sim' else 1)
                tx_ase = st.text_input("Autorização Serviço Extra", nota_data['TX_ASE'].iloc[0])

            # Seção 5: Executantes
            st.header("Executantes")
            col1, col2 = st.columns(2)
            with col1:
                cd_executante_1 = st.text_input("Código do Executante 1", nota_data['CD_EXECUTANTE_1'].iloc[0])
            with col2:
                cd_executante_2 = st.text_input("Código do Executante 2", nota_data['CD_EXECUTANTE_2'].iloc[0])

            # Seção 6: Observações
            st.header("Observações")
            dt_atualizacao = st.date_input("Data de Atualização", nota_data['DT_ATUALIZACAO'].iloc[0])
            tx_observacao = st.text_area("Observação Adicional", nota_data['TX_OBSERVACAO'].iloc[0], height=100)
            
            # Botão de submissão
            submit_button = st.form_submit_button(label="Atualizar Nota")

        # Atualizar dados na tabela se o botão de envio for clicado
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

            # Chama a função de update passando o ID_NOTA correto
            update_data('timecenter.TB_NOTA_MANUTENCAO', 'ID_NOTA', nota_data['ID_NOTA_MANUTENCAO'].iloc[0], updated_data)
    else:
        st.warning("Nenhuma nota encontrada para as seleções atuais.")

# Função principal que chama a tela de editar nota
def main():
    edit_nota_manutencao()

if __name__ == "__main__":
    main()
