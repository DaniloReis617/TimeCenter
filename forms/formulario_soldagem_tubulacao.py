import streamlit as st
import pandas as pd

# Dados de preparação para soldagem
soldagem_tubulacao = pd.DataFrame([{'Diâmetro Nominal': '2"',
  'SCH 40 - Carbono (min)': 75,
  'SCH 40 - Inox (min)': 80,
  'SCH 40 - Aço Liga (min)': 90,
  'SCH 80 - Carbono (min)': 85,
  'SCH 80 - Inox (min)': 90,
  'SCH 80 - Aço Liga (min)': 100,
  'SCH 120 - Carbono (min)': 90,
  'SCH 120 - Inox (min)': 90,
  'SCH 120 - Aço Liga (min)': 100,
  'SCH 160 - Carbono (min)': 110,
  'SCH 160 - Inox (min)': 120,
  'SCH 160 - Aço Liga (min)': 120},
 {'Diâmetro Nominal': '2.1/2"',
  'SCH 40 - Carbono (min)': 75,
  'SCH 40 - Inox (min)': 80,
  'SCH 40 - Aço Liga (min)': 90,
  'SCH 80 - Carbono (min)': 85,
  'SCH 80 - Inox (min)': 90,
  'SCH 80 - Aço Liga (min)': 100,
  'SCH 120 - Carbono (min)': 90,
  'SCH 120 - Inox (min)': 90,
  'SCH 120 - Aço Liga (min)': 100,
  'SCH 160 - Carbono (min)': 110,
  'SCH 160 - Inox (min)': 120,
  'SCH 160 - Aço Liga (min)': 120},
 {'Diâmetro Nominal': '3"',
  'SCH 40 - Carbono (min)': 85,
  'SCH 40 - Inox (min)': 90,
  'SCH 40 - Aço Liga (min)': 100,
  'SCH 80 - Carbono (min)': 100,
  'SCH 80 - Inox (min)': 120,
  'SCH 80 - Aço Liga (min)': 120,
  'SCH 120 - Carbono (min)': 120,
  'SCH 120 - Inox (min)': 140,
  'SCH 120 - Aço Liga (min)': 140,
  'SCH 160 - Carbono (min)': 130,
  'SCH 160 - Inox (min)': 160,
  'SCH 160 - Aço Liga (min)': 160},
 {'Diâmetro Nominal': '3.1/2"',
  'SCH 40 - Carbono (min)': 85,
  'SCH 40 - Inox (min)': 90,
  'SCH 40 - Aço Liga (min)': 100,
  'SCH 80 - Carbono (min)': 100,
  'SCH 80 - Inox (min)': 120,
  'SCH 80 - Aço Liga (min)': 120,
  'SCH 120 - Carbono (min)': 120,
  'SCH 120 - Inox (min)': 140,
  'SCH 120 - Aço Liga (min)': 140,
  'SCH 160 - Carbono (min)': 130,
  'SCH 160 - Inox (min)': 160,
  'SCH 160 - Aço Liga (min)': 160},
 {'Diâmetro Nominal': '4"',
  'SCH 40 - Carbono (min)': 130,
  'SCH 40 - Inox (min)': 140,
  'SCH 40 - Aço Liga (min)': 150,
  'SCH 80 - Carbono (min)': 150,
  'SCH 80 - Inox (min)': 160,
  'SCH 80 - Aço Liga (min)': 180,
  'SCH 120 - Carbono (min)': 160,
  'SCH 120 - Inox (min)': 180,
  'SCH 120 - Aço Liga (min)': 200,
  'SCH 160 - Carbono (min)': 210,
  'SCH 160 - Inox (min)': 220,
  'SCH 160 - Aço Liga (min)': 220},
 {'Diâmetro Nominal': '5"',
  'SCH 40 - Carbono (min)': 130,
  'SCH 40 - Inox (min)': 140,
  'SCH 40 - Aço Liga (min)': 150,
  'SCH 80 - Carbono (min)': 150,
  'SCH 80 - Inox (min)': 160,
  'SCH 80 - Aço Liga (min)': 180,
  'SCH 120 - Carbono (min)': 160,
  'SCH 120 - Inox (min)': 180,
  'SCH 120 - Aço Liga (min)': 200,
  'SCH 160 - Carbono (min)': 210,
  'SCH 160 - Inox (min)': 220,
  'SCH 160 - Aço Liga (min)': 220},
 {'Diâmetro Nominal': '6"',
  'SCH 40 - Carbono (min)': 150,
  'SCH 40 - Inox (min)': 170,
  'SCH 40 - Aço Liga (min)': 180,
  'SCH 80 - Carbono (min)': 180,
  'SCH 80 - Inox (min)': 190,
  'SCH 80 - Aço Liga (min)': 200,
  'SCH 120 - Carbono (min)': 200,
  'SCH 120 - Inox (min)': 210,
  'SCH 120 - Aço Liga (min)': 210,
  'SCH 160 - Carbono (min)': 210,
  'SCH 160 - Inox (min)': 230,
  'SCH 160 - Aço Liga (min)': 230},
 {'Diâmetro Nominal': '8"',
  'SCH 40 - Carbono (min)': 200,
  'SCH 40 - Inox (min)': 200,
  'SCH 40 - Aço Liga (min)': 200,
  'SCH 80 - Carbono (min)': 215,
  'SCH 80 - Inox (min)': 220,
  'SCH 80 - Aço Liga (min)': 230,
  'SCH 120 - Carbono (min)': 230,
  'SCH 120 - Inox (min)': 240,
  'SCH 120 - Aço Liga (min)': 260,
  'SCH 160 - Carbono (min)': 250,
  'SCH 160 - Inox (min)': 260,
  'SCH 160 - Aço Liga (min)': 280},
 {'Diâmetro Nominal': '10"',
  'SCH 40 - Carbono (min)': 240,
  'SCH 40 - Inox (min)': 260,
  'SCH 40 - Aço Liga (min)': 260,
  'SCH 80 - Carbono (min)': 270,
  'SCH 80 - Inox (min)': 280,
  'SCH 80 - Aço Liga (min)': 300,
  'SCH 120 - Carbono (min)': 300,
  'SCH 120 - Inox (min)': 310,
  'SCH 120 - Aço Liga (min)': 320,
  'SCH 160 - Carbono (min)': 320,
  'SCH 160 - Inox (min)': 340,
  'SCH 160 - Aço Liga (min)': 340},
 {'Diâmetro Nominal': '12"',
  'SCH 40 - Carbono (min)': 280,
  'SCH 40 - Inox (min)': 300,
  'SCH 40 - Aço Liga (min)': 300,
  'SCH 80 - Carbono (min)': 310,
  'SCH 80 - Inox (min)': 320,
  'SCH 80 - Aço Liga (min)': 320,
  'SCH 120 - Carbono (min)': 330,
  'SCH 120 - Inox (min)': 340,
  'SCH 120 - Aço Liga (min)': 340,
  'SCH 160 - Carbono (min)': 340,
  'SCH 160 - Inox (min)': 360,
  'SCH 160 - Aço Liga (min)': 360},
 {'Diâmetro Nominal': '14"',
  'SCH 40 - Carbono (min)': 300,
  'SCH 40 - Inox (min)': 320,
  'SCH 40 - Aço Liga (min)': 350,
  'SCH 80 - Carbono (min)': 350,
  'SCH 80 - Inox (min)': 370,
  'SCH 80 - Aço Liga (min)': 370,
  'SCH 120 - Carbono (min)': 380,
  'SCH 120 - Inox (min)': 390,
  'SCH 120 - Aço Liga (min)': 390,
  'SCH 160 - Carbono (min)': 400,
  'SCH 160 - Inox (min)': 420,
  'SCH 160 - Aço Liga (min)': 420},
 {'Diâmetro Nominal': '16"',
  'SCH 40 - Carbono (min)': 380,
  'SCH 40 - Inox (min)': 390,
  'SCH 40 - Aço Liga (min)': 400,
  'SCH 80 - Carbono (min)': 410,
  'SCH 80 - Inox (min)': 420,
  'SCH 80 - Aço Liga (min)': 420,
  'SCH 120 - Carbono (min)': 430,
  'SCH 120 - Inox (min)': 440,
  'SCH 120 - Aço Liga (min)': 440,
  'SCH 160 - Carbono (min)': 440,
  'SCH 160 - Inox (min)': 450,
  'SCH 160 - Aço Liga (min)': 460},
 {'Diâmetro Nominal': '18"',
  'SCH 40 - Carbono (min)': 420,
  'SCH 40 - Inox (min)': 440,
  'SCH 40 - Aço Liga (min)': 440,
  'SCH 80 - Carbono (min)': 440,
  'SCH 80 - Inox (min)': 450,
  'SCH 80 - Aço Liga (min)': 470,
  'SCH 120 - Carbono (min)': 460,
  'SCH 120 - Inox (min)': 470,
  'SCH 120 - Aço Liga (min)': 490,
  'SCH 160 - Carbono (min)': 500,
  'SCH 160 - Inox (min)': 510,
  'SCH 160 - Aço Liga (min)': 520},
 {'Diâmetro Nominal': '20"',
  'SCH 40 - Carbono (min)': 460,
  'SCH 40 - Inox (min)': 480,
  'SCH 40 - Aço Liga (min)': 500,
  'SCH 80 - Carbono (min)': 500,
  'SCH 80 - Inox (min)': 520,
  'SCH 80 - Aço Liga (min)': 520,
  'SCH 120 - Carbono (min)': 520,
  'SCH 120 - Inox (min)': 540,
  'SCH 120 - Aço Liga (min)': 540,
  'SCH 160 - Carbono (min)': 540,
  'SCH 160 - Inox (min)': 560,
  'SCH 160 - Aço Liga (min)': 560},
 {'Diâmetro Nominal': '24"',
  'SCH 40 - Carbono (min)': 540,
  'SCH 40 - Inox (min)': 560,
  'SCH 40 - Aço Liga (min)': 560,
  'SCH 80 - Carbono (min)': 600,
  'SCH 80 - Inox (min)': 620,
  'SCH 80 - Aço Liga (min)': 620,
  'SCH 120 - Carbono (min)': 620,
  'SCH 120 - Inox (min)': 630,
  'SCH 120 - Aço Liga (min)': 650,
  'SCH 160 - Carbono (min)': 680,
  'SCH 160 - Inox (min)': 700,
  'SCH 160 - Aço Liga (min)': 720}])

