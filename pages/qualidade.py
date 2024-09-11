import streamlit as st
import os
import pandas as pd
import numpy as np
from utils import apply_custom_style_and_header, get_db_connection, get_vw_nota_manutencao_hh_data, read_data, create_data, update_data, get_projetos_por_usuario, get_descricao_projetos, get_all_projetos, delete_data

def qualidade_screen():
    apply_custom_style_and_header("Tela de Qualidade")

    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        st.write(f"Exibindo dados para o projeto {projeto_info['TX_DESCRICAO']}")
    else:
        st.error("Selecione um projeto na tela inicial.")

    # Criar as abas
    tab1, tab2, tab3, tab4 = st.tabs([
        "Plano de Inspeção", 
        "Plano de Ensaios", 
        "Mapa de Juntas", 
        "Plano de Teste"
    ])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Conteúdo da aba Importação do Plano de Inspeção")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Importação do Plano de Inspeção
    
    # Conteúdo da aba 2
    with tab2:
        st.write("Conteúdo da aba Importação do Plano de Ensaios")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Importação do Plano de Ensaios
    
    # Conteúdo da aba 3
    with tab3:
        st.write("Conteúdo da aba Importação do Mapa de Juntas")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Importação do Mapa de Juntas
    
    # Conteúdo da aba 4
    with tab4:
        st.write("Conteúdo da aba Importação do Plano de Teste")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Importação do Plano de Teste

def app():
    qualidade_screen()