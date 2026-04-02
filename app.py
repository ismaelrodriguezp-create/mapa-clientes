import streamlit as st
import pandas as pd
from components.mapa_clientes import mostrar_mapa, mostrar_kpis_mapa, mostrar_tabla_clientes

st.set_page_config(page_title="Mapa de Clientes", page_icon="🗺️", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0A1628; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    section[data-testid="stSidebar"] { background: #060E1E; border-right: 1px solid #1E3A5F; }
    section[data-testid="stSidebar"] * { color: #94A3B8 !important; }
    div[data-testid="metric-container"] {
        background: #0F2044;
        border: 1px solid #1E3A5F;
        border-radius: 16px;
        padding: 16px 20px;
        box-shadow: 0 0 20px rgba(59,130,246,0.08);
    }
    div[data-testid="metric-container"] label { color: #64748B !important; font-size: 12px !important; }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #E2E8F0 !important; font-size: 22px !important; font-weight: 700 !important; }
    h1, h2, h3, h4 { color: #E2E8F0 !important; }
    p { color: #94A3B8; }
    .stDataFrame { background: #0F2044; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex; align-items:center; gap:14px; margin-bottom:4px;">
    <div style="background:linear-gradient(135deg,#1D4ED8,#0EA5E9); border-radius:14px; padding:10px 14px; box-shadow:0 0 20px rgba(59,130,246,0.3);">
        <span style="font-size:24px;">🗺️</span>
    </div>
    <div>
        <h1 style="margin:0; font-size:26px; font-weight:700;">Mapa de Clientes</h1>
        <p style="margin:0; font-size:13px;">Distribución geográfica · Lima, Perú</p>
    </div>
</div>
<hr style="border:none; border-top:1px solid #1E3A5F; margin:16px 0 20px;">
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<p style='font-size:11px; color:#475569; font-weight:600; letter-spacing:0.08em;'>DATOS</p>", unsafe_allow_html=True)
    archivo = st.file_uploader("Subir Excel o CSV", type=["csv","xlsx"])
    st.markdown("<hr style='border-color:#1E3A5F; margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px; color:#475569; font-weight:600; letter-spacing:0.08em;'>FILTROS</p>", unsafe_allow_html=True)

if archivo:
    df = pd.read_csv(archivo) if archivo.name.endswith(".csv") else pd.read_excel(archivo)
    st.sidebar.success("✓ Archivo cargado")
else:
    df = pd.read_csv("data/clientes_ejemplo.csv")
    st.sidebar.info("Usando datos de ejemplo")

cats = ["Todas"] + sorted(df["categoria"].unique().tolist())
cat_sel = st.sidebar.selectbox("Categoría", cats)
df_filtrado = df[df["categoria"] == cat_sel] if cat_sel != "Todas" else df

ventas_min = int(df["ventas"].min())
ventas_max = int(df["ventas"].max())
rango = st.sidebar.slider("Rango de ventas (S/)", ventas_min, ventas_max, (ventas_min, ventas_max), step=1000)
df_filtrado = df_filtrado[(df_filtrado["ventas"] >= rango[0]) & (df_filtrado["ventas"] <= rango[1])]

st.markdown("""
<div style="display:flex; gap:12px; margin-bottom:12px; font-size:12px; color:#64748B;">
    <span><span style="color:#3B82F6;">●</span> Retail</span>
    <span><span style="color:#10B981;">●</span> Distribuidora</span>
    <span><span style="color:#F59E0B;">●</span> Supermercado</span>
    <span><span style="color:#EF4444;">●</span> Bodega</span>
    <span style="color:#475569; margin-left:8px;">· Tamaño del círculo = volumen de ventas</span>
</div>
""", unsafe_allow_html=True)

mostrar_kpis_mapa(df_filtrado)
st.markdown("<br>", unsafe_allow_html=True)
mostrar_mapa(df_filtrado)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### 📊 Ventas por distrito")
mostrar_tabla_clientes(df_filtrado)

st.markdown("""
<hr style="border:none; border-top:1px solid #1E3A5F; margin-top:2rem;">
<p style="text-align:center; font-size:12px;">Mapa de Clientes · Python & Streamlit · Desarrollado por Ismael Rodriguez</p>
""", unsafe_allow_html=True)
