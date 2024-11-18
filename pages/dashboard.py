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
        df_projeto_nota_declaracao_escopo = st.session_state['project_data']['projeto_nota_declaracao_escopo']          
        df_apoio = st.session_state['project_data']['marge_apoio']                  
        df_informativo = st.session_state['project_data']['marge_informativo']
        df_recurso = st.session_state['project_data']['marge_recurso']
        
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
        st.subheader("Projeto - Geral")

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
        
        with col1:
            with st.container(border=True):
                st.metric("Valor Orçamento", f"R$ {valor_orcamento:,.2f}")
                
        with col2:
            with st.container(border=True):
                st.metric("Custo Total Projeto Geral", f"R$ {custo_projeto_total:,.2f}")
                
        with col3:
            with st.container(border=True):
                st.metric("Percentual Gasto", f"{percentual_gasto:.2f}%")
                
        with col4:
            with st.container(border=True):
                st.metric("Percentual Contingência", f"{percentual_contingencia:.2f}%")

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
        st.subheader("Projeto - Despesas")

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
        st.subheader("Notas de Manutenção - Principal")

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
        with col1:
            with st.container(border=True):
                st.metric("Custo Aprovado", f"R$ {custo_aprovado:,.2f}")
                
        with col2:
            with st.container(border=True):
                st.metric("Custo Pendente de Aprovação", f"R$ {custo_pendente:,.2f}")
                
        with col3:
            with st.container(border=True):
                st.metric("Custo Reprovado", f"R$ {custo_reprovado:,.2f}")
                
        with col4:
            with st.container(border=True):
                st.metric("Quantidade de Notas", f"{quantidade_notas}")

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
        with col1:
            with st.container(border=True):        
                st.plotly_chart(fig_situacao, use_container_width=True)
        
        with col2:
            with st.container(border=True): 
                st.plotly_chart(fig_status, use_container_width=True)

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
        st.subheader("Notas de Manutenção - Apoios")
                
        # Agrupamos e contamos as ocorrências de cada tipo de apoio
        df_apoio_count = df_apoio['TX_TIPO'].value_counts().reset_index()
        df_apoio_count.columns = ['Tipo', 'Quantidade']  # Renomear as colunas para facilitar a visualização

        # Exibir Métrica de Custos Totais
        custos_totais = df_apoio['VL_CUSTO_TOTAL'].sum()  # Supondo que a coluna VL_CUSTO_TOTAL existe em df_apoio
        with st.container(border=True):
            st.metric("Custos Totais", f"R$ {custos_totais:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        # Separar o layout com colunas e contêineres
        st.subheader("Graficos de Apoio")
        with st.container(border=True):
            # Criar gráfico de barras para "Quantidade de Apoios pelo Tipo"
            fig = px.bar(
                df_apoio_count, 
                x="Tipo", 
                y="Quantidade", 
                text="Quantidade",
                title="Quantidade de Apoios x Tipo",
                labels={"Tipo": "Tipo de Apoio", "Quantidade": "Quantidade"},
            )
            fig.update_traces(marker_color="teal", textposition="outside")
            fig.update_layout(
                title_x=0.5,
                xaxis_tickangle=0,
                xaxis_title="",
                yaxis_title="",
            )
            st.plotly_chart(fig, use_container_width=True)

 
        # Tabelas de detalhes por tipo de apoio
        st.subheader("Detalhes de Empresas e Notas de Apoio por Tipo")
        # Tabela 1 - Coluna da esquerda
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown("#### Empresas Primárias Executantes e Notas de Apoio")
                # Exibir a tabela de apoio
                st.dataframe(df_apoio_count, use_container_width=True, hide_index=True)  

        # Tabela 2 - Coluna da direita (simulação de outra tabela para mostrar variação)
        with col2:
            with st.container(border=True):
                st.markdown("#### Empresas Secundárias Executantes e Notas de Apoio")
                # Exibir a mesma tabela ou uma variação, caso existam dados adicionais
                st.dataframe(df_apoio_count, use_container_width=True, hide_index=True) 

    # Conteúdo da aba 3
    with tab5:
        st.subheader("Notas de Manutenção - Informativos")
        
        # 1. Gráfico de Barras - Contagem de Informativos por Descrição
        df_descricao_count = df_informativo['TX_DESCRICAO'].value_counts().reset_index()
        df_descricao_count.columns = ['Descrição', 'Quantidade']

        # 2. Tabela - Família de Equipamentos e Quantidade (usando df_nota_principal)
        df_familia_count = df_nota_principal['TX_FAMILIA_EQUIPAMENTOS'].value_counts().reset_index()
        df_familia_count.columns = ['Família Equipamentos', 'Quantidade']
        df_familia_count = df_familia_count.sort_values(by="Quantidade", ascending=False)

        # 3. Gráfico de Rosca - Notas de Manutenção por Família de Equipamentos (usando df_nota_principal)
        df_familia_pizza = df_familia_count.copy().head(10)  # Usando o mesmo DataFrame da tabela para consistência
        with st.container(border=True):
            # Exibir o Gráfico de Barras
            fig_bar = px.bar(
                df_descricao_count, 
                x="Descrição", 
                y="Quantidade", 
                text="Quantidade",
                title="Top 10 Informativos por Descrição",                
                labels={"Descrição": "Descrição", "Quantidade": "Quantidade"},
            )
            fig_bar.update_traces(marker_color="teal", textposition="outside")
            fig_bar.update_layout(
                title_x=0.5,
                xaxis_tickangle=0,
                xaxis_title="",
                yaxis_title="Quantidade",
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("Detalhamento de Informativo") 
        # Exibir Tabela e Gráfico de Rosca lado a lado
        col1, col2 = st.columns([1, 1])

        with col1:
            with st.container(border=True):
                st.subheader("Família de Equipamentos")
                st.dataframe(df_descricao_count, use_container_width=True, hide_index=True) 

        with col2:
            with st.container(border=True):            
                fig_pie = px.pie(
                    df_familia_pizza, 
                    names="Família Equipamentos", 
                    values="Quantidade",
                    title="Notas de Manutenção x Família de Equipamentos",
                    hole=0.4,  # Cria um gráfico de rosca (donut)
                )
                fig_pie.update_traces(textinfo='percent')  # Exibir porcentagem e rótulo
                st.plotly_chart(fig_pie, use_container_width=True)

    # Conteúdo da aba 3
    with tab6:
        st.subheader("Notas de Manutenção - Recursos")
        
        # Calcular VL_HH como produto de VL_DURACAO e VL_QUANTIDADE
        df_recurso['VL_HH'] = df_recurso['VL_DURACAO'] * df_recurso['VL_QUANTIDADE']
        # Filtrar `df_recurso` para incluir apenas registros onde `GID_NOTA_MANUTENCAO` não está em branco
        df_recurso_filtrado = df_recurso[df_recurso['GID_NOTA_MANUTENCAO'].isin(df_nota_principal['GID_NOTA_MANUTENCAO'])]

        # Agrupar por `TX_DESCRICAO` e somar `VL_HH`, ordenando de forma decrescente
        df_hh_por_tipo = df_recurso_filtrado.groupby('TX_DESCRICAO')['VL_HH'].sum().reset_index()
        df_hh_por_tipo = df_hh_por_tipo.sort_values(by="VL_HH", ascending=False)  # Ordenar de forma decrescente
        # Obter a ordem das categorias para `TX_DESCRICAO` conforme o valor decrescente de `VL_HH`
        categoria_ordem_hh = df_hh_por_tipo['TX_DESCRICAO'].tolist()
        # Exibir Métrica de Custos Totais
        custos_totais = df_recurso['VL_CUSTO_TOTAL'].sum()  # Supondo que a coluna VL_CUSTO_TOTAL existe em df_recurso
        with st.container(border=True):
            st.metric("Custos Totais", f"R$ {custos_totais:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.subheader("Visualização Gráfica de Recursos")
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):    
                # Gráfico 1: HH por Tipo           
                fig = px.bar(
                    df_hh_por_tipo, 
                    x="VL_HH", 
                    y="TX_DESCRICAO", 
                    text=df_hh_por_tipo["VL_HH"].apply(lambda x: f"{x // 1000} Mil"),
                    title="HH x Tipo", 
                    labels={"VL_HH": "Horas Homem", "TX_DESCRICAO": "Tipo de Recurso"},
                    category_orders={"TX_DESCRICAO": categoria_ordem_hh}  # Forçar ordem decrescente                    
                )
                fig.update_traces(marker_color="teal", textposition="outside")
                fig.update_layout(
                    title_x=0.5,
                    xaxis_tickangle=-45,
                    xaxis_title="",
                    yaxis_title="",
                    xaxis=dict(showticklabels=False),
                )
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                with st.container(border=True): 
                    # Gráfico 2: Quantidade de Notas por Tipo
                    df_qtd_notas_por_tipo = df_recurso_filtrado['TX_DESCRICAO'].value_counts().reset_index()
                    df_qtd_notas_por_tipo.columns = ['Tipo', 'Quantidade']
                    df_qtd_notas_por_tipo = df_qtd_notas_por_tipo.sort_values(by="Quantidade", ascending=False)  # Ordenar de forma decrescente
                    # Obter a ordem das categorias para `Tipo` conforme o valor decrescente de `Quantidade`
                    categoria_ordem_qtd = df_qtd_notas_por_tipo['Tipo'].tolist()
                    fig_notas = px.bar(
                        df_qtd_notas_por_tipo, 
                        x="Quantidade", 
                        y="Tipo", 
                        text="Quantidade",
                        title="Qtde. Notas x Tipo",                        
                        labels={"Quantidade": "Quantidade de Notas", "Tipo": "Tipo de Recurso"},
                        category_orders={"Tipo": categoria_ordem_qtd}  # Forçar ordem decrescente
                    )
                    fig_notas.update_traces(marker_color="teal", textposition="outside")
                    fig_notas.update_layout(
                        title_x=0.5,
                        xaxis_title="",
                        yaxis_title="",
                        xaxis=dict(showticklabels=False),  # Ocultar os rótulos do eixo x para uma aparência mais limpa
                    )
                    st.plotly_chart(fig_notas, use_container_width=True)       

    # Conteúdo da aba 3
    with tab7:
        st.subheader("Notas de Manutenção HH e Custos")
        
        # Realizar o merge para garantir que `TX_FAMILIA_EQUIPAMENTOS` está em `df_recurso`
        df_recurso_completo = pd.merge(df_recurso, df_nota_principal[['GID_NOTA_MANUTENCAO', 'TX_FAMILIA_EQUIPAMENTOS']], on="GID_NOTA_MANUTENCAO", how="left")

        # 1. Quantidade de Notas por `TX_FAMILIA_EQUIPAMENTOS` (contagem de `ID_NOTA_MANUTENCAO` em `df_nota_principal`)
        df_qtd_notas = df_nota_principal.groupby('TX_FAMILIA_EQUIPAMENTOS')['ID_NOTA_MANUTENCAO'].count().reset_index()
        df_qtd_notas.columns = ['TX_FAMILIA_EQUIPAMENTOS', 'Qtde_Notas']
        df_qtd_notas = df_qtd_notas.sort_values(by="Qtde_Notas", ascending=False).head(10)

        # 2. HH Total por `TX_FAMILIA_EQUIPAMENTOS` (soma de `VL_HH` em `df_recurso_completo`)
        df_hh_total = df_recurso_completo.groupby('TX_FAMILIA_EQUIPAMENTOS')['VL_HH'].sum().reset_index()
        df_hh_total = df_hh_total.sort_values(by="VL_HH", ascending=False).head(10)

        # 3. Custo Total por `TX_FAMILIA_EQUIPAMENTOS` (soma de `VL_CUSTO_TOTAL` em `df_nota_principal`)
        df_custo_total = df_nota_principal.groupby('TX_FAMILIA_EQUIPAMENTOS')['VL_CUSTO_TOTAL'].sum().reset_index()
        df_custo_total = df_custo_total.sort_values(by="VL_CUSTO_TOTAL", ascending=False).head(10)


        # Configurar layout dos gráficos
        col1, col2, col3 = st.columns(3)

        # Gráfico 1: Qtde. de Notas
        with col1:
            with st.container(border=True): 
                fig_qtd_notas = px.bar(
                    df_qtd_notas,
                    x="Qtde_Notas",
                    y="TX_FAMILIA_EQUIPAMENTOS",
                    orientation="h",
                    text="Qtde_Notas",
                    title="Qtde. de Notas",                
                    labels={"Qtde_Notas": "Quantidade de Notas", "TX_FAMILIA_EQUIPAMENTOS": "Família de Equipamentos"},
                )
                fig_qtd_notas.update_traces(marker_color="teal", textposition="outside")
                fig_qtd_notas.update_layout(
                    title_x=0.5,
                    xaxis_title="",
                    yaxis_title="",
                    yaxis=dict(categoryorder="total ascending"),
                )
                st.plotly_chart(fig_qtd_notas, use_container_width=True)

        # Gráfico 2: HH Total
        with col2:
            with st.container(border=True): 
                fig_hh_total = px.bar(
                    df_hh_total,
                    x="VL_HH",
                    y="TX_FAMILIA_EQUIPAMENTOS",
                    orientation="h",
                    text=df_hh_total["VL_HH"].apply(lambda x: f"{x // 1000} Mil"),  # Exibir valores em milhares
                    title="HH Total",                
                    labels={"VL_HH": "Horas Homem Total", "TX_FAMILIA_EQUIPAMENTOS": "Família de Equipamentos"},
                )
                fig_hh_total.update_traces(marker_color="green", textposition="outside")
                fig_hh_total.update_layout(
                    title_x=0.5,
                    xaxis_title="",
                    yaxis_title="",
                    yaxis=dict(categoryorder="total ascending"),
                )
                st.plotly_chart(fig_hh_total, use_container_width=True)

        # Gráfico 3: Custo Total
        with col3:
            with st.container(border=True): 
                fig_custo_total = px.bar(
                    df_custo_total,
                    x="VL_CUSTO_TOTAL",
                    y="TX_FAMILIA_EQUIPAMENTOS",
                    orientation="h",
                    text=df_custo_total["VL_CUSTO_TOTAL"].apply(lambda x: f"{x // 1000} Mil"),  # Exibir valores em milhares
                    title="Custo Total",                 
                    labels={"VL_CUSTO_TOTAL": "Custo Total", "TX_FAMILIA_EQUIPAMENTOS": "Família de Equipamentos"},
                )
                fig_custo_total.update_traces(marker_color="orange", textposition="outside")
                fig_custo_total.update_layout(
                    title_x=0.5,
                    xaxis_title="",
                    yaxis_title="",
                    yaxis=dict(categoryorder="total ascending"),
                )
                st.plotly_chart(fig_custo_total, use_container_width=True)

    # Conteúdo da aba 3
    with tab8:
        st.subheader("Notas de Manutenção - Top 5")
        
        # Calcular VL_HH como produto de VL_DURACAO e VL_QUANTIDADE
        df_recurso['VL_HH'] = df_recurso['VL_DURACAO'] * df_recurso['VL_QUANTIDADE']

        # Filtrar `df_recurso` para incluir apenas registros onde `GID_NOTA_MANUTENCAO` não está em branco
        df_recurso_filtrado = df_recurso[df_recurso['GID_NOTA_MANUTENCAO'].isin(df_nota_principal['GID_NOTA_MANUTENCAO'])]

        # Realizar o merge para garantir que `TX_NOTA` está presente em `df_recurso_completo`
        df_recurso_completo = pd.merge(
            df_recurso,
            df_nota_principal[['GID_NOTA_MANUTENCAO', 'TX_NOTA']],
            on="GID_NOTA_MANUTENCAO",
            how="left"
        )

        # Converter `TX_NOTA` para string, preenchendo valores ausentes com "N/A"
        df_nota_principal['TX_NOTA'] = df_nota_principal['TX_NOTA'].astype(str).fillna("None")
        df_recurso_completo['TX_NOTA'] = df_recurso_completo['TX_NOTA'].astype(str).fillna("None")

        # 1. Preparar dados para o gráfico de Top 5 Custos
        df_top_custos = (
            df_nota_principal.groupby('TX_NOTA', as_index=False)['VL_CUSTO_TOTAL']
            .sum()
            .sort_values(by='VL_CUSTO_TOTAL', ascending=False)
            .head(5)
            .rename(columns={'TX_NOTA': 'Nota', 'VL_CUSTO_TOTAL': 'Valor'})
        )

        # 2. Preparar dados para o gráfico de Top 5 HH
        df_top_hh = (
            df_recurso_completo.groupby('TX_NOTA', as_index=False)['VL_HH']
            .sum()
            .sort_values(by='VL_HH', ascending=False)
            .head(5)
            .rename(columns={'TX_NOTA': 'Nota', 'VL_HH': 'Horas_Homem'})
        )

            # Configurar layout dos gráficos
        col1, col2 = st.columns(2)

        # Gráfico 1: Top 5 Custos
        with col1:
            valor_limite_custos = df_top_custos['Valor'].mean()  # Usar a média como limite para exemplo
            fig_custos = go.Figure()

            for index, row in df_top_custos.iterrows():
                text_position = "inside" if row["Valor"] >= valor_limite_custos else "outside"
                fig_custos.add_trace(go.Bar(
                    y=[row["Nota"]],
                    x=[row["Valor"]],
                    orientation='h',
                    text=f"R$ {row['Valor'] / 1e6:.1f} Mi",
                    textposition=text_position,
                    texttemplate="%{text}",
                    name=row["Nota"]
                ))

            fig_custos.update_layout(
                title="Top 5 Custos",
                xaxis_title="Custo Total (Milhões)",
                yaxis_title="",
                showlegend=False,
                yaxis=dict(categoryorder="total ascending", tickfont=dict(size=14)),  # Aumentar margem e diminuir fonte
                margin=dict(l=200),  # Ajuste a margem para dar mais espaço ao eixo Y
                width=900
            )

            with st.container(border=True): 
                st.plotly_chart(fig_custos, use_container_width=True)

        # Gráfico 2: Top 5 HH
        with col2:
            valor_limite_hh = df_top_hh['Horas_Homem'].mean()
            fig_hh = go.Figure()

            for index, row in df_top_hh.iterrows():
                text_position = "inside" if row["Horas_Homem"] >= valor_limite_hh else "outside"
                fig_hh.add_trace(go.Bar(
                    y=[row["Nota"]],
                    x=[row["Horas_Homem"]],
                    orientation='h',
                    text=f"{row['Horas_Homem']}",
                    textposition=text_position,
                    texttemplate="%{text}",
                    name=row["Nota"]
                ))

            fig_hh.update_layout(
                title="Top 5 HH",
                xaxis_title="Horas Homem (HH)",
                yaxis_title="",
                showlegend=False,
                yaxis=dict(categoryorder="total ascending", tickfont=dict(size=14)),
                margin=dict(l=200),
                width=900
            )

            with st.container(border=True): 
                st.plotly_chart(fig_hh, use_container_width=True)
 
def app():
    dashboard_screen()