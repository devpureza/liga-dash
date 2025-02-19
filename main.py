import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Aula", page_icon=":books:", layout="wide")

# Convertendo arquivo Excel para CSV
df_excel = pd.read_excel("intermedgo.xlsx")
df_excel.to_csv("teste.csv", index=False)

aula = pd.read_csv("teste.csv")


# Limpando a coluna Valor (removendo R$ e convertendo para float)
# aula['Valor'] = aula['Valor'].str.replace('R$', '').str.replace('.', '').str.replace(',', '.').astype(float)

# Limpando a coluna Repasse (removendo R$ e convertendo para float)
# aula['Repasse'] = aula['Repasse'].str.replace('R$', '').str.replace('.', '').str.replace(',', '.').astype(float)


# Criando barra lateral para filtros
st.sidebar.header("Filtros:")

# Adicionando checkboxes para controlar a visibilidade
st.sidebar.header("Exibir/Ocultar Elementos:")
mostrar_tabela = st.sidebar.checkbox("Mostrar Tabela de Dados", value=True)
mostrar_ranking = st.sidebar.checkbox("Mostrar Ranking de Vendas", value=True)
mostrar_vendas = st.sidebar.checkbox("Mostrar Vendas por Atlética", value=True)
mostrar_repasses = st.sidebar.checkbox("Mostrar Repasses por Atlética", value=True)
st.sidebar.divider()

# Obtendo lista única de atléticas
atleticas = aula['Nome da atlética'].unique()

# Adicionando checkbox para selecionar todas
selecionar_todas = st.sidebar.checkbox("Selecionar Todas", value=True)

# Ajustando o multiselect baseado no checkbox
atleticas_selecionadas = st.sidebar.multiselect(
    "Selecione as Atléticas:",
    options=atleticas,
    default=atleticas if selecionar_todas else []
)

# Se o checkbox estiver marcado, seleciona todas as atléticas
if selecionar_todas:
    atleticas_selecionadas = atleticas

# Filtrando o dataframe baseado na seleção
df_filtrado = aula[aula['Nome da atlética'].isin(atleticas_selecionadas)]

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
    st.write("### Tabela de Dados")
    st.dataframe(df_filtrado)

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


