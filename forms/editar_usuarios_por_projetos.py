import streamlit as st
from utils import update_data, get_usuarios_df, get_projetos_por_usuario, get_all_projetos

@st.dialog("Editar")
def editar_projeto_usuario():
    # Obter os dados dos usuários
    usuarios_df = get_usuarios_df()  # Função que obtém os dados dos usuários

    if usuarios_df.empty:
        st.error("Não há usuários disponíveis para edição de projetos.")
        return
    
    # Selecionar o usuário
    usuario_selecionado = st.selectbox(
        "Selecione um usuário", 
        usuarios_df['TX_LOGIN'], 
        key="edicao_usuario_projeto"
    )
    usuario_info = usuarios_df[usuarios_df['TX_LOGIN'] == usuario_selecionado].iloc[0]

    # Mostrar o ID do usuário selecionado
    st.text_input("ID do Usuário", value=usuario_info['GID'], key="edicao_cd_usuario", disabled=True)

    # Obter os projetos associados ao usuário
    projetos_usuario_df = get_projetos_por_usuario(usuario_info['GID'])

    if projetos_usuario_df.empty:
        st.error("Este usuário não tem projetos associados.")
        return

    # Obter a lista completa de projetos para associar as descrições
    projetos_desc_df = get_all_projetos()

    # Fazer o merge para associar as descrições dos projetos com os IDs dos projetos do usuário
    projetos_usuario_desc_df = projetos_usuario_df.merge(projetos_desc_df, left_on='CD_PROJETO', right_on='GID', how='left')

    # Verifique se o merge trouxe a coluna de descrição
    if 'TX_DESCRICAO' not in projetos_usuario_desc_df.columns:
        st.error("Não foi possível associar descrições aos projetos do usuário.")
        return

    with st.form(key="form_edicao_projeto"):

        # Selecionar o projeto a ser editado
        projeto_selecionado = st.selectbox(
            "Selecione um projeto para editar", 
            projetos_usuario_desc_df['TX_DESCRICAO'],  # Agora temos a descrição
            key="edicao_projeto_usuario"
        )
        projeto_info = projetos_usuario_desc_df[projetos_usuario_desc_df['TX_DESCRICAO'] == projeto_selecionado].iloc[0]

        # Verifique se 'NR_NIVEL' está disponível
        if 'NR_NIVEL' in projeto_info:
            nivel_acesso_atual = projeto_info['NR_NIVEL']
        else:
            #st.warning("A coluna 'NR_NIVEL' não está disponível. Usando um valor padrão.")
            nivel_acesso_atual = 1  # Definindo um valor padrão, pode ser ajustado conforme a lógica do seu sistema.

        status_atual = projeto_info['FL_STATUS'] if 'FL_STATUS' in projeto_info else 'A'

        # Mapeamentos de Nível e Status
        nivel_mapping = {1: "Visualizador", 2: "Gestor", 4: "Administrador", 8: "Super Usuário"}
        status_mapping = {"A": "Ativo", "I": "Inativo"}

        # Editar o nível de acesso e o status
        nivel_acesso = st.selectbox(
            "Nível de Acesso", 
            ["Visualizador", "Gestor", "Administrador", "Super Usuário"], 
            index=list(nivel_mapping.values()).index(nivel_mapping[nivel_acesso_atual]),
            key="edicao_nivel_acesso"
        )
        status_projeto = st.selectbox(
            "Status no Projeto", 
            ["Ativo", "Inativo"], 
            index=["Ativo", "Inativo"].index(status_mapping[status_atual]),
            key="edicao_status_projeto"
        )

        # Botão para salvar as alterações
        submit_button = st.form_submit_button("Salvar Alterações")

    if submit_button:
        # Mapear os valores para salvar
        nivel_reverso_mapping = {"Visualizador": 1, "Gestor": 2, "Administrador": 4, "Super Usuário": 8}
        status_reverso_mapping = {"Ativo": "A", "Inativo": "I"}

        projeto_atualizado = {
            "NR_NIVEL": nivel_reverso_mapping[nivel_acesso],
            "FL_STATUS": status_reverso_mapping[status_projeto]
        }
        with st.spinner("Salvando informações, por favor aguarde..."):
            # Função para atualizar o projeto do usuário na tabela timecenter.TB_USUARIO_PROJETO
            update_data("timecenter.TB_USUARIO_PROJETO", "CD_PROJETO", projeto_info['CD_PROJETO'], projeto_atualizado)
            st.success(f"Projeto {projeto_selecionado} atualizado com sucesso para o usuário {usuario_selecionado}!")

# Função principal para chamar a tela de edição
def main():
    editar_projeto_usuario()

if __name__ == "__main__":
    main()
