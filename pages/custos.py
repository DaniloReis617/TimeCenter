import streamlit as st 
import os
import pandas as pd
import numpy as np
from utils import apply_custom_style_and_header, get_db_connection, get_vw_nota_manutencao_hh_data, read_data, create_data, update_data, get_projetos_por_usuario, get_descricao_projetos, get_all_projetos, delete_data

def custos_screen():
    apply_custom_style_and_header("Tela de Custos")

    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        st.write(f"Exibindo dados para o projeto {projeto_info['TX_DESCRICAO']}")
        
        # Aqui você usaria st.session_state['projeto_info'] para filtrar dados dessa tela
        # Exemplo de como usar as informações do projeto para filtrar dados
        st.write(f"Informações do projeto selecionado: {projeto_info}")
        
        # Supondo que você tenha um DataFrame `dados` que precisa ser filtrado
        # dados_filtrados = dados[dados['projeto_id'] == projeto_info['GID']]
        # st.write(dados_filtrados)
    else:
        st.error("Selecione um projeto na tela inicial.")

    # Criar as abas
    tab1, tab2, tab3 = st.tabs(["Prévia dos Custos", "Base Orçamentária", "Gestão do Desembolso"])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Conteúdo da aba Prévia dos Custos do Projeto")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Prévia dos Custos"
    
    # Conteúdo da aba 2
    with tab2:
        st.write("Conteúdo da aba Base Orçamentária do Projeto")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Base Orçamentária"
    
    # Conteúdo da aba 3
    with tab3:
        st.write("Conteúdo da aba Gestão do Desembolso do Projeto")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Gestão do Desembolso"
 
def app():
    custos_screen()