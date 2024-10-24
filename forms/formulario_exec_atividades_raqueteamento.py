import streamlit as st
import pandas as pd

# Dados da execução de 'atividade's
exec_atividades_raqueteamento = pd.DataFrame([
        {'ClassePressao': "150#", 'Diametro': "Até 4 """, 'Atividade': "Raqueteamento", 'Duracao': "1,0", 'QtRec': "2", 'Hh': "2,0"},
        {'ClassePressao': "150#", 'Diametro': "Até 4""", 'Atividade': "Desraqueteamento", 'Duracao': "0,8", 'QtRec': "2", 'Hh': "1,6"},
        {'ClassePressao': "150#", 'Diametro': "6"" a 8""", 'Atividade': "Raqueteamento", 'Duracao': "1,5", 'QtRec': "2", 'Hh': "3,0"},
        {'ClassePressao': "150#", 'Diametro': "6"" a 8""", 'Atividade': "Desraqueteamento", 'Duracao': "1,2", 'QtRec': "2", 'Hh': "2,4"},
        {'ClassePressao': "150#", 'Diametro': "10"" a 18""", 'Atividade': "Raqueteamento", 'Duracao': "2,0", 'QtRec': "2", 'Hh': "4,0"},
        {'ClassePressao': "150#", 'Diametro': "10"" a 18""", 'Atividade': "Desraqueteamento", 'Duracao': "1,6", 'QtRec': "2", 'Hh': "3,2"},
        {'ClassePressao': "150#", 'Diametro': "20"" a 30""", 'Atividade': "Raqueteamento", 'Duracao': "3,0", 'QtRec': "2", 'Hh': "6,0"},
        {'ClassePressao': "150#", 'Diametro': "20"" a 30""", 'Atividade': "Desraqueteamento", 'Duracao': "2,4", 'QtRec': "2", 'Hh': "4,8"},
        {'ClassePressao': "150#", 'Diametro': "Acima de 30""", 'Atividade': "Raqueteamento", 'Duracao': "4,0", 'QtRec': "2", 'Hh': "8,0"},
        {'ClassePressao': "150#", 'Diametro': "Acima de 30""", 'Atividade': "Desraqueteamento", 'Duracao': "3,2", 'QtRec': "2", 'Hh': "6,4"},
        {'ClassePressao': "300#", 'Diametro': "Até 4""", 'Atividade': "Raqueteamento", 'Duracao': "1,0", 'QtRec': "2", 'Hh': "2,0"},
        {'ClassePressao': "300#", 'Diametro': "Até 4""", 'Atividade': "Desraqueteamento", 'Duracao': "0,8", 'QtRec': "2", 'Hh': "1,6"},
        {'ClassePressao': "300#", 'Diametro': "6"" a 8""", 'Atividade': "Raqueteamento", 'Duracao': "1,5", 'QtRec': "2", 'Hh': "3,0"},
        {'ClassePressao': "300#", 'Diametro': "6"" a 8""", 'Atividade': "Desraqueteamento", 'Duracao': "1,2", 'QtRec': "2", 'Hh': "2,4"},
        {'ClassePressao': "300#", 'Diametro': "10"" a 18""", 'Atividade': "Raqueteamento", 'Duracao': "2,0", 'QtRec': "2", 'Hh': "4,0"},
        {'ClassePressao': "300#", 'Diametro': "10"" a 18""", 'Atividade': "Desraqueteamento", 'Duracao': "1,6", 'QtRec': "2", 'Hh': "3,2"},
        {'ClassePressao': "300#", 'Diametro': "20"" a 24""", 'Atividade': "Raqueteamento", 'Duracao': "3,0", 'QtRec': "2", 'Hh': "6,0"},
        {'ClassePressao': "300#", 'Diametro': "20"" a 24""", 'Atividade': "Desraqueteamento", 'Duracao': "2,4", 'QtRec': "2", 'Hh': "4,8"},
        {'ClassePressao': "300#", 'Diametro': "Acima de 24""", 'Atividade': "Raqueteamento", 'Duracao': "4,0", 'QtRec': "2", 'Hh': "8,0"},
        {'ClassePressao': "300#", 'Diametro': "Acima de 24""", 'Atividade': "Desraqueteamento", 'Duracao': "3,2", 'QtRec': "2", 'Hh': "6,4"},
        {'ClassePressao': "600#", 'Diametro': "Até 4""", 'Atividade': "Raqueteamento", 'Duracao': "1,5", 'QtRec': "2", 'Hh': "3,0"},
        {'ClassePressao': "600#", 'Diametro': "Até 4""", 'Atividade': "Desraqueteamento", 'Duracao': "1,2", 'QtRec': "2", 'Hh': "2,4"},
        {'ClassePressao': "600#", 'Diametro': "6"" a 8""", 'Atividade': "Raqueteamento", 'Duracao': "2,0", 'QtRec': "2", 'Hh': "4,0"},
        {'ClassePressao': "600#", 'Diametro': "6"" a 8""", 'Atividade': "Desraqueteamento", 'Duracao': "1,6", 'QtRec': "2", 'Hh': "3,2"},
        {'ClassePressao': "600#", 'Diametro': "10"" a 18""", 'Atividade': "Raqueteamento", 'Duracao': "3,0", 'QtRec': "2", 'Hh': "6,0"},
        {'ClassePressao': "600#", 'Diametro': "10"" a 18""", 'Atividade': "Desraqueteamento", 'Duracao': "2,4", 'QtRec': "2", 'Hh': "4,8"},
        {'ClassePressao': "600#", 'Diametro': "20"" a 24""", 'Atividade': "Raqueteamento", 'Duracao': "4,0", 'QtRec': "2", 'Hh': "8,0"},
        {'ClassePressao': "600#", 'Diametro': "20"" a 24""", 'Atividade': "Desraqueteamento", 'Duracao': "3,2", 'QtRec': "2", 'Hh': "6,4"},
        {'ClassePressao': "600#", 'Diametro': "Acima de 24""", 'Atividade': "Raqueteamento", 'Duracao': "6,0", 'QtRec': "2", 'Hh': "12,0"},
        {'ClassePressao': "600#", 'Diametro': "Acima de 24""", 'Atividade': "Desraqueteamento", 'Duracao': "4,8", 'QtRec': "2", 'Hh': "9,6"},
        {'ClassePressao': "900#", 'Diametro': "Até 4""", 'Atividade': "Raqueteamento", 'Duracao': "1,5", 'QtRec': "2", 'Hh': "3,0"},
        {'ClassePressao': "900#", 'Diametro': "Até 4""", 'Atividade': "Desraqueteamento", 'Duracao': "1,2", 'QtRec': "2", 'Hh': "2,4"},
        {'ClassePressao': "900#", 'Diametro': "6"" a 8""", 'Atividade': "Raqueteamento", 'Duracao': "2,0", 'QtRec': "2", 'Hh': "4,0"},
        {'ClassePressao': "900#", 'Diametro': "6"" a 8""", 'Atividade': "Desraqueteamento", 'Duracao': "1,6", 'QtRec': "2", 'Hh': "3,2"},
        {'ClassePressao': "900#", 'Diametro': "10"" a 18""", 'Atividade': "Raqueteamento", 'Duracao': "3,0", 'QtRec': "2", 'Hh': "6,0"},
        {'ClassePressao': "900#", 'Diametro': "10"" a 18""", 'Atividade': "Desraqueteamento", 'Duracao': "2,4", 'QtRec': "2", 'Hh': "4,8"},
        {'ClassePressao': "900#", 'Diametro': "20"" a 24""", 'Atividade': "Raqueteamento", 'Duracao': "4,0", 'QtRec': "2", 'Hh': "8,0"},
        {'ClassePressao': "900#", 'Diametro': "20"" a 24""", 'Atividade': "Desraqueteamento", 'Duracao': "3,2", 'QtRec': "2", 'Hh': "6,4"},
        {'ClassePressao': "900#", 'Diametro': "Acima de 24""", 'Atividade': "Raqueteamento", 'Duracao': "6,0", 'QtRec': "2", 'Hh': "12,0"},
        {'ClassePressao': "900#", 'Diametro': "Acima de 24""", 'Atividade': "Desraqueteamento", 'Duracao': "4,8", 'QtRec': "2", 'Hh': "9,6"}
])

