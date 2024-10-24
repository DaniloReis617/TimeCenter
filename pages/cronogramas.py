import streamlit as st
import os
import base64
from forms.formulario_pintura import show_servico_pintura_form  # Importando o formulário de pintura
from forms.formulario_exec_atividades_raqueteamento import show_exec_atividades_form  # Importando o formulário de execução de atividades
from forms.formulario_exec_atividades_torque import show_exec_atividades_torque_form 
from forms.formulario_exec_atividades_boca_visita import show_exec_atividades_boca_visita_form 
from forms.formulario_exec_atividades_Trocadores_De_Calor import show_exec_atividades_Trocadores_De_Calor_form 
from forms.formulario_exec_atividades_Remocao_Instalacao_Valvulas import show_exec_atividades_Remocao_Instalacao_Valvulas_form 
from forms.formulario_exec_atividades_Servico_Limpeza_Hidrojato import show_exec_atividades_Servico_Limpeza_Hidrojato_form 
from forms.formulario_exec_atividades_bandejamento import show_exec_atividades_bandejamento_form 


def cronogramas_screen():
    st.title("Tela de Cronogramas")

    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        st.write(f"Exibindo dados para o projeto {projeto_info['TX_DESCRICAO']}")
    else:
        st.error("Selecione um projeto na tela inicial.")

    # Controle para exibir o formulário de pintura
    if 'show_form' not in st.session_state:
        st.session_state['show_form'] = False

    # Controle para exibir o formulário de execução de atividades
    if 'show_form_execucao' not in st.session_state:
        st.session_state['show_form_execucao'] = False

    # Variável para controlar a atividade selecionada
    if 'selected_activity' not in st.session_state:
        st.session_state['selected_activity'] = None

    # Criar as abas
    tab1, tab2, tab3 = st.tabs([
        "Detalhamento das FT's", 
        "Auditoria dos Cronogramas",
        "Calculadora de Métricas"
    ])
    
    # Conteúdo da aba 1
    with tab1:
        st.write("Conteúdo da aba Detalhamento das FT's")
    
    # Conteúdo da aba 2
    with tab2:
        st.write("Conteúdo da aba Auditoria dos Cronogramas")
    
    # Conteúdo da aba 3 - Calculadora de Métricas
    with tab3:
        if not st.session_state['show_form'] and not st.session_state['show_form_execucao']:
            st.header("Calculadora de Métricas")

            # Pasta de imagens
            image_folder = 'assets'
            images = {
                "Serviço de Pintura": os.path.join(image_folder, "servico_pintura.jpg"),
                "Execução de Atividades": os.path.join(image_folder, "execucao_atividades.jpg"),
                "Serviço de Isolamento": os.path.join(image_folder, "servico_isolamento.jpeg"),
                "Serviço de Andaime": os.path.join(image_folder, "servico_andaime.jpg"),
                "Caldeiraria e Solda": os.path.join(image_folder, "servico_calderaria.jpg"),
                "Item em Destaque": os.path.join(image_folder, "item_destaque.jpeg")
            }

            # Tamanho fixo da altura das imagens usando CSS
            img_height = "200px"

            # Adicionar CSS para controlar a altura das imagens
            st.markdown(
                f"""
                <style>
                .image-container img {{
                    height: {img_height};
                    object-fit: cover;
                    width: 100%;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

            def display_image(image_path, alt_text):
                if os.path.exists(image_path):
                    st.markdown(f'<div class="image-container"><img src="data:image/jpeg;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" alt="{alt_text}"></div>', unsafe_allow_html=True)
                else:
                    st.error(f"Imagem não encontrada: {alt_text}")

            # Primeira linha de containers (4 colunas)
            with st.container():
                col1, col2, col3, col4 = st.columns(4)
                
                # Container 1 (Serviço de Pintura)
                with col1:
                    display_image(images["Serviço de Pintura"], "Serviço de Pintura")
                    if st.button("Serviço de Pintura", use_container_width=True, key='pintura_btn'):
                        st.session_state['show_form'] = True
                        st.rerun()  # Atualiza a interface imediatamente
                
                # Container 2 (Execução de Atividades)
                with col2:
                    display_image(images["Execução de Atividades"], "Execução de Atividades")
                    if st.button("Execução de Atividades", use_container_width=True, key='execucao_btn'):
                        st.session_state['show_form_execucao'] = True
                        st.rerun()  # Atualiza a interface imediatamente
                
                # Container 3 (Serviço de Isolamento)
                with col3:
                    display_image(images["Serviço de Isolamento"], "Serviço de Isolamento")
                    st.button("Serviço de Isolamento", use_container_width=True)
                
                # Container 4 (Serviço de Andaime)
                with col4:
                    display_image(images["Serviço de Andaime"], "Serviço de Andaime")
                    st.button("Serviço de Andaime", use_container_width=True)
            
            # Segunda linha de containers (4 colunas)
            with st.container():
                col5, col6, col7, col8 = st.columns(4)
                
                # Container 5 (Caldeiraria e Solda)
                with col5:
                    display_image(images["Caldeiraria e Solda"], "Caldeiraria e Solda")
                    st.button("Caldeiraria e Solda", use_container_width=True)
                
                # Container 6 (Item em Destaque)
                with col6:
                    display_image(images["Item em Destaque"], "Item em Destaque")
                    st.button("Item em Destaque", use_container_width=True)

                # Container vazio nas colunas 7 e 8 para manter o layout alinhado
                with col7:
                    st.empty()

                with col8:
                    st.empty()

        elif st.session_state['show_form']:
            show_servico_pintura_form()
        
        elif st.session_state['show_form_execucao']:

            # Container maior que pega a tela inteira
            with st.container():
                # Criando duas colunas dentro do container
                col1, col2 = st.columns([1, 3])  # Coluna 1 menor e coluna 2 maior
                
                # Primeiro container dentro da primeira coluna para o rádio
                with col1:
                    with st.container():
                        # Mostrar a galeria de atividades
                        st.subheader("Selecione uma Atividade para Execução")
                        atividades = [
                            "RAQUETEAMENTO / DESRAQ. DE UNIÕES FLANGEADAS",
                            "FECHAM/TORQUE UNIÕES FLANGEADAS",
                            "ABERTURA / FECHAMENTO DE BOCA DE VISITA",
                            "BANDEJAMENTO",
                            "REMOÇÃO / INSTALAÇÃO DE VÁLVULAS FLANGEADAS",
                            "TROCADORES DE CALOR",
                            "PADRÃO ENSAIOS NÃO DESTRUTIVOS (END's)",
                            "SERVIÇO DE LIMPEZA COM HIDROJATO"
                        ]
                        
                        # Substituindo os botões por um rádio
                        atividade_selecionada = st.radio("Selecione a atividade", atividades)

                        # Botão de reset
                        if st.button("Voltar"):
                            st.session_state['show_form_execucao'] = False
                            st.rerun()

                        # Segundo container na segunda coluna para mostrar o resultado
                with col2:
                    with st.container():
                        st.subheader("Resultado da Seleção")
                        # Lógica de navegação com base na opção selecionada
                        if atividade_selecionada == "RAQUETEAMENTO / DESRAQ. DE UNIÕES FLANGEADAS":
                            st.expander("Calculo de RAQUETEAMENTO / DESRAQ. DE UNIÕES FLANGEADAS")
                            show_exec_atividades_form()
                        elif atividade_selecionada == "FECHAM/TORQUE UNIÕES FLANGEADAS":
                            st.expander("Calculo de FECHAM/TORQUE UNIÕES FLANGEADAS")
                            show_exec_atividades_torque_form()
                        elif atividade_selecionada == "ABERTURA / FECHAMENTO DE BOCA DE VISITA":
                            st.expander("Calculo de ABERTURA / FECHAMENTO DE BOCA DE VISITA")
                            show_exec_atividades_boca_visita_form()
                        elif atividade_selecionada == "BANDEJAMENTO":
                            st.expander("Calculo de BANDEJAMENTO")
                            show_exec_atividades_bandejamento_form()
                        elif atividade_selecionada == "REMOÇÃO / INSTALAÇÃO DE VÁLVULAS FLANGEADAS":
                            st.expander("Calculo de REMOÇÃO / INSTALAÇÃO DE VÁLVULAS FLANGEADAS")
                            show_exec_atividades_Remocao_Instalacao_Valvulas_form()
                        elif atividade_selecionada == "TROCADORES DE CALOR":
                            st.expander("Calculo de TROCADORES DE CALOR")
                            show_exec_atividades_Trocadores_De_Calor_form()
                        elif atividade_selecionada == "PADRÃO ENSAIOS NÃO DESTRUTIVOS (END's)":
                            st.expander("Calculo de PADRÃO ENSAIOS NÃO DESTRUTIVOS (END's)")
                        elif atividade_selecionada == "SERVIÇO DE LIMPEZA COM HIDROJATO":
                            st.expander("Calculo de SERVIÇO DE LIMPEZA COM HIDROJATO")
                            show_exec_atividades_Servico_Limpeza_Hidrojato_form()


def app():
    cronogramas_screen()

if __name__ == "__main__":
    app()
