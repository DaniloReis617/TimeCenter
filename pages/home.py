import streamlit as st
import pandas as pd
from utils import apply_custom_style_and_header, get_all_projetos, get_projetos_por_usuario, get_descricao_projetos
from utils import (get_servicos_projeto, get_informativo_projeto, get_recurso_projeto,
                   get_apoio_projeto, get_situacao_motivo_projeto, get_setor_solicitante_projeto,
                   get_setor_responsavel_projeto, get_familia_equipamentos_projeto, get_plantas_projeto,
                   get_especialidades_projeto, get_areas_projeto, get_sistemas_operacionais_projeto,
                   get_escopo_origem_projeto, get_escopo_tipo_projeto, get_executantes_projeto, 
                   get_vw_nota_manutencao_hh_data, get_nota_manutencao_geral, 
                   get_nota_manutencao_custo_total, get_projeto_despesa, 
                   get_projeto_despesa_total, get_projeto_total, 
                   get_projeto_total_data, get_nota_manutencao_declaracao_escopo, 
                   read_data, get_dados_projetos, get_vw_nota_manutencao,
                   get_vw_nota_manutencao_apoio, get_vw_nota_manutencao_informativo,
                   get_vw_nota_manutencao_material,get_vw_nota_manutencao_recurso)

def merge_with_gids(projeto_gid):
    # Obter o DataFrame principal com a coluna `GID_PROJETO`
    df_principal = get_vw_nota_manutencao(projeto_gid)
    
    # Verificar se o DataFrame principal está vazio
    if df_principal.empty:
        st.warning("Nenhuma nota foi encontrada no DataFrame principal.")
        return pd.DataFrame()  # Retornar um DataFrame vazio se não houver dados
    
    # Obter os demais DataFrames e fazer merge com `df_principal`
    df_apoio = get_vw_nota_manutencao_apoio().merge(
        df_principal[['GID_NOTA_MANUTENCAO', 'GID_PROJETO']], 
        on='GID_NOTA_MANUTENCAO', 
        how='left'
    )
    
    df_informativo = get_vw_nota_manutencao_informativo().merge(
        df_principal[['GID_NOTA_MANUTENCAO', 'GID_PROJETO']], 
        on='GID_NOTA_MANUTENCAO', 
        how='left'
    )
    
    df_recurso = get_vw_nota_manutencao_recurso().merge(
        df_principal[['GID_NOTA_MANUTENCAO', 'GID_PROJETO']], 
        on='GID_NOTA_MANUTENCAO', 
        how='left'
    )
    
    # Filtrar os DataFrames para manter apenas as linhas com o GID_PROJETO especificado
    df_apoio = df_apoio[df_apoio['GID_PROJETO'] == projeto_gid]
    df_informativo = df_informativo[df_informativo['GID_PROJETO'] == projeto_gid]
    df_recurso = df_recurso[df_recurso['GID_PROJETO'] == projeto_gid]    
    
    return df_apoio, df_informativo, df_recurso


# Função para carregar os dados com base no GID_PROJETO
@st.cache_data
def load_project_data(selected_gid):
    """Carrega todos os dados relacionados ao projeto selecionado."""
    # Carrega os dados principais
    project_data = {
        'visualizar_notas_de_manutencao': get_vw_nota_manutencao_hh_data(selected_gid),
        'notas_de_manutencao_geral': get_nota_manutencao_geral(selected_gid),
        'projeto_nota_custo_total': get_nota_manutencao_custo_total(selected_gid),
        'vw_notas_de_manutencao': get_vw_nota_manutencao(selected_gid),        
        'projeto_nota_declaracao_escopo': get_nota_manutencao_declaracao_escopo(selected_gid),
        'projeto_despesa': get_projeto_despesa(selected_gid),
        'projeto_despesa_total': get_projeto_despesa_total(selected_gid),
        'dados_projetos': get_dados_projetos(selected_gid),
        'projeto_total': get_projeto_total(selected_gid),
        'projeto_total_data': get_projeto_total_data(selected_gid),                               
        'servicos': get_servicos_projeto(selected_gid),
        'situacao_motivo': get_situacao_motivo_projeto(selected_gid),
        'setor_solicitante': get_setor_solicitante_projeto(selected_gid),
        'setor_responsavel': get_setor_responsavel_projeto(selected_gid),
        'familia_equipamentos': get_familia_equipamentos_projeto(selected_gid),
        'plantas': get_plantas_projeto(selected_gid),
        'especialidades': get_especialidades_projeto(selected_gid),
        'areas': get_areas_projeto(selected_gid),
        'sistemas_operacionais': get_sistemas_operacionais_projeto(selected_gid),
        'escopo_origem': get_escopo_origem_projeto(selected_gid),
        'escopo_tipo': get_escopo_tipo_projeto(selected_gid),
        'executantes': get_executantes_projeto(selected_gid)
    }
    
    # Realizar o merge para adicionar GID_PROJETO aos DataFrames
    df_apoio, df_informativo, df_recurso = merge_with_gids(selected_gid)
    project_data['apoio'] = df_apoio
    project_data['informativo'] = df_informativo
    project_data['recurso'] = df_recurso
    
    return project_data