# Função para exibir o formulário baseado nos dados
def show_exec_atividades_form():
    st.subheader("Formulário: Execução de 'Atividade's Raqueteamento e Desraqueteamento")

    # Seleção de Atividade
    atividade = st.selectbox("Atividade:", exec_atividades_raqueteamento['Atividade'].unique())

    # Filtrar as opções da Classe de Pressão com base na 'atividade'
    classe_pressao_opcoes = exec_atividades_raqueteamento[exec_atividades_raqueteamento['Atividade'] == atividade]['ClassePressao'].unique()
    classe_pressao = st.selectbox("Classe de Pressão:", classe_pressao_opcoes)

    # Filtrar as opções de Diâmetro com base na Classe de Pressão
    diametro_opcoes = exec_atividades_raqueteamento[(exec_atividades_raqueteamento['Atividade'] == atividade) & (exec_atividades_raqueteamento['ClassePressao'] == classe_pressao)]['Diametro'].unique()
    diametro = st.selectbox("Diâmetro:", diametro_opcoes)

    # Filtrar os dados da tabela com base nas seleções
    atividade_selecionada = exec_atividades_raqueteamento[(exec_atividades_raqueteamento['Atividade'] == atividade) & 
                                                          (exec_atividades_raqueteamento['ClassePressao'] == classe_pressao) & 
                                                          (exec_atividades_raqueteamento['Diametro'] == diametro)].iloc[0]
    
    # Exibir os resultados da consulta
    st.write(f"Duração (hs): {atividade_selecionada['Duracao']}")
    st.write(f"Qt Rec. (Ca): {atividade_selecionada['QtRec']}")
    st.write(f"Hh: {atividade_selecionada['Hh']}")

    # Campo para inserir quantidade de M²
    QT_REC = st.number_input("Qt Rec. (Ca):", min_value=1)
    
    # Calcular Tempo Estimado
    if st.button("Calcular"):
        resultado = float(QT_REC) * float(atividade_selecionada['Duracao'].replace(',', '.'))
        st.success(f"Tempo Estimado: {round(resultado, 2)} horas")

# Função principal que chama o formulário
def main():
    show_exec_atividades_form()

if __name__ == "__main__":
    main()
