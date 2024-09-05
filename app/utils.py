#TimeCenter/app/UTILS.PY É O QUE TEM MINHAS FUNÇÕES
import pyodbc
import pandas as pd
from datetime import datetime
import streamlit as st

@st.cache_resource
def get_db_connection():
    """Estabelece a conexão com o banco de dados utilizando Streamlit Secrets."""
    try:
        conn = pyodbc.connect(
            f"DRIVER={{{st.secrets['database']['driver']}}};"
            f"SERVER={st.secrets['database']['server']};"
            f"DATABASE={st.secrets['database']['database']};"
            f"UID={st.secrets['database']['username']};"
            f"PWD={st.secrets['database']['password']}"
        )
        return conn
    except pyodbc.Error as e:
        st.error(f"Erro na conexão com o banco de dados: {e}")
        return None

def get_tables_and_views(conn):
    """Obtém todas as tabelas e views do banco de dados com seus nomes completos."""
    query = """
    SELECT TABLE_SCHEMA, TABLE_NAME, 'TABLE' AS TYPE
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE = 'BASE TABLE'
    UNION ALL
    SELECT TABLE_SCHEMA, TABLE_NAME, 'VIEW' AS TYPE
    FROM INFORMATION_SCHEMA.VIEWS
    """
    try:
        tables_views_df = pd.read_sql(query, conn)
        tables_views_df['FULL_NAME'] = tables_views_df['TABLE_SCHEMA'] + '.' + tables_views_df['TABLE_NAME']
        return tables_views_df
    except Exception as e:
        st.error(f"Erro ao obter tabelas e views: {e}")
        return pd.DataFrame()

def get_columns(conn, table_name):
    """Obtém todas as colunas de uma tabela específica."""
    table_name_only = table_name.split('.')[-1]
    query = """
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = ?
    """
    try:
        return pd.read_sql(query, conn, params=(table_name_only,))['COLUMN_NAME'].tolist()
    except Exception as e:
        st.error(f"Erro ao obter colunas da tabela {table_name}: {e}")
        return []

def get_distinct_values(conn, table_name, column_name):
    """Obtém valores distintos de uma coluna específica."""
    query = f"SELECT DISTINCT {column_name} FROM {table_name}"
    try:
        return pd.read_sql(query, conn)[column_name].tolist()
    except Exception as e:
        st.error(f"Erro ao obter valores distintos para a coluna {column_name} na tabela {table_name}: {e}")
        return []

def read_data(conn, table_name, filter_condition=''):
    """Lê dados de uma tabela ou view com um filtro opcional."""
    query = f"SELECT * FROM {table_name}"
    if filter_condition:
        query += f" WHERE {filter_condition}"
    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Erro ao ler dados da tabela {table_name}: {e}")
        return pd.DataFrame()
    
def get_vw_nota_manutencao_hh_data(conn):
    """Lê a tabela VW_NOTA_MANUTENCAO_HH e retorna as colunas específicas."""
    query = """
        SELECT GID_PROJETO, ID_NOTA_MANUTENCAO, TX_NOTA, TX_ORDEM, TX_TAG, TX_FAMILIA_EQUIPAMENTOS, 
        TX_NOME_SOLICITANTE, TX_DESCRICAO_SERVICO, VL_HH_TOTAL, VL_CUSTO_TOTAL, 
        TX_ESCOPO_TIPO, TX_SITUACAO FROM Dbo.VW_NOTA_MANUTENCAO_HH
    """
    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Erro ao ler dados da tabela VW_NOTA_MANUTENCAO_HH: {e}")
        return pd.DataFrame()

def create_data(conn, table_name, new_data):
    """Insere um novo registro em uma tabela."""
    columns = ', '.join(new_data.keys())
    placeholders = ', '.join(['?'] * len(new_data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    try:
        cursor = conn.cursor()
        cursor.execute(query, list(new_data.values()))
        conn.commit()
    except Exception as e:
        st.error(f"Erro ao adicionar registro na tabela {table_name}: {e}")

def update_data(conn, table_name, id_column, id_value, updated_data):
    """Atualiza um registro existente em uma tabela."""
    set_clause = ', '.join([f"{col} = ?" for col in updated_data.keys()])
    query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(query, list(updated_data.values()) + [id_value])
        conn.commit()
    except Exception as e:
        st.error(f"Erro ao atualizar registro na tabela {table_name}: {e}")

def delete_data(conn, table_name, id_column, id_value):
    """Deleta um registro existente em uma tabela."""
    query = f"DELETE FROM {table_name} WHERE {id_column} = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(query, [id_value])
        conn.commit()
    except Exception as e:
        st.error(f"Erro ao deletar registro da tabela {table_name}: {e}")

def validate_login(conn, username):
    """Valida o login do usuário e retorna os detalhes do usuário se válido."""
    query = """
    SELECT TX_LOGIN, GID, ID, FL_STATUS, NR_NIVEL 
    FROM timecenter.TB_USUARIO 
    WHERE TX_LOGIN = ?
    """
    try:
        df = pd.read_sql(query, conn, params=(username,))
        if not df.empty:
            # Traduzir NR_NIVEL para o nome do perfil
            nivel_mapping = {1: "Visualizador", 2: "Gestor", 4: "Administrador", 8: "Super Usuário"}
            perfil = nivel_mapping.get(df['NR_NIVEL'].iloc[0], "Perfil Desconhecido")

            user_details = {
                'login': df['TX_LOGIN'].iloc[0],
                'gid': df['GID'].iloc[0],
                'id': df['ID'].iloc[0],
                'status': df['FL_STATUS'].iloc[0],
                'perfil': perfil  # Usando o nome do perfil traduzido
            }
            return True, user_details  # Retorna um bool e um dicionário com detalhes do usuário
        else:
            return False, None  # Se falhar, retorna False e None
    except Exception as e:
        st.error(f"Erro na validação de login para o usuário {username}: {e}")
        return False, None

def apply_custom_style_and_header(title):
    # Adiciona estilo personalizado
    st.markdown("""
        <style>
        .main {
            background-color: white;  /* Cor de fundo padrão */
            color: black;  /* Texto em preto */
            font-family: Arial, sans-serif;
        }
        .stButton button {
            width: 100%;
            padding: 10px;
            background-color: white;
            color: black;
            border: none;
            cursor: pointer;
            font-size: 16px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .stButton button:hover {
            background-color: #e0e0e0;
        }
        .left-aligned-title {
            text-align: left;
            font-size: 32px;  /* Aumenta o tamanho da fonte */
            font-weight: bold;
            color: black;  /* Texto em preto */
            font-family: Calibri, sans-serif;  /* Fonte Calibri */
        }
        .centered-time {
            text-align: right;
            font-size: 18px;
            color: black;  /* Hora em preto */
        }
        </style>
    """, unsafe_allow_html=True)

    # Cabeçalho da tela
    col1, col2, col3 = st.columns([5, 3.5, 1.5])

    with col1:
        st.markdown(f"<h1 class='left-aligned-title'>{title}</h1>", unsafe_allow_html=True)
    
    with col2:
        if 'user_info' in st.session_state:
            user_login = st.session_state['user_info'].get('login', 'Usuário não identificado')
            user_perfil = st.session_state['user_info'].get('perfil', 'Perfil não identificado')
            # Concatenar o login com o perfil do usuário, separados por um espaço
            st.markdown(f"<h4 class='centered-time'>Usuário: {user_login} ({user_perfil})</h4>", unsafe_allow_html=True)
    with col3:    
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        st.markdown(f"<h4 class='centered-time'>{current_time}</h4>", unsafe_allow_html=True)