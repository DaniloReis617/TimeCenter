import streamlit as st
import os
import re
import pandas as pd
from utils import get_db_connection, validate_login

def app():
    login()

def login():
    with st.container():
        col1, col2, col3 = st.columns([3.5, 4, 3.5])
        with col2:
            col1, col2, col3 = st.columns([3, 4, 3])
            with col2:
                st.image("./assets/logo_timenow_vertical_cor.png", width=200)

            st.write("Bem-vindo ao Time Center, por favor realize o seu login!")
            with st.form(key="form_login", clear_on_submit=True):
                username = st.text_input("Email", placeholder="Digite seu Email")
                submit_button = st.form_submit_button('Entrar')
                
                if submit_button:  
                    handle_login(username)

def handle_login(username):
    """Lida com o processo de login, incluindo validação e navegação."""
    if not re.match(r"[^@]+@[^@]+\.[^@]+", username):
        st.error("Por favor, insira um email válido.")
        return
    
    try:
        conn = get_db_connection()
        if conn:
            is_valid, user_details = validate_login(conn, username)
            if is_valid:
                st.session_state['authenticated'] = True
                st.session_state['user_info'] = user_details
                st.success(f"Login bem-sucedido! Bem-vindo, {st.session_state['user_info']['login']}!")
                st.rerun()  # Atualiza a página após o login bem-sucedido
            else:
                st.error("Usuário inválido. Tente novamente.")
        else:
            st.error("Não foi possível conectar ao banco de dados.")
    except Exception as e:
        st.error(f"Erro ao tentar autenticar: {e}")