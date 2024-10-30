import streamlit as st 
import os
import pandas as pd
import numpy as np
from utils import apply_custom_style_and_header, get_db_connection, get_vw_nota_manutencao_hh_data, read_data, create_data, update_data, get_projetos_por_usuario, get_descricao_projetos, get_all_projetos, delete_data

def dashboard_screen():
    apply_custom_style_and_header("Tela de Dashboard")

    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        st.write(f"Exibindo dados para o projeto {projeto_info['TX_DESCRICAO']}")
    else:
        st.error("Selecione um projeto na tela inicial.")

    # Criar as abas
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
        ["Projeto Geral",
        "Projeto Despesas",
        "Nota - Principal",
        "Nota - Apoios",
        "Nota - Informativos",
        "Nota - Recursos",
        "Nota - HH e Custos",
        "Nota - Top 5"
        ])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Projeto Geral")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Prévia dos dashboard"
    
    # Conteúdo da aba 2
    with tab2:
        st.write("Projeto Despesas")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Base Orçamentária"
    
    # Conteúdo da aba 3
    with tab3:
        st.write("Nota - Principal")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Gestão do Desembolso"

    # Conteúdo da aba 3
    with tab4:
        st.write("Nota - Apoios")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Gestão do Desembolso"

    # Conteúdo da aba 3
    with tab5:
        st.write("Nota - Informativos")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Gestão do Desembolso"

    # Conteúdo da aba 3
    with tab6:
        st.write("Nota - Recursos")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Gestão do Desembolso"

    # Conteúdo da aba 3
    with tab7:
        st.write("Nota - HH e Custos")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Gestão do Desembolso"

    # Conteúdo da aba 3
    with tab8:
        st.write("Nota - Top 5")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Gestão do Desembolso"
 
def app():
    dashboard_screen()