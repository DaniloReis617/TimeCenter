import streamlit as st
import pandas as pd

def cronogramas_screen():
    st.title("Tela de Cronogramas")

    if 'projeto_info' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        st.write(f"Exibindo dados para o projeto {projeto_info['TX_DESCRICAO']}")
    else:
        st.error("Selecione um projeto na tela inicial.")

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
        st.header("Atividades de Execução")
        atividades_execucao = [
            {"ID": 1, "Atividades": "RAQUETEAMENTO / DESRAQ. DE UNIÕES FLANGEADAS"},
            {"ID": 2, "Atividades": "FECHAM/TORQUE UNIÕES FLANGEADAS"},
            {"ID": 3, "Atividades": "ABERTURA / FECHAMENTO DE BOCA DE VISITA"},
            {"ID": 4, "Atividades": "BANDEJAMENTO"},
            {"ID": 5, "Atividades": "REMOÇÃO / INSTALAÇÃO DE VÁLVULAS FLANGEADAS"},
            {"ID": 6, "Atividades": "TROCADORES DE CALOR"},
            {"ID": 7, "Atividades": "PADRÃO ENSAIOS NÃO DESTRUTIVOS (END's)"},
            {"ID": 8, "Atividades": "SERVIÇO DE LIMPEZA COM HIDROJATO"}
        ]
        atividade_selecionada = st.selectbox("Selecione uma Atividade", [atividade['Atividades'] for atividade in atividades_execucao])
        st.write(f"Atividade Selecionada: {atividade_selecionada}")
        
        st.header("Etapas de Recursos")
        etapas_recursos = [
            {"Etapa": "Preparação de Superfície", "Tipo": "Ferramenta manual", "m2_dia": 6, "Pintores": 1, "Ajudante": None},
            {"Etapa": "Preparação de Superfície", "Tipo": "Ferramenta mecânica", "m2_dia": 10, "Pintores": 1, "Ajudante": None},
            {"Etapa": "Preparação de Superfície", "Tipo": "Jateamento abrasivo (cabine de jato)", "m2_dia": 30, "Pintores": 2, "Ajudante": 1},
            {"Etapa": "Preparação de Superfície", "Tipo": "Hidrojateamento (pistola)", "m2_dia": 20, "Pintores": 2, "Ajudante": 1},
            {"Etapa": "Preparação de Superfície", "Tipo": "Hidrojateamento (robô)", "m2_dia": 35, "Pintores": 2, "Ajudante": 1},
            {"Etapa": "Método de Aplicação", "Tipo": "Pistola convencional", "m2_dia": 75, "Pintores": 2, "Ajudante": 1},
            {"Etapa": "Método de Aplicação", "Tipo": "Pistola airless", "m2_dia": 160, "Pintores": 2, "Ajudante": 1},
            {"Etapa": "Método de Aplicação", "Tipo": "Rolo", "m2_dia": 30, "Pintores": 1, "Ajudante": None},
            {"Etapa": "Método de Aplicação", "Tipo": "Trincha (stripe coat)", "m2_dia": 20, "Pintores": 1, "Ajudante": None}
        ]
        etapa_selecionada = st.selectbox("Selecione uma Etapa de Recursos", [recurso['Etapa'] for recurso in etapas_recursos])
        st.write(f"Etapa Selecionada: {etapa_selecionada}")
        recurso_filtrado = [recurso for recurso in etapas_recursos if recurso['Etapa'] == etapa_selecionada]
        for recurso in recurso_filtrado:
            st.text(f"Tipo: {recurso['Tipo']}, m²/dia: {recurso['m2_dia']}, Pintores: {recurso['Pintores']}, Ajudante: {recurso['Ajudante']}")
        
        st.header("Descrição e Quantidades")
        descricao_quant = [
            {"Descricao": "Silicato de Cálcio", "Tipo": "Tubulação até 4\"", "Quant_ml": 18, "Qt_Rec_Is_Fu": 2},
            {"Descricao": "Silicato de Cálcio", "Tipo": "Tubulação de 5\" a 8\"", "Quant_ml": 15, "Qt_Rec_Is_Fu": 2},
            {"Descricao": "Silicato de Cálcio", "Tipo": "Tubulação de 10\" até 16\"", "Quant_ml": 12, "Qt_Rec_Is_Fu": 2},
            {"Descricao": "Manta de Fibra Cerâmica", "Tipo": "Tubulação até 4\"", "Quant_ml": 40, "Qt_Rec_Is_Fu": 2}
        ]
        descricao_selecionada = st.selectbox("Selecione uma Descrição", [item['Descricao'] for item in descricao_quant])
        descricao_filtrada = [item for item in descricao_quant if item['Descricao'] == descricao_selecionada]
        for item in descricao_filtrada:
            st.text(f"Tipo: {item['Tipo']}, Quantidade (ml): {item['Quant_ml']}, Qt_Rec_Is_Fu: {item['Qt_Rec_Is_Fu']}")

def app():
    cronogramas_screen()

if __name__ == "__main__":
    app()
