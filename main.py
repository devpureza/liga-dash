import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Liga - Dashboard de eventos", page_icon=":books:", layout="wide")

# Convertendo arquivo Excel para CSV
df_excel = pd.read_excel("intermed19022025.xlsx")
df_excel.to_csv("infos_filtradas.csv", index=False)

csv = pd.read_csv("infos_filtradas.csv")

#logo na barra lateral
st.logo("logo-white.png", size="large", link="https://www.deualiga.com.br")

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
atleticas = csv['Nome da atlética'].unique()

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
df_filtrado = csv[csv['Nome da atlética'].isin(atleticas_selecionadas)]
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
        top_3_vendas = vendas_por_atletica.head(7)
        
        st.markdown("""
            <h3 style='color: #FFFFFF; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);'>
                🏆 Top vendas por atlética
            </h3>
        """, unsafe_allow_html=True)
        
        for i, row in top_3_vendas.iterrows():
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏅"
            st.markdown(f"""
                <div style='
                    background-color: rgba(30,136,229,0.1);
                    padding: 10px;
                    border-radius: 10px;
                    margin: 5px 0;
                    border-left: 5px solid #1E88E5;
                '>
                    <p style='font-size: 16px; margin: 0;'>
                        {medal} {row['Nome da atlética']} 
                        <span style='float: right; font-weight: bold;'>
                            {row['Número de Vendas']} vendas
                        </span>
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
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



