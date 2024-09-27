import streamlit as st
import pandas as pd

# Dados da execução de atividades - Fechamento Torque
exec_atividades_torque = pd.DataFrame([
    {"ClassePressao": "150#", "Diametro": "Até 1.1/2\"", "Duracao": "0.5", "QtRec": 1, "Hh": "0.5"},
    {"ClassePressao": "150#", "Diametro": "2\" a 2.1/2\"", "Duracao": "0.8", "QtRec": 2, "Hh": "1.5"},
    {"ClassePressao": "150#", "Diametro": "3\"", "Duracao": "1.0", "QtRec": 2, "Hh": "2.0"},
    {"ClassePressao": "150#", "Diametro": "4\"", "Duracao": "1.0", "QtRec": 2, "Hh": "2.0"},
    {"ClassePressao": "150#", "Diametro": "6\"", "Duracao": "1.0", "QtRec": 2, "Hh": "2.0"}
])

# Função para exibir o formulário baseado nos dados
def show_exec_atividades_torque_form():
    st.subheader("Formulário: Execução de Atividades - Fechamento Torque")

    # Seleção de Classe de Pressão
    classe_pressao = st.selectbox("Classe de Pressão:", exec_atividades_torque['ClassePressao'].unique())

    # Filtrar as opções de Diâmetro com base na Classe de Pressão
    diametro_opcoes = exec_atividades_torque[exec_atividades_torque['ClassePressao'] == classe_pressao]['Diametro'].unique()
    diametro = st.selectbox("Diâmetro:", diametro_opcoes)

    # Filtrar os dados da tabela com base nas seleções
    atividade_selecionada = exec_atividades_torque[(exec_atividades_torque['ClassePressao'] == classe_pressao) & 
                                                   (exec_atividades_torque['Diametro'] == diametro)].iloc[0]
    
    # Exibir os resultados da consulta
    st.write(f"Duração (hs): {atividade_selecionada['Duracao']}")
    st.write(f"QTD: {atividade_selecionada['QtRec']}")
    st.write(f"HH: {atividade_selecionada['Hh']}")

    # Botões de ação
    if st.button("Calcular"):
        resultado = float(atividade_selecionada['QtRec']) * float(atividade_selecionada['Duracao'])
        st.success(f"Tempo Estimado: {round(resultado, 2)} horas")

    # Botão para resetar
    if st.button("Reset"):
        st.rerun()

    # Botão para voltar
    if st.button("Voltar",key="btn_torque"):
        st.session_state['show_form'] = False

# Função principal que chama o formulário
def main():
    show_exec_atividades_torque_form()

if __name__ == "__main__":
    main()
