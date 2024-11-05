import streamlit as st
import pandas as pd

# Dados da execução de atividades - Fechamento Torque
exec_atividades_torque = pd.DataFrame([
    {'ClassePressao': "150#", 'Diametro': "Até 1.1/2""", 'Duracao': "0.5", 'QtRec': "1", 'Hh': "0.5"},
    {'ClassePressao': "150#", 'Diametro': "2"" a 2.1/2""", 'Duracao': "0.8", 'QtRec': "2", 'Hh': "1.5"},
    {'ClassePressao': "150#", 'Diametro': "3""", 'Duracao': "1.0", 'QtRec': "2", 'Hh': "2.0"},
    {'ClassePressao': "150#", 'Diametro': "4""", 'Duracao': "1.0", 'QtRec': "2", 'Hh': "2.0"},
    {'ClassePressao': "150#", 'Diametro': "6""", 'Duracao': "1.0", 'QtRec': "2", 'Hh': "2.0"},
    {'ClassePressao': "150#", 'Diametro': "8""", 'Duracao': "1.2", 'QtRec': "2", 'Hh': "2.4"},
    {'ClassePressao': "150#", 'Diametro': "10""", 'Duracao': "1.5", 'QtRec': "2", 'Hh': "3.0"},
    {'ClassePressao': "150#", 'Diametro': "12"" a 14""", 'Duracao': "2.0", 'QtRec': "2", 'Hh': "4.0"},
    {'ClassePressao': "150#", 'Diametro': "16""", 'Duracao': "2.3", 'QtRec': "2", 'Hh': "4.5"},
    {'ClassePressao': "150#", 'Diametro': "18"" a 20""", 'Duracao': "2.5", 'QtRec': "2", 'Hh': "5.0"},
    {'ClassePressao': "150#", 'Diametro': "22""", 'Duracao': "2.5", 'QtRec': "2", 'Hh': "5.0"},
    {'ClassePressao': "150#", 'Diametro': "24"" a 26""", 'Duracao': "2.8", 'QtRec': "2", 'Hh': "5.6"},
    {'ClassePressao': "150#", 'Diametro': "30""", 'Duracao': "3.0", 'QtRec': "2", 'Hh': "6.0"},
    {'ClassePressao': "150#", 'Diametro': "36""", 'Duracao': "3.2", 'QtRec': "2", 'Hh': "6.4"},
    {'ClassePressao': "150#", 'Diametro': "42"" a 44""", 'Duracao': "3.5", 'QtRec': "2", 'Hh': "7.0"},
    {'ClassePressao': "150#", 'Diametro': "48""", 'Duracao': "4.0", 'QtRec': "2", 'Hh': "8.0"},
    {'ClassePressao': "150#", 'Diametro': "50"" a 54""", 'Duracao': "4.5", 'QtRec': "2", 'Hh': "9.0"},
    {'ClassePressao': "300#", 'Diametro': "Até 1.1/2""", 'Duracao': "0.5", 'QtRec': "1", 'Hh': "0.5"},
    {'ClassePressao': "300#", 'Diametro': "2"" a 2.1/2""", 'Duracao': "0.8", 'QtRec': "1", 'Hh': "0.8"},
    {'ClassePressao': "300#", 'Diametro': "3""", 'Duracao': "1.0", 'QtRec': "2", 'Hh': "2.0"},
    {'ClassePressao': "300#", 'Diametro': "4""", 'Duracao': "1.0", 'QtRec': "2", 'Hh': "2.0"},
    {'ClassePressao': "300#", 'Diametro': "6""", 'Duracao': "1.0", 'QtRec': "2", 'Hh': "2.0"},
    {'ClassePressao': "300#", 'Diametro': "8""", 'Duracao': "1.2", 'QtRec': "2", 'Hh': "2.4"},
    {'ClassePressao': "300#", 'Diametro': "10""", 'Duracao': "1.5", 'QtRec': "2", 'Hh': "3.0"},
    {'ClassePressao': "300#", 'Diametro': "12"" a 14""", 'Duracao': "2.0", 'QtRec': "2", 'Hh': "4.0"},
    {'ClassePressao': "300#", 'Diametro': "16""", 'Duracao': "2.3", 'QtRec': "2", 'Hh': "4.5"},
    {'ClassePressao': "300#", 'Diametro': "18"" a 20""", 'Duracao': "2.5", 'QtRec': "2", 'Hh': "5.0"},
    {'ClassePressao': "300#", 'Diametro': "22""", 'Duracao': "2.5", 'QtRec': "2", 'Hh': "5.0"},
    {'ClassePressao': "300#", 'Diametro': "24"" a 26""", 'Duracao': "2.8", 'QtRec': "2", 'Hh': "5.6"},
    {'ClassePressao': "300#", 'Diametro': "30""", 'Duracao': "3.0", 'QtRec': "2", 'Hh': "6.0"},
    {'ClassePressao': "300#", 'Diametro': "36""", 'Duracao': "3.2", 'QtRec': "2", 'Hh': "6.4"},
    {'ClassePressao': "300#", 'Diametro': "42"" a 44""", 'Duracao': "3.5", 'QtRec': "2", 'Hh': "7.0"},
    {'ClassePressao': "300#", 'Diametro': "48""", 'Duracao': "4.0", 'QtRec': "2", 'Hh': "8.0"},
    {'ClassePressao': "300#", 'Diametro': "50"" a 54""", 'Duracao': "4.5", 'QtRec': "2", 'Hh': "9.0"},
    {'ClassePressao': "600#", 'Diametro': "Até 1.1/2""", 'Duracao': "0.5", 'QtRec': "1", 'Hh': "0.5"},
    {'ClassePressao': "600#", 'Diametro': "2"" a 2.1/2""", 'Duracao': "0.8", 'QtRec': "1", 'Hh': "0.8"},
    {'ClassePressao': "600#", 'Diametro': "3""", 'Duracao': "1.0", 'QtRec': "2", 'Hh': "2.0"},
    {'ClassePressao': "600#", 'Diametro': "4""", 'Duracao': "1.2", 'QtRec': "2", 'Hh': "2.4"},
    {'ClassePressao': "600#", 'Diametro': "6""", 'Duracao': "1.5", 'QtRec': "2", 'Hh': "3.0"},
    {'ClassePressao': "600#", 'Diametro': "8""", 'Duracao': "1.5", 'QtRec': "2", 'Hh': "3.0"},
    {'ClassePressao': "600#", 'Diametro': "10""", 'Duracao': "1.8", 'QtRec': "2", 'Hh': "3.6"},
    {'ClassePressao': "600#", 'Diametro': "12"" a 14""", 'Duracao': "2.3", 'QtRec': "2", 'Hh': "4.5"},
    {'ClassePressao': "600#", 'Diametro': "16""", 'Duracao': "2.5", 'QtRec': "2", 'Hh': "5.0"},
    {'ClassePressao': "600#", 'Diametro': "18"" a 20""", 'Duracao': "2.8", 'QtRec': "2", 'Hh': "5.5"},
    {'ClassePressao': "600#", 'Diametro': "22""", 'Duracao': "3.0", 'QtRec': "2", 'Hh': "6.0"},
    {'ClassePressao': "600#", 'Diametro': "24"" a 26""", 'Duracao': "3.2", 'QtRec': "2", 'Hh': "6.4"},
    {'ClassePressao': "600#", 'Diametro': "30""", 'Duracao': "3.5", 'QtRec': "2", 'Hh': "7.0"},
    {'ClassePressao': "600#", 'Diametro': "36""", 'Duracao': "4.0", 'QtRec': "2", 'Hh': "8.0"},
    {'ClassePressao': "600#", 'Diametro': "42"" a 44""", 'Duracao': "4.5", 'QtRec': "2", 'Hh': "9.0"},
    {'ClassePressao': "600#", 'Diametro': "48""", 'Duracao': "4.5", 'QtRec': "2", 'Hh': "9.0"},
    {'ClassePressao': "600#", 'Diametro': "50"" a 54""", 'Duracao': "5.0", 'QtRec': "2", 'Hh': "10.0"},
    {'ClassePressao': "900#", 'Diametro': "3""", 'Duracao': "1.0", 'QtRec': "2", 'Hh': "2.0"},
    {'ClassePressao': "900#", 'Diametro': "4""", 'Duracao': "1.5", 'QtRec': "2", 'Hh': "3.0"},
    {'ClassePressao': "900#", 'Diametro': "6""", 'Duracao': "1.8", 'QtRec': "2", 'Hh': "3.5"},
    {'ClassePressao': "900#", 'Diametro': "8""", 'Duracao': "2.0", 'QtRec': "2", 'Hh': "4.0"},
    {'ClassePressao': "900#", 'Diametro': "10""", 'Duracao': "2.3", 'QtRec': "2", 'Hh': "4.5"},
    {'ClassePressao': "900#", 'Diametro': "12"" a 14""", 'Duracao': "2.5", 'QtRec': "2", 'Hh': "5.0"},
    {'ClassePressao': "900#", 'Diametro': "16""", 'Duracao': "2.8", 'QtRec': "2", 'Hh': "5.5"},
    {'ClassePressao': "900#", 'Diametro': "18"" a 20""", 'Duracao': "3.0", 'QtRec': "2", 'Hh': "6.0"},
    {'ClassePressao': "900#", 'Diametro': "22""", 'Duracao': "3.2", 'QtRec': "2", 'Hh': "6.4"},
    {'ClassePressao': "900#", 'Diametro': "24"" a 26""", 'Duracao': "3.5", 'QtRec': "2", 'Hh': "7.0"},
    {'ClassePressao': "900#", 'Diametro': "30""", 'Duracao': "4.0", 'QtRec': "2", 'Hh': "8.0"},
    {'ClassePressao': "900#", 'Diametro': "36""", 'Duracao': "4.5", 'QtRec': "2", 'Hh': "9.0"},
    {'ClassePressao': "900#", 'Diametro': "42"" a 44""", 'Duracao': "5.0", 'QtRec': "2", 'Hh': "10.0"},
    {'ClassePressao': "900#", 'Diametro': "48""", 'Duracao': "5.0", 'QtRec': "2", 'Hh': "10.0"},
    {'ClassePressao': "1500#", 'Diametro': "Até 1.1/2""", 'Duracao': "0.5", 'QtRec': "2", 'Hh': "1.0"},
    {'ClassePressao': "1500#", 'Diametro': "2"" a 2.1/2""", 'Duracao': "1.0", 'QtRec': "2", 'Hh': "2.0"},
    {'ClassePressao': "1500#", 'Diametro': "3""", 'Duracao': "1.0", 'QtRec': "2", 'Hh': "2.0"},
    {'ClassePressao': "1500#", 'Diametro': "4""", 'Duracao': "1.8", 'QtRec': "2", 'Hh': "3.5"},
    {'ClassePressao': "1500#", 'Diametro': "6""", 'Duracao': "2.0", 'QtRec': "2", 'Hh': "4.0"},
    {'ClassePressao': "1500#", 'Diametro': "8""", 'Duracao': "2.3", 'QtRec': "2", 'Hh': "4.5"},
    {'ClassePressao': "1500#", 'Diametro': "10""", 'Duracao': "2.5", 'QtRec': "2", 'Hh': "5.0"},
    {'ClassePressao': "1500#", 'Diametro': "12"" a 14""", 'Duracao': "3.0", 'QtRec': "2", 'Hh': "6.0"},
    {'ClassePressao': "1500#", 'Diametro': "16""", 'Duracao': "3.5", 'QtRec': "2", 'Hh': "7.0"},
    {'ClassePressao': "1500#", 'Diametro': "18"" a 20""", 'Duracao': "4.0", 'QtRec': "2", 'Hh': "8.0"},
    {'ClassePressao': "1500#", 'Diametro': "22""", 'Duracao': "4.5", 'QtRec': "2", 'Hh': "9.0"},
    {'ClassePressao': "1500#", 'Diametro': "24"" a 26""", 'Duracao': "5.0", 'QtRec': "2", 'Hh': "10.0"},
    {'ClassePressao': "2500#", 'Diametro': "Até 1.1/2""", 'Duracao': "0.5", 'QtRec': "2", 'Hh': "1.0"},
    {'ClassePressao': "2500#", 'Diametro': "2"" a 2.1/2""", 'Duracao': "1.0", 'QtRec': "2", 'Hh': "2.0"},
    {'ClassePressao': "2500#", 'Diametro': "3""", 'Duracao': "1.0", 'QtRec': "2", 'Hh': "2.0"},
    {'ClassePressao': "2500#", 'Diametro': "4""", 'Duracao': "2.0", 'QtRec': "2", 'Hh': "4.0"},
    {'ClassePressao': "2500#", 'Diametro': "6""", 'Duracao': "2.5", 'QtRec': "2", 'Hh': "5.0"},
    {'ClassePressao': "2500#", 'Diametro': "8""", 'Duracao': "3.0", 'QtRec': "2", 'Hh': "6.0"},
    {'ClassePressao': "2500#", 'Diametro': "10""", 'Duracao': "3.5", 'QtRec': "2", 'Hh': "7.0"},
    {'ClassePressao': "2500#", 'Diametro': "12""", 'Duracao': "4.0", 'QtRec': "2", 'Hh': "8.0"}
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
    #st.write(f"Duração (hs): {atividade_selecionada['Duracao']}")
    st.write(f"Qtde de Recursos: {atividade_selecionada['QtRec']}")
    st.write(f"HH: {atividade_selecionada['Hh']}")
    
    # Converter a duração para minutos primeiro
    duracao_minutos = float(atividade_selecionada['Duracao'].replace(',', '.')) * 60  # Converte horas para minutos
    # Calcular o tempo total em minutos
    resultado = duracao_minutos

    # Condição para exibir o tempo em minutos ou horas
    if resultado < 60:
        st.success(f"Duração: {round(resultado, 2)} minutos")
    else:
        horas = resultado / 60
        st.success(f"Duração: {round(horas, 2)} horas")

# Função principal que chama o formulário
def main():
    show_exec_atividades_torque_form()

if __name__ == "__main__":
    main()
