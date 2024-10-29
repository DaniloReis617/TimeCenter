import streamlit as st
import pandas as pd

# Dados da execução de 'atividade's
exec_atividades_Trocadores_De_Calor = pd.DataFrame([
    {'Descricao': "Abrir tampa", 'Dimensoes': "Até 500 tubos", 'Duracao': "2", 'Rec':"2"},
    {'Descricao': "Abrir tampa", 'Dimensoes': "501 a 1000 tubos", 'Duracao': "2,5", 'Rec':"2"},
    {'Descricao': "Abrir tampa", 'Dimensoes': "1001 a 1500 tubos", 'Duracao': "3", 'Rec':"2"},
    {'Descricao': "Abrir tampa", 'Dimensoes': "Acima de 1500 tubos", 'Duracao': "3,5", 'Rec':"2"},
    {'Descricao': "Fechar tampa", 'Dimensoes': "Até 500 tubos", 'Duracao': "2,5", 'Rec':"2"},
    {'Descricao': "Fechar tampa", 'Dimensoes': "501 a 1000 tubos", 'Duracao': "3", 'Rec':"2"},
    {'Descricao': "Fechar tampa", 'Dimensoes': "1001 a 1500 tubos", 'Duracao': "3,5", 'Rec':"2"},
    {'Descricao': "Fechar tampa", 'Dimensoes': "Acima de 1500 tubos", 'Duracao': "4", 'Rec':"2"},
    {'Descricao': "Remover carretel", 'Dimensoes': "Até 500 tubos", 'Duracao': "3", 'Rec':"2"},
    {'Descricao': "Remover carretel", 'Dimensoes': "501 a 1000 tubos", 'Duracao': "3,5", 'Rec':"2"},
    {'Descricao': "Remover carretel", 'Dimensoes': "1001 a 1500 tubos", 'Duracao': "4", 'Rec':"2"},
    {'Descricao': "Remover carretel", 'Dimensoes': "Acima de 1500 tubos", 'Duracao': "4,5", 'Rec':"2"},
    {'Descricao': "Instalar carretel", 'Dimensoes': "Até 500 tubos", 'Duracao': "4", 'Rec':"2"},
    {'Descricao': "Instalar carretel", 'Dimensoes': "501 a 1000 tubos", 'Duracao': "4,5", 'Rec':"2"},
    {'Descricao': "Instalar carretel", 'Dimensoes': "1001 a 1500 tubos", 'Duracao': "5", 'Rec':"2"},
    {'Descricao': "Instalar carretel", 'Dimensoes': "Acima de 1500 tubos", 'Duracao': "5,5", 'Rec':"2"},
    {'Descricao': "Remover boleado", 'Dimensoes': "Até 500 tubos", 'Duracao': "3", 'Rec':"2"},
    {'Descricao': "Remover boleado", 'Dimensoes': "501 a 1000 tubos", 'Duracao': "3,5", 'Rec':"2"},
    {'Descricao': "Remover boleado", 'Dimensoes': "1001 a 1500 tubos", 'Duracao': "4", 'Rec':"2"},
    {'Descricao': "Remover boleado", 'Dimensoes': "Acima de 1500 tubos", 'Duracao': "4", 'Rec':"2"},
    {'Descricao': "Instalar boleado", 'Dimensoes': "Até 500 tubos", 'Duracao': "3,5", 'Rec':"2"},
    {'Descricao': "Instalar boleado", 'Dimensoes': "501 a 1000 tubos", 'Duracao': "4", 'Rec':"2"},
    {'Descricao': "Instalar boleado", 'Dimensoes': "1001 a 1500 tubos", 'Duracao': "4,5", 'Rec':"2"},
    {'Descricao': "Instalar boleado", 'Dimensoes': "Acima de 1500 tubos", 'Duracao': "5", 'Rec':"2"},
    {'Descricao': "Remover flutuante", 'Dimensoes': "Até 500 tubos", 'Duracao': "2,5", 'Rec':"2"},
    {'Descricao': "Remover flutuante", 'Dimensoes': "501 a 1000 tubos", 'Duracao': "3", 'Rec':"2"},
    {'Descricao': "Remover flutuante", 'Dimensoes': "1001 a 1500 tubos", 'Duracao': "3,5", 'Rec':"2"},
    {'Descricao': "Remover flutuante", 'Dimensoes': "Acima de 1500 tubos", 'Duracao': "3,5", 'Rec':"2"},
    {'Descricao': "Instalar flutuante", 'Dimensoes': "Até 500 tubos", 'Duracao': "3", 'Rec':"2"},
    {'Descricao': "Instalar flutuante", 'Dimensoes': "501 a 1000 tubos", 'Duracao': "3,5", 'Rec':"2"},
    {'Descricao': "Instalar flutuante", 'Dimensoes': "1001 a 1500 tubos", 'Duracao': "3,5", 'Rec':"2"},
    {'Descricao': "Instalar flutuante", 'Dimensoes': "Acima de 1500 tubos", 'Duracao': "4", 'Rec':"2"},
    {'Descricao': "1o. Teste hidrostático", 'Dimensoes': "Até 500 tubos", 'Duracao': "3", 'Rec':"2"},
    {'Descricao': "1o. Teste hidrostático", 'Dimensoes': "501 a 1000 tubos", 'Duracao': "4", 'Rec':"2"},
    {'Descricao': "1o. Teste hidrostático", 'Dimensoes': "1001 a 1500 tubos", 'Duracao': "6", 'Rec':"2"},
    {'Descricao': "1o. Teste hidrostático", 'Dimensoes': "Acima de 1500 tubos", 'Duracao': "8", 'Rec':"2"},
    {'Descricao': "2o. Teste hidrostático", 'Dimensoes': "Até 500 tubos", 'Duracao': "4", 'Rec':"2"},
    {'Descricao': "2o. Teste hidrostático", 'Dimensoes': "501 a 1000 tubos", 'Duracao': "5", 'Rec':"2"},
    {'Descricao': "2o. Teste hidrostático", 'Dimensoes': "1001 a 1500 tubos", 'Duracao': "6", 'Rec':"2"},
    {'Descricao': "2o. Teste hidrostático", 'Dimensoes': "Acima de 1500 tubos", 'Duracao': "8", 'Rec':"2"},
    {'Descricao': "3o. Teste hidrostático", 'Dimensoes': "Até 500 tubos", 'Duracao': "3", 'Rec':"2"},
    {'Descricao': "3o. Teste hidrostático", 'Dimensoes': "501 a 1000 tubos", 'Duracao': "4", 'Rec':"2"},
    {'Descricao': "3o. Teste hidrostático", 'Dimensoes': "1001 a 1500 tubos", 'Duracao': "5", 'Rec':"2"},
    {'Descricao': "3o. Teste hidrostático", 'Dimensoes': "Acima de 1500 tubos", 'Duracao': "6", 'Rec':"2"}
])

