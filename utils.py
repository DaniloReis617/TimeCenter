# utils.py
import pyodbc
import os
import pandas as pd
import numpy as np
from datetime import datetime
import time
import streamlit as st

def get_db_connection():
    """Estabelece uma nova conexão com o banco de dados utilizando Streamlit Secrets."""
    try:
        conn = pyodbc.connect(
            f"DRIVER={{{st.secrets['database']['driver']}}};"
            f"SERVER={st.secrets['database']['server']};"
            f"DATABASE={st.secrets['database']['database']};"
            f"UID={st.secrets['database']['username']};"
            f"PWD={st.secrets['database']['password']}",
            timeout=30  # Define um timeout para a tentativa de conexão
        )
        return conn
    except pyodbc.Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {str(e)}")
        return None

def execute_read_query(query, params=None):
    """Executa uma consulta SELECT com tratamento de reconexão."""
    retries = 3
    for attempt in range(retries):
        try:
            with get_db_connection() as conn:
                if conn is None:
                    raise Exception("Conexão com o banco de dados não estabelecida.")
                df = pd.read_sql(query, conn, params=params)
                return df
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            else:
                st.error("Ocorreu um erro ao executar a consulta ao banco de dados.")
                return pd.DataFrame()

def execute_write_query(query, params=None):
    """Executa uma consulta de escrita (INSERT, UPDATE, DELETE) com tratamento de reconexão."""
    retries = 3
    for attempt in range(retries):
        try:
            with get_db_connection() as conn:
                if conn is None:
                    raise Exception("Conexão com o banco de dados não estabelecida.")
                with conn.cursor() as cursor:
                    cursor.execute(query, params or [])
                    conn.commit()
                return True
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            else:
                st.error(f"Ocorreu um erro ao executar a operação no banco de dados: {str(e)}")
                return False

def validate_login(username):
    """Valida o login do usuário e retorna os detalhes do usuário se válido."""
    query = """
    SELECT TX_LOGIN, GID, ID, FL_STATUS, NR_NIVEL 
    FROM timecenter.TB_USUARIO 
    WHERE TX_LOGIN = ?
    """
    user_df = execute_read_query(query, params=(username,))
    if not user_df.empty:
        # Traduzir NR_NIVEL para o nome do perfil
        nivel_mapping = {1: "Visualizador", 2: "Gestor", 4: "Administrador", 8: "Super Usuário"}
        perfil = nivel_mapping.get(user_df['NR_NIVEL'].iloc[0], "Perfil Desconhecido")

        user_details = {
            'login': user_df['TX_LOGIN'].iloc[0],
            'gid': user_df['GID'].iloc[0],
            'id': user_df['ID'].iloc[0],
            'status': user_df['FL_STATUS'].iloc[0],
            'perfil': perfil  # Usando o nome do perfil traduzido
        }
        st.session_state['user_details'] = user_details  # Armazenar os detalhes no estado da sessão
        return True, user_details  # Retorna um bool e um dicionário com detalhes do usuário
    else:
        return False, None  # Se falhar, retorna False e None

def get_tables_and_views():
    """Obtém todas as tabelas e views do banco de dados com seus nomes completos."""
    query = """
    SELECT TABLE_SCHEMA, TABLE_NAME, 'TABLE' AS TYPE
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE = 'BASE TABLE'
    UNION ALL
    SELECT TABLE_SCHEMA, TABLE_NAME, 'VIEW' AS TYPE
    FROM INFORMATION_SCHEMA.VIEWS
    """
    tables_views_df = execute_read_query(query)
    if not tables_views_df.empty:
        tables_views_df['FULL_NAME'] = tables_views_df['TABLE_SCHEMA'] + '.' + tables_views_df['TABLE_NAME']
    return tables_views_df

def get_columns(table_name):
    """Obtém todas as colunas de uma tabela específica."""
    table_name_only = table_name.split('.')[-1]
    query = """
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = ?
    """
    columns_df = execute_read_query(query, params=(table_name_only,))
    if not columns_df.empty:
        return columns_df['COLUMN_NAME'].tolist()
    else:
        return []

