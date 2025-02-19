import streamlit as st

def filtros_sidebar(df):
    """
    Cria todos os elementos da barra lateral
    Args:
        df (DataFrame): DataFrame com os dados originais
    Returns:
        dict: Dicionário com todas as seleções feitas na sidebar
    """
    #logo na barra lateral
    st.sidebar.image("logo-white.png")

    # Cabeçalho dos filtros
    st.sidebar.header("Filtros:")

    # Checkboxes para controlar visibilidade
    st.sidebar.header("Exibir/Ocultar Elementos:")
    mostrar_tabela = st.sidebar.checkbox("Mostrar Tabela de Dados", value=True)
    mostrar_ranking = st.sidebar.checkbox("Mostrar Ranking de Vendas", value=True)
    mostrar_vendas = st.sidebar.checkbox("Mostrar Vendas por Atlética", value=True)
    mostrar_repasses = st.sidebar.checkbox("Mostrar Repasses por Atlética", value=True)
    st.sidebar.divider()

    # Obtendo lista única de atléticas
    atleticas = df['Nome da atlética'].unique()

    # Checkbox para selecionar todas
    selecionar_todas = st.sidebar.checkbox("Selecionar Todas", value=True)

    # Multiselect baseado no checkbox
    atleticas_selecionadas = st.sidebar.multiselect(
        "Selecione as Atléticas:",
        options=atleticas,
        default=atleticas if selecionar_todas else []
    )

    # Se o checkbox estiver marcado, seleciona todas as atléticas
    if selecionar_todas:
        atleticas_selecionadas = atleticas
    
    # Filtra o DataFrame baseado nas atléticas selecionadas
    df_filtrado = df[df['Nome da atlética'].isin(atleticas_selecionadas)]

    # Retorna uma tupla com o DataFrame filtrado e as opções de visualização
    return (
        df_filtrado,
        mostrar_tabela,
        mostrar_ranking,
        mostrar_vendas,
        mostrar_repasses
    )