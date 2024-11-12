import streamlit as st
import pandas as pd

# Dados da execução de atividades - Abertura e Fechamento de Boca de Visita
exec_atividades_Remocao_Instalacao_Valvulas = pd.DataFrame([
    {'ClassePressao': "150#", 'Diametro': "Até 2""", 'Atividade': "Remoção", 'Duracao': '0,5', 'QtRec': '2', 'Hh': '1,0'},
    {'ClassePressao': "150#", 'Diametro': "Até 2""", 'Atividade': "Instalação", 'Duracao': '0,7', 'QtRec': '2', 'Hh': '1,4'},
    {'ClassePressao': "150#", 'Diametro': "3""", 'Atividade': "Remoção", 'Duracao': '0,8', 'QtRec': '2', 'Hh': '1,6'},
    {'ClassePressao': "150#", 'Diametro': "3""", 'Atividade': "Instalação", 'Duracao': '1,6', 'QtRec': '2', 'Hh': '3,2'},
    {'ClassePressao': "150#", 'Diametro': "4""", 'Atividade': "Remoção", 'Duracao': '1,0', 'QtRec': '2', 'Hh': '2,0'},
    {'ClassePressao': "150#", 'Diametro': "4""", 'Atividade': "Instalação", 'Duracao': '1,8', 'QtRec': '2', 'Hh': '3,6'},
    {'ClassePressao': "150#", 'Diametro': "6""", 'Atividade': "Remoção", 'Duracao': '1,2', 'QtRec': '2', 'Hh': '2,4'},
    {'ClassePressao': "150#", 'Diametro': "6""", 'Atividade': "Instalação", 'Duracao': '2,0', 'QtRec': '2', 'Hh': '4,0'},
    {'ClassePressao': "150#", 'Diametro': "8""", 'Atividade': "Remoção", 'Duracao': '1,5', 'QtRec': '2', 'Hh': '3,0'},
    {'ClassePressao': "150#", 'Diametro': "8""", 'Atividade': "Instalação", 'Duracao': '2,0', 'QtRec': '2', 'Hh': '4,0'},
    {'ClassePressao': "150#", 'Diametro': "10""", 'Atividade': "Remoção", 'Duracao': '1,8', 'QtRec': '2', 'Hh': '3,6'},
    {'ClassePressao': "150#", 'Diametro': "10""", 'Atividade': "Instalação", 'Duracao': '2,5', 'QtRec': '2', 'Hh': '5,0'},
    {'ClassePressao': "150#", 'Diametro': "12""", 'Atividade': "Remoção", 'Duracao': '2,0', 'QtRec': '2', 'Hh': '4,0'},
    {'ClassePressao': "150#", 'Diametro': "12""", 'Atividade': "Instalação", 'Duracao': '3,0', 'QtRec': '2', 'Hh': '6,0'},
    {'ClassePressao': "150#", 'Diametro': "16""", 'Atividade': "Remoção", 'Duracao': '2,3', 'QtRec': '2', 'Hh': '4,6'},
    {'ClassePressao': "150#", 'Diametro': "16""", 'Atividade': "Instalação", 'Duracao': '3,5', 'QtRec': '2', 'Hh': '7,0'},
    {'ClassePressao': "150#", 'Diametro': "18""", 'Atividade': "Remoção", 'Duracao': '2,5', 'QtRec': '2', 'Hh': '5,0'},
    {'ClassePressao': "150#", 'Diametro': "18""", 'Atividade': "Instalação", 'Duracao': '3,5', 'QtRec': '2', 'Hh': '7,0'},
    {'ClassePressao': "150#", 'Diametro': "20""", 'Atividade': "Remoção", 'Duracao': '2,5', 'QtRec': '2', 'Hh': '5,0'},
    {'ClassePressao': "150#", 'Diametro': "20""", 'Atividade': "Instalação", 'Duracao': '4,0', 'QtRec': '2', 'Hh': '8,0'},
    {'ClassePressao': "150#", 'Diametro': "24""", 'Atividade': "Remoção", 'Duracao': '2,8', 'QtRec': '2', 'Hh': '5,6'},
    {'ClassePressao': "150#", 'Diametro': "24""", 'Atividade': "Instalação", 'Duracao': '4,5', 'QtRec': '2', 'Hh': '9,0'},
    {'ClassePressao': "150#", 'Diametro': "26""", 'Atividade': "Remoção", 'Duracao': '2,8', 'QtRec': '2', 'Hh': '5,6'},
    {'ClassePressao': "150#", 'Diametro': "26""", 'Atividade': "Instalação", 'Duracao': '4,5', 'QtRec': '2', 'Hh': '9,0'},
    {'ClassePressao': "150#", 'Diametro': "28""", 'Atividade': "Remoção", 'Duracao': '3,0', 'QtRec': '2', 'Hh': '6,0'},
    {'ClassePressao': "150#", 'Diametro': "28""", 'Atividade': "Instalação", 'Duracao': '5,0', 'QtRec': '2', 'Hh': '10,0'},
    {'ClassePressao': "150#", 'Diametro': "30""", 'Atividade': "Remoção", 'Duracao': '2,0', 'QtRec': '4', 'Hh': '8,0'},
    {'ClassePressao': "150#", 'Diametro': "30""", 'Atividade': "Instalação", 'Duracao': '3,0', 'QtRec': '4', 'Hh': '12,0'},
    {'ClassePressao': "150#", 'Diametro': "32""", 'Atividade': "Remoção", 'Duracao': '2,0', 'QtRec': '4', 'Hh': '8,0'},
    {'ClassePressao': "150#", 'Diametro': "32""", 'Atividade': "Instalação", 'Duracao': '3,0', 'QtRec': '4', 'Hh': '12,0'},
    {'ClassePressao': "150#", 'Diametro': "36""", 'Atividade': "Remoção", 'Duracao': '2,5', 'QtRec': '4', 'Hh': '10,0'},
    {'ClassePressao': "150#", 'Diametro': "36""", 'Atividade': "Instalação", 'Duracao': '3,0', 'QtRec': '4', 'Hh': '12,0'},
    {'ClassePressao': "300#", 'Diametro': "Até 2""", 'Atividade': "Remoção", 'Duracao': '0,5', 'QtRec': '2', 'Hh': '1,0'},
    {'ClassePressao': "300#", 'Diametro': "Até 2""", 'Atividade': "Instalação", 'Duracao': '0,7', 'QtRec': '2', 'Hh': '1,4'},
    {'ClassePressao': "300#", 'Diametro': "3""", 'Atividade': "Remoção", 'Duracao': '0,8', 'QtRec': '2', 'Hh': '1,6'},
    {'ClassePressao': "300#", 'Diametro': "3""", 'Atividade': "Instalação", 'Duracao': '1,6', 'QtRec': '2', 'Hh': '3,2'},
    {'ClassePressao': "300#", 'Diametro': "4""", 'Atividade': "Remoção", 'Duracao': '1,0', 'QtRec': '2', 'Hh': '2,0'},
    {'ClassePressao': "300#", 'Diametro': "4""", 'Atividade': "Instalação", 'Duracao': '1,8', 'QtRec': '2', 'Hh': '3,6'},
    {'ClassePressao': "300#", 'Diametro': "6""", 'Atividade': "Remoção", 'Duracao': '1,2', 'QtRec': '2', 'Hh': '2,4'},
    {'ClassePressao': "300#", 'Diametro': "6""", 'Atividade': "Instalação", 'Duracao': '2,0', 'QtRec': '2', 'Hh': '4,0'},
    {'ClassePressao': "300#", 'Diametro': "8""", 'Atividade': "Remoção", 'Duracao': '1,5', 'QtRec': '2', 'Hh': '3,0'},
    {'ClassePressao': "300#", 'Diametro': "8""", 'Atividade': "Instalação", 'Duracao': '2,0', 'QtRec': '2', 'Hh': '4,0'},
    {'ClassePressao': "300#", 'Diametro': "10""", 'Atividade': "Remoção", 'Duracao': '1,8', 'QtRec': '2', 'Hh': '3,6'},
    {'ClassePressao': "300#", 'Diametro': "10""", 'Atividade': "Instalação", 'Duracao': '2,5', 'QtRec': '2', 'Hh': '5,0'},
    {'ClassePressao': "300#", 'Diametro': "12""", 'Atividade': "Remoção", 'Duracao': '2,0', 'QtRec': '2', 'Hh': '4,0'},
    {'ClassePressao': "300#", 'Diametro': "12""", 'Atividade': "Instalação", 'Duracao': '3,0', 'QtRec': '2', 'Hh': '6,0'},
    {'ClassePressao': "300#", 'Diametro': "16""", 'Atividade': "Remoção", 'Duracao': '2,3', 'QtRec': '2', 'Hh': '4,6'},
    {'ClassePressao': "300#", 'Diametro': "16""", 'Atividade': "Instalação", 'Duracao': '3,5', 'QtRec': '2', 'Hh': '7,0'},
    {'ClassePressao': "300#", 'Diametro': "18""", 'Atividade': "Remoção", 'Duracao': '2,5', 'QtRec': '2', 'Hh': '5,0'},
    {'ClassePressao': "300#", 'Diametro': "18""", 'Atividade': "Instalação", 'Duracao': '3,5', 'QtRec': '2', 'Hh': '7,0'},
    {'ClassePressao': "300#", 'Diametro': "20""", 'Atividade': "Remoção", 'Duracao': '2,5', 'QtRec': '2', 'Hh': '5,0'},
    {'ClassePressao': "300#", 'Diametro': "20""", 'Atividade': "Instalação", 'Duracao': '4,0', 'QtRec': '2', 'Hh': '8,0'},
    {'ClassePressao': "300#", 'Diametro': "24""", 'Atividade': "Remoção", 'Duracao': '2,8', 'QtRec': '2', 'Hh': '5,6'},
    {'ClassePressao': "300#", 'Diametro': "24""", 'Atividade': "Instalação", 'Duracao': '4,5', 'QtRec': '2', 'Hh': '9,0'},
    {'ClassePressao': "300#", 'Diametro': "26""", 'Atividade': "Remoção", 'Duracao': '2,8', 'QtRec': '2', 'Hh': '5,6'},
    {'ClassePressao': "300#", 'Diametro': "26""", 'Atividade': "Instalação", 'Duracao': '4,5', 'QtRec': '2', 'Hh': '9,0'},
    {'ClassePressao': "300#", 'Diametro': "28""", 'Atividade': "Remoção", 'Duracao': '3,0', 'QtRec': '2', 'Hh': '6,0'},
    {'ClassePressao': "300#", 'Diametro': "28""", 'Atividade': "Instalação", 'Duracao': '5,0', 'QtRec': '2', 'Hh': '10,0'},
    {'ClassePressao': "300#", 'Diametro': "30""", 'Atividade': "Remoção", 'Duracao': '2,0', 'QtRec': '4', 'Hh': '8,0'},
    {'ClassePressao': "300#", 'Diametro': "30""", 'Atividade': "Instalação", 'Duracao': '3,0', 'QtRec': '4', 'Hh': '12,0'},
    {'ClassePressao': "300#", 'Diametro': "32""", 'Atividade': "Remoção", 'Duracao': '2,0', 'QtRec': '4', 'Hh': '8,0'},
    {'ClassePressao': "300#", 'Diametro': "32""", 'Atividade': "Instalação", 'Duracao': '3,0', 'QtRec': '4', 'Hh': '12,0'},
    {'ClassePressao': "300#", 'Diametro': "36""", 'Atividade': "Remoção", 'Duracao': '2,5', 'QtRec': '4', 'Hh': '10,0'},
    {'ClassePressao': "300#", 'Diametro': "36""", 'Atividade': "Instalação", 'Duracao': '3,0', 'QtRec': '4', 'Hh': '12,0'},
    {'ClassePressao': "600#", 'Diametro': "Até 2""", 'Atividade': "Remoção", 'Duracao': '0,5', 'QtRec': '2', 'Hh': '1,0'},
    {'ClassePressao': "600#", 'Diametro': "Até 2""", 'Atividade': "Instalação", 'Duracao': '0,7', 'QtRec': '2', 'Hh': '1,4'},
    {'ClassePressao': "600#", 'Diametro': "3""", 'Atividade': "Remoção", 'Duracao': '0,8', 'QtRec': '2', 'Hh': '1,6'},
    {'ClassePressao': "600#", 'Diametro': "3""", 'Atividade': "Instalação", 'Duracao': '1,6', 'QtRec': '2', 'Hh': '3,2'},
    {'ClassePressao': "600#", 'Diametro': "4""", 'Atividade': "Remoção", 'Duracao': '1,2', 'QtRec': '2', 'Hh': '2,4'},
    {'ClassePressao': "600#", 'Diametro': "4""", 'Atividade': "Instalação", 'Duracao': '2,0', 'QtRec': '2', 'Hh': '4,0'},
    {'ClassePressao': "600#", 'Diametro': "6""", 'Atividade': "Remoção", 'Duracao': '1,5', 'QtRec': '2', 'Hh': '3,0'},
    {'ClassePressao': "600#", 'Diametro': "6""", 'Atividade': "Instalação", 'Duracao': '2,5', 'QtRec': '2', 'Hh': '5,0'},
    {'ClassePressao': "600#", 'Diametro': "8""", 'Atividade': "Remoção", 'Duracao': '1,8', 'QtRec': '2', 'Hh': '3,6'},
    {'ClassePressao': "600#", 'Diametro': "8""", 'Atividade': "Instalação", 'Duracao': '2,5', 'QtRec': '2', 'Hh': '5,0'},
    {'ClassePressao': "600#", 'Diametro': "10""", 'Atividade': "Remoção", 'Duracao': '2,0', 'QtRec': '2', 'Hh': '4,0'},
    {'ClassePressao': "600#", 'Diametro': "10""", 'Atividade': "Instalação", 'Duracao': '3,0', 'QtRec': '2', 'Hh': '6,0'},
    {'ClassePressao': "600#", 'Diametro': "12""", 'Atividade': "Remoção", 'Duracao': '2,5', 'QtRec': '2', 'Hh': '5,0'},
    {'ClassePressao': "600#", 'Diametro': "12""", 'Atividade': "Instalação", 'Duracao': '3,0', 'QtRec': '2', 'Hh': '6,0'},
    {'ClassePressao': "600#", 'Diametro': "16""", 'Atividade': "Remoção", 'Duracao': '2,8', 'QtRec': '2', 'Hh': '5,6'},
    {'ClassePressao': "600#", 'Diametro': "16""", 'Atividade': "Instalação", 'Duracao': '4,0', 'QtRec': '2', 'Hh': '8,0'},
    {'ClassePressao': "600#", 'Diametro': "18""", 'Atividade': "Remoção", 'Duracao': '2,8', 'QtRec': '2', 'Hh': '5,6'},
    {'ClassePressao': "600#", 'Diametro': "18""", 'Atividade': "Instalação", 'Duracao': '4,0', 'QtRec': '2', 'Hh': '8,0'},
    {'ClassePressao': "600#", 'Diametro': "20""", 'Atividade': "Remoção", 'Duracao': '3,0', 'QtRec': '2', 'Hh': '6,0'},
    {'ClassePressao': "600#", 'Diametro': "20""", 'Atividade': "Instalação", 'Duracao': '5,0', 'QtRec': '2', 'Hh': '10,0'},
    {'ClassePressao': "600#", 'Diametro': "24""", 'Atividade': "Remoção", 'Duracao': '3,0', 'QtRec': '2', 'Hh': '6,0'},
    {'ClassePressao': "600#", 'Diametro': "24""", 'Atividade': "Instalação", 'Duracao': '5,5', 'QtRec': '2', 'Hh': '11,0'},
    {'ClassePressao': "600#", 'Diametro': "26""", 'Atividade': "Remoção", 'Duracao': '3,0', 'QtRec': '2', 'Hh': '6,0'},
    {'ClassePressao': "600#", 'Diametro': "26""", 'Atividade': "Instalação", 'Duracao': '5,5', 'QtRec': '2', 'Hh': '11,0'},
    {'ClassePressao': "600#", 'Diametro': "28""", 'Atividade': "Remoção", 'Duracao': '3,5', 'QtRec': '2', 'Hh': '7,0'},
    {'ClassePressao': "600#", 'Diametro': "28""", 'Atividade': "Instalação", 'Duracao': '5,5', 'QtRec': '2', 'Hh': '11,0'},
    {'ClassePressao': "600#", 'Diametro': "30""", 'Atividade': "Remoção", 'Duracao': '3,0', 'QtRec': '4', 'Hh': '12,0'},
    {'ClassePressao': "600#", 'Diametro': "30""", 'Atividade': "Instalação", 'Duracao': '4,0', 'QtRec': '4', 'Hh': '16,0'},
    {'ClassePressao': "600#", 'Diametro': "32""", 'Atividade': "Remoção", 'Duracao': '3,0', 'QtRec': '4', 'Hh': '12,0'},
    {'ClassePressao': "600#", 'Diametro': "32""", 'Atividade': "Instalação", 'Duracao': '4,0', 'QtRec': '4', 'Hh': '16,0'},
    {'ClassePressao': "600#", 'Diametro': "36""", 'Atividade': "Remoção", 'Duracao': '3,0', 'QtRec': '4', 'Hh': '12,0'},
    {'ClassePressao': "600#", 'Diametro': "36""", 'Atividade': "Instalação", 'Duracao': '4,0', 'QtRec': '4', 'Hh': '16,0'}
])

