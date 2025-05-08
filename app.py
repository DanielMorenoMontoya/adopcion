# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time # Import time for spinner

# --- Configuración de la Página ---
st.set_page_config(
    layout="wide",
    page_title="Herramienta de Adopción SaaS B2B Latam",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# --- Estilos CSS Mejorados (v9 - Correcciones finales modo claro y colores) ---
NEW_PRIMARY_COLOR = "#00535E"
LIGHT_BACKGROUND_COLOR = "#f0f2f5" # Un gris muy claro para el fondo general
WHITE_BACKGROUND_COLOR = "#FFFFFF" # Blanco para elementos como inputs, tarjetas, etc.
TEXT_COLOR_ON_LIGHT_BG = "#1a1a1a" # Negro/gris oscuro para texto principal
SECONDARY_TEXT_COLOR = "#4f4f4f" # Gris medio para texto secundario o menos importante
DEFAULT_TEXT_COLOR_INPUT_LABELS = "#495057" # Color para etiquetas de inputs
BORDER_COLOR = "#ced4da" # Color de borde estándar

st.markdown(f"""
<style>
    /* --- Forzar Tema Claro Global --- */
    html, body, div[data-testid="stAppViewContainer"], div[data-testid="stReportViewContainer"], div.main, section[data-testid="stSidebar"] {{
        background-color: {LIGHT_BACKGROUND_COLOR} !important;
        color: {TEXT_COLOR_ON_LIGHT_BG} !important;
    }}
    section[data-testid="stHeader"] {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
        border-bottom: 1px solid #e0e0e0;
    }}
    section[data-testid="stHeader"] h1, section[data-testid="stHeader"] p, section[data-testid="stHeader"] .stToolbar {{ 
        color: {TEXT_COLOR_ON_LIGHT_BG} !important;
    }}

    /* --- Textos Generales y Títulos --- */
    body {{
        font-family: 'Inter', sans-serif;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {TEXT_COLOR_ON_LIGHT_BG} !important;
        font-weight: 600;
    }}
    p, .stMarkdown p {{
        color: {SECONDARY_TEXT_COLOR} !important;
        line-height: 1.6;
    }}
    .stCaption {{
        color: #666 !important;
        font-style: italic;
    }}

    /* --- Pestañas --- */
    .stTabs [data-baseweb="tab-list"] {{
        border-bottom: 2px solid #e0e0e0;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important;
        color: #666 !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: #e9ecef !important;
        color: #333 !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: {NEW_PRIMARY_COLOR} !important;
        border-bottom: 3px solid {NEW_PRIMARY_COLOR} !important;
    }}

    /* --- Botones --- */
    .stButton>button, .stDownloadButton>button {{
        background-color: {NEW_PRIMARY_COLOR} !important;
        color: white !important;
        border: none !important;
    }}
    .stButton>button:hover, .stDownloadButton>button:hover {{
        background-color: color-mix(in srgb, {NEW_PRIMARY_COLOR} 80%, black) !important;
    }}

    /* --- Tarjetas y Cajas de Información --- */
    .metric-card, .info-box, .warning-box, .success-box, .pessimistic-box {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
        color: {TEXT_COLOR_ON_LIGHT_BG} !important;
    }}
    .metric-card h2 {{
        color: {NEW_PRIMARY_COLOR} !important;
    }}
    .info-box {{
        border-left-color: #17a2b8; background-color: #e8f7f9 !important;}}
    .warning-box {{
        border-left-color: #ffc107; background-color: #fff9e6 !important; }}
    .pessimistic-box {{
        border-left-color: #fd7e14; background-color: #fff3e0 !important; }}
    .success-box {{
        border-left-color: #28a745; background-color: #eaf6ec !important; }}
    .metric-card h3, .info-box h4, .warning-box h4, .success-box h4, .pessimistic-box h4 {{
        color: {TEXT_COLOR_ON_LIGHT_BG} !important;
    }}

    /* --- Entradas (Inputs) --- */
    .stTextInput>div>div>input,
    .stSelectbox>div>div,
    .stMultiSelect>div>div[data-baseweb="select"] {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
        color: {TEXT_COLOR_ON_LIGHT_BG} !important;
        border: 1px solid {BORDER_COLOR} !important;
    }}
    /* Placeholder text color for inputs */
    .stTextInput input::placeholder {{
        color: #888 !important;
    }}
    /* Dropdown list items for st.selectbox and st.multiselect */
    div[data-baseweb="popover"] ul[role="listbox"] li[role="option"] > div {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
        color: {TEXT_COLOR_ON_LIGHT_BG} !important;
    }}
    div[data-baseweb="popover"] ul[role="listbox"] li[aria-selected="true"] > div {{
        background-color: color-mix(in srgb, {NEW_PRIMARY_COLOR} 20%, {WHITE_BACKGROUND_COLOR}) !important;
        color: {NEW_PRIMARY_COLOR} !important;
    }}

    /* Estilos para Sliders (st.slider y st.select_slider) */
    .stSlider [data-baseweb="slider"] > div:nth-child(1) /* Track inactivo */
    {{
        background-color: #D3D3D3 !important;
    }}
    .stSlider [data-baseweb="slider"] > div:nth-child(2) > div, /* Barra activa de st.slider */
    .stSlider div[data-testid="stTickBar"] > div[style*="background: rgb(0, 83, 94)"] /* Barra activa de st.select_slider (color nuevo) */
    {{
        background-color: {NEW_PRIMARY_COLOR} !important;
    }}
    .stSlider [data-baseweb="slider"] > div:nth-child(3) > div /* Círculo/Thumb */
    {{
        background-color: {NEW_PRIMARY_COLOR} !important;
        border: 2px solid {NEW_PRIMARY_COLOR} !important;
    }}
    /* Texto del valor actual del slider (ej. 'Media') */
    .stSlider > div > div[data-testid="stTextLabel"] > div,
    .stSlider > div > div[style*="text-align: center;"] > div,
    .stSlider > div > div[style*="text-align: center;"]
    {{
        color: {NEW_PRIMARY_COLOR} !important;
        background-color: transparent !important;
        font-weight: bold;
    }}
    /* Etiquetas de los extremos del st.select_slider (ej. 'Muy Baja', 'Muy Alta') */
    .stSlider div[data-testid="stTickBar"] > div,
    .stSlider div[data-testid="stTickBar"] span,
    .stSlider div[role="listbox"] div[role="option"] > div /* Opciones de st.select_slider */
    {{
        background-color: transparent !important;
        color: {DEFAULT_TEXT_COLOR_INPUT_LABELS} !important;
        padding: 0px !important; /* Reducir padding para evitar que se vea como fondo */
        border-radius: 0px !important;
        font-weight: normal !important;
    }}

    /* Radio Buttons */
    .stRadio>div {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
        border: 1px solid {BORDER_COLOR} !important;
    }}
    .stRadio label span {{
        color: {DEFAULT_TEXT_COLOR_INPUT_LABELS} !important;
    }}
    .stRadio input[type="radio"]:checked + div {{
        background-color: color-mix(in srgb, {NEW_PRIMARY_COLOR} 15%, {WHITE_BACKGROUND_COLOR}) !important;
        border-color: {NEW_PRIMARY_COLOR} !important;
        color: color-mix(in srgb, {NEW_PRIMARY_COLOR} 80%, black) !important;
    }}

    /* Etiquetas de todos los inputs */
    .stSelectbox label, .stSlider label, .stMultiSelect label, .stRadio label, .stTextInput label {{
        color: {DEFAULT_TEXT_COLOR_INPUT_LABELS} !important;
        font-weight: 500;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }}

    /* Chips/Tags de st.multiselect */
    .stMultiSelect span[data-baseweb="tag"],
    .stMultiSelect span[data-baseweb="tag"] span {{
        background-color: {NEW_PRIMARY_COLOR} !important;
        color: white !important;
    }}
    .stMultiSelect span[data-baseweb="tag"] svg {{
        fill: white !important;
    }}

    /* --- DataFrames y Gráficos --- */
    .stDataFrame,
    .stDataFrame table,
    .stDataFrame th,
    .stDataFrame td {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
        color: {TEXT_COLOR_ON_LIGHT_BG} !important;
        border-color: #e0e0e0 !important; /* Borde más claro para tablas */
    }}
    .stDataFrame thead th {{
        background-color: #f8f9fa !important; /* Un fondo ligeramente diferente para encabezados de tabla */
    }}
    .stPlotlyChart {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
    }}

    /* --- Footer --- */
    footer {{
        visibility: hidden;
    }}
    .footer-custom {{
        text-align: center;
        padding: 1.5rem 0;
        margin-top: 3rem;
        font-size: 0.9rem;
        color: #6c757d;
        border-top: 1px solid #e0e0e0;
    }}

</style>
""", unsafe_allow_html=True)

# --- Datos (Actualizados y Adaptados) ---
# (El resto del código Python permanece igual)
# ... (código de datos, lógica de la app, etc.) ...

# --- Título y Descripción ---
st.title("🚀 Herramienta de Estimación de Adopción SaaS")
st.markdown("**Plataforma interactiva para definir objetivos de adopción en software contable B2B para Latam.**")
st.markdown("--- ")

# --- Componentes de la Herramienta (Pestañas) ---
tab2, tab1, tab3 = st.tabs(["🧮 Calculadora Predictiva", "🧭 Explorador de Benchmarks", "📄 Generador de Informes"])

# --- Funciones Auxiliares ---
def extract_avg(range_str):
    try:
        parts = str(range_str).replace("%".encode("utf-8").decode("utf-8"), "").replace("$".encode("utf-8").decode("utf-8"), "").split("-")
        if len(parts) == 2:
            return (float(parts[0]) + float(parts[1])) / 2
        elif len(parts) == 1 and parts[0] != "":
            if ":" in parts[0]:
                return float(parts[0].split(":")[0])
            return float(parts[0])
        else:
            return np.nan
    except:
        return np.nan

# Configuración de tema para Matplotlib/Seaborn para gráficos
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.facecolor"] = WHITE_BACKGROUND_COLOR
plt.rcParams["figure.facecolor"] = WHITE_BACKGROUND_COLOR
plt.rcParams["text.color"] = TEXT_COLOR_ON_LIGHT_BG
plt.rcParams["axes.labelcolor"] = SECONDARY_TEXT_COLOR
plt.rcParams["xtick.color"] = SECONDARY_TEXT_COLOR
plt.rcParams["ytick.color"] = SECONDARY_TEXT_COLOR
plt.rcParams["axes.edgecolor"] = BORDER_COLOR

# --- Pestaña Calculadora Predictiva ---
with tab2:
    st.header("🧮 Calculadora Predictiva de Tasa de Adopción")
    st.markdown("""
    <div class="info-box">
    <h4 style="margin-top:0">💡 ¿Cómo funciona?</h4>
    Introduce las características de tu nueva funcionalidad y observa la estimación del rango de adopción
    esperado a los 3 meses.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("1. Define tu Funcionalidad")
    with st.container():
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            nombre_funcionalidad = st.text_input("Nombre de la Funcionalidad:", placeholder="Ej: Facturación Electrónica 4.0", help="Nombre descriptivo para identificarla.")
            tipo_funcionalidad = st.selectbox(
                "Tipo de Funcionalidad:",
                ["Facturación electrónica", "Reportes fiscales", "Inventarios", "Contabilidad", "Ventas en POS", "Nómina electrónica"],
                index=0, help="Categoría principal de la funcionalidad.")
            complejidad = st.select_slider(
                "Nivel de Complejidad Percibida:",
                options=["Muy Baja", "Baja", "Media", "Alta", "Muy Alta"],
                value="Media", help="¿Qué tan difícil es para el usuario entender y usar la funcionalidad?")
            segmento = st.multiselect(
                "Segmento(s) de Usuario Objetivo:",
                ["Pequeña empresa", "Mediana empresa", "Contador", "Auxiliar contable", "Dueño de negocio", "Usuario final POS"],
                default=["Pequeña empresa"], help="¿A quién va dirigida principalmente?")
            paises = st.multiselect(
                "País(es) Objetivo(s):",
                ["Colombia", "México", "Costa Rica", "República Dominicana"],
                default=["Colombia"], help="Mercados principales de lanzamiento.")

        with col_in2:
            valor_percibido = st.select_slider(
                "Valor Percibido / Urgencia:",
                options=["Muy Bajo", "Bajo", "Medio", "Alto", "Muy Alto"],
                value="Medio", help="¿Cuánto valor aporta al usuario y qué tan urgente es su necesidad?")
            regulatorio = st.radio("¿Es un Requisito Regulatorio?", ("No", "Sí"), horizontal=True, help="¿Es obligatorio por ley o normativa en el país/países objetivo?")
            esfuerzo_mkt = st.select_slider(
                "Esfuerzo de Marketing/Comunicación Planeado:",
                options=["Muy Bajo", "Bajo", "Medio", "Alto", "Muy Alto"],
                value="Medio", help="Nivel de inversión en promoción y comunicación.")
            esfuerzo_soporte = st.select_slider(
                "Esfuerzo de Soporte/Capacitación Planeado:",
                options=["Muy Bajo", "Bajo", "Medio", "Alto", "Muy Alto"],
                value="Medio", help="Nivel de inversión en documentación, tutoriales y soporte.")
            integracion_compleja = st.radio("¿Requiere Integración Compleja por parte del Usuario?", ("No", "Sí"), horizontal=True, help="¿Necesita el usuario configurar conexiones complejas con otros sistemas?")

    # --- Lógica de Predicción (Adaptada a nuevos países y funcionalidades) ---
    if tipo_funcionalidad == "Facturación electrónica": base_score = 45
    elif tipo_funcionalidad == "Reportes fiscales": base_score = 40
    elif tipo_funcionalidad == "Nómina electrónica": base_score = 38
    elif tipo_funcionalidad == "Contabilidad": base_score = 30
    elif tipo_funcionalidad == "Inventarios": base_score = 28
    elif tipo_funcionalidad == "Ventas en POS": base_score = 25
    else: base_score = 30

    complejidad_map = {"Muy Baja": 15, "Baja": 10, "Media": 0, "Alta": -10, "Muy Alta": -20}
    base_score += complejidad_map[complejidad]
    valor_map = {"Muy Bajo": -15, "Bajo": -10, "Medio": 0, "Alto": 10, "Muy Alto": 20}
    base_score += valor_map[valor_percibido]
    if regulatorio == "Sí": base_score += 25
    esfuerzo_mkt_map = {"Muy Bajo": -10, "Bajo": -5, "Medio": 0, "Alto": 8, "Muy Alto": 15}
    base_score += esfuerzo_mkt_map[esfuerzo_mkt]
    esfuerzo_soporte_map = {"Muy Bajo": -10, "Bajo": -5, "Medio": 0, "Alto": 8, "Muy Alto": 15}
    base_score += esfuerzo_soporte_map[esfuerzo_soporte]
    if integracion_compleja == "Sí": base_score -= 15
    
    segment_impact = 0
    if "Pequeña empresa" in segmento: segment_impact += 2
    if "Mediana empresa" in segmento: segment_impact -= 3
    if "Contador" in segmento: segment_impact += 8
    if "Auxiliar contable" in segmento: segment_impact += 5
    if "Dueño de negocio" in segmento: segment_impact -= 5
    if "Usuario final POS" in segmento: segment_impact -= 2
    base_score += segment_impact
    
    country_impact = 0
    country_factors = {"México": 3, "Colombia": 3, "Costa Rica": -1, "República Dominicana": -2}
    for pais in paises:
        country_impact += country_factors.get(pais, 0)
    if len(paises) > 0:
        country_impact = country_impact / len(paises)
    base_score += country_impact
    
    base_score = max(10, min(90, base_score))
    
    rango_objetivo_base = f"{max(5, int(base_score - 7))}% - {min(95, int(base_score + 7))}%"
    rango_objetivo_optimista = f"{max(10, int(base_score))}% - {min(100, int(base_score + 15))}%"
    rango_objetivo_pesimista = f"{max(0, int(base_score - 15))}% - {min(90, int(base_score))}%"
    
    base_medio = (max(5, int(base_score - 7)) + min(95, int(base_score + 7))) / 2
    optimista_medio = (max(10, int(base_score)) + min(100, int(base_score + 15))) / 2
    pesimista_medio = (max(0, int(base_score - 15)) + min(90, int(base_score))) / 2

    st.subheader("2. Resultados de la Estimación")
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Tasa Objetivo (Base)</h3>
            <h2>{rango_objetivo_base}</h2>
        </div>
        """, unsafe_allow_html=True, help="Estimación central de la tasa de adopción esperada a los 3 meses.")
    with col_res2:
        st.markdown(f"""
        <div class="success-box">
            <h4>📈 Escenario Optimista</h4>
            <h3 style="color:#28a745; margin:0; font-size: 1.8rem;">{rango_objetivo_optimista}</h3>
        </div>
        """, unsafe_allow_html=True)
    with col_res3:
        st.markdown(f"""
        <div class="pessimistic-box">
            <h4>📉 Escenario Pesimista</h4>
            <h3 style="color:#fd7e14; margin:0; font-size: 1.8rem;">{rango_objetivo_pesimista}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("#### Comparación Visual de Escenarios")
        fig, ax = plt.subplots(figsize=(8, 4))
        scenarios = ["Pesimista", "Base", "Optimista"]
        values = [pesimista_medio, base_medio, optimista_medio]
        bar_colors = ["#fd7e14", NEW_PRIMARY_COLOR, "#28a745"]
        bars = ax.bar(scenarios, values, color=bar_colors, width=0.5)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1.5,
                    f"{int(height)}%", ha="center", va="bottom", fontsize=11, fontweight="medium")
        ax.set_ylim(0, 105)
        ax.set_ylabel("Tasa de Adopción (%)", fontsize=10)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)
    
    st.markdown("--- ")
    st.subheader("3. Análisis y Recomendaciones")
    with st.container():
        st.markdown("#### Factores Clave de Influencia")
        factores = []
        if regulatorio == "Sí": factores.append(("✅ Requisito Regulatorio", "Muy Positivo", "+25%"))
        if complejidad in ["Muy Baja", "Baja"]: factores.append(("👍 Baja Complejidad", "Positivo", "+10-15%"))
        elif complejidad in ["Alta", "Muy Alta"]: factores.append(("👎 Alta Complejidad", "Negativo", "-10-20%"))
        if valor_percibido in ["Alto", "Muy Alto"]: factores.append(("⭐ Alto Valor Percibido", "Positivo", "+10-20%"))
        elif valor_percibido in ["Bajo", "Muy Bajo"]: factores.append(("📉 Bajo Valor Percibido", "Negativo", "-10-15%"))
        if esfuerzo_mkt in ["Alto", "Muy Alto"]: factores.append(("📢 Alto Esfuerzo Marketing", "Positivo", "+8-15%"))
        if esfuerzo_soporte in ["Alto", "Muy Alto"]: factores.append(("🎓 Alto Esfuerzo Soporte", "Positivo", "+8-15%"))
        if integracion_compleja == "Sí": factores.append(("🔗 Integración Compleja", "Negativo", "-15%"))
        if "Contador" in segmento: factores.append(("👨‍💼 Segmento Contador", "Positivo", "+8%"))
        if "Dueño de negocio" in segmento: factores.append(("🏢 Segmento Dueño Negocio", "Negativo", "-5%"))
        if abs(country_impact) > 1: 
             factores.append(("🌍 Impacto País (Promedio)", "Positivo" if country_impact > 0 else "Negativo", f"{country_impact:+.1f}%"))
        
        if factores:
            factores_df = pd.DataFrame(factores, columns=["Factor", "Impacto", "Efecto Aprox."])
            st.dataframe(factores_df, use_container_width=True, hide_index=True)
        else:
            st.info("No se identificaron factores con impacto significativo.")

        st.markdown("#### Recomendaciones Accionables")
        recomendaciones = []
        if complejidad in ["Alta", "Muy Alta"]: recomendaciones.append("Simplificar onboarding y crear tutoriales claros.")
        if valor_percibido in ["Bajo", "Muy Bajo", "Medio"]: recomendaciones.append("Comunicar beneficios y ROI de forma efectiva.")
        if esfuerzo_mkt in ["Bajo", "Muy Bajo", "Medio"]: recomendaciones.append("Intensificar comunicación y marketing.")
        if esfuerzo_soporte in ["Bajo", "Muy Bajo", "Medio"]: recomendaciones.append("Mejorar recursos de capacitación y soporte.")
        if integracion_compleja == "Sí": recomendaciones.append("Ofrecer asistencia para la integración o simplificarla.")
        if not recomendaciones:
            recomendaciones.append("¡Buen trabajo! Parece que los factores están bien alineados. Continúa monitoreando.")
        
        for rec in recomendaciones:
            st.markdown(f"- {rec}")

# --- Pestaña Explorador de Benchmarks ---
with tab1:
    st.header("🧭 Explorador de Benchmarks de Adopción SaaS B2B (Latam)")
    st.markdown("""
    <div class="info-box">
    <h4 style="margin-top:0">📊 Datos de Referencia</h4>
    Consulta benchmarks estimados para la industria de software contable en Latinoamérica. 
    Estos valores son promedios y pueden variar significativamente.
    </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(benchmarks_df, use_container_width=True, hide_index=True)
    
    st.subheader("Evolución Histórica de Adopción (Ejemplos)")
    st.markdown("Tasas de adopción de funcionalidades lanzadas previamente (datos de ejemplo para ilustración).")
    
    line_chart_df = historical_df.copy()
    for col in ["Tasa Adopción 1 Mes", "Tasa Adopción 3 Meses", "Tasa Adopción 6 Meses"]:
        line_chart_df[col] = line_chart_df[col].str.rstrip("%".encode("utf-8").decode("utf-8")).astype("float") / 100.0
    
    line_chart_df_melted = line_chart_df.melt(
        id_vars=["Funcionalidad", "País"],
        value_vars=["Tasa Adopción 1 Mes", "Tasa Adopción 3 Meses", "Tasa Adopción 6 Meses"],
        var_name="Meses", 
        value_name="Tasa de Adopción"
    )
    line_chart_df_melted["Meses"] = line_chart_df_melted["Meses"].map({
        "Tasa Adopción 1 Mes": 1,
        "Tasa Adopción 3 Meses": 3,
        "Tasa Adopción 6 Meses": 6
    })
    line_chart_df_melted["Etiqueta"] = line_chart_df_melted["Funcionalidad"] + " (" + line_chart_df_melted["País"] + ")"

    if not line_chart_df_melted.empty:
        fig_line, ax_line = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=line_chart_df_melted, x="Meses", y="Tasa de Adopción", hue="Etiqueta", marker="o", ax=ax_line, palette="viridis")
        ax_line.set_title("Curva de Adopción Histórica por Funcionalidad y País", fontsize=15)
        ax_line.set_xlabel("Meses desde Lanzamiento", fontsize=12)
        ax_line.set_ylabel("Tasa de Adopción Acumulada", fontsize=12)
        ax_line.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))
        ax_line.legend(title="Funcionalidad (País)", bbox_to_anchor=(1.05, 1), loc="upper left")
        ax_line.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        st.pyplot(fig_line)
    else:
        st.warning("No hay datos históricos disponibles para graficar.")

# --- Pestaña Generador de Informes (Placeholder) ---
with tab3:
    st.header("📄 Generador de Informes")
    st.info("Esta funcionalidad estará disponible próximamente. Permitirá generar un resumen de las estimaciones y benchmarks.")

# --- Footer Personalizado ---
st.markdown("""
<div class="footer-custom">
    Hecho con ❤️ por un IA | Herramienta de Estimación de Adopción v9
</div>
""", unsafe_allow_html=True)

