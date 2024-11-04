import streamlit as st
import pandas as pd

# Dados da aplicação de isolamento térmico
isolamento_termico = pd.DataFrame([
    {'Descrição': 'Tubulação até 4"', 'Quant. (ml)': 18, 'Qt Rec. (Is/Fu)': 2, 'Tipo de Material': 'Silicato de Cálcio'},
    {'Descrição': 'Tubulação de 5" a 8"', 'Quant. (ml)': 15, 'Qt Rec. (Is/Fu)': 2, 'Tipo de Material': 'Silicato de Cálcio'},
    {'Descrição': 'Tubulação de 10" até 16"', 'Quant. (ml)': 12, 'Qt Rec. (Is/Fu)': 2, 'Tipo de Material': 'Silicato de Cálcio'},
    {'Descrição': 'Tubulação de 18" até 24"', 'Quant. (ml)': 10, 'Qt Rec. (Is/Fu)': 2, 'Tipo de Material': 'Silicato de Cálcio'},
    {'Descrição': 'Instalação funilaria', 'Quant. (ml)': 20, 'Qt Rec. (Is/Fu)': 2, 'Tipo de Material': 'Silicato de Cálcio'},
    {'Descrição': 'Tubulação até 4"', 'Quant. (ml)': 40, 'Qt Rec. (Is/Fu)': 2, 'Tipo de Material': 'Manta de Fibra Cerâmica'},
    {'Descrição': 'Tubulação de 5" a 8"', 'Quant. (ml)': 36, 'Qt Rec. (Is/Fu)': 2, 'Tipo de Material': 'Manta de Fibra Cerâmica'},
    {'Descrição': 'Tubulação de 10" até 16"', 'Quant. (ml)': 30, 'Qt Rec. (Is/Fu)': 2, 'Tipo de Material': 'Manta de Fibra Cerâmica'},
    {'Descrição': 'Tubulação de 18" até 24"', 'Quant. (ml)': 20, 'Qt Rec. (Is/Fu)': 2, 'Tipo de Material': 'Manta de Fibra Cerâmica'},
    {'Descrição': 'Instalação funilaria', 'Quant. (ml)': 20, 'Qt Rec. (Is/Fu)': 2, 'Tipo de Material': 'Manta de Fibra Cerâmica'}
])

def show_isolamento_termico_form():
    st.subheader("Formulário: Aplicação de Isolamento Térmico")

    # Tipo de Material - Seleção Distinta
    tipo_material = st.selectbox("Tipo de Material:", isolamento_termico['Tipo de Material'].unique())

    # Filtrar as descrições com base no tipo de material selecionado
    descricoes_disponiveis = isolamento_termico[isolamento_termico['Tipo de Material'] == tipo_material]['Descrição'].unique()
    descricao = st.selectbox("Descrição:", descricoes_disponiveis)

    # Buscar os detalhes com base nas seleções
    isolamento_selecionado = isolamento_termico[(isolamento_termico['Tipo de Material'] == tipo_material) & 
                                                (isolamento_termico['Descrição'] == descricao)].iloc[0]
    
    # Mostrar quantidade de material e quantidade de recursos conforme a seleção
    st.text(f"Qtde (ml): {isolamento_selecionado['Quant. (ml)']}")
    st.text(f"Qtde de Recursos (Is/Fu): {isolamento_selecionado['Qt Rec. (Is/Fu)']}")
    
    # Campo para inserir quantidade de material
    qtd_ml = st.number_input("Qtde de Recursos (Is/Fu):", min_value=1)
    
    # Calcular Tempo Estimado
    if st.button("Calcular"):
        # Calcular o tempo estimado com base na quantidade e nos recursos
        tempo_estimado = qtd_ml / isolamento_selecionado['Quant. (ml)'] * isolamento_selecionado['Qt Rec. (Is/Fu)']
        st.success(f"Tempo: {round(tempo_estimado, 2)} horas")

    # Botão de reset
    if st.button("Voltar"):
        st.session_state['show_form_servico_isolamento'] = False
        st.rerun()
    

# Função principal que chama o formulário
def main():
    show_isolamento_termico_form()

if __name__ == "__main__":
    main()
