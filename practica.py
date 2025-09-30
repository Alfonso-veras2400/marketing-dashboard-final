# pip install -r requirements.txt

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time


# CONFIGURACIÓN DE LA PÁGINA

# Configura las propiedades de la página de Streamlit
st.set_page_config(
    page_title="📊 Dashboard de Marketing | Insights Visuales",  # Título de la pestaña del navegador
    page_icon="🎯",  # Icono que aparece en la pestaña
    layout="wide",  # Diseño de página ancho para mejor visualización
    initial_sidebar_state="expanded"  # Barra lateral expandida por defecto
)


# ESTILOS CSS PERSONALIZADOS
#
# Aplica estilos CSS para el diseño dark mode y mejorar la experiencia de usuario
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fondo principal */
    .stApp {
        background-color: #ffffff; # fondo blanco puro
        color: #1a1a1a;
    }

    /* Encabezados */
    h1, h2, h3, h4, h5, h6 {
        color: #0077cc !important;
        font-weight: 600;
    }

    /* Métricas */
    div[data-testid="stMetricValue"] {
        background-color: #f0f8ff;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #b3e0ff;
    }

    /* Selectores */
    div[data-baseweb="select"] {
        background-color: #f5fff5;
        border: 1px solid #99e699;
        border-radius: 8px;
        color: #1a1a1a;
    }

    /* Sliders */
    div[data-testid="stSlider"] {
        background-color: #f0f8ff;
        border-radius: 8px;
        padding: 10px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f5fff5 !important;
    }

    /* Contenedor principal */
    section.main > div {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    /* Botones */
    .stButton > button {
        background-color: #33cc99 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
    }

    .stButton > button:hover {
        background-color: #29a87a !important;
    }

    /* Tarjetas personalizadas */
    .metric-card {
        background: linear-gradient(135deg, #f0f8ff, #f5fff5);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #cce7ff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    .insight-box {
        background-color: #f0f8ff;
        border-left: 4px solid #33cc99;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }

    .chart-container {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e6e6e6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    .footer {
        text-align: center;
        padding: 20px;
        color: #4d4d4d;
        font-size: 0.9em;
    }

    .participant-card {
        background-color: #f5fff5;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #99e699;
        margin: 5px 0;
    }

    .emoji-header {
        font-size: 1.5em;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ENCABEZADO (LOGO, TÍTULO, PARTICIPANTES)

# Crea tres columnas para organizar el encabezado
col_logo, col_titulo, col_nombres = st.columns([1, 3, 1.5])

# Columna del logo (izquierda)
with col_logo:
    try:
        # Intenta cargar el logo desde el archivo
        st.image("logo.png", width=220)
    except Exception as e:
        # Si no hay logo, muestra un emoji como placeholder
        st.markdown("<div style='text-align: center; font-size: 3em;'>🎯</div>", unsafe_allow_html=True)

# Columna del título y participantes (centro)
with col_titulo:
    # Título principal del dashboard
    st.markdown("<h1 style='text-align: center; margin-bottom: 0.5rem;'>📊 Dashboard de Marketing Estratégico</h1>", unsafe_allow_html=True)
    # Descripción del dashboard con tamaño de fuente aumentado
    st.markdown("<p style='text-align: center; color: #8b949e; font-size: 1.6em;'>📈 Análisis de Campaña de Marketing con 🔍 Insights Visuales 🎯</p>", unsafe_allow_html=True)

    # Nueva fila para los participantes centrados
    participantes = [
        "Dariel A. Peña",
        "Elvis R. Rosado", 
        "Yaridis Terrero",
        "Arismendy J. Padilla",
        "Alfonso Veras"
    ]
    
    # Crea 5 columnas para distribuir los participantes
    cols = st.columns([1, 1, 1, 1, 1])
    for i, participante in enumerate(participantes):
        # Coloca cada participante en una columna específica
        with cols[i]:
            # Muestra cada participante en una tarjeta con emoji
            st.markdown(f"<div style='text-align: center;'><div class='participant-card'>👤 {participante}</div></div>", unsafe_allow_html=True)
            
# ================================
# RESUMEN DEL DASHBOARD
# ================================
# Línea divisoria
st.markdown("---")
# Bloque de información con teoría y uso del dashboard
st.markdown("""
<div class='insight-box'>
    <h3>🎯 Teoría del KPI: Segmentación por Edad</h3>
    <p>La edad es un factor determinante en marketing porque define patrones de consumo, poder adquisitivo y preferencias. Este dashboard permite analizar y segmentar clientes para tomar decisiones estratégicas basadas en datos visuales interactivos.</p>
    <p>✨ <strong>Usa los filtros en la barra lateral</strong> para explorar diferentes segmentos de clientes y descubrir insights personalizados.</p>
</div>
""", unsafe_allow_html=True)

# ================================
# CARGA Y PREPARACIÓN DE DATOS
# ================================
# Función para cargar y preparar los datos con cache
@st.cache_data
def cargar_datos(path: str):
    """
    Carga y prepara los datos para el dashboard
    
    Args:
        path (str): Ruta del archivo CSV
    
    Returns:
        pandas.DataFrame: DataFrame con datos procesados
    """
    # Carga el archivo Excel
    df = pd.read_csv(path, sep=';')
    
    # Calcula la edad a partir del año de nacimiento
    df["Edad"] = 2025 - df["Year_Birth"]
    
    # Calcula el gasto total sumando todas las categorías de gasto
    df["GastoTotal"] = (
        df["MntWines"] + df["MntFruits"] + df["MntMeatProducts"] +
        df["MntFishProducts"] + df["MntSweetProducts"] + df["MntGoldProds"]
    )
    
    # Asigna estado civil (renombrado para claridad)
    df["EstadoCivil"] = df["Marital_Status"]
    
    # Genera datos de género aleatoriamente (para demostración)
    np.random.seed(42)
    df["Genero"] = np.random.choice(["Hombre", "Mujer"], size=len(df))
    
    # Crea rangos de edad para agrupamiento
    df["RangoEdad"] = pd.cut(df["Edad"], bins=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], right=False)
    
    return df

# Carga los datos del archivo
df = cargar_datos("marketing_campaign.csv")


# BARRA LATERAL DE FILTROS

# Contenido de la barra lateral
with st.sidebar:
    # Título de los filtros
    st.markdown("<h2 style='color: #58a6ff;'>⚙️ Filtros de Segmentación</h2>", unsafe_allow_html=True)
    
    # Filtro por estado civil con emojis
    estados_civiles = sorted(df['EstadoCivil'].unique())
    estado_civil_seleccionado = st.multiselect(
        "_estado_civil",
        options=estados_civiles,
        default=estados_civiles,
        format_func=lambda x: f"💍 {x}" if x in ['Married', 'Together'] else f"👤 {x}"
    )

    # Filtro por rango de edad con emojis
    rangos_edad_opciones = sorted(df['RangoEdad'].astype(str).unique())
    rango_edad_seleccionado = st.multiselect(
        "rango_edad",
        options=rangos_edad_opciones,
        default=rangos_edad_opciones,
        format_func=lambda x: f"🎂 {x}"
    )

    # Filtro por género con emojis
    generos = df['Genero'].unique()
    genero_seleccionado = st.multiselect(
        "genero",
        options=generos,
        default=generos,
        format_func=lambda x: f"♂️ {x}" if x == "Hombre" else f"♀️ {x}"
    )
    
    # Botón para actualizar el dashboard
    actualizar = st.button("🔄 Actualizar Dashboard", type="primary")

# Aplica los filtros seleccionados al DataFrame
df_filtrado = df[
    df['EstadoCivil'].isin(estado_civil_seleccionado) &
    df['RangoEdad'].astype(str).isin(rango_edad_seleccionado) &
    df['Genero'].isin(genero_seleccionado)
]

# ================================
# MÉTRICAS PRINCIPALES
# ================================
# Título de las métricas clave
st.markdown("### 📊 Métricas Clave del Segmento Seleccionado")

# Crea 4 columnas para las métricas
col1, col2, col3, col4 = st.columns(4)

# Métrica 1: Total de clientes segmentados
with col1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric(
        label="👥 Clientes Segmentados", 
        value=f"{len(df_filtrado):,}",
        delta=f"{len(df_filtrado)/len(df)*100:.1f}% del total"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Métrica 2: Gasto promedio
with col2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric(
        label="💰 Gasto Promedio", 
        value=f"${df_filtrado['GastoTotal'].mean():,.2f}",
        delta=f"${df_filtrado['GastoTotal'].std():,.2f} std"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Métrica 3: Edad promedio
with col3:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.metric(
        label=" Edad Promedio", 
        value=f"{df_filtrado['Edad'].mean():.1f} años",
        delta=f"{df_filtrado['Edad'].std():.1f} años std"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Métrica 4: Género dominante
with col4:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    genero_dominante = df_filtrado['Genero'].mode()[0] if not df_filtrado.empty else "N/A"
    st.metric(
        label="👤 Género Dominante", 
        value=genero_dominante,
        delta=f"{df_filtrado['Genero'].value_counts().iloc[0] if not df_filtrado.empty else 0} clientes"
    )
    st.markdown("</div>", unsafe_allow_html=True)


# CUERPO PRINCIPAL DEL DASHBOARD

# Línea divisoria
st.markdown("---")

# Verifica si hay datos filtrados
if df_filtrado.empty:
    # Mensaje de error si no hay datos
    st.error("⚠️ No hay datos disponibles para los filtros seleccionados. Por favor, amplía tu selección.")
else:
    # PRIMERA FILA DE GRÁFICOS
    col1, col2 = st.columns(2)

    # Gráfico 1: Distribución de Edades
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("🎂 Distribución de Edades")
        
        # Histograma interactivo con Plotly
        fig = px.histogram(
            df_filtrado, 
            x="Edad", 
            nbins=25,
            title="Distribución de Clientes por Edad",
            color_discrete_sequence=['#58a6ff']
        )

        fig.update_layout(
            plot_bgcolor='#161b22',
            paper_bgcolor='#161b22',
            font_color='#e6edf3',
            title_font_size=16,
            title_x=0.5
        )
        fig.update_traces(xbins=dict(size=10))
        fig.update_traces(marker_line_width=1, marker_line_color="#0d1117")
        fig.update_xaxes(dtick=10)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("📊 Histograma mostrando la frecuencia de clientes por edad")
        st.markdown("</div>", unsafe_allow_html=True)

    # Gráfico 2: Edad por Estado Civil
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("💍 Edad por Estado Civil")
        
        # Box plot interactivo
        fig = px.box(
            df_filtrado, 
            x="EstadoCivil", 
            y="Edad",
            title="Distribución de Edades por Estado Civil",
            color="EstadoCivil",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            plot_bgcolor='#161b22',
            paper_bgcolor='#161b22',
            font_color='#e6edf3',
            title_font_size=16,
            title_x=0.5,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("📦 Diagrama de cajas mostrando la distribución de edades por estado civil")
        st.markdown("</div>", unsafe_allow_html=True)

    # SEGUNDA FILA DE GRÁFICOS
    col3, col4 = st.columns(2)

    # Gráfico 3: Gasto Promedio por Rango de Edad
    with col3:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("💸 Gasto Promedio por Rango de Edad")
        
        # Agrupa datos por rango de edad para calcular gasto promedio
        gasto_por_rango = df_filtrado.groupby("RangoEdad")["GastoTotal"].mean().reset_index()
        gasto_por_rango['RangoEdad'] = gasto_por_rango['RangoEdad'].astype(str)
        
        # Gráfico de barras con color progresivo
        fig = px.bar(
            gasto_por_rango,
            x='RangoEdad',
            y='GastoTotal',
            title='Gasto Total Promedio por Rango de Edad',
            color='GastoTotal',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            plot_bgcolor='#161b22',
            paper_bgcolor='#161b22',
            font_color='#e6edf3',
            title_font_size=16,
            title_x=0.5,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("📊 Barras mostrando el gasto promedio en cada rango de edad")
        st.markdown("</div>", unsafe_allow_html=True)

    # Gráfico 4: Pirámide Poblacional
    with col4:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("👥 Pirámide Poblacional por Género")
        
        # Prepara datos para la pirámide poblacional
        pop = df_filtrado.groupby(["Edad", "Genero"]).size().unstack(fill_value=0)
        if "Hombre" not in pop: pop["Hombre"] = 0
        if "Mujer" not in pop: pop["Mujer"] = 0
        pop["Hombre"] = -pop["Hombre"]

        # Crea gráfico de doble barra horizontal
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=pop.index,
            x=pop["Hombre"],
            name='Hombres',
            orientation='h',
            marker_color='#1f6feb'
        ))
        fig.add_trace(go.Bar(
            y=pop.index,
            x=pop["Mujer"],
            name='Mujeres',
            orientation='h',
            marker_color='#ea60df'
        ))

        fig.update_layout(
            title='Distribución de Clientes por Edad y Género',
            plot_bgcolor='#161b22',
            paper_bgcolor='#161b22',
            font_color='#e6edf3',
            title_font_size=16,
            title_x=0.5,
            barmode='relative',
            bargap=0.0,
            bargroupgap=0
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("📊 Gráfico de doble barra mostrando distribución por género y edad")
        st.markdown("</div>", unsafe_allow_html=True)

    # GRÁFICO ADICIONAL: Distribución de Género
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("👤 Distribución de Género")
    
    # Crea gráfico de pastel con agujero central
    genero_counts = df_filtrado['Genero'].value_counts()
    fig = px.pie(
        values=genero_counts.values,
        names=genero_counts.index,
        title='Distribución de Clientes por Género',
        color_discrete_sequence=['#1f6feb', '#ea60df'],
        hole=0.4
    )
    fig.update_layout(
        plot_bgcolor='#161b22',
        paper_bgcolor='#161b22',
        font_color='#e6edf3',
        title_font_size=16,
        title_x=0.5
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

  
    # STORYTELLING FINAL
  
    st.markdown("---")
    st.markdown("<h3 style='color: #58a6ff;'>📈 Insights y Recomendaciones Estratégicas</h3>", unsafe_allow_html=True)
    
    # Columnas para insights
    col_insights1, col_insights2 = st.columns(2)
    
    # Insights izquierdos
    with col_insights1:
        st.markdown("""
        <div class='insight-box'>
            <h4>🎯 Público Objetivo Principal</h4>
            <p>El segmento seleccionado tiene un <strong>promedio de edad de {:.1f} años</strong>, lo que indica una base de clientes madura y estable, ideal para estrategias de fidelización y valor a largo plazo.</p> 
        </div>
        """.format(df_filtrado['Edad'].mean()), unsafe_allow_html=True)
        
        st.markdown("""
        <div class='insight-box'>
            <h4>💰 Potencial de Compra</h4>
            <p>El grupo de edad entre <strong>{}</strong> registra el mayor gasto promedio de ${:.2f}, indicando que este segmento es el más valioso para campañas de alto valor.</p>
        </div>
        """.format(
            df_filtrado.groupby("RangoEdad")["GastoTotal"].mean().idxmax(),
            df_filtrado.groupby("RangoEdad")["GastoTotal"].mean().max()
        ), unsafe_allow_html=True)

    # Insights derechos
    with col_insights2:
        st.markdown("""
        <div class='insight-box'>
            <h4>👥 Composición Demográfica</h4>
            <p>El género dominante es <strong>{}</strong> con {:,} clientes, lo que indica que las estrategias de marketing deberían considerar preferencias específicas de este grupo.</p>
        """.format(
            df_filtrado['Genero'].mode()[0],
            df_filtrado['Genero'].value_counts().iloc[0]
        ), unsafe_allow_html=True)
        
        st.markdown("""
        <div class='insight-box'>
            <h4>💍 Estado Civil y Compromiso</h4>
            <p>El estado civil más común es <strong>{}</strong>, sugiriendo que las campañas familiares o de pareja podrían ser particularmente efectivas para este segmento.</p>
        </div>
        """.format(df_filtrado['EstadoCivil'].mode()[0]), unsafe_allow_html=True)

    # Recomendaciones estratégicas
    st.markdown("""
    <div style='background-color: #f0f8ff; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-top: 20px;'>
        <h4>💡 Estrategia Recomendada</h4>
        <p>👉 <strong>Segmentación Dinámica:</strong> Aprovecha los filtros para crear campañas personalizadas basadas en edad, género y estado civil. Combina los insights para crear mensajes específicos que resuenen con cada subsegmento.</p>
        <p>👉 <strong>Enfoque en Gasto:</strong> Dirige recursos hacia el grupo de edad con mayor poder adquisitivo identificado y adapta el contenido del mensaje para maximizar la conversión.</p>
    </div>
    """, unsafe_allow_html=True)

# FOOTER - Pie de página
st.markdown("---")
st.markdown("<div class='footer'>📊 Dashboard de Marketing | Desarrollado por Equipo de Análisis  Grupo # 1| 🎯 Insights Estratégicos</div>", unsafe_allow_html=True)