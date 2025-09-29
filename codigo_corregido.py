#Cambios aplicados:
#Edad ahora usa el año actual en vez de 2025.
#Se manejan NaN en columnas de gasto.
#Los rangos de edad ahora tienen etiquetas como 20-29 (mucho más claro).
#Insight de público objetivo ahora usa la mediana de edad en vez de la desviación estándar.
#El campo Genero ahora se crea solo si no está en el CSV.
#Código más limpio y ordenado.


import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Marketing - Segmentación",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------
# Cargar datos y preprocesar
# -------------------------------
@st.cache_data
def cargar_datos(path):
    df = pd.read_csv(path, sep=";")
    
    # Calcular edad dinámicamente
    current_year = pd.Timestamp.now().year
    df["Edad"] = current_year - df["Year_Birth"]
    
    # Manejo de NaN en montos antes de sumar
    cols = ["MntWines","MntFruits","MntMeatProducts",
            "MntFishProducts","MntSweetProducts","MntGoldProds"]
    df["GastoTotal"] = df[cols].fillna(0).sum(axis=1)
    
    # Renombrar columnas
    df.rename(columns={"Marital_Status": "EstadoCivil"}, inplace=True)
    
    # Si no existe género en el dataset → simularlo
    if "Gender" in df.columns:
        df["Genero"] = df["Gender"].map({"M": "Hombre", "F": "Mujer"})
    else:
        np.random.seed(42)
        df["Genero"] = np.random.choice(["Hombre","Mujer"], size=len(df))
    
    # Crear rangos de edad con etiquetas claras
    bins = list(range(10, 101, 10))  # 10-19, 20-29, ... 90-99
    labels = [f"{i}-{i+9}" for i in bins[:-1]]
    df["RangoEdad"] = pd.cut(df["Edad"], bins=bins, labels=labels, right=False)
    
    return df

df = cargar_datos("marketing_campaign.csv")

# -------------------------------
# Sidebar de filtros
# -------------------------------
st.sidebar.header("🎯 Segmentación de Clientes")

estados_civiles = df["EstadoCivil"].dropna().unique()
rangos_edades = df["RangoEdad"].dropna().unique()
generos = df["Genero"].dropna().unique()

filtros_estado = st.sidebar.multiselect("👥 Estado Civil", options=estados_civiles, default=estados_civiles)
filtros_edad = st.sidebar.multiselect("📊 Rango de Edad", options=rangos_edades, default=rangos_edades)
filtros_genero = st.sidebar.multiselect("⚧ Género", options=generos, default=generos)

df_filtrado = df[
    (df["EstadoCivil"].isin(filtros_estado)) &
    (df["RangoEdad"].isin(filtros_edad)) &
    (df["Genero"].isin(filtros_genero))
]

# -------------------------------
# Métricas principales
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👤 Clientes Segmentados",
        f"{len(df_filtrado):,}",
        delta=f"{(len(df_filtrado)/len(df)*100):.1f}% del total"
    )
with col2:
    gasto_prom = df_filtrado["GastoTotal"].mean()
    st.metric("💰 Gasto Promedio", f"${gasto_prom:,.0f}")
with col3:
    edad_prom = df_filtrado["Edad"].mean()
    st.metric("🎂 Edad Promedio", f"{edad_prom:.1f} años")
with col4:
    if not df_filtrado.empty:
        genero_dom = df_filtrado["Genero"].mode()[0]
        count_dom = (df_filtrado["Genero"] == genero_dom).sum()
        st.metric("⚧ Género Dominante", genero_dom, delta=f"{count_dom} clientes")
    else:
        st.metric("⚧ Género Dominante", "N/A")

# -------------------------------
# Gráficos
# -------------------------------
if df_filtrado.empty:
    st.error("⚠️ No hay datos con los filtros aplicados.")
    st.stop()

# Histograma
fig1 = px.histogram(df_filtrado, x="Edad", nbins=25, title="📊 Distribución de Edades")
st.plotly_chart(fig1, use_container_width=True)

# Boxplot por estado civil
fig2 = px.box(df_filtrado, x="EstadoCivil", y="Edad", color="EstadoCivil",
              title="🎂 Edad por Estado Civil", color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig2, use_container_width=True)

# Gasto promedio por rango
gasto_por_rango = df_filtrado.groupby("RangoEdad")["GastoTotal"].mean().reset_index()
fig3 = px.bar(gasto_por_rango, x="RangoEdad", y="GastoTotal", 
              title="💵 Gasto Promedio por Rango de Edad",
              color="GastoTotal", color_continuous_scale="Blues")
st.plotly_chart(fig3, use_container_width=True)

# Pirámide poblacional
pop = df_filtrado.groupby(["Edad","Genero"]).size().unstack(fill_value=0)
for g in ["Hombre","Mujer"]:
    if g not in pop.columns:
        pop[g] = 0
pop["Hombre"] = -pop["Hombre"]

fig4 = go.Figure()
fig4.add_bar(y=pop.index, x=pop["Hombre"], name="Hombres", orientation="h")
fig4.add_bar(y=pop.index, x=pop["Mujer"], name="Mujeres", orientation="h")
fig4.update_layout(title="👥 Pirámide Poblacional", barmode="overlay")
st.plotly_chart(fig4, use_container_width=True)

# Pie de géneros
genero_counts = df_filtrado["Genero"].value_counts()
fig5 = px.pie(genero_counts, values=genero_counts.values, names=genero_counts.index,
              hole=0.4, title="⚧ Distribución de Género")
st.plotly_chart(fig5, use_container_width=True)

# -------------------------------
# Insights
# -------------------------------
st.subheader("📌 Insights del Segmento")
if not df_filtrado.empty:
    pub_objetivo = df_filtrado["Edad"].median()
    gasto_top = gasto_por_rango.loc[gasto_por_rango["GastoTotal"].idxmax()]
    st.markdown(f"""
    - 🎯 **Público Objetivo Principal:** {int(pub_objetivo)} años (mediana).
    - 💰 **Mayor Gasto Promedio:** {gasto_top["RangoEdad"]} con ${gasto_top["GastoTotal"]:,.0f}.
    - 👥 **Estado Civil más común:** {df_filtrado["EstadoCivil"].mode()[0]}.
    """)
