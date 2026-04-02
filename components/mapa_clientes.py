import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COLORES = {
    "Retail": "#3B82F6",
    "Distribuidora": "#10B981",
    "Supermercado": "#F59E0B",
    "Bodega": "#EF4444"
}

def mostrar_mapa(df):
    df = df.copy()
    df["color"] = df["categoria"].map(COLORES).fillna("#3B82F6")
    df["tamanio"] = (df["ventas"] / df["ventas"].max() * 40).clip(lower=8)
    df["texto"] = df["cliente"] + "<br>" + df["distrito"] + "<br>S/ " + df["ventas"].apply(lambda x: f"{x:,}")

    fig = go.Figure()

    for cat, color in COLORES.items():
        subset = df[df["categoria"] == cat]
        if len(subset) == 0:
            continue
        fig.add_trace(go.Scattermapbox(
            lat=subset["lat"],
            lon=subset["lon"],
            mode="markers",
            marker=dict(
                size=subset["tamanio"],
                color=color,
                opacity=0.85,
            ),
            text=subset["texto"],
            hovertemplate="%{text}<extra></extra>",
            name=cat
        ))

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=-12.05, lon=-77.03),
            zoom=10.5
        ),
        height=520,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#0A1628",
        legend=dict(
            bgcolor="#0F2044",
            font=dict(color="#E2E8F0", size=12),
            bordercolor="#1E3A5F",
            borderwidth=1
        )
    )
    st.plotly_chart(fig, use_container_width=True)

def mostrar_kpis_mapa(df):
    total_clientes = len(df)
    total_ventas   = df["ventas"].sum()
    mejor_cliente  = df.loc[df["ventas"].idxmax(), "cliente"]
    top_distrito   = df.groupby("distrito")["ventas"].sum().idxmax()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Total clientes",  f"{total_clientes}")
    col2.metric("💰 Ventas totales",  f"S/ {total_ventas:,.0f}")
    col3.metric("🏆 Mejor cliente",   mejor_cliente)
    col4.metric("📍 Distrito top",    top_distrito)

def mostrar_tabla_clientes(df):
    resumen = df.groupby("distrito").agg(
        Clientes=("cliente", "count"),
        Ventas=("ventas", "sum")
    ).reset_index().sort_values("Ventas", ascending=False)
    resumen["Ventas"] = resumen["Ventas"].apply(lambda x: f"S/ {x:,.0f}")
    resumen.columns = ["Distrito", "Clientes", "Ventas"]
    st.dataframe(resumen, use_container_width=True, hide_index=True)