def home_screen():
    apply_custom_style_and_header("Tela Home")
    
    st.markdown("""
        ## Instruções
        - No logo da empresa na part superior esquerda clique na seta para expandir a barra lateral para navegar entre as seções.
        - Cada seção oferece diferentes funcionalidades relacionadas ao gerenciamento de projetos.
        - Selecione o projeto do qual irá trabalhar e espere carregar os dados sobre ele e depois navegue para as outras telas do App.
    """)
    st.info("Selecione um projeto a caixa de seleção abaixo espere carregar os dados para começar a explorar o aplicativo.")    

    # Obter detalhes do usuário logado
    user_details = st.session_state.get('user_details', None)
    
    if user_details:
        user_login = user_details['login']
        user_id = user_details['id']
        user_gid = user_details['gid']
        user_profile = user_details['perfil']
        
        if user_profile in ['Super Usuário', 'Administrador']:
            # Obter todos os projetos ativos
            projetos_df = get_all_projetos()
        else:
            # Obter projetos do usuário logado
            projetos_df = get_projetos_por_usuario(user_gid)
            if projetos_df.empty:
                st.warning(f"Este usuário ({user_login}) não tem projetos.")
                return
            
            # Obter descrições dos projetos
            projetos_desc_df = get_descricao_projetos(projetos_df['CD_PROJETO'].unique().tolist())
            
            # Fazer o merge com base na coluna GID, mantendo os GIDs do projeto e usuário separados temporariamente
            projetos_df = projetos_df.merge(projetos_desc_df, left_on='CD_PROJETO', right_on='GID', suffixes=('_usuario', ''))

            # Remover a coluna GID do usuário (GID_usuario), mantendo apenas o GID do projeto
            if 'GID_usuario' in projetos_df.columns:
                projetos_df = projetos_df.drop(columns=['GID_usuario'])
        
        # Filtrar projetos de acordo com o perfil do usuário
        #projetos_df = get_all_projetos() if user_profile in ['Super Usuário', 'Administrador'] else get_projetos_por_usuario(user_gid)
        
        if not projetos_df.empty:
            # Inclui uma opção em branco para o selectbox
            projeto_selecionado = st.selectbox(
                "Selecione um projeto para carregar os dados:",
                [""] + projetos_df['TX_DESCRICAO'].tolist(),
                key="projeto_selecionado"
            )
            
            if projeto_selecionado != "":
                # Encontrar o registro completo do projeto selecionado
                projeto_info = projetos_df.loc[projetos_df['TX_DESCRICAO'] == projeto_selecionado].iloc[0]
                st.session_state['projeto_info'] = projeto_info.to_dict()
                
                selected_gid = projeto_info['GID']

                # Usar st.spinner e barra de progresso durante o carregamento dos dados
                with st.spinner("Carregando dados do projeto, por favor aguarde..."):
                    # Barra de progresso inicializada
                    progress_bar = st.progress(0)

                    # Carregar e armazenar todos os dados do projeto selecionado após a seleção
                    project_data = load_project_data(selected_gid)
                    progress_bar.progress(25)  # Atualiza a barra para 25%
                    # Armazenar os dados no estado da sessão
                    st.session_state['project_data'] = project_data
                    progress_bar.progress(50)  # Atualiza a barra para 50%                    
                    # Acessar as notas de manutenção diretamente
                    visualizar_notas_df = st.session_state['project_data']['visualizar_notas_de_manutencao']
                    progress_bar.progress(75)  # Atualiza a barra para 75%                    
                    notas_geral_df = st.session_state['project_data']['notas_de_manutencao_geral']
                    progress_bar.progress(100)  # Atualiza a barra para 100%

                st.success("Dados do projeto carregados com sucesso!")                
        else:
            st.warning("Este usuário não possui projetos ativos.")
    else:
        st.error("Usuário não logado ou detalhes do usuário não definidos.")

def app():
    home_screen()
