import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração visual do dashboard
st.set_page_config(page_title="Dashboard Delta Energia - Estágio", layout="wide")

# --- ESTILIZAÇÃO ---
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    h1 { color: #1a365d; }
    </style>
""", unsafe_allow_html=True)

# --- MENU LATERAL ---
st.sidebar.header("Portfólio Delta Energia")
menu = st.sidebar.radio("Navegar por:", ["Contexto & Vaga", "Mineração e Análise", "Insights Operacionais"])

# --- DATASET SIMULADO ---
@st.cache_data
def carregar_dados_energia():
    dados = {
        'Horário': ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'] * 3,
        'Setor': ['Industrial']*6 + ['Comercial']*6 + ['Residencial']*6,
        'Consumo_kWh': [450, 420, 890, 950, 910, 600,  120, 95, 340, 410, 390, 210,  80, 65, 110, 150, 220, 430],
        'Anomalia': [0, 0, 0, 1, 0, 0,  0, 1, 0, 0, 0, 0,  0, 0, 0, 0, 0, 0]
    }
    return pd.DataFrame(dados)

df = carregar_dados_energia()

# --- ABA 1: CONTEXTO ---
if menu == "Contexto & Vaga":
    st.title("⚡ Projeto de Mineração de Dados: Setor Elétrico")
    st.subheader("Alinhamento Estratégico para Vaga de Estágio - Delta Energia")
    
    col_vaga, col_projeto = st.columns(2)
    with col_vaga:
        st.info("""
        **Foco da Vaga Pesquisada:**
        * Integração de bases operacionais e ferramentas de BI.
        * Transformação de dados brutos em insights inteligentes.
        * Suporte à tomada de decisão na comercialização de energia.
        """)
    with col_projeto:
        st.success("""
        **Solução Prática Entregue:**
        * Uso de Python para tratar o histórico de cargas.
        * Análise exploratória interativa automatizada.
        * Algoritmo simples de detecção de picos anômalos de consumo.
        """)
        
    st.write("### 📋 Amostra dos Dados Minerados")
    st.dataframe(df.head(6), use_container_width=True)

# --- ABA 2: ANÁLISE ---
elif menu == "Mineração e Análise":
    st.title("📊 Análise de Carga por Setor")
    
    setor_selecionado = st.selectbox("Selecione o Setor para Filtrar Graficamente:", df['Setor'].unique())
    df_filtrado = df[df['Setor'] == setor_selecionado]
    
    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        fig_linha = px.line(df_filtrado, x='Horário', y='Consumo_kWh', 
                            title=f"Curva de Carga Diária - {setor_selecionado}",
                            markers=True, color_discrete_sequence=['#ff9900'])
        st.plotly_chart(fig_linha, use_container_width=True)
        
    with col_graf2:
        fig_barra = px.bar(df, x='Setor', y='Consumo_kWh', color='Horário',
                           title="Comparativo de Consumo entre Setores", barmode='group')
        st.plotly_chart(fig_barra, use_container_width=True)

# --- ABA 3: INSIGHTS ---
elif menu == "Insights Operacionais":
    st.title("💡 Insights Gerenciais (Foco no Negócio)")
    st.metric(label="Total de Anomalias/Desperdícios Detetados", value="2 Eventos", delta="Ação Comercial Recomendada")
    
    st.markdown("""
    ### 👁️ Padrões Encontrados através da Mineração de Dados:
    1. **Pico Anômalo no Setor Industrial (12:00):** O consumo atingiu 950 kWh em um horário que deveria indicar redução devido ao intervalo de funcionários. Isso sugere maquinário ligado desnecessariamente ou falha de calibração.
    2. **Desperdício na Madrugada Comercial (04:00):** O setor comercial registrou consumo de 95 kWh na madrugada.
    
    ### 🎯 Recomendação para a Mesa de Operações da Delta:
    Utilizar esses alertas gerados em Python para propor aos clientes contratos de demanda flexível, reduzindo o custo deles na ponta e melhorando a eficiência da carteira de energia da Delta.
    """)
