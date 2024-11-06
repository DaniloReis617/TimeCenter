import streamlit as st 
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import apply_custom_style_and_header

def convert_to_float(value):
    # Remove 'R$', substitui ',' por '.' e converte para float
    try:
        return float(str(value).replace('R$', '').replace(',', '').strip())
    except ValueError:
        return None  # Retorna None se não for possível converter

def convert_percent_to_float(value):
    # Remove '%' e converte para decimal, por exemplo, "5%" para 0.05
    try:
        return float(str(value).replace('%', '').replace(',', '.').strip()) / 100
    except ValueError:
        return None

def dashboard_screen():
    apply_custom_style_and_header("Tela de Dashboard")

    # Verifica se as informações do projeto e os dados carregados estão disponíveis
    if 'projeto_info' in st.session_state and 'project_data' in st.session_state:
        projeto_info = st.session_state['projeto_info']
        st.header(f"Projeto: {projeto_info['TX_DESCRICAO']}")

        # Usar dados do projeto já carregados em `st.session_state`
        df_Projeto = st.session_state['project_data']['dados_projetos']
        df_Projeto_total = st.session_state['project_data']['projeto_total']
        df_Projeto_total_data = st.session_state['project_data']['projeto_total_data']  
        df_Projeto_despesa = st.session_state['project_data']['projeto_despesa'] 
        df_Projeto_despesa_total = st.session_state['project_data']['projeto_despesa_total']   
        df_nota_principal = st.session_state['project_data']['vw_notas_de_manutencao']             
        
    else:
        st.error("Selecione um projeto na tela inicial.")
        return

    # Criar as abas
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
        ["Projeto Geral",
        "Projeto Despesas",
        "Nota - Principal",
        "Nota - Apoios",
        "Nota - Informativos",
        "Nota - Recursos",
        "Nota - HH e Custos",
        "Nota - Top 5"
        ])
    
    # Conteúdo da aba 1
    with tab1:
        # Aplicar o estilo e o cabeçalho personalizado
        st.title("Dashboard de Projeto")

            # Garantir que as colunas monetárias estejam em formato numérico
        if 'VL_VALOR_ORCAMENTO' in df_Projeto.columns:
            df_Projeto['VL_VALOR_ORCAMENTO'] = df_Projeto['VL_VALOR_ORCAMENTO'].apply(convert_to_float)
        
        for column in ['VL_CUSTO_TOTAL_APOIO', 'VL_CUSTO_TOTAL_MATERIAL', 'VL_DESPESA_TOTAL', 'VL_CUSTO_TOTAL_RECURSO']:
            if column in df_Projeto_total.columns:
                df_Projeto_total[column] = df_Projeto_total[column].apply(convert_to_float)

            if column in df_Projeto_total_data.columns:
                df_Projeto_total_data[column] = df_Projeto_total_data[column].apply(convert_to_float)

        # Garantir que a coluna percentual esteja em formato decimal
        if 'VL_PERCENTUAL_CONTINGENCIA' in df_Projeto.columns:
            df_Projeto['VL_PERCENTUAL_CONTINGENCIA'] = df_Projeto['VL_PERCENTUAL_CONTINGENCIA'].apply(convert_percent_to_float)

        # Verifica se o DataFrame de escopo está vazio
        if df_Projeto.empty:
            st.warning("Nenhum dado foi encontrado para o projeto selecionado.")
            return

        # Calcular o custo total do projeto
        custo_projeto_total = df_Projeto_total[['VL_CUSTO_TOTAL_APOIO', 'VL_CUSTO_TOTAL_MATERIAL', 'VL_DESPESA_TOTAL', 'VL_CUSTO_TOTAL_RECURSO']].sum().sum()

        # Dados para as métricas principais
        valor_orcamento = df_Projeto['VL_VALOR_ORCAMENTO'].sum()
        percentual_gasto = (custo_projeto_total / valor_orcamento) * 100 if valor_orcamento else 0
        percentual_contingencia = df_Projeto['VL_PERCENTUAL_CONTINGENCIA'].mean() * 100  # Multiplica por 100 para exibir como percentual
        

        # Exibir as métricas principais
        col1, col2, col3, col4 = st.columns(4)
        with st.container(border=True):
            col1.metric("Valor Orçamento", f"R$ {valor_orcamento:,.2f}")
        with st.container(border=True):            
            col2.metric("Custo Total Projeto Geral", f"R$ {custo_projeto_total:,.2f}")
        with st.container(border=True):            
            col3.metric("Percentual Gasto", f"{percentual_gasto:.2f}%")
        with st.container(border=True):            
            col4.metric("Percentual Contingência", f"{percentual_contingencia:.2f}%")

        # Gráfico de Pizza para Divisão dos Custos e Despesas
        labels = ["Custo total material", "Custo total apoio", "Custo total despesa", "Custo total recurso"]
        values = [
            df_Projeto_total['VL_CUSTO_TOTAL_MATERIAL'].sum(),
            df_Projeto_total['VL_CUSTO_TOTAL_APOIO'].sum(),
            df_Projeto_total['VL_DESPESA_TOTAL'].sum(),
            df_Projeto_total['VL_CUSTO_TOTAL_RECURSO'].sum()
        ]
        fig_pizza = px.pie(
            values=values,
            names=labels,
            hole=0.5,
            title="Divisão dos Custos e Despesas"
        )
        fig_pizza.update_traces(textposition='outside', textinfo='percent+label+value')
        with st.container(border=True):
            st.plotly_chart(fig_pizza, use_container_width=True)

        # Gráfico de Barras Empilhadas para Lançamentos por Mês com Filtro de Ano
        if 'DT_LANCAMENTO' in df_Projeto_total_data.columns:
            # Converter para datetime e extrair o ano e o mês
            df_Projeto_total_data['ANO'] = pd.to_datetime(df_Projeto_total_data['DT_LANCAMENTO'], errors='coerce').dt.year
            df_Projeto_total_data['MES'] = pd.to_datetime(df_Projeto_total_data['DT_LANCAMENTO'], errors='coerce').dt.strftime('%b')

            # Criar um filtro de ano com os anos únicos disponíveis
            anos_disponiveis = df_Projeto_total_data['ANO'].dropna().unique()
            ano_selecionado = st.selectbox("Selecione o Ano", sorted(anos_disponiveis), index=0)

            # Filtrar os dados com base no ano selecionado
            df_filtrado = df_Projeto_total_data[df_Projeto_total_data['ANO'] == ano_selecionado]

            # Preparar os dados para o gráfico de barras empilhadas
            df_barras = df_filtrado[['MES', 'VL_CUSTO_TOTAL_APOIO', 'VL_CUSTO_TOTAL_MATERIAL', 'VL_DESPESA_TOTAL', 'VL_CUSTO_TOTAL_RECURSO']]
            df_barras = df_barras.melt(id_vars="MES", var_name="Tipo de Custo", value_name="Valor")

            # Gráfico de barras empilhadas para lançamentos por mês
            fig_barras = px.bar(
                df_barras,
                x="MES",
                y="Valor",
                color="Tipo de Custo",
                title=f"Lançamentos por Mês - Ano {ano_selecionado}",
                category_orders={"MES": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]},
                text_auto='.2s'
            )
            fig_barras.update_layout(xaxis_title="", yaxis_title="")
            with st.container(border=True):
                st.plotly_chart(fig_barras, use_container_width=True)
        else:
            st.warning("Dados de lançamentos mensais não encontrados.")
    
    # Conteúdo da aba 2
    with tab2:
        st.title("Projeto Despesas")

        # Garantir que as colunas monetárias estejam em formato numérico
        if 'VL_VALOR_CUSTO' in df_Projeto_despesa.columns:
            df_Projeto_despesa['VL_VALOR_CUSTO'] = df_Projeto_despesa['VL_VALOR_CUSTO'].apply(convert_to_float)
            
        if 'VL_DESPESA_TOTAL' in df_Projeto_despesa_total.columns:
            df_Projeto_despesa_total['VL_DESPESA_TOTAL'] = df_Projeto_despesa_total['VL_DESPESA_TOTAL'].apply(convert_to_float)
        
        # Calcular o valor total de despesas
        valor_despesas = df_Projeto_despesa['VL_VALOR_CUSTO'].sum()        
        
        with st.container(border=True):          
            # Exibir a métrica de Valor Despesas
            st.metric("Valor Despesas", f"R$ {valor_despesas:,.2f}")

        # Converter a coluna DT_LANCAMENTO para o tipo datetime e extrair mês e ano
        df_Projeto_total_data['DT_LANCAMENTO'] = pd.to_datetime(df_Projeto_total_data['DT_LANCAMENTO'], errors='coerce')
        df_Projeto_total_data['Mês'] = df_Projeto_total_data['DT_LANCAMENTO'].dt.strftime('%b %Y')  # Extrair apenas o mês e ano

        # Ordenar por data para cálculo de despesas acumuladas
        df_Projeto_total_data = df_Projeto_total_data.sort_values(by='DT_LANCAMENTO')

        # Calcular a despesa acumulada por mês
        df_Projeto_total_data['Despesas Acumuladas'] = df_Projeto_total_data['VL_DESPESA_TOTAL'].cumsum()
        
        # Adicionar uma coluna formatada para os rótulos no formato desejado
        df_Projeto_total_data['Despesas Acumuladas Formatado'] = df_Projeto_total_data['Despesas Acumuladas'].apply(lambda x: f"R$ {x:,.2f}")

        with st.container(border=True):  
            # Gráfico de linha para a Curva de Despesas (Acumuladas)
            fig_curva = go.Figure()
            fig_curva.add_trace(go.Scatter(
                x=df_Projeto_total_data['Mês'], 
                y=df_Projeto_total_data['Despesas Acumuladas'], 
                mode='lines+markers+text',  # Adiciona os rótulos
                text=df_Projeto_total_data['Despesas Acumuladas Formatado'],  # Define os rótulos com os valores
                textposition="top center",  # Posiciona os rótulos acima dos pontos 
                name="Curva de Despesas Acumuladas"
            ))
            fig_curva.update_layout(
                title="Curva de Despesas Acumuladas",
                xaxis_title="",
                yaxis_title=""
            )
            st.plotly_chart(fig_curva, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1: 
            # Preparar dados para o gráfico de barras horizontais (Divisão das Despesas)
            df_barras = df_Projeto_despesa_total.groupby("TX_DESCRICAO", as_index=False)["VL_DESPESA_TOTAL"].sum()
            df_barras = df_barras.rename(columns={"TX_DESCRICAO": "Categoria", "VL_DESPESA_TOTAL": "Valor"})

            # Ordenar o DataFrame pelo eixo X (Valor) de forma decrescente
            df_barras = df_barras.sort_values(by="Valor", ascending=True)

            # Definir um limite para o comprimento da barra para decidir o posicionamento do rótulo
            valor_limite = df_barras['Valor'].mean()  # Usar a média como limite para exemplo

            # Criar o gráfico de barras com plotly.graph_objects
            fig_barras = go.Figure()

            for index, row in df_barras.iterrows():
                # Definir posição do rótulo com base no valor da barra
                text_position = "inside" if row["Valor"] >= valor_limite else "outside"
                
                fig_barras.add_trace(go.Bar(
                    y=[row["Categoria"]],
                    x=[row["Valor"]],
                    orientation='h',
                    text=f"R$ {row['Valor']:,.2f}",  # Formatação do rótulo
                    textposition=text_position,
                    texttemplate="%{text}",
                    name=row["Categoria"]
                ))

            # Configurar layout do gráfico
            fig_barras.update_layout(
                title="Divisão das Despesas",
                xaxis_title="",
                yaxis_title="",
                showlegend=False
            )

            # Exibir o gráfico em Streamlit
            with st.container(border=True): 
                st.plotly_chart(fig_barras, use_container_width=True)
            
        with col2:        
            # Preparar dados para a tabela de descrição das despesas usando as colunas reais
            df_tabela = df_Projeto_despesa[['TX_DESCRICAO', 'TX_OBSERVACAO', 'VL_VALOR_CUSTO']].copy()
            df_tabela = df_tabela.rename(columns={
                "TX_DESCRICAO": "Descrição Tipo",
                "TX_OBSERVACAO": "Observação",
                "VL_VALOR_CUSTO": "Custo Lançado"
            })

            # Formatar a coluna 'Custo Lançado' para exibir valores monetários
            df_tabela['Custo Lançado'] = df_tabela['Custo Lançado'].apply(lambda x: f"R$ {x:,.2f}")
            
            # Exibir a tabela de descrição das despesas
            with st.container(border=True):            
                st.write("### Descrição das Despesas")
                st.dataframe(df_tabela, use_container_width=True, hide_index=True)
    
    # Conteúdo da aba 3
    with tab3:
        st.title("Dashboard de Notas de Manutenção - Principal")

        # Filtros na tela principal
        with st.expander("Filtros"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                id_nota = st.selectbox("ID Nota Manutenção", ["Todos"] + sorted(df_nota_principal['ID_NOTA_MANUTENCAO'].dropna().unique().tolist()))

            with col2:
                # Remover valores None/NaN para evitar erros de comparação ao ordenar
                setores_disponiveis = df_nota_principal['TX_SETOR_SOLICITANTE'].dropna().unique().tolist()
                setor_solicitante = st.selectbox("Setor Solicitante", ["Todos"] + sorted(setores_disponiveis))

            with col3:
                familias_disponiveis = df_nota_principal['TX_FAMILIA_EQUIPAMENTOS'].dropna().unique().tolist()
                familia_equipamento = st.selectbox("Família Equipamento", ["Todos"] + sorted(familias_disponiveis))

        # Aplicar os filtros ao DataFrame
        df_filtrado = df_nota_principal.copy()
        if id_nota != "Todos":
            df_filtrado = df_filtrado[df_filtrado['ID_NOTA_MANUTENCAO'] == id_nota]
        if setor_solicitante != "Todos":
            df_filtrado = df_filtrado[df_filtrado['TX_SETOR_SOLICITANTE'] == setor_solicitante]
        if familia_equipamento != "Todos":
            df_filtrado = df_filtrado[df_filtrado['TX_FAMILIA_EQUIPAMENTOS'] == familia_equipamento]

        # Métricas principais

        st.subheader("Resumo de Notas de Manutenção")
        custo_aprovado = df_filtrado[df_filtrado['TX_SITUACAO'] == 'Aprovada']['VL_CUSTO_TOTAL'].sum()
        custo_pendente = df_filtrado[df_filtrado['TX_SITUACAO'] == 'Pendente']['VL_CUSTO_TOTAL'].sum()
        custo_reprovado = df_filtrado[df_filtrado['TX_SITUACAO'] == 'Reprovada']['VL_CUSTO_TOTAL'].sum()
        quantidade_notas = df_filtrado['ID_NOTA_MANUTENCAO'].nunique()

        col1, col2, col3, col4 = st.columns(4)
        with st.container(border=True):        
            col1.metric("Custo Aprovado", f"R$ {custo_aprovado:,.2f}")
        with st.container(border=True):            
            col2.metric("Custo Pendente de Aprovação", f"R$ {custo_pendente:,.2f}")
        with st.container(border=True):            
            col3.metric("Custo Reprovado", f"R$ {custo_reprovado:,.2f}")
        with st.container(border=True):            
            col4.metric("Quantidade de Notas", f"{quantidade_notas}")

        # Gráfico de Pizza - Notas de Manutenção por Situação
        situacao_counts = df_filtrado['TX_SITUACAO'].value_counts()
        fig_situacao = px.pie(
            names=situacao_counts.index,
            values=situacao_counts.values,
            title="Notas de Manutenção por Situação",
            hole=0.4
        )
        fig_situacao.update_traces(textinfo='percent+label+value')
        fig_situacao.update_layout(showlegend=True)

        # Gráfico de Pizza - Notas de Manutenção por Status do Escopo
        escopo_counts = df_filtrado['TX_ESCOPO_TIPO'].value_counts()
        fig_status = px.pie(
            names=escopo_counts.index,
            values=escopo_counts.values,
            title="Notas de Manutenção por Status do Escopo",
            hole=0.4
        )
        fig_status.update_traces(textinfo='percent+label+value')
        fig_status.update_layout(showlegend=True)

        # Exibir os gráficos lado a lado
        st.subheader("Distribuição de Notas de Manutenção")
        col1, col2 = st.columns(2)
        with st.container(border=True):        
            col1.plotly_chart(fig_situacao, use_container_width=True)
        with st.container(border=True):            
            col2.plotly_chart(fig_status, use_container_width=True)

        # Dados para as tabelas
        tipos_servicos = df_filtrado['TX_SERVICO'].value_counts().reset_index()
        tipos_servicos.columns = ["Tipos de Serviços", "Quantidade"]

        tipos_motivos = df_filtrado['TX_SITUACAO_MOTIVO'].value_counts().reset_index()
        tipos_motivos.columns = ["Tipos de Motivos", "Quantidade"]

        familias_equipamentos = df_filtrado['TX_FAMILIA_EQUIPAMENTOS'].value_counts().reset_index()
        familias_equipamentos.columns = ["Famílias de Equipamentos", "Quantidade"]

        st.subheader("Detalhamento de Notas de Manutenção")
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):            
                st.write("Tipos de Serviços")
                st.dataframe(tipos_servicos, use_container_width=True, hide_index=True)

        with col2:
            with st.container(border=True):              
                st.write("Tipos de Motivos")
                st.dataframe(tipos_motivos, use_container_width=True, hide_index=True)

        with col3:
            with st.container(border=True):              
                st.write("Famílias de Equipamentos")
                st.dataframe(familias_equipamentos, use_container_width=True, hide_index=True)

    # Conteúdo da aba 3
    with tab4:
        st.write("Nota - Apoios")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Gestão do Desembolso"

    # Conteúdo da aba 3
    with tab5:
        st.write("Nota - Informativos")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Gestão do Desembolso"

    # Conteúdo da aba 3
    with tab6:
        st.write("Nota - Recursos")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Gestão do Desembolso"

    # Conteúdo da aba 3
    with tab7:
        st.write("Nota - HH e Custos")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Gestão do Desembolso"

    # Conteúdo da aba 3
    with tab8:
        st.write("Nota - Top 5")
        # Aqui você pode adicionar mais detalhes específicos ou gráficos para "Gestão do Desembolso"
 
def app():
    dashboard_screen()