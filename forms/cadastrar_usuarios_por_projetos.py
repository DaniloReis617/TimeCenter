import streamlit as st
import uuid
from utils import create_data, get_all_projetos, get_usuarios_df

@st.dialog("Cadastrar")
def add_projeto_usuario():
    # Obter os dados dos usuários
    usuarios_df = get_usuarios_df()  # Função que obtém os dados dos usuários
    projetos_desc_df = get_all_projetos()  # Função que obtém todos os projetos

    if usuarios_df.empty:
        st.error("Não há usuários disponíveis para cadastro de projetos.")
        return
    if projetos_desc_df.empty:
        st.error("Não há projetos disponíveis.")
        return

    # Criar o formulário para selecionar usuário e projeto
    with st.form(key="form_cadastro_projeto"):
        st.header("Cadastrar Projeto para Usuário")

        # Gerar um novo GUID
        var_Novo_GID = uuid.uuid4()
        cd_GID = str(var_Novo_GID)

        # Selecionar o usuário para cadastro
        usuario_selecionado_cadastro = st.selectbox(
            "Selecione um usuário", 
            usuarios_df['TX_LOGIN'].tolist(), 
            key="cadastro_usuario_projeto"
        )
        usuario_info_cadastro = usuarios_df[usuarios_df['TX_LOGIN'] == usuario_selecionado_cadastro].iloc[0]

        # Selecionar o projeto pela descrição (TX_DESCRICAO)
        projeto_selecionado = st.selectbox(
            "Selecione um projeto", 
            projetos_desc_df['TX_DESCRICAO'], 
            key="cadastro_projeto_usuario"
        )
        cd_projeto = projetos_desc_df.loc[projetos_desc_df['TX_DESCRICAO'] == projeto_selecionado, 'GID'].iloc[0]

        # Botão de submissão
        submit_button = st.form_submit_button("Cadastrar Projeto para Usuário")

        if submit_button:

            novo_projeto_usuario = {
                "GID": cd_GID,
                "CD_PROJETO": cd_projeto,  # ID do projeto selecionado
                "CD_USUARIO": usuario_info_cadastro['GID'],  # ID do usuário selecionado
            }
            with st.spinner("Salvando informações, por favor aguarde..."):
                # Cadastrar o projeto para o usuário na tabela timecenter.TB_USUARIO_PROJETO
                create_data("timecenter.TB_USUARIO_PROJETO", novo_projeto_usuario)
                st.success(f"Projeto {projeto_selecionado} cadastrado com sucesso para o usuário {usuario_selecionado_cadastro}!")

# Função principal para chamar o formulário
def main():
    add_projeto_usuario()

if __name__ == "__main__":
    main()
