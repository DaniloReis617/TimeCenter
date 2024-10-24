import streamlit as st
import pandas as pd

# Dados da execução de 'atividade's
exec_atividades_Servico_Limpeza_Hidrojato = pd.DataFrame([
    {'Descricao': "Limpeza Padrão", 'CapBomba': "A partir de 10.000 PSI", 'TempoPorTubo': 1},
    {'Descricao': "Limp. Para IRIS", 'CapBomba': "A partir de 20.000 PSI", 'TempoPorTubo': 2}
])

# Função para exibir o formulário baseado nos dados
def show_exec_atividades_Servico_Limpeza_Hidrojato_form():
    st.subheader("Formulário: Execução de Servico de Limpeza Hidrojato")

    # Seleção de Atividade
    vardescricao = st.selectbox("Descrição:", exec_atividades_Servico_Limpeza_Hidrojato['Descricao'].unique())

    # Filtrar as opções da Classe de Pressão com base na 'atividade'
    CapBomba_opcoes = exec_atividades_Servico_Limpeza_Hidrojato[exec_atividades_Servico_Limpeza_Hidrojato['Descricao'] == vardescricao]['CapBomba'].unique()
    CapBomba = st.selectbox("Dimensões:", CapBomba_opcoes)

    # Filtrar os dados da tabela com base nas seleções
    atividade_selecionada = exec_atividades_Servico_Limpeza_Hidrojato[(exec_atividades_Servico_Limpeza_Hidrojato['Descricao'] == vardescricao) & 
                                                          (exec_atividades_Servico_Limpeza_Hidrojato['CapBomba'] == CapBomba)].iloc[0]
    
    # Exibir os resultados da consulta
    st.write(f"Duração (hs): {atividade_selecionada['TempoPorTubo']}")

    # Campo para inserir quantidade de M²
    var_Tempo_Por_Tubo = st.number_input("Qt Rec:", min_value=1)
    
    # Calcular Tempo Estimado
    if st.button("Calcular"):
        resultado = float(var_Tempo_Por_Tubo) * float(atividade_selecionada['TempoPorTubo'])
        st.success(f"Tempo Estimado: {round(resultado, 2)} horas")

# Função principal que chama o formulário
def main():
    show_exec_atividades_Servico_Limpeza_Hidrojato_form()

if __name__ == "__main__":
    main()
