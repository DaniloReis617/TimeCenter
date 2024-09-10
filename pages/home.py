import streamlit as st
import pandas as pd
from utils import apply_custom_style_and_header, get_db_connection, get_all_projetos

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
    
    # Conexão com o banco de dados
    conn = get_db_connection()
    if conn is not None:
        # Obter todos os projetos ativos
        projetos_df = get_all_projetos(conn)
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
        st.error("Não foi possível conectar ao banco de dados para obter os projetos.")

def app():
    home_screen()
