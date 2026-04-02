import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium

COLORES = {
    "Retail": "#3B82F6",
    "Distribuidora": "#10B981",
    "Supermercado": "#F59E0B",
    "Bodega": "#EF4444"
}

def mostrar_mapa(df):
    m = folium.Map(
        location=[-12.05, -77.03],
        zoom_start=11,
        tiles="CartoDB dark_matter"
    )

    for _, row in df.iterrows():
        color = COLORES.get(row["categoria"], "#3B82F6")
        radio = max(8, min(25, int(row["ventas"] / 5000)))

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=radio,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(f"""
                <div style='font-family:sans-serif; min-width:150px;'>
                    <b style='color:#1e293b;'>{row['cliente']}</b><br>
                    <span style='color:#64748b;'>{row['distrito']}</span><br>
                    <span style='color:#059669; font-weight:bold;'>S/ {row['ventas']:,}</span>
                </div>
            """, max_width=200),
            tooltip=f"{row['cliente']} — S/ {row['ventas']:,}"
        ).add_to(m)

    heat_data = [[row["lat"], row["lon"], row["ventas"]] for _, row in df.iterrows()]
    HeatMap(heat_data, radius=35, blur=25, min_opacity=0.3,
            gradient={"0.4": "#1e40af", "0.6": "#3b82f6", "0.8": "#06b6d4", "1.0": "#ffffff"}).add_to(m)

    st_folium(m, width=None, height=520, returned_objects=[])

def mostrar_kpis_mapa(df):
    total_clientes = len(df)
    total_ventas = df["ventas"].sum()
    mejor_cliente = df.loc[df["ventas"].idxmax(), "cliente"]
    top_distrito = df.groupby("distrito")["ventas"].sum().idxmax()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Total clientes",     f"{total_clientes}")
    col2.metric("💰 Ventas totales",     f"S/ {total_ventas:,.0f}")
    col3.metric("🏆 Mejor cliente",      mejor_cliente)
    col4.metric("📍 Distrito top",       top_distrito)

def mostrar_tabla_clientes(df):
    resumen = df.groupby("distrito").agg(
        Clientes=("cliente", "count"),
        Ventas=("ventas", "sum")
    ).reset_index().sort_values("Ventas", ascending=False)
    resumen["Ventas"] = resumen["Ventas"].apply(lambda x: f"S/ {x:,.0f}")
    resumen.columns = ["Distrito", "Clientes", "Ventas"]
    st.dataframe(resumen, use_container_width=True, hide_index=True)