def show_soldagem_tubulacao_form():
    st.subheader("Formulário: Soldagem de Tubulação")

    # Selecionar o diâmetro nominal
    diametro_nominal = st.selectbox("Diâmetro Nominal:", soldagem_tubulacao['Diâmetro Nominal'].unique())

    # Filtrar com base no diâmetro selecionado
    soldagem_selecionada = soldagem_tubulacao[soldagem_tubulacao['Diâmetro Nominal'] == diametro_nominal].iloc[0]
    
    # Mostrar as informações para cada tipo de material
    st.text(f"SCH 40 - Carbono (min): {soldagem_selecionada['SCH 40 - Carbono (min)']}")
    st.text(f"SCH 40 - Inox (min): {soldagem_selecionada['SCH 40 - Inox (min)']}")
    st.text(f"SCH 40 - Aço Liga (min): {soldagem_selecionada['SCH 40 - Aço Liga (min)']}")
    st.text(f"SCH 80 - Carbono (min): {soldagem_selecionada['SCH 80 - Carbono (min)']}")
    st.text(f"SCH 80 - Inox (min): {soldagem_selecionada['SCH 80 - Inox (min)']}")
    st.text(f"SCH 80 - Aço Liga (min): {soldagem_selecionada['SCH 80 - Aço Liga (min)']}")
    st.text(f"SCH 120 - Carbono (min): {soldagem_selecionada['SCH 120 - Carbono (min)']}")
    st.text(f"SCH 120 - Inox (min): {soldagem_selecionada['SCH 120 - Inox (min)']}")
    st.text(f"SCH 120 - Aço Liga (min): {soldagem_selecionada['SCH 120 - Aço Liga (min)']}")
    st.text(f"SCH 160 - Carbono (min): {soldagem_selecionada['SCH 160 - Carbono (min)']}")
    st.text(f"SCH 160 - Inox (min): {soldagem_selecionada['SCH 160 - Inox (min)']}")
    st.text(f"SCH 160 - Aço Liga (min): {soldagem_selecionada['SCH 160 - Aço Liga (min)']}")

    # Campo para inserir a quantidade de soldagem a ser realizada
    qtd_soldagem = st.number_input("Quantidade de Soldagem (min):", min_value=1)
    
    # Calcular o tempo estimado
    if st.button("Calcular"):
        tempo_estimado = qtd_soldagem * soldagem_selecionada['SCH 40 - Carbono (min)']
        # Condição para exibir o tempo em minutos ou horas
        if tempo_estimado < 60:
            st.success(f"Tempo: {round(tempo_estimado, 2)} minutos")
        else:
            horas = tempo_estimado / 60
            st.success(f"Tempo: {round(horas, 2)} horas")

# Função principal que chama o formulário
def main():
    show_soldagem_tubulacao_form()

if __name__ == "__main__":
    main()
