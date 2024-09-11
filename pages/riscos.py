import streamlit as st
import os
import pandas as pd
import numpy as np
from utils import apply_custom_style_and_header, get_db_connection, get_vw_nota_manutencao_hh_data, read_data, create_data, update_data, get_projetos_por_usuario, get_descricao_projetos, get_all_projetos, delete_data

def riscos_screen():
    apply_custom_style_and_header("Tela de Riscos")

    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        st.write(f"Exibindo dados para o projeto {projeto_info['TX_DESCRICAO']}")
    else:
        st.error("Selecione um projeto na tela inicial.")

    # Criar as abas
    tab1 = st.tabs([
        "Mapeamento dos Riscos por Nota"
    ])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Conteúdo da aba Mapeamento dos Riscos por Nota")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Mapeamento dos Riscos por Nota

def app():
    riscos_screen()