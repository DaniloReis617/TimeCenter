import streamlit as st
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

        # Selecionar o usuário para cadastro
        usuario_selecionado_cadastro = st.selectbox(
            "Selecione um usuário", 
            usuarios_df['TX_LOGIN'], 
            key="cadastro_usuario_projeto"
        )
        usuario_info_cadastro = usuarios_df[usuarios_df['TX_LOGIN'] == usuario_selecionado_cadastro].iloc[0]

        # Mostrar o ID do usuário selecionado (GID)
        st.text_input("ID do Usuário", value=usuario_info_cadastro['GID'], key="cadastro_cd_usuario", disabled=True)

        # Selecionar o projeto pela descrição (TX_DESCRICAO)
        projeto_selecionado = st.selectbox(
            "Selecione um projeto", 
            projetos_desc_df['TX_DESCRICAO'], 
            key="cadastro_projeto_usuario"
        )
        cd_projeto = projetos_desc_df.loc[projetos_desc_df['TX_DESCRICAO'] == projeto_selecionado, 'GID'].iloc[0]

        # Nível de Acesso e Status do Projeto
        nivel_acesso = st.selectbox("Nível de Acesso", ["Visualizador", "Gestor", "Administrador", "Super Usuário"], key="cadastro_nivel_acesso_usuario")
        status_projeto = st.selectbox("Status no Projeto", ["Ativo", "Inativo"], key="cadastro_status_projeto_usuario")
        
        # Botão de submissão
        submit_button = st.form_submit_button("Cadastrar Projeto para Usuário")

        if submit_button:
            # Mapear nível e status para os valores esperados na tabela
            nivel_reverso_mapping = {"Visualizador": 1, "Gestor": 2, "Administrador": 4, "Super Usuário": 8}
            status_reverso_mapping = {"Ativo": "A", "Inativo": "I"}

            novo_projeto_usuario = {
                "CD_PROJETO": cd_projeto,  # ID do projeto selecionado
                "CD_USUARIO": usuario_info_cadastro['GID'],  # ID do usuário selecionado
                "NR_NIVEL": nivel_reverso_mapping[nivel_acesso],
                "FL_STATUS": status_reverso_mapping[status_projeto]
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