def get_distinct_values(table_name, column_name):
    """Obtém valores distintos de uma coluna específica."""
    query = f"SELECT DISTINCT {column_name} FROM {table_name}"
    distinct_df = execute_read_query(query)
    if not distinct_df.empty:
        return distinct_df[column_name].tolist()
    else:
        return []

def read_data(table_name, filter_condition=''):
    """Lê dados de uma tabela ou view com um filtro opcional."""
    query = f"SELECT * FROM {table_name}"
    if filter_condition:
        query += f" WHERE {filter_condition}"
    data_df = execute_read_query(query)
    return data_df

def get_vw_nota_manutencao_hh_data(projeto_gid):
    """Lê a tabela VW_NOTA_MANUTENCAO_HH e retorna todas colunas."""
    query = """
    SELECT * 
    FROM Dbo.VW_NOTA_MANUTENCAO_HH
    WHERE GID_PROJETO = ?
    ORDER BY ID_NOTA_MANUTENCAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_nota_manutencao_geral(projeto_gid):
    query = """
    SELECT * 
    FROM timecenter.TB_NOTA_MANUTENCAO
    WHERE CD_PROJETO = ?
    ORDER BY ID
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()
    
def get_vw_nota_manutencao(projeto_gid):
    query = """
    SELECT * 
    FROM timecenter.VW_NOTA_MANUTENCAO
    WHERE GID_PROJETO = ?
    ORDER BY ID_NOTA_MANUTENCAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()
    
def get_vw_nota_manutencao_apoio():
    query = """
    SELECT * 
    FROM timecenter.VW_NOTA_MANUTENCAO_APOIO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn)  # Remover `params=[projeto_gid]`
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_vw_nota_manutencao_informativo():
    query = """
    SELECT * 
    FROM timecenter.VW_NOTA_MANUTENCAO_INFORMATIVO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn)  # Remover `params=[projeto_gid]`
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_vw_nota_manutencao_material():
    query = """
    SELECT * 
    FROM timecenter.VW_NOTA_MANUTENCAO_MATERIAL
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn)  # Remover `params=[projeto_gid]`
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_vw_nota_manutencao_recurso():
    query = """
    SELECT * 
    FROM timecenter.VW_NOTA_MANUTENCAO_RECURSO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn)  # Remover `params=[projeto_gid]`
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()        
    
def get_nota_manutencao_declaracao_escopo(projeto_gid):
    query = """
    SELECT * 
    FROM timecenter.VW_NOTA_MANUTENCAO_DECLARACAO_ESCOPO
    WHERE ID_PROJETO = ?
    ORDER BY ID
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_nota_manutencao_custo_total(projeto_gid):
    query = """
    SELECT * 
    FROM timecenter.VW_NOTA_MANUTENCAO_TOTAL
    WHERE GID_PROJETO = ?
    ORDER BY DT_LANCAMENTO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()
    
def get_projeto_despesa(projeto_gid):
    query = """
    SELECT * 
    FROM timecenter.VW_PROJETO_DESPESA
    WHERE GID_PROJETO = ?
    ORDER BY ID
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()
    
