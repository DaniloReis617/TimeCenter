import streamlit as st
from utils import get_db_connection, validate_login  # Assumindo que estas funções estão definidas em app/utils.py

# Configuração inicial da página
st.set_page_config(page_title="Time Center", page_icon="./assets/icone_timenow_cor.png", layout="wide")

# Verificar se o usuário está logado e obter o perfil
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['user_profile'] = None

def load_page(page_name):
    """Carrega a página dinamicamente com base no nome da página."""
    module = __import__(f'pages.{page_name}', fromlist=['app'])
    return module.app

def logout():
    """Função para deslogar o usuário."""
    st.session_state['authenticated'] = False
    st.session_state['user_profile'] = None
    st.rerun()

# Determinar as páginas acessíveis com base no perfil do usuário
def get_accessible_pages(user_profile):
    if user_profile == "Super Usuário" or user_profile == "Administrador":
        return {
            "Home": "home",
            "Stakeholders": "stakeholders",
            "Escopo": "escopo",
            "Custos": "custos",
            "Recursos": "recursos",
            "Qualidade": "qualidade",
            "Cronogramas": "cronogramas",
            "Riscos": "riscos",
            "Aquisições": "aquisicoes",
            "Integração": "integracao",
            "Administração": "adm",
        }
    elif user_profile == "Gestor":
        return {
            "Home": "home",
            "Stakeholders": "stakeholders",
            "Escopo": "escopo",
            "Custos": "custos",
            "Recursos": "recursos",
            "Cronogramas": "cronogramas",
        }
    else:  # Visualizador
        return {
            "Home": "home",
            "Stakeholders": "stakeholders",
        }

# Navegação entre páginas
if not st.session_state['authenticated']:
    pages = {"Login": "login"}
else:
    pages = get_accessible_pages(st.session_state['user_info']['perfil'])

st.sidebar.title("Navegação")
st.logo("./assets/logo_timenow_horizontal_cor.png")
selection = st.sidebar.radio("Ir para", list(pages.keys()))
page_app = load_page(pages[selection])
page_app()