# Função para exibir o formulário baseado nos dados
def show_exec_atividades_Trocadores_De_Calor_form():
    st.subheader("Formulário: Execução de Trocadores de Calor")

    # Seleção de Atividade
    vardescricao = st.selectbox("Descrição:", exec_atividades_Trocadores_De_Calor['Descricao'].unique())

    # Filtrar as opções da Classe de Pressão com base na 'atividade'
    dimensoes_opcoes = exec_atividades_Trocadores_De_Calor[exec_atividades_Trocadores_De_Calor['Descricao'] == vardescricao]['Dimensoes'].unique()
    dimensoes = st.selectbox("Dimensões:", dimensoes_opcoes)

    # Filtrar os dados da tabela com base nas seleções
    atividade_selecionada = exec_atividades_Trocadores_De_Calor[(exec_atividades_Trocadores_De_Calor['Descricao'] == vardescricao) & 
                                                          (exec_atividades_Trocadores_De_Calor['Dimensoes'] == dimensoes)].iloc[0]
    
    # Exibir os resultados da consulta
    st.write(f"Duração (hs): {atividade_selecionada['Duracao']}")
    st.write(f"Qtde Recursos: {atividade_selecionada['Rec']}")
    
    # Calcular Tempo Estimado
    if st.button("Calcular Tempo Estimado"):
        resultado = float(atividade_selecionada['Rec']) * float(atividade_selecionada['Duracao'].replace(',', '.'))
        st.success(f"Tempo Estimado: {round(resultado, 2)} horas")

# Função principal que chama o formulário
def main():
    show_exec_atividades_Trocadores_De_Calor_form()

if __name__ == "__main__":
    main()
