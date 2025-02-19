import streamlit as st

def ranking_atleticas(vendas_por_atletica):
    """
    Exibe o ranking de top vendas por atlética
    Args:
        vendas_por_atletica (DataFrame): DataFrame com as colunas 'Nome da atlética' e 'Número de Vendas'
    """
    top_vendas = vendas_por_atletica.head(7)
    
    st.markdown("""
        <h3 style='color: #FFFFFF; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);'>
            🏆 Top vendas por atlética
        </h3>
    """, unsafe_allow_html=True)
    
    for i, row in top_vendas.iterrows():
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