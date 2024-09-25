import streamlit as st

def show_execucao_atividades_form():
    st.subheader("Formulário: Execução de Atividades")

    # Exemplo de dados para o formulário de Execução de Atividades
    atividades = ["Raqueteamento", "Desraqueteamento", "Uniões Flangeadas"]
    classes_pressao = ["Classe A", "Classe B", "Classe C"]
    diametros = ["1/2\"", "3/4\"", "1\"", "2\""]

    # Organizar os campos em duas colunas
    col1, col2 = st.columns(2)

    # Coluna 1
    with col1:
        atividade = st.selectbox("Atividade:", atividades)
        diametro = st.selectbox("Diâmetro Externo:", diametros)
        duracao_horas = st.number_input("Duração (hs):", min_value=0.0, step=0.5)

    # Coluna 2
    with col2:
        classe_pressao = st.selectbox("Classe de Pressão:", classes_pressao)
        quantidade = st.number_input("Qt Rec. (Ca):", min_value=0)
        hh = st.number_input("HH:", min_value=0.0, step=0.5)

    # Colocar os botões lado a lado
    col_calcular, col_voltar = st.columns([1, 1])

    # Botão de calcular tempo estimado
    with col_calcular:
        if st.button("Calcular"):
            resultado_horas = duracao_horas * quantidade
            st.success(f"Tempo Estimado: {round(resultado_horas, 2)} horas")

    # Botão de voltar
    with col_voltar:
        if st.button("Voltar"):
            st.session_state['show_form_execucao'] = False
            st.rerun()

# Função principal que chama a tela de adicionar nota
def main():
    show_execucao_atividades_form()

if __name__ == "__main__":
    main()