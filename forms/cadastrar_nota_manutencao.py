import streamlit as st
from utils import get_db_connection, create_data

def add_nota_manutencao():
    # Conexão com o banco de dados
    conn = get_db_connection()
    
    if conn:
        st.title("Adicionar Nota de Manutenção")
        
        # Criação do formulário para adicionar uma nova nota
        with st.form(key="nota_manutencao_form"):
            col1, col2, col3 = st.columns(3)

            with col1:
                cd_projeto = st.text_input("Código do Projeto", placeholder="Digite o código do projeto")
                tx_nota = st.text_input("Descrição da Nota", placeholder="Digite a descrição da nota")
                tx_ordem = st.text_input("Ordem", placeholder="Digite o número da ordem")
                tx_tag = st.text_input("Tag", placeholder="Digite o tag")
                tx_tag_linha = st.text_input("Tag da Linha", placeholder="Digite o tag da linha")
                cd_servico = st.text_input("Código do Serviço", placeholder="Digite o código do serviço")
                tx_descricao_servico = st.text_area("Descrição do Serviço", placeholder="Descreva o serviço")
                
            with col2:
                cd_situacao_motivo = st.text_input("Motivo da Situação", placeholder="Digite o motivo da situação")
                cd_setor_solicitante = st.text_input("Código do Setor Solicitante", placeholder="Digite o código do setor solicitante")
                tx_nome_solicitante = st.text_input("Nome do Solicitante", placeholder="Digite o nome do solicitante")
                cd_setor_responsavel = st.text_input("Código do Setor Responsável", placeholder="Digite o código do setor responsável")
                cd_familia_equipamentos = st.text_input("Família de Equipamentos", placeholder="Digite a família de equipamentos")
                cd_planta = st.text_input("Código da Planta", placeholder="Digite o código da planta")
                cd_especialidade = st.text_input("Código da Especialidade", placeholder="Digite o código da especialidade")
                
            with col3:
                tx_rec_inspecao = st.text_input("Recomendação de Inspeção", placeholder="Digite a recomendação")
                cd_area = st.text_input("Código da Área", placeholder="Digite o código da área")
                cd_sistema_operacional_1 = st.text_input("Sistema Operacional 1", placeholder="Digite o sistema operacional 1")
                cd_sistema_operacional_2 = st.text_input("Sistema Operacional 2", placeholder="Digite o sistema operacional 2")
                cd_escopo_origem = st.text_input("Origem do Escopo", placeholder="Digite a origem do escopo")
                tx_equipamento_mestre = st.text_input("Equipamento Mestre", placeholder="Digite o equipamento mestre")
                fl_nmp = st.selectbox("Tem Nota Manut. Parada?", ["Sim", "Não"])
                fl_ase = st.selectbox("Tem Autorização de Serviço Extra?", ["Sim", "Não"])
                tx_ase = st.text_input("Autorização Serviço Extra", placeholder="Digite a autorização")
                cd_escopo_tipo = st.text_input("Tipo de Escopo", placeholder="Digite o tipo do escopo")
                cd_executante_1 = st.text_input("Código do Executante 1", placeholder="Digite o código do executante 1")
                cd_executante_2 = st.text_input("Código do Executante 2", placeholder="Digite o código do executante 2")
                dt_atualizacao = st.date_input("Data de Atualização")
                tx_observacao = st.text_area("Observação Adicional", placeholder="Digite as observações")
            
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
                "CD_SITUACAO_MOTIVO": cd_situacao_motivo,
                "CD_SETOR_SOLICITANTE": cd_setor_solicitante,
                "TX_NOME_SOLICITANTE": tx_nome_solicitante,
                "CD_SETOR_RESPONSAVEL": cd_setor_responsavel,
                "CD_FAMILIA_EQUIPAMENTOS": cd_familia_equipamentos,
                "CD_PLANTA": cd_planta,
                "CD_ESPECIALIDADE": cd_especialidade,
                "TX_REC_INSPECAO": tx_rec_inspecao,
                "CD_AREA": cd_area,
                "CD_SISTEMA_OPERACIONAL_1": cd_sistema_operacional_1,
                "CD_SISTEMA_OPERACIONAL_2": cd_sistema_operacional_2,
                "CD_ESCOPO_ORIGEM": cd_escopo_origem,
                "TX_EQUIPAMENTO_MESTRE": tx_equipamento_mestre,
                "FL_NMP": fl_nmp,
                "FL_ASE": fl_ase,
                "TX_ASE": tx_ase,
                "CD_ESCOPO_TIPO": cd_escopo_tipo,
                "CD_EXECUTANTE_1": cd_executante_1,
                "CD_EXECUTANTE_2": cd_executante_2,
                "DT_ATUALIZACAO": dt_atualizacao,
                "TX_OBSERVACAO": tx_observacao
            }

            create_data(conn, "timecenter.TB_NOTA_MANUTENCAO", new_nota)
            st.success("Nota de Manutenção adicionada com sucesso!")
    else:
        st.error("Erro ao conectar ao banco de dados.")

# Função principal que chama a tela de adicionar nota
def main():
    add_nota_manutencao()

if __name__ == "__main__":
    main()
