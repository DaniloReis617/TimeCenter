import streamlit as st
import pandas as pd

# Dados da execução de atividades - Abertura e Fechamento de Boca de Visita
exec_atividades_boca_visita = pd.DataFrame([
    {'ClassePressao': "150#", 'Diametro': "18""", 'Atividade': "Abertura", 'Duracao': "1.0", 'QtRec': "2", 'Hh': "2.0"},
    {'ClassePressao': "150#", 'Diametro': "18""", 'Atividade': "Fechamento", 'Duracao': "1.5", 'QtRec': "2", 'Hh': "3.0"},
    {'ClassePressao': "150#", 'Diametro': "20""", 'Atividade': "Abertura", 'Duracao': "1.5", 'QtRec': "2", 'Hh': "3.0"},
    {'ClassePressao': "150#", 'Diametro': "20""", 'Atividade': "Fechamento", 'Duracao': "2.0", 'QtRec': "2", 'Hh': "4.0"},
    {'ClassePressao': "150#", 'Diametro': "24""", 'Atividade': "Abertura", 'Duracao': "2.0", 'QtRec': "2", 'Hh': "4.0"},
    {'ClassePressao': "150#", 'Diametro': "24""", 'Atividade': "Fechamento", 'Duracao': "2.5", 'QtRec': "2", 'Hh': "5.0"},
    {'ClassePressao': "300#", 'Diametro': "18""", 'Atividade': "Abertura", 'Duracao': "1.5", 'QtRec': "2", 'Hh': "3.0"},
    {'ClassePressao': "300#", 'Diametro': "18""", 'Atividade': "Fechamento", 'Duracao': "2.0", 'QtRec': "2", 'Hh': "4.0"},
    {'ClassePressao': "300#", 'Diametro': "20""", 'Atividade': "Abertura", 'Duracao': "2.0", 'QtRec': "2", 'Hh': "4.0"},
    {'ClassePressao': "300#", 'Diametro': "20""", 'Atividade': "Fechamento", 'Duracao': "2.5", 'QtRec': "2", 'Hh': "5.0"},
    {'ClassePressao': "300#", 'Diametro': "24""", 'Atividade': "Abertura", 'Duracao': "2.0", 'QtRec': "2", 'Hh': "4.0"},
    {'ClassePressao': "300#", 'Diametro': "24""", 'Atividade': "Fechamento", 'Duracao': "2.5", 'QtRec': "2", 'Hh': "5.0"}
])

# Função para exibir o formulário baseado nos dados
def show_exec_atividades_boca_visita_form():
    st.subheader("Formulário: Execução de Abertura/Fechamento de Boca de Visita")

    # Seleção de Atividade
    atividade = st.selectbox("Atividade:", exec_atividades_boca_visita['Atividade'].unique())

    # Filtrar as opções da Classe de Pressão com base na Atividade
    classe_pressao_opcoes = exec_atividades_boca_visita[exec_atividades_boca_visita['Atividade'] == atividade]['ClassePressao'].unique()
    classe_pressao = st.selectbox("Classe de Pressão:", classe_pressao_opcoes)

    # Filtrar as opções de Diâmetro com base na Classe de Pressão e Atividade
    diametro_opcoes = exec_atividades_boca_visita[(exec_atividades_boca_visita['Atividade'] == atividade) & 
                                                  (exec_atividades_boca_visita['ClassePressao'] == classe_pressao)]['Diametro'].unique()
    diametro = st.selectbox("Diâmetro:", diametro_opcoes)

    # Filtrar os dados da tabela com base nas seleções
    atividade_selecionada = exec_atividades_boca_visita[(exec_atividades_boca_visita['Atividade'] == atividade) & 
                                                        (exec_atividades_boca_visita['ClassePressao'] == classe_pressao) & 
                                                        (exec_atividades_boca_visita['Diametro'] == diametro)].iloc[0]
    
    # Exibir os resultados da consulta
    st.write(f"Qtde de Recursos: {atividade_selecionada['QtRec']}")
    st.write(f"Hh: {atividade_selecionada['Hh']}")
    #st.write(f"Duração (hs): {atividade_selecionada['Duracao']}")
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
    show_exec_atividades_boca_visita_form()

if __name__ == "__main__":
    main()