# Função para exibir o formulário baseado nos dados
def show_exec_atividades_Remocao_Instalacao_Valvulas_form():
    st.subheader("Formulário: Execução de Remocao/Instalacao Valvulas")

    # Seleção de Atividade
    atividade = st.selectbox("Atividade:", exec_atividades_Remocao_Instalacao_Valvulas['Atividade'].unique())

    # Filtrar as opções da Classe de Pressão com base na Atividade
    classe_pressao_opcoes = exec_atividades_Remocao_Instalacao_Valvulas[exec_atividades_Remocao_Instalacao_Valvulas['Atividade'] == atividade]['ClassePressao'].unique()
    classe_pressao = st.selectbox("Classe de Pressão:", classe_pressao_opcoes)

    # Filtrar as opções de Diâmetro com base na Classe de Pressão
    diametro_opcoes = exec_atividades_Remocao_Instalacao_Valvulas[(exec_atividades_Remocao_Instalacao_Valvulas['Atividade'] == atividade) & (exec_atividades_Remocao_Instalacao_Valvulas['ClassePressao'] == classe_pressao)]['Diametro'].unique()
    diametro = st.selectbox("Diâmetro:", diametro_opcoes)

    # Filtrar os dados da tabela com base nas seleções
    atividade_selecionada = exec_atividades_Remocao_Instalacao_Valvulas[(exec_atividades_Remocao_Instalacao_Valvulas['Atividade'] == atividade) & 
                                                          (exec_atividades_Remocao_Instalacao_Valvulas['ClassePressao'] == classe_pressao) & 
                                                          (exec_atividades_Remocao_Instalacao_Valvulas['Diametro'] == diametro)].iloc[0]
    
    # Exibir os resultados da consulta
    #st.write(f"Duração (hs): {atividade_selecionada['Duracao']}")
    st.write(f"Qtde Recursos: {atividade_selecionada['QtRec']}")
    st.write(f"Hh: {atividade_selecionada['Hh']}")
    
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
    show_exec_atividades_Remocao_Instalacao_Valvulas_form()

if __name__ == "__main__":
    main()
