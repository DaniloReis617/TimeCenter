import streamlit as st
import pandas as pd
import math

# Função para exibir o formulário baseado nos dados
def show_andaime_form():
    # Título do aplicativo
    st.subheader("Formulário de Cálculo de Andaimes")

    # Entradas de dados
    col1, col2 = st.columns(2)
    with col1:
        altura = st.number_input("Altura (A) em metros", min_value=0.25, step=0.25)
        largura = st.number_input("Largura (L) em metros", min_value=0.0, step=0.1)
        comprimento = st.number_input("Comprimento (C) em metros", min_value=0.0, step=0.1)
        
    with col2:
        qtd_andaime = st.number_input("Qtde de Andaimes", min_value=1, step=1)
        quant_patamar = st.number_input("Qtde de Patamares", min_value=1, step=1)
        recursos = st.number_input("Recursos", min_value=1, step=1)

    # Variável de controle para saber se o botão foi pressionado
    if st.button("Calcular"):
        # Cálculos dos campos
        gc = altura + 1.5  # Guarda Corpo
        ext_lat = (largura + 0.25) * (comprimento + 0.25)  # Extensão Lateral
        quant_m3 = gc * ext_lat * qtd_andaime  # Quantidade em m³
        fator_conv_ml_sem_gc = altura * largura * comprimento * 4  # Fator sem GC
        fator_conv_ml_com_gc = quant_m3 * 4  # Fator com GC
        tipo_tubular = fator_conv_ml_com_gc * 0.3  # Tubular 30%
        tipo_encaixe = fator_conv_ml_com_gc * 0.7  # Encaixe 70%
        quant_prancha = (largura / 0.285) + 0.5  # Quantidade de Pranchas
        prancha_ml_sgc = comprimento * quant_patamar * quant_prancha  # Prancha ml
        rodape_ml_sgc = (2 * (largura + comprimento)) * quant_patamar  # Rodapé ml
        brac_fixa = tipo_tubular * 0.8  # Braçadeira Fixa
        brac_gir = tipo_tubular * 0.2  # Braçadeira Giratória

        # Produtividade de Montagem e Desmontagem
        prod_ma_mont_h = math.ceil(fator_conv_ml_com_gc / (270 / 60))  # Prod MA Montagem em horas (arredondado para cima)
        prod_ma_mont_d = math.ceil(prod_ma_mont_h / (480 / 60))  # Prod MA Montagem em dias (8h = 1 dia, arredondado para cima)
        prod_ma_desmont_h = math.ceil(fator_conv_ml_com_gc / (310 / 60))  # Prod MA Desmontagem em horas (arredondado para cima)
        prod_ma_desmont_d = math.ceil(prod_ma_desmont_h / (480 / 60))  # Prod MA Desmontagem em dias (8h = 1 dia, arredondado para cima)
        
        # Produtividade da Equipe
        prod_equipe_mont_d = math.ceil(prod_ma_mont_d / recursos)  # Prod Equipe Montagem em dias (arredondado para cima)
        prod_equipe_desmont_d = math.ceil(prod_ma_desmont_d / recursos)  # Prod Equipe Desmontagem em dias (arredondado para cima)

        # Função para converter dias decimais para dias, horas e minutos (8 horas = 1 dia)
        def converter_para_dias_horas_minutos(valor_em_dias):
            dias = int(valor_em_dias)
            horas_decimais = (valor_em_dias - dias) * 8  # Convertendo para horas totais (8 horas = 1 dia)
            horas = int(horas_decimais)
            minutos = int((horas_decimais - horas) * 60)
            return f"{dias} dias, {horas} horas, {minutos} minutos"

        # Conversão dos resultados
        tempo_montagem_formatado = converter_para_dias_horas_minutos(prod_equipe_mont_d)
        tempo_desmontagem_formatado = converter_para_dias_horas_minutos(prod_equipe_desmont_d)

        # Exibição de explicação para o usuário
        st.markdown("### Explicação dos Cálculos:")
        st.markdown("""
        Este formulário realiza uma série de cálculos para estimar as **necessidades** e o **tempo de trabalho** 
        para montar e desmontar andaimes, baseado nas dimensões e quantidade informada. Aqui está o que cada cálculo representa:
        
        - **GC (Guarda Corpo)**: O comprimento do guarda-corpo necessário para a segurança, com base na altura do andaime.
        - **Extensão Lateral**: O cálculo da área lateral que o andaime ocupará, considerando as dimensões fornecidas.
        - **Quantidade (m³)**: O volume total de material necessário para o andaime.
        - **Fator de Conversão**: Relacionado ao número de metros lineares necessários para montar o andaime sem ou com guarda-corpo.
        - **Tipo Tubular e Encaixe**: A distribuição dos materiais, com 30% para componentes tubulares e 70% para componentes de encaixe.
        - **Quantidade de Pranchas**: O número de pranchas necessárias para o andaime, baseado na largura informada.
        - **Prancha e Rodapé (ml)**: O cálculo dos metros lineares de prancha e rodapé necessários para a montagem.
        - **Braçadeiras Fixa e Giratória**: A quantidade de braçadeiras necessária para fixar o andaime, com base nos materiais tubulares.
        - **Produtividade de Montagem/Desmontagem**: O tempo estimado para a montagem e desmontagem, considerando a produtividade dos recursos.

        Esses cálculos são essenciais para **planejar a logística** do andaime, **dimensionar materiais** adequados, e **estimativas de tempo** para a equipe envolvida na montagem/desmontagem. A precisão desses valores ajuda a **evitar desperdícios** e **garantir eficiência** durante a execução do projeto.
        """)

        # Exibindo os resultados com layout de cards
        st.markdown("### Resultados Calculados:")

        # Criar layout com colunas para exibir os resultados de forma mais organizada
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**GC (Guarda Corpo):** {round(gc, 2)} m")
            st.markdown(f"**Extensão Lateral:** {round(ext_lat, 2)} m²")
            st.markdown(f"**Quantidade (m³):** {round(quant_m3, 2)} m³")
            st.markdown(f"**Fator Conv. (ml) sem GC:** {round(fator_conv_ml_sem_gc, 2)} ml")
            st.markdown(f"**Fator Conv. (ml) com GC:** {round(fator_conv_ml_com_gc, 2)} ml")
            st.markdown(f"**Tipo Tubular (30%):** {round(tipo_tubular, 2)} ml")
            st.markdown(f"**Tipo Encaixe (70%):** {round(tipo_encaixe, 2)} ml")
            st.markdown(f"**Quantidade de Pranchas:** {round(quant_prancha, 2)} unidades")
            
        with col2:
            st.markdown(f"**Prancha ml (sem GC):** {round(prancha_ml_sgc, 2)} ml")
            st.markdown(f"**Rodapé ml (sem GC):** {round(rodape_ml_sgc, 2)} ml")
            st.markdown(f"**Braçadeira Fixa (And Tubular):** {round(brac_fixa, 2)} ml")
            st.markdown(f"**Braçadeira Giratória (And Tubular):** {round(brac_gir, 2)} ml")
            st.markdown(f"**Prod. MA Montagem (h):** {round(prod_ma_mont_h, 2)} h")
            st.markdown(f"**Prod. MA Montagem (d):** {round(prod_ma_mont_d, 2)} dias")
            st.markdown(f"**Prod. MA Desmontagem (h):** {round(prod_ma_desmont_h, 2)} h")
            st.markdown(f"**Prod. MA Desmontagem (d):** {round(prod_ma_desmont_d, 2)} dias")

        # Exibindo tempo de montagem e desmontagem
        st.markdown(f"**Tempo para Montagem da Equipe:** {tempo_montagem_formatado}")
        st.markdown(f"**Tempo para Desmontagem da Equipe:** {tempo_desmontagem_formatado}")

    # Botão de reset
    if st.button("Voltar"):
        st.session_state['show_form_servico_andaime'] = False
        st.rerun()

# Função principal que chama o formulário
def main():
    show_andaime_form()

if __name__ == "__main__":
    main()
