#TimeCenter\pages\ADMIN.py É A TELA DE ADMINISTRAÇÃO DO APP ONDE SOMENTE OS USUÁRIOS COM A COLUNA NR_NIVEL DA TABELA 'timecenter.TB_USUARIO' É IGUAL A "SUPER USUÁRIO" PODEM ACESSAR
import streamlit as st
from utils import get_db_connection, get_tables_and_views, get_columns, get_distinct_values, read_data

def admin_screen():
    st.title("Tela de Administração")
    st.write("Visualize e edite todas as tabelas aqui.")

    conn = get_db_connection()
    if conn:
        tables_and_views = get_tables_and_views(conn)
        st.write("Tabelas e Views disponíveis:")
        st.dataframe(tables_and_views[['TABLE_SCHEMA', 'TABLE_NAME', 'TYPE']], height=200)

        selected_full_name = st.selectbox("Selecione uma tabela ou view", tables_and_views['FULL_NAME'])
        if selected_full_name:
            columns = get_columns(conn, selected_full_name)
            selected_column = st.selectbox(f"Selecione uma coluna em '{selected_full_name}'", columns)
            if selected_column:
                distinct_values = get_distinct_values(conn, selected_full_name, selected_column)
                selected_value = st.selectbox(f"Selecione um valor distinto em '{selected_column}'", [''] + distinct_values)
                filter_condition = f"{selected_column} = '{selected_value}'" if selected_value else ''
                if st.button('Mostrar Dados'):
                    data = read_data(conn, selected_full_name, filter_condition)
                    st.write(f"Dados de {selected_full_name}:")
                    st.dataframe(data, height=400)

    if st.button("Voltar para Home"):
        st.query_params.page = "home"

    if st.button("Ir para Cadastro de Notas de Manutenção"):
        st.query_params.page = "cadastro_de_notas_de_manutencao"

    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.query_params.page = "login"

# Verifique se o usuário está autenticado
if 'authenticated' in st.session_state and st.session_state['authenticated']:
    admin_screen()
else:
    st.warning("Você precisa fazer login.")
    st.query_params.page = "login"

def app():
    admin_screen()
