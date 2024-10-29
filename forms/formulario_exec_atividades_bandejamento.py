import streamlit as st
import pandas as pd

# Dados da execução de 'atividade's
exec_atividades_bandejamento = pd.DataFrame([
    {'Descricao': "Abrir Alçapão de Torre (por Alçapão)", 'Duracao': "0.25", 'QtRec': "2", 'Hh': "0.5"},
    {'Descricao': "Fechar Alçapão de Torre (por Alçapão)", 'Duracao': "0.25", 'QtRec': "2", 'Hh': "0.5"},
    {'Descricao': "Remover Bandejas de Torre de Diâmetro até 1500 mm", 'Duracao': "2.5", 'QtRec': "3", 'Hh': "7.5"},
    {'Descricao': "Remover Bandejas de Torre de Diâmetro de 1501 mm até 2500 mm", 'Duracao': "4.0", 'QtRec': "5", 'Hh': "20.0"},
    {'Descricao': "Remover Bandejas de Torre de Diâmetro de 2501 mm até 4000 mm", 'Duracao': "5.5", 'QtRec': "5", 'Hh': "27.5"},
    {'Descricao': "Remover Bandejas de Torre de Diâmetro acima de 4001 mm", 'Duracao': "7.0", 'QtRec': "5", 'Hh': "35.0"},
    {'Descricao': "Instalar Bandejas de Torre de Diâmetro até 1500 mm", 'Duracao': "3.0", 'QtRec': "3", 'Hh': "9.0"},
    {'Descricao': "Instalar Bandejas de Torre de Diâmetro de 1501 mm até 2500 mm", 'Duracao': "6.0", 'QtRec': "5", 'Hh': "30.0"},
    {'Descricao': "Instalar Bandejas de Torre de Diâmetro de 2501 mm até 4000 mm", 'Duracao': "8.0", 'QtRec': "5", 'Hh': "40.0"},
    {'Descricao': "Instalar Bandejas de Torre de Diâmetro acima de 4001 mm", 'Duracao': "10.0", 'QtRec': "5", 'Hh': "50.0"}
])

# Função para exibir o formulário baseado nos dados
def show_exec_atividades_bandejamento_form():
    st.subheader("Formulário: Execução de Atividades - Bandejamento")

    # Seleção de Classe de Pressão
    vardescricao = st.selectbox("Descrição:", exec_atividades_bandejamento['Descricao'].unique())

    # Filtrar as opções de Diâmetro com base na Classe de Pressão
    duracao_opcoes = exec_atividades_bandejamento[exec_atividades_bandejamento['Descricao'] == vardescricao]['Duracao'].unique()
    duracao = st.selectbox("Diâmetro:", duracao_opcoes)

    # Filtrar os dados da tabela com base nas seleções
    atividade_selecionada = exec_atividades_bandejamento[(exec_atividades_bandejamento['Descricao'] == vardescricao) & 
                                                   (exec_atividades_bandejamento['Duracao'] == duracao)].iloc[0]
    
    # Exibir os resultados da consulta
    st.write(f"Duração (hs): {atividade_selecionada['Duracao']}")
    st.write(f"Qtde de Recursos: {atividade_selecionada['QtRec']}")
    #st.write(f"HH: {atividade_selecionada['Hh']}")
    st.success(f"Tempo Estimado: {round(float(atividade_selecionada['Hh'].replace(',', '.')), 2)} horas")

# Função principal que chama o formulário
def main():
    show_exec_atividades_bandejamento_form()

if __name__ == "__main__":
    main()
