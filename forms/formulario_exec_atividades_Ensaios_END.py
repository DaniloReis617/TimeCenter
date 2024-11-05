import streamlit as st
import pandas as pd

# Dados dos Ensaios Não Destrutivos (ENDs)
exec_atividades_END = pd.DataFrame([
    {'Ensaio': 'VA', 'Preparação Equip. (h)': 0, 'ml/h': 12.0, 'Tubulação': 'Até 24"', 'Tempo (min)': 10.0, 'Rec. (Ca)': 0, 'Prep. Superf. Tempo (min)': 0},
    {'Ensaio': 'VA', 'Preparação Equip. (h)': 0, 'ml/h': 12.0, 'Tubulação': '30" a 70"', 'Tempo (min)': 15.0, 'Rec. (Ca)': 0, 'Prep. Superf. Tempo (min)': 0},
    {'Ensaio': 'VS', 'Preparação Equip. (h)': 0, 'ml/h': 12.0, 'Tubulação': 'Até 24"', 'Tempo (min)': 10.0, 'Rec. (Ca)': 0, 'Prep. Superf. Tempo (min)': 0},
    {'Ensaio': 'VS', 'Preparação Equip. (h)': 0, 'ml/h': 12.0, 'Tubulação': '30" a 70"', 'Tempo (min)': 15.0, 'Rec. (Ca)': 0, 'Prep. Superf. Tempo (min)': 0},
    {'Ensaio': 'LP', 'Preparação Equip. (h)': 0, 'ml/h': 3.0, 'Tubulação': 'Até 8"', 'Tempo (min)': 45.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 5.0},
    {'Ensaio': 'LP', 'Preparação Equip. (h)': 0, 'ml/h': 3.0, 'Tubulação': '10" a 14"', 'Tempo (min)': 50.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 10.0},
    {'Ensaio': 'LP', 'Preparação Equip. (h)': 0, 'ml/h': 3.0, 'Tubulação': '16" a 24"', 'Tempo (min)': 60.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 15.0},
    {'Ensaio': 'LP', 'Preparação Equip. (h)': 0, 'ml/h': 3.0, 'Tubulação': '30" a 36"', 'Tempo (min)': 70.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 20.0},
    {'Ensaio': 'LP', 'Preparação Equip. (h)': 0, 'ml/h': 3.0, 'Tubulação': '40" a 70"', 'Tempo (min)': 90.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 30.0},
    {'Ensaio': 'PM', 'Preparação Equip. (h)': 2.0, 'ml/h': 4.0, 'Tubulação': 'Até 8"', 'Tempo (min)': 15.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 5.0},
    {'Ensaio': 'PM', 'Preparação Equip. (h)': 2.0, 'ml/h': 4.0, 'Tubulação': '10" a 14"', 'Tempo (min)': 20.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 10.0},
    {'Ensaio': 'PM', 'Preparação Equip. (h)': 2.0, 'ml/h': 4.0, 'Tubulação': '16" a 24"', 'Tempo (min)': 30.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 15.0},
    {'Ensaio': 'PM', 'Preparação Equip. (h)': 2.0, 'ml/h': 4.0, 'Tubulação': '30" a 36"', 'Tempo (min)': 40.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 20.0},
    {'Ensaio': 'PM', 'Preparação Equip. (h)': 2.0, 'ml/h': 4.0, 'Tubulação': '40" a 70"', 'Tempo (min)': 50.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 30.0},
    {'Ensaio': 'US', 'Preparação Equip. (h)': 1.0, 'ml/h': 2.0, 'Tubulação': 'Até 8"', 'Tempo (min)': 30.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 10.0},
    {'Ensaio': 'US', 'Preparação Equip. (h)': 1.0, 'ml/h': 2.0, 'Tubulação': '10" a 14"', 'Tempo (min)': 40.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 15.0},
    {'Ensaio': 'US', 'Preparação Equip. (h)': 1.0, 'ml/h': 2.0, 'Tubulação': '16" a 24"', 'Tempo (min)': 50.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 20.0},
    {'Ensaio': 'US', 'Preparação Equip. (h)': 1.0, 'ml/h': 2.0, 'Tubulação': '30" a 36"', 'Tempo (min)': 60.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 30.0},
    {'Ensaio': 'US', 'Preparação Equip. (h)': 1.0, 'ml/h': 2.0, 'Tubulação': '40" a 70"', 'Tempo (min)': 90.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 40.0},
    {'Ensaio': 'Medição Dureza', 'Preparação Equip. (h)': 0, 'ml/h': 0, 'Tubulação': 'Até 8"', 'Tempo (min)': 10.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 5.0},
    {'Ensaio': 'Medição Dureza', 'Preparação Equip. (h)': 0, 'ml/h': 0, 'Tubulação': '10" a 14"', 'Tempo (min)': 15.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 10.0},
    {'Ensaio': 'Medição Dureza', 'Preparação Equip. (h)': 0, 'ml/h': 0, 'Tubulação': '16" a 24"', 'Tempo (min)': 20.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 15.0},
    {'Ensaio': 'Medição Dureza', 'Preparação Equip. (h)': 0, 'ml/h': 0, 'Tubulação': '30" a 36"', 'Tempo (min)': 25.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 20.0},
    {'Ensaio': 'Medição Dureza', 'Preparação Equip. (h)': 0, 'ml/h': 0, 'Tubulação': '40" a 70"', 'Tempo (min)': 30.0, 'Rec. (Ca)': 1.0, 'Prep. Superf. Tempo (min)': 30.0},
    {'Ensaio': 'IRIS', 'Preparação Equip. (h)': 2.0, 'ml/h': 110.0, 'Tubulação': 0, 'Tempo (min)': 0, 'Rec. (Ca)': 0, 'Prep. Superf. Tempo (min)': 0},
    {'Ensaio': 'Eddy Current', 'Preparação Equip. (h)': 2.0, 'ml/h': 220.0, 'Tubulação': 0, 'Tempo (min)': 0, 'Rec. (Ca)': 0, 'Prep. Superf. Tempo (min)': 0}
])

