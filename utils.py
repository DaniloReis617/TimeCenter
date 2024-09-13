#TimeCenter/app/UTILS.PY É O QUE TEM MINHAS FUNÇÕES
import pyodbc
import os
import pandas as pd
from datetime import datetime
import time
import streamlit as st

@st.cache_resource
def get_db_connection():
    """Estabelece ou restabelece a conexão com o banco de dados utilizando Streamlit Secrets."""
    retries = 3
    for _ in range(retries):
        try:
            conn = pyodbc.connect(
                f"DRIVER={{{st.secrets['database']['driver']}}};"
                f"SERVER={st.secrets['database']['server']};"
                f"DATABASE={st.secrets['database']['database']};"
                f"UID={st.secrets['database']['username']};"
                f"PWD={st.secrets['database']['password']}",
                timeout=30  # Define um timeout para a tentativa de conexão
            )
            if conn:
                return conn
        except pyodbc.Error as e:
            st.error(f"Tentativa de reconexão falhou: {e}")
            time.sleep(2)  # Espera antes de tentar novamente
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

def get_projetos_por_usuario(conn, gid_usuario):
    """Retorna os projetos associados ao GID de um usuário."""
    query = "SELECT * FROM timecenter.TB_USUARIO_PROJETO WHERE CD_USUARIO = ?"
    
    try:
        return pd.read_sql(query, conn, params=[gid_usuario])
    except Exception as e:
        st.error(f"Erro ao obter projetos para o usuário {gid_usuario}: {e}")
        return pd.DataFrame()

def get_descricao_projetos(conn, cd_projetos_list):
    """Retorna as descrições dos projetos com base na lista de GIDs fornecidos."""
    query = f"""
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_PROJETO 
    WHERE GID IN ({','.join(['?'] * len(cd_projetos_list))})
    """
    
    try:
        return pd.read_sql(query, conn, params=cd_projetos_list)
    except Exception as e:
        st.error(f"Erro ao obter descrições dos projetos: {e}")
        return pd.DataFrame()

def get_all_projetos(conn):
    """Retorna todos os projetos ativos (FL_STATUS = 'A') da tabela timecenter.TB_PROJETO."""
    query = """
    SELECT ID, GID, TX_DESCRICAO, FL_STATUS, DT_INICIO, DT_TERMINO
    FROM timecenter.TB_PROJETO
    WHERE FL_STATUS = 'A'
    """
    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Erro ao obter os projetos ativos: {e}")
        return pd.DataFrame()
    
def delete_data(conn, table_name, id_column, id_value):
    """Deleta um registro existente em uma tabela."""
    query = f"DELETE FROM {table_name} WHERE {id_column} = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(query, [id_value])
        conn.commit()
    except Exception as e:
        st.error(f"Erro ao deletar registro da tabela {table_name}: {e}")

# Função principal para aplicar estilo customizado e criar o cabeçalho
def apply_custom_style_and_header(title):
    st.markdown("""
        <style>
        .main {
            background-color: white;  /* Cor de fundo padrão */
            color: black;  /* Texto em preto */
            font-family: Arial, sans-serif;
        }
        .stButton button {
            width: auto;
            padding: 5px 10px;
            background-color: #f44336;
            color: white;
            border: none;
            cursor: pointer;
            font-size: 14px;
            border-radius: 5px;
        }
        .stButton button:hover {
            background-color: #e57373;
        }
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background-color: white;
            border-bottom: 2px solid #f0f0f0;
            position: fixed;
            width: 100%;
            top: 0;
            left: 0;
            z-index: 1000;
        }
        .title-container {
            flex-grow: 1;
            text-align: left;
            padding-left: 240px; /* Ajuste para alinhar o título ao lado do sidebar */
        }
        .title-container h1 {
            font-size: 32px;
            font-weight: bold;
            color: black;
            font-family: Calibri, sans-serif;
            margin: 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Cabeçalho com título ao lado do sidebar
    st.markdown(f"""
        <div class="header-container">
            <div class="title-container">
                <h1>{title}</h1>
            </div>
            <div class="user-info">
                {get_user_info()}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Criar um espaçamento para o conteúdo abaixo, já que o cabeçalho é fixo
    st.markdown("<div style='margin-top: 1px;'></div>", unsafe_allow_html=True)

# Função para exibir o login, perfil do usuário e a hora atual
def get_user_info():
    if 'user_info' in st.session_state:
        user_login = st.session_state['user_info'].get('login', 'Usuário não identificado')
        user_perfil = st.session_state['user_info'].get('perfil', 'Perfil não identificado')
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return f"<div style='text-align: right;'>Usuário: {user_login} ({user_perfil})<br>Data e Hora: {current_time}</div>"
    return ""