import streamlit as st
import re
import pandas as pd
from utils import get_db_connection, validate_login
from pages import screens  # Módulo com as telas


st.set_page_config(
    page_title="Time Center", 
    page_icon="imagens/icone_timenow_cor.png",  
    layout="wide"
)

# Inicialização do estado de autenticação
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Inicialização do estado da tela
if 'current_screen' not in st.session_state:
    st.session_state['current_screen'] = 'home'

def main():
    if st.session_state['authenticated']:
        with st.sidebar:
            st.logo("imagens/logo_timenow_horizontal_cor.png")
            st.title("Navegação")

            # Obter o perfil do usuário autenticado
            user_perfil = st.session_state['user_info']['perfil']

            # Define as telas permitidas com base no perfil do usuário
            if user_perfil == "Super Usuário":
                permitted_screens = ('Home', 'Stakeholders', 'Escopo', 'Custos', 'Recursos', 
                                     'Qualidade', 'Cronogramas', 'Riscos', 'Aquisições', 'Integração', 'Administração')
            elif user_perfil == "Administrador":
                permitted_screens = ('Home', 'Stakeholders', 'Escopo', 'Custos', 'Recursos', 
                                     'Qualidade', 'Cronogramas', 'Riscos', 'Aquisições', 'Integração', 'Administração')
            elif user_perfil == "Gestor":
                permitted_screens = ('Home', 'Stakeholders', 'Escopo', 'Custos', 'Recursos', 
                                     'Qualidade', 'Cronogramas', 'Riscos', 'Aquisições', 'Integração')
            else:  # Visualizador
                permitted_screens = ('Home', 'Stakeholders', 'Escopo', 'Custos', 'Recursos', 
                                     'Qualidade', 'Cronogramas')

            st.session_state['current_screen'] = st.radio("Ir para:", permitted_screens)

            # Botão para deslogar
            if st.button("Sair"):
                logout()

        # Controle de navegação entre as telas
        if st.session_state['current_screen'] == 'Home':
            screens.home_screen()
        elif st.session_state['current_screen'] == 'Stakeholders':
            screens.stakeholders_screen()
        elif st.session_state['current_screen'] == 'Escopo':
            screens.escopo_screen()
        elif st.session_state['current_screen'] == 'Custos':
            screens.custos_screen()
        elif st.session_state['current_screen'] == 'Recursos':
            screens.recursos_screen()
        elif st.session_state['current_screen'] == 'Qualidade':
            screens.qualidade_screen()
        elif st.session_state['current_screen'] == 'Cronogramas':
            screens.cronogramas_screen()
        elif st.session_state['current_screen'] == 'Riscos':
            screens.riscos_screen()
        elif st.session_state['current_screen'] == 'Aquisições':
            screens.aquisicoes_screen()
        elif st.session_state['current_screen'] == 'Integração':
            screens.integracao_screen()
        elif st.session_state['current_screen'] == 'Administração' and user_perfil in ['Super Usuário', 'Administrador']:
            screens.adm_screen()
    else:
        login_screen()

def logout():
    """Função para deslogar o usuário."""
    st.session_state['authenticated'] = False
    st.session_state['user_info'] = None
    st.session_state['current_screen'] = 'login'
    st.rerun()  # Atualiza a página para redirecionar para a tela de login

def login_screen():
    with st.container():
        col1, col2, col3 = st.columns([3.5, 4, 3.5])
        with col2:
            col1, col2, col3 = st.columns([3, 4, 3])
            with col2:
                st.image("imagens/logo_timenow_vertical_cor.png", width=250)

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

if __name__ == "__main__":
    main()