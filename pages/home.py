import streamlit as st
import pandas as pd
from utils import apply_custom_style_and_header, get_all_projetos, get_projetos_por_usuario

def home_screen():
    apply_custom_style_and_header("Tela Home")
    
    st.write("Esta é a tela inicial do seu aplicativo. Você pode navegar entre as diferentes seções usando o menu à esquerda.")
    st.markdown("""
        ## Instruções
        - Use a barra lateral para navegar entre as seções.
        - Cada seção oferece diferentes funcionalidades relacionadas ao gerenciamento de projetos.
        - Clique em uma seção no menu à esquerda para começar.
    """)
    st.info("Selecione uma seção no menu para começar a explorar o aplicativo.")
    
    # Obter detalhes do usuário logado
    user_details = st.session_state.get('user_details', None)
    
    if user_details:
        user_id = user_details['id']
        user_gid = user_details['gid']
        user_profile = user_details['perfil']
        
        if user_profile in ['Super Usuário', 'Administrador']:
            # Obter todos os projetos ativos
            projetos_df = get_all_projetos()
        else:
            # Obter projetos do usuário logado
            projetos_df = get_projetos_por_usuario(user_gid)
        
        if not projetos_df.empty:
            # Dropdown para selecionar um projeto
            projeto_selecionado = st.selectbox(
                "Selecione um projeto para filtrar as informações nas outras telas:",
                projetos_df['TX_DESCRICAO'].tolist(),
                key="projeto_selecionado"
            )
            # Encontrar o registro completo do projeto selecionado
            projeto_info = projetos_df.loc[projetos_df['TX_DESCRICAO'] == projeto_selecionado].iloc[0]
            # Armazenar as informações do projeto no estado da sessão
            st.session_state['projeto_info'] = projeto_info.to_dict()
        else:
            st.error("Não há projetos ativos disponíveis para seleção.")
    else:
        st.error("Usuário não logado ou detalhes do usuário não definidos.")

def app():
    home_screen()
