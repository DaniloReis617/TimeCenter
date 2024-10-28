import streamlit as st
import pandas as pd
from utils import apply_custom_style_and_header, get_all_projetos, get_projetos_por_usuario, get_descricao_projetos
from utils import (get_servicos_projeto, get_nota_informativo_projeto, get_nota_recurso_projeto,
                   get_nota_apoio_projeto, get_situacao_motivo_projeto, get_setor_solicitante_projeto,
                   get_setor_responsavel_projeto, get_familia_equipamentos_projeto, get_plantas_projeto,
                   get_especialidades_projeto, get_areas_projeto, get_sistemas_operacionais_projeto,
                   get_escopo_origem_projeto, get_escopo_tipo_projeto, get_executantes_projeto, 
                   get_vw_nota_manutencao_hh_data)

@st.cache_data
def load_project_data(selected_gid):
    """Carrega todos os dados relacionados ao projeto selecionado."""
    return {
        'servicos': get_servicos_projeto(selected_gid),
        'informativo': get_nota_informativo_projeto(selected_gid),
        'recurso': get_nota_recurso_projeto(selected_gid),
        'apoio': get_nota_apoio_projeto(selected_gid),
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

@st.cache_data
def load_tela_escopo_data(selected_gid):
    """Carrega os dados específicos da tela de escopo para o projeto selecionado."""
    df = get_vw_nota_manutencao_hh_data()

    if df is None or df.empty:
        return pd.DataFrame()  # Retorna um DataFrame vazio

    # Filtra os dados para o GID_PROJETO específico
    df = df[df['GID_PROJETO'] == selected_gid]
    return df

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
        user_gid = user_details['gid']
        user_profile = user_details['perfil']
        
        # Filtrar projetos de acordo com o perfil do usuário
        projetos_df = get_all_projetos() if user_profile in ['Super Usuário', 'Administrador'] else get_projetos_por_usuario(user_gid)
        
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
                    progress_bar.progress(50)  # Atualiza a barra para 50%

                    tela_escopo_data = load_tela_escopo_data(selected_gid)
                    progress_bar.progress(100)  # Atualiza a barra para 100%

                # Armazenar os dados no estado da sessão
                st.session_state['project_data'] = project_data
                st.session_state['tela_escopo_data'] = tela_escopo_data
                
                st.success("Dados do projeto carregados com sucesso!")
                
                # Exibir os nomes dos DataFrames carregados
                st.subheader("DataFrames carregados:")
                loaded_dataframes = list(project_data.keys()) + ['tela_escopo_data']
                st.write(", ".join(loaded_dataframes))  # Exibe os nomes dos DataFrames
                
        else:
            st.warning("Este usuário não possui projetos ativos.")
    else:
        st.error("Usuário não logado ou detalhes do usuário não definidos.")

def app():
    home_screen()
