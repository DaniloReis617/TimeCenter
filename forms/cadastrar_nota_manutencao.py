import streamlit as st 
from utils import create_data

@st.dialog("Cadastrar Nova Nota",width="large")
def add_nota_manutencao():
    
    # Criação do formulário para adicionar uma nova nota
    with st.form(key="nota_manutencao_form"):
        # Seção 1: Identificação da Nota
        st.header("Identificação da Nota")
        col1, col2 = st.columns(2)

        with col1:
            cd_projeto = st.text_input("Código do Projeto", placeholder="Digite o código do projeto")
            tx_nota = st.text_input("Descrição da Nota", placeholder="Digite a descrição da nota")
            tx_ordem = st.text_input("Ordem", placeholder="Digite o número da ordem")
            tx_tag = st.text_input("Tag", placeholder="Digite o tag")
            tx_tag_linha = st.text_input("Tag da Linha", placeholder="Digite o tag da linha")
        with col2:
            cd_servico = st.text_input("Código do Serviço", placeholder="Digite o código do serviço")
            tx_descricao_servico = st.text_area("Descrição do Serviço", placeholder="Descreva o serviço", height=150)

        # Seção 2: Solicitante e Responsável
        st.header("Solicitante e Responsável")
        col1, col2 = st.columns(2)
        with col1:
            cd_setor_solicitante = st.text_input("Código do Setor Solicitante", placeholder="Digite o código do setor solicitante")
            tx_nome_solicitante = st.text_input("Nome do Solicitante", placeholder="Digite o nome do solicitante")
        with col2:
            cd_setor_responsavel = st.text_input("Código do Setor Responsável", placeholder="Digite o código do setor responsável")

        # Seção 3: Detalhes Técnicos
        st.header("Detalhes Técnicos")
        col1, col2 = st.columns(2)
        with col1:
            cd_familia_equipamentos = st.text_input("Família de Equipamentos", placeholder="Digite a família de equipamentos")
            cd_planta = st.text_input("Código da Planta", placeholder="Digite o código da planta")
            cd_area = st.text_input("Código da Área", placeholder="Digite o código da área")
            cd_especialidade = st.text_input("Código da Especialidade", placeholder="Digite o código da especialidade")
        with col2:
            cd_sistema_operacional_1 = st.text_input("Sistema Operacional 1", placeholder="Digite o sistema operacional 1")
            cd_sistema_operacional_2 = st.text_input("Sistema Operacional 2", placeholder="Digite o sistema operacional 2")
            tx_equipamento_mestre = st.text_input("Equipamento Mestre", placeholder="Digite o equipamento mestre")

        # Seção 4: Escopo e Situação
        st.header("Escopo e Situação")
        col1, col2 = st.columns(2)
        with col1:
            cd_escopo_origem = st.text_input("Origem do Escopo", placeholder="Digite a origem do escopo")
            cd_escopo_tipo = st.text_input("Tipo de Escopo", placeholder="Digite o tipo do escopo")
            cd_situacao_motivo = st.text_input("Motivo da Situação", placeholder="Digite o motivo da situação")
            tx_rec_inspecao = st.text_input("Recomendação de Inspeção", placeholder="Digite a recomendação")
        with col2:
            fl_nmp = st.selectbox("Tem Nota Manut. Parada?", ["Sim", "Não"])
            fl_ase = st.selectbox("Tem Autorização de Serviço Extra?", ["Sim", "Não"])
            tx_ase = st.text_input("Autorização Serviço Extra", placeholder="Digite a autorização")

        # Seção 5: Executantes
        st.header("Executantes")
        col1, col2 = st.columns(2)
        with col1:
            cd_executante_1 = st.text_input("Código do Executante 1", placeholder="Digite o código do executante 1")
        with col2:
            cd_executante_2 = st.text_input("Código do Executante 2", placeholder="Digite o código do executante 2")

        # Seção 6: Observações
        st.header("Observações")
        dt_atualizacao = st.date_input("Data de Atualização")
        tx_observacao = st.text_area("Observação Adicional", placeholder="Digite as observações", height=100)
        
        # Botão para submissão
        submit_button = st.form_submit_button(label="Adicionar Nota")
    
    # Inserir dados na tabela se o botão for clicado
    if submit_button:
        new_nota = {
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

        create_data("timecenter.TB_NOTA_MANUTENCAO", new_nota)
        # A função create_data já trata das mensagens de sucesso ou erro

# Função principal que chama a tela de adicionar nota
def main():
    add_nota_manutencao()

if __name__ == "__main__":
    main()