def get_projeto_despesa_total(projeto_gid):
    query = """
    SELECT * 
    FROM timecenter.VW_PROJETO_DESPESA_TOTAL
    WHERE GID_PROJETO = ?
    ORDER BY DT_LANCAMENTO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_dados_projetos(projeto_gid):
    query = """
    SELECT * 
    FROM timecenter.TB_PROJETO
    WHERE GID = ?
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_projeto_total(projeto_gid):
    query = """
    SELECT * 
    FROM timecenter.VW_PROJETO_TOTAL
    WHERE GID_PROJETO = ?
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()
    
def get_projeto_total_data(projeto_gid):
    query = """
    SELECT * 
    FROM timecenter.VW_PROJETO_TOTAL_DATA
    WHERE GID_PROJETO = ?
    ORDER BY DT_LANCAMENTO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def create_data(table_name, new_data):
    """Insere um novo registro em uma tabela e traz mais informações em caso de erro."""
    try:
        # Monta a query de inserção
        columns = ', '.join(new_data.keys())
        placeholders = ', '.join(['?'] * len(new_data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        params = list(new_data.values())

        # Tenta executar a query
        success = execute_write_query(query, params)

        if success:
            st.success("Registro adicionado com sucesso!")
        else:
            st.error(f"Erro ao adicionar registro na tabela {table_name}.")

    except Exception as e:
        # Mensagem detalhada do erro, com os parâmetros e query
        error_message = (
            f"Erro ao adicionar registro na tabela {table_name}.\n"
            f"Query: {query}\n"
            f"Parâmetros: {params}\n"
            f"Detalhes do erro: {str(e)}"
        )
        st.error(error_message)

def convert_to_native_types(data):
    """Converte tipos numpy/pandas para tipos nativos de Python compatíveis com o banco."""
    for key, value in data.items():
        if isinstance(value, (np.int64, np.int32, int)):  # Converte para int
            data[key] = int(value)
        elif isinstance(value, (np.float64, np.float32, float)):  # Converte para float
            data[key] = float(value)
        elif isinstance(value, (pd.Timestamp, np.datetime64)):  # Converte datas para string
            data[key] = value.strftime('%Y-%m-%d %H:%M:%S') if isinstance(value, pd.Timestamp) else str(pd.to_datetime(value))
        elif pd.isna(value):  # Verifica valores nulos
            data[key] = None
        elif isinstance(value, (str, np.str_)):  # Converte strings
            data[key] = str(value)
        else:
            data[key] = value  # Mantém o valor original se já for nativo do Python
    return data

def update_data(table_name, id_column, id_value, updated_data):
    """Atualiza um registro existente em uma tabela e traz mais informações em caso de erro."""
    try:
        # Monta o SET clause para a query de atualização
        set_clause = ', '.join([f"{col} = ?" for col in updated_data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = ?"
        params = list(updated_data.values()) + [id_value]

        # Tenta executar a query
        success = execute_write_query(query, params)

        if success:
            st.success("Registro atualizado com sucesso!")
        else:
            st.error(f"Erro ao atualizar registro na tabela {table_name}.")

    except Exception as e:
        # Mensagem detalhada do erro, com os parâmetros e query
        error_message = (
            f"Erro ao atualizar registro na tabela {table_name}.\n"
            f"Query: {query}\n"
            f"Parâmetros: {params}\n"
            f"Detalhes do erro: {str(e)}"
        )
        st.error(error_message)


def delete_data(table_name, id_column, id_value):
    """Deleta um registro existente em uma tabela e traz mais informações em caso de erro."""
    try:
        # Monta a query de exclusão
        query = f"DELETE FROM {table_name} WHERE {id_column} = ?"
        params = [id_value]

        # Tenta executar a query
        success = execute_write_query(query, params)

        if success:
            st.success("Registro deletado com sucesso!")
        else:
            st.error(f"Erro ao deletar registro da tabela {table_name}.")

    except Exception as e:
        # Mensagem detalhada do erro, com os parâmetros e query
        error_message = (
            f"Erro ao deletar registro na tabela {table_name}.\n"
            f"Query: {query}\n"
            f"Parâmetros: {params}\n"
            f"Detalhes do erro: {str(e)}"
        )
        st.error(error_message)

def get_projetos_por_usuario(gid_usuario):
    """Retorna os projetos associados ao GID de um usuário."""
    query = "SELECT * FROM timecenter.TB_USUARIO_PROJETO WHERE CD_USUARIO = ?"
    projetos_df = execute_read_query(query, params=[gid_usuario])
    return projetos_df

def get_usuarios_df():
    query = """
    SELECT TX_LOGIN, GID, ID, FL_STATUS, NR_NIVEL 
    FROM timecenter.TB_USUARIO
    """
    usuarios_df = execute_read_query(query)
    return usuarios_df

def get_descricao_projetos(cd_projetos_list):
    """Retorna as descrições dos projetos com base na lista de GIDs fornecidos."""
    placeholders = ','.join(['?'] * len(cd_projetos_list))
    query = f"""
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_PROJETO 
    WHERE GID IN ({placeholders})
    """
    projetos_df = execute_read_query(query, params=cd_projetos_list)
    return projetos_df

def get_servicos_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_CADASTRO_SERVICO 
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar os serviços: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_informativo_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_CADASTRO_INFORMATIVO 
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar os serviços: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()
    
def get_recurso_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO, VL_VALOR_CUSTO 
    FROM timecenter.TB_CADASTRO_RECURSO 
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar os serviços: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()
    
def get_apoio_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO, VL_VALOR_CUSTO, VL_PERCENTUAL_CUSTO  
    FROM timecenter.TB_CADASTRO_APOIO 
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar os serviços: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()
    
def get_situacao_motivo_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_CADASTRO_SITUACAO_MOTIVO 
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar os motivos de situação: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_setor_solicitante_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_CADASTRO_SETOR_SOLICITANTE 
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar os setores solicitantes: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_setor_responsavel_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_CADASTRO_SETOR_RESPONSAVEL 
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar os setores responsáveis: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_familia_equipamentos_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_CADASTRO_FAMILIA_EQUIPAMENTOS 
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as famílias de equipamentos: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_plantas_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_CADASTRO_PLANTA 
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as plantas: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_especialidades_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_CADASTRO_ESPECIALIDADE 
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as especialidades: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_areas_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_CADASTRO_AREA 
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as áreas: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_sistemas_operacionais_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_CADASTRO_SISTEMA_OPERACIONAL 
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar os sistemas operacionais: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()
    
def get_escopo_origem_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_CADASTRO_ESCOPO_ORIGEM
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as origens de escopo: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_escopo_tipo_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_CADASTRO_ESCOPO_TIPO
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar os tipos de escopo: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()
    
def get_lancamento_despesas(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_CADASTRO_DESPESA
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar os tipos de escopo: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()

def get_executantes_projeto(projeto_gid):
    query = """
    SELECT GID, TX_DESCRICAO 
    FROM timecenter.TB_CADASTRO_EXECUTANTE
    WHERE CD_PROJETO = ?
    ORDER BY TX_DESCRICAO
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn, params=[projeto_gid])
            return df
        except Exception as e:
            st.error(f"Erro ao buscar os executantes: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()


def get_all_projetos():
    """Retorna todos os projetos ativos (FL_STATUS = 'A') da tabela timecenter.TB_PROJETO."""
    query = """
    SELECT ID, GID, TX_DESCRICAO, FL_STATUS, DT_INICIO, DT_TERMINO
    FROM timecenter.TB_PROJETO
    WHERE FL_STATUS = 'A'
    """
    projetos_df = execute_read_query(query)
    return projetos_df

def get_all_empresas():
    query = """
    SELECT * 
    FROM timecenter.TB_EMPRESAS
    """
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn)  # Remover `params=[projeto_gid]`
            return df
        except Exception as e:
            st.error(f"Erro ao buscar as Notas de manutenção: {e}")
            return pd.DataFrame()
    else:
        st.error("Não foi possível conectar ao banco de dados.")
        return pd.DataFrame()   

# Função para aplicar estilo customizado e criar o cabeçalho
def apply_custom_style_and_header(title):
    st.markdown("""
        <style>
        .main {
            background-color: white;  /* Cor de fundo padrão */
            color: black;  /* Texto em preto */
            font-family: Arial, sans-serif;
        }
        .stButton button {
            background-color: rgb(55, 100, 88);  /* Nova cor do botão */
            color: white;
            border: none;
            cursor: pointer;
            font-size: 14px;
            border-radius: 5px;
        }
        .stButton button:hover {
            background-color: rgb(45, 90, 78);  /* Cor mais escura ao passar o mouse */
            color: white;  /* Texto permanece branco */
        }
        .stButton button:active {
            background-color: rgb(45, 90, 78);  /* Manter a mesma cor quando clicado */
            color: white;  /* Texto permanece branco quando clicado */
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
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

# Função para exibir o login, perfil do usuário e a hora atual
def get_user_info():
    if 'user_details' in st.session_state:
        user_login = st.session_state['user_details'].get('login', 'Usuário não identificado')
        user_perfil = st.session_state['user_details'].get('perfil', 'Perfil não identificado')
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return f"<div style='text-align: right;'>Usuário: {user_login} ({user_perfil})<br>Data e Hora: {current_time}</div>"
    return ""