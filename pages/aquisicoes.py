import streamlit as st
import os
import pandas as pd
import numpy as np
from utils import apply_custom_style_and_header, get_db_connection, get_vw_nota_manutencao_hh_data, read_data, create_data, update_data, get_projetos_por_usuario, get_descricao_projetos, get_all_projetos, delete_data

def aquisicoes_screen():
    apply_custom_style_and_header("Tela de Aquisições")

    st.write("Conteúdo da tela de Aquisições")

    # Criar as abas
    tab1, tab2 = st.tabs([
        "Plano de Contratação", 
        "Lista de Materiais e Equipamentos"
    ])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Conteúdo da aba Plano de Contratação")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Plano de Contratação
    
    # Conteúdo da aba 2
    with tab2:
        st.write("Conteúdo da aba Lista de Materiais e Equipamentos")
        # Adicione aqui o conteúdo ou as funcionalidades específicas para Lista de Materiais e Equipamentos
