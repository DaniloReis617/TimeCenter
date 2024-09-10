import streamlit as st 
import os
import pandas as pd
import numpy as np
from utils import apply_custom_style_and_header, get_db_connection, get_vw_nota_manutencao_hh_data, read_data, create_data, update_data, get_projetos_por_usuario, get_descricao_projetos, get_all_projetos, delete_data

def recursos_screen():
    apply_custom_style_and_header("Tela de Recursos")

    st.write("Conteúdo da tela de Recursos")

    # Criar as abas
    tab1, tab2, tab3 = st.tabs(["Comparativo do HH", "Levantamento do HH", "Histograma Preliminar"])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Conteúdo da aba Comparativo do HH")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Comparativo do HH"
    
    # Conteúdo da aba 2
    with tab2:
        st.write("Conteúdo da aba Levantamento do HH")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Levantamento do HH"
    
    # Conteúdo da aba 3
    with tab3:
        st.write("Conteúdo da aba Histograma Preliminar")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Histograma Preliminar"

def app():
    recursos_screen()