# Função para exibir o formulário baseado nos dados
def show_exec_atividades_END_form():
    st.subheader("Formulário: Execução de Ensaios Não Destrutivos (ENDs)")

    # Seleção de Ensaio
    var_ensaio = st.selectbox("Ensaio:", exec_atividades_END['Ensaio'].unique())

    # Filtrar as opções de Tubulação com base no Ensaio
    tubulacao_opcoes = exec_atividades_END[exec_atividades_END['Ensaio'] == var_ensaio]['Tubulação'].unique()
    var_tubulacao = st.selectbox("Tubulação:", tubulacao_opcoes)

    # Filtrar os dados da tabela com base nas seleções
    ensaio_selecionado = exec_atividades_END[(exec_atividades_END['Ensaio'] == var_ensaio) & 
                                             (exec_atividades_END['Tubulação'] == var_tubulacao)].iloc[0]
    
    # Exibir os resultados da consulta
    st.write(f"Preparação Superfície (min): {ensaio_selecionado['Prep. Superf. Tempo (min)']}")
    st.write(f"Preparação Equipamento (h): {ensaio_selecionado['Preparação Equip. (h)']}")
    st.write(f"Qtde de Recurso: {ensaio_selecionado['Rec. (Ca)']}")
    st.write(f"Tempo de Execução (min): {ensaio_selecionado['Tempo (min)']}")

    # Campo para inserir a quantidade de Tubos
    #var_qt_tubos = st.number_input("Quantidade de Tubos:", min_value=1)

    # Converter a preparação do equipamento de horas para minutos
    preparacao_equipamento_min = float(ensaio_selecionado['Preparação Equip. (h)']) * 60
    
    # Somar os tempos de preparação
    total_preparacao_min = (
        float(ensaio_selecionado['Prep. Superf. Tempo (min)']) +
        preparacao_equipamento_min
    )
    
    # Multiplicar pelo tempo de execução considerando a quantidade de tubos
    tempo_estimado = total_preparacao_min * float(ensaio_selecionado['Tempo (min)'])

    # Condição para exibir o tempo em minutos ou horas
    if tempo_estimado < 60:
        st.success(f"Duração: {round(tempo_estimado, 2)} minutos")
    else:
        horas = tempo_estimado / 60
        st.success(f"Duração: {round(horas, 2)} horas")

# Função principal que chama o formulário
def main():
    show_exec_atividades_END_form()

if __name__ == "__main__":
    main()
