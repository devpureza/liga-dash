import streamlit as st
import pandas as pd
import plotly.express as px
from src.top_vendas_atleticas import ranking_atleticas
from src.sidebar import filtros_sidebar

st.set_page_config(page_title="Liga - Dashboard de eventos", page_icon=":books:", layout="wide")

# Converte arquivo excel em csv e le o arquivo csv
df_excel = pd.read_excel("intermed19022025.xlsx")
df_excel.to_csv("infos_filtradas.csv", index=False)
csv = pd.read_csv("infos_filtradas.csv")

# Aplicando os filtros da sidebar
df_filtrado, mostrar_tabela, mostrar_ranking, mostrar_vendas, mostrar_repasses = filtros_sidebar(csv)


# Criando DataFrame simplificado com dados selecionados
df_dados = df_filtrado[['Nome da atlética','Nome do ingresso','Nome do lote', 'Nome do comprador', 'Valor do bilhete original', 'Valor do repasse']]

# Contando o número de vendas por atlética
vendas_por_atletica = df_filtrado['Nome da atlética'].value_counts().reset_index()
vendas_por_atletica.columns = ['Nome da atlética', 'Número de Vendas']

# Gráfico com dados da coluna 'atlética' usando df_filtrado
fig = px.bar(vendas_por_atletica, 
             y='Nome da atlética', 
             x='Número de Vendas',
             title='Ranking de vendas')

# Calculando o valor total por atlética
valores_por_atletica = df_filtrado.groupby('Nome da atlética')['Valor do bilhete original'].sum().reset_index()
valores_por_atletica = valores_por_atletica.sort_values('Valor do bilhete original', ascending=True)

# Criando o gráfico de valores totais
fig_valores = px.bar(valores_por_atletica,
                    x='Nome da atlética',
                    y='Valor do bilhete original',
                    title='Vendas (R$) por atlética')

# Formatando o eixo y para mostrar valores em reais
fig_valores.update_traces(texttemplate='R$ %{y:.2f}', textposition='outside')
fig_valores.update_layout(yaxis_title='Valor Total')

# Calculando o repasse total por atlética
repasses_por_atletica = df_filtrado.groupby('Nome da atlética')['Valor do repasse'].sum().reset_index()
repasses_por_atletica = repasses_por_atletica.sort_values('Valor do repasse', ascending=True)

# Criando o gráfico de repasses
fig_repasses = px.bar(repasses_por_atletica,
                     x='Nome da atlética',
                     y='Valor do repasse',
                     title='Repasses (R$) por atlética')

# Formatando o eixo y para mostrar valores em reais
fig_repasses.update_traces(texttemplate='R$ %{y:.2f}', textposition='outside')
fig_repasses.update_layout(yaxis_title='Repasse Total')

# Exibindo a tabela principal condicionalmente
if mostrar_tabela:
    col1, col2 = st.columns(2)
    with col1:
        st.write("### INTERMEDGO - 2025: últimas vendas")
        st.dataframe(df_dados)
    with col2:
        ranking_atleticas(vendas_por_atletica)

# Totalizadores de venda
col1, col2, col3 = st.columns(3)

with col1:
    total_vendas = df_filtrado['Valor do bilhete original'].sum()
    st.markdown(f"""
        <div style='
            background-color: rgba(30,136,229,0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 5px;
            border: 1px solid rgba(30,136,229,0.2);
            text-align: center;
        '>
            <p style='color: #666; font-size: 14px; margin-bottom: 5px;'>💰 Total de Vendas</p>
            <p style='font-size: 24px; font-weight: bold; margin: 0;'>
                R$ {total_vendas:,.2f}
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    total_repasse = df_filtrado['Valor do repasse'].sum()
    st.markdown(f"""
        <div style='
            background-color: rgba(30,136,229,0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 5px;
            border: 1px solid rgba(30,136,229,0.2);
            text-align: center;
        '>
            <p style='color: #666; font-size: 14px; margin-bottom: 5px;'>💸 Total de Repasse</p>
            <p style='font-size: 24px; font-weight: bold; margin: 0;'>
                R$ {total_repasse:,.2f}
            </p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    qtd_vendas = len(df_filtrado)
    st.markdown(f"""
        <div style='
            background-color: rgba(30,136,229,0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 5px;
            border: 1px solid rgba(30,136,229,0.2);
            text-align: center;
        '>
            <p style='color: #666; font-size: 14px; margin-bottom: 5px;'>🎫 Quantidade de Vendas</p>
            <p style='font-size: 24px; font-weight: bold; margin: 0;'>
                {qtd_vendas:,}
            </p>
        </div>
    """, unsafe_allow_html=True)

            
# Exibindo os dois primeiros gráficos em colunas se estiverem habilitados
if mostrar_ranking or mostrar_vendas:
    col1, col2 = st.columns(2)

    if mostrar_ranking:
        with col1:
            st.plotly_chart(fig, use_container_width=True)

    if mostrar_vendas:
        with col2:
            st.plotly_chart(fig_valores, use_container_width=True)

# Exibindo o gráfico de repasses condicionalmente
if mostrar_repasses:
    st.plotly_chart(fig_repasses, use_container_width=True)



