import streamlit as st
import pandas as pd

# Dados do serviço de pintura
servico_pintura = pd.DataFrame([
    {"Etapa": "Preparação de Superfície", "Tipo": "Ferramenta manual", "m2_dia": 6, "Pintores": 1, "Ajudante": 0},
    {"Etapa": "Preparação de Superfície", "Tipo": "Ferramenta mecânica", "m2_dia": 10, "Pintores": 1, "Ajudante": 0},
    {"Etapa": "Preparação de Superfície", "Tipo": "Jateamento abrasivo (cabine de jato)", "m2_dia": 30, "Pintores": 2, "Ajudante": 1},
    {"Etapa": "Preparação de Superfície", "Tipo": "Hidrojateamento (pistola)", "m2_dia": 20, "Pintores": 2, "Ajudante": 1},
    {"Etapa": "Preparação de Superfície", "Tipo": "Hidrojateamento (robô)", "m2_dia": 35, "Pintores": 2, "Ajudante": 1},
    {"Etapa": "Método de Aplicação", "Tipo": "Pistola convencional", "m2_dia": 75, "Pintores": 2, "Ajudante": 1},
    {"Etapa": "Método de Aplicação", "Tipo": "Pitola air less", "m2_dia": 160, "Pintores": 2, "Ajudante": 1},
    {"Etapa": "Método de Aplicação", "Tipo": "Rolo", "m2_dia": 30, "Pintores": 1, "Ajudante": 0},
    {"Etapa": "Método de Aplicação", "Tipo": "Trincha (stripe coat)", "m2_dia": 20, "Pintores": 1, "Ajudante": 0}
])

def show_servico_pintura_form():
    st.subheader("Formulário: Serviço de Pintura")

    # Etapa - Seleção Distinta
    etapa = st.selectbox("Etapa:", servico_pintura['Etapa'].unique())

    # Filtrar os tipos com base na etapa selecionada
    tipos_disponiveis = servico_pintura[servico_pintura['Etapa'] == etapa]['Tipo'].unique()
    tipo = st.selectbox("Tipo:", tipos_disponiveis)

    # Buscar os detalhes com base nas seleções
    servico_selecionado = servico_pintura[(servico_pintura['Etapa'] == etapa) & (servico_pintura['Tipo'] == tipo)].iloc[0]
    
    # Mostrar M² Dia, Pintor e Ajudante conforme a seleção
    st.text(f"M² por Dia: {servico_selecionado['m2_dia']}")
    st.text(f"Pintores: {servico_selecionado['Pintores']}")
    st.text(f"Ajudantes: {servico_selecionado['Ajudante'] if servico_selecionado['Ajudante'] is not None else 0}")
    
    # Campo para inserir quantidade de M²
    qtd_m2 = st.number_input("Qtde M²:", min_value=1)
    
    # Calcular Tempo Estimado
    if st.button("Calcular"):
        # Calcular a produtividade por hora
        produtividade_por_hora = servico_selecionado['m2_dia'] / 8
        tempo_estimado = qtd_m2 / produtividade_por_hora if qtd_m2 > 0 else 0
        st.success(f"Tempo Estimado: {round(tempo_estimado, 2)} horas")

    # Botão de reset
    if st.button("Voltar"):
        st.session_state['show_form'] = False
        st.rerun()
    

# Função principal que chama o formulário
def main():
    show_servico_pintura_form()

if __name__ == "__main__":
    main()
