import streamlit as st
from utils import apply_custom_style_and_header

def Cadastro_Auxiliar_screen():
    apply_custom_style_and_header("Cadastro Auxiliar")

    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        st.write(f"Exibindo dados para o projeto {projeto_info['TX_DESCRICAO']}")
    else:
        st.error("Selecione um projeto na tela inicial.")

    # Container maior que pega a tela inteira
    with st.container():
        # Criando duas colunas dentro do container
        col1, col2 = st.columns([1, 3])  # Coluna 1 menor e coluna 2 maior
        
        # Primeiro container dentro da primeira coluna para o rádio
        with col1:
            with st.container():
                st.subheader("Selecione a Opção")

                # Opções de cadastro
                cadastro_opcoes = [
                    "Despesa", 
                    "Sist. Operacional", 
                    "Situação Motivo", 
                    "Setor Solicitante", 
                    "Setor Responsável", 
                    "Serviço", 
                    "Recurso", 
                    "Planta", 
                    "Informativo", 
                    "Família Equipamentos", 
                    "Executante", 
                    "Especialidade", 
                    "Escopo Tipo", 
                    "Escopo Origem", 
                    "Área", 
                    "Apoio"
                ]
                
                # Botão de seleção de rádio para escolher a ação
                opcao_selecionada = st.radio("Cadastro Auxiliar:", cadastro_opcoes)

        # Segundo container na segunda coluna para mostrar o resultado
        with col2:
            with st.container():
                st.subheader("Resultado da Seleção")

                # Lógica de navegação com base na opção selecionada
                if opcao_selecionada == "Despesa":
                    st.write("Acessando tela de Cadastro de Despesa")
                elif opcao_selecionada == "Sist. Operacional":
                    st.write("Acessando tela de Cadastro de Sistema Operacional")
                elif opcao_selecionada == "Situação Motivo":
                    st.write("Acessando tela de Cadastro de Situação Motivo")
                elif opcao_selecionada == "Setor Solicitante":
                    st.write("Acessando tela de Cadastro de Setor Solicitante")
                elif opcao_selecionada == "Setor Responsável":
                    st.write("Acessando tela de Cadastro de Setor Responsável")
                elif opcao_selecionada == "Serviço":
                    st.write("Acessando tela de Cadastro de Serviço")
                elif opcao_selecionada == "Recurso":
                    st.write("Acessando tela de Cadastro de Recurso")
                elif opcao_selecionada == "Planta":
                    st.write("Acessando tela de Cadastro de Planta")
                elif opcao_selecionada == "Informativo":
                    st.write("Acessando tela de Cadastro de Informativo")
                elif opcao_selecionada == "Família Equipamentos":
                    st.write("Acessando tela de Cadastro de Família de Equipamentos")
                elif opcao_selecionada == "Executante":
                    st.write("Acessando tela de Cadastro de Executante")
                elif opcao_selecionada == "Especialidade":
                    st.write("Acessando tela de Cadastro de Especialidade")
                elif opcao_selecionada == "Escopo Tipo":
                    st.write("Acessando tela de Cadastro de Escopo Tipo")
                elif opcao_selecionada == "Escopo Origem":
                    st.write("Acessando tela de Cadastro de Escopo Origem")
                elif opcao_selecionada == "Área":
                    st.write("Acessando tela de Cadastro de Área")
                elif opcao_selecionada == "Apoio":
                    st.write("Acessando tela de Cadastro de Apoio")

# Função principal do aplicativo
def app():
    Cadastro_Auxiliar_screen()

if __name__ == "__main__":
    app()
