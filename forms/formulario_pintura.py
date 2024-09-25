import streamlit as st

def show_servico_pintura_form():
    st.subheader("Formulário: Serviço de Pintura")

    # Exemplo de dados para o formulário de Serviço de Pintura
    etapas = ["Preparação de Superfície", "Método de Aplicação"]
    tipos = {
        "Preparação de Superfície": ["Ferramenta manual", "Pistola airless"],
        "Método de Aplicação": ["Pistola airless", "Rolo"]
    }
    
    # Organizar os campos em duas colunas
    col1, col2 = st.columns(2)
    
    # Coluna 1
    with col1:
        etapa = st.selectbox("Etapa:", etapas)
        m2_dia = st.number_input("M² por dia:", min_value=1, value=50)
        pintores = st.number_input("Número de Pintores:", min_value=1, value=2)

    # Coluna 2
    with col2:
        tipo = st.selectbox("Tipo:", tipos[etapa])
        qtd_m2 = st.number_input("QTD M²:", min_value=0)
        ajudantes = st.number_input("Número de Ajudantes:", min_value=0, value=1)

    # Colocar os botões lado a lado
    col_calcular, col_voltar = st.columns([1, 1])
    
    # Botão de calcular tempo estimado
    with col_calcular:
        if st.button("Calcular"):
            resultado_hora = m2_dia / 8
            resultado = qtd_m2 * resultado_hora
            st.success(f"Tempo Estimado: {round(resultado, 2)} horas")

    # Botão de voltar
    with col_voltar:
        if st.button("Voltar"):
            st.session_state['show_form'] = False
            st.rerun()  # Atualiza a interface imediatamente

# Função principal que chama a tela de adicionar nota
def main():
    show_servico_pintura_form()

if __name__ == "__main__":
    main()
