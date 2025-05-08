# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time

# --- Configuración de la Página ---
st.set_page_config(
    layout="wide",
    page_title="Herramienta de Adopción SaaS B2B Latam",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# --- Definición de Colores y Estilos ---
PRIMARY_COLOR = "#00535E"
LIGHT_BACKGROUND_COLOR = "#f0f2f5"
WHITE_BACKGROUND_COLOR = "#FFFFFF"
TEXT_COLOR_DARK = "#1a1a1a"
TEXT_COLOR_MEDIUM = "#4f4f4f"
TEXT_COLOR_LABELS = "#495057"
BORDER_COLOR_STANDARD = "#ced4da"

st.markdown(f"""
<style>
    /* --- Forzar Tema Claro Global --- */
    html, body,
    div[data-testid="stAppViewContainer"],
    div[data-testid="stReportViewContainer"],
    div.main,
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] {{
        background-color: {LIGHT_BACKGROUND_COLOR} !important;
        color: {TEXT_COLOR_DARK} !important;
    }}

    section[data-testid="stHeader"] {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
        border-bottom: 1px solid #e0e0e0;
    }}
    section[data-testid="stHeader"] h1,
    section[data-testid="stHeader"] p,
    section[data-testid="stHeader"] .stToolbar,
    section[data-testid="stHeader"] .stToolbar button svg {{
        color: {TEXT_COLOR_DARK} !important;
        fill: {TEXT_COLOR_DARK} !important;
    }}

    /* --- Textos Generales y Títulos --- */
    h1, h2, h3, h4, h5, h6 {{
        color: {TEXT_COLOR_DARK} !important;
        font-weight: 600;
    }}
    p, .stMarkdown p {{
        color: {TEXT_COLOR_MEDIUM} !important;
    }}
    .stCaption {{
        color: {TEXT_COLOR_MEDIUM} !important; opacity: 0.8;
    }}

    /* --- Pestañas --- */
    .stTabs [data-baseweb="tab-list"] {{
        border-bottom: 2px solid #e0e0e0;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important;
        color: {TEXT_COLOR_MEDIUM} !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: #e9ecef !important;
        color: {TEXT_COLOR_DARK} !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: {PRIMARY_COLOR} !important;
        border-bottom: 3px solid {PRIMARY_COLOR} !important;
    }}

    /* --- Botones --- */
    .stButton>button, .stDownloadButton>button {{
        background-color: {PRIMARY_COLOR} !important;
        color: {WHITE_BACKGROUND_COLOR} !important;
        border: none !important;
        border-radius: 6px;
    }}
    .stButton>button:hover, .stDownloadButton>button:hover {{
        background-color: color-mix(in srgb, {PRIMARY_COLOR} 80%, black) !important;
    }}

    /* --- Tarjetas y Cajas de Información --- */
    .metric-card, .info-box, .warning-box, .success-box, .pessimistic-box {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
        color: {TEXT_COLOR_DARK} !important;
        border-radius: 8px;
        padding: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        border-left: 5px solid;
    }}
    .metric-card {{
        border-left-color: {PRIMARY_COLOR};
    }}
    .metric-card h2 {{
        color: {PRIMARY_COLOR} !important;
    }}
    .info-box {{ border-left-color: #17a2b8; background-color: #e8f7f9 !important; }}
    .warning-box {{ border-left-color: #ffc107; background-color: #fff9e6 !important; }}
    .pessimistic-box {{ border-left-color: #fd7e14; background-color: #fff3e0 !important; }}
    .success-box {{ border-left-color: #28a745; background-color: #eaf6ec !important; }}
    .metric-card h3, .info-box h4, .warning-box h4, .success-box h4, .pessimistic-box h4 {{
        color: {TEXT_COLOR_DARK} !important;
        margin-top: 0;
    }}

    /* --- Entradas (Inputs) --- */
    .stTextInput>div>div>input,
    .stSelectbox>div>div,
    .stMultiSelect>div>div[data-baseweb="select"] {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
        color: {TEXT_COLOR_DARK} !important;
        border: 1px solid {BORDER_COLOR_STANDARD} !important;
        border-radius: 6px;
    }}
    .stTextInput input::placeholder {{
        color: #888 !important;
    }}
    div[data-baseweb="popover"] ul[role="listbox"] li[role="option"] > div {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
        color: {TEXT_COLOR_DARK} !important;
    }}
    div[data-baseweb="popover"] ul[role="listbox"] li[aria-selected="true"] > div {{
        background-color: color-mix(in srgb, {PRIMARY_COLOR} 20%, {WHITE_BACKGROUND_COLOR}) !important;
        color: {PRIMARY_COLOR} !important;
    }}

    /* --- Sliders (Corregidos) --- */
    .stSlider [data-baseweb="slider"] > div:nth-child(1) {{
        background-color: #D3D3D3 !important;
    }}
    .stSlider [data-baseweb="slider"] > div:nth-child(2) > div,
    .stSlider div[data-testid="stTickBar"] > div[style*="background"] {{
        background-color: {PRIMARY_COLOR} !important;
    }}
    .stSlider [data-baseweb="slider"] > div:nth-child(3) > div {{
        background-color: {PRIMARY_COLOR} !important;
        border: 2px solid {PRIMARY_COLOR} !important;
    }}
    .stSlider > div > div[data-testid="stTextLabel"] > div,
    .stSlider > div > div[style*="text-align: center;"] > div,
    .stSlider > div > div[style*="text-align: center;"] {{
        color: {PRIMARY_COLOR} !important;
        background-color: transparent !important;
        font-weight: bold;
    }}
    .stSlider div[data-testid="stTickBar"] > div,
    .stSlider div[data-testid="stTickBar"] span {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
        color: {TEXT_COLOR_LABELS} !important;
        padding: 2px 8px !important;
        border-radius: 4px !important;
        font-weight: normal !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}

    /* --- Radio Buttons --- */
    .stRadio>div {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
        border: 1px solid {BORDER_COLOR_STANDARD} !important;
        border-radius: 6px;
    }}
    .stRadio label span {{
        color: {TEXT_COLOR_LABELS} !important;
    }}
    .stRadio input[type="radio"]:checked + div {{
        background-color: color-mix(in srgb, {PRIMARY_COLOR} 15%, {WHITE_BACKGROUND_COLOR}) !important;
        border-color: {PRIMARY_COLOR} !important;
        color: {PRIMARY_COLOR} !important;
    }}

    /* --- Etiquetas de inputs --- */
    .stSelectbox label, .stSlider label, .stMultiSelect label, .stRadio label, .stTextInput label {{
        color: {TEXT_COLOR_LABELS} !important;
        font-weight: 500;
    }}

    /* --- Chips/Tags --- */
    .stMultiSelect span[data-baseweb="tag"],
    .stMultiSelect span[data-baseweb="tag"] span {{
        background-color: {PRIMARY_COLOR} !important;
        color: {WHITE_BACKGROUND_COLOR} !important;
        border-radius: 0.25rem;
    }}
    .stMultiSelect span[data-baseweb="tag"] svg {{
        fill: {WHITE_BACKGROUND_COLOR} !important;
    }}

    /* --- DataFrames (Tablas) --- */
    .stDataFrame,
    .stDataFrame table,
    .stDataFrame th,
    .stDataFrame td,
    .stDataFrame div[data-testid="stTableOverflow"] {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
        color: {TEXT_COLOR_DARK} !important;
        border-color: #e0e0e0 !important;
    }}
    .stDataFrame thead th {{
        background-color: #f8f9fa !important;
        color: {TEXT_COLOR_DARK} !important;
    }}

    /* --- Gráficos --- */
    .stPlotlyChart, div[data-testid="stImage"] img {{
        background-color: {WHITE_BACKGROUND_COLOR} !important;
        border-radius: 8px;
    }}

    /* --- Footer --- */
    footer {{ visibility: hidden; }}
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

# --- Datos ---
benchmark_data = {
    'Métrica': [
        'Tasa Activación (SAR) - Software Contable Latam',
        'Tasa Adopción Funcionalidad - Software Contable Latam',
        'Tasa Adopción - Facturación Electrónica (Regulatorio Fuerte)',
        'Tasa Adopción - Reportes Fiscales (Regulatorio Fuerte)',
        'Tasa Adopción - Nómina Electrónica (Regulatorio Variable)',
        'Tasa Adopción - Contabilidad Core',
        'Tasa Adopción - Inventarios',
        'Tasa Adopción - Ventas en POS',
        'Tasa Retención (Mes 1) - Software Contable Latam',
        'Tasa Rotación Anual (Churn) - Software Contable Latam',
        'Ratio LTV:CAC - Software Contable Latam'
    ],
    'Valor Benchmark (Promedio/Rango)': [
        '28-35%', '26-32%', '45-60%', '35-45%', '30-50%',
        '25-35%', '20-30%', '20-28%', '50-55%', '4-6%', '3.5:1'
    ],
    'Fuente': ['Estimación Industria Latam'] * 11,
    'Notas': [
        'Rango saludable para software contable en Latam',
        'Promedio general, varía por tipo de funcionalidad y país',
        'Mayor por requisitos regulatorios fuertes (ej. MX, CO)',
        'Alta por necesidad de cumplimiento fiscal (ej. MX, CO)',
        'Depende de obligatoriedad en cada país',
        'Funcionalidad central, adopción más estable',
        'Relevante para ciertos segmentos (retail, etc.)',
        'Adopción puede ser más lenta por hardware/configuración',
        'Retención inicial clave',
        'Churn anual esperado',
        'Relación valor cliente vs costo adquisición'
    ],
    'Región': ['Latam'] * 11,
    'Año': ['2024'] * 11
}

historical_data = {
    'Funcionalidad': [
        'Facturación Electrónica México', 'Facturación Electrónica Colombia', 
        'Reportes Fiscales México', 'Reportes Fiscales Colombia', 'Nómina Electrónica Colombia',
        'Inventarios México', 'Contabilidad General Colombia', 'Ventas en POS México', 'Ventas en POS Costa Rica'
    ],
    'Tipo': [
        'Facturación electrónica', 'Facturación electrónica', 'Reportes fiscales', 'Reportes fiscales', 'Nómina electrónica',
        'Inventarios', 'Contabilidad', 'Ventas en POS', 'Ventas en POS'
    ],
    'Complejidad': ['Media', 'Media', 'Media', 'Media', 'Alta', 'Media', 'Baja', 'Media', 'Media'],
    'País': [
        'México', 'Colombia', 'México', 'Colombia', 'Colombia', 
        'México', 'Colombia', 'México', 'Costa Rica'
    ],
    'Tasa Adopción 1 Mes': ['25%', '22%', '20%', '18%', '15%', '12%', '18%', '10%', '8%'],
    'Tasa Adopción 3 Meses': ['55%', '48%', '40%', '38%', '35%', '28%', '30%', '25%', '20%'],
    'Tasa Adopción 6 Meses': ['78%', '72%', '60%', '58%', '55%', '45%', '50%', '40%', '35%'],
    'Requisito Regulatorio': ['Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'No', 'No', 'No', 'No'],
    'Año Lanzamiento': ['2022', '2022', '2022', '2023', '2023', '2023', '2022', '2023', '2024']
}

# Creación de DataFrames
try:
    benchmarks_df = pd.DataFrame(benchmark_data)
except Exception as e:
    st.error(f"Error al crear DataFrame de benchmarks: {e}")
    benchmarks_df = pd.DataFrame()

try:
    historical_df = pd.DataFrame(historical_data)
except Exception as e:
    st.error(f"Error al crear DataFrame histórico: {e}")
    historical_df = pd.DataFrame()

# --- Funciones Auxiliares ---
def extract_avg(range_str):
    try:
        parts = str(range_str).replace("%", "").replace("$", "").split("-")
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

# Configuración de gráficos
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.facecolor"] = WHITE_BACKGROUND_COLOR
plt.rcParams["figure.facecolor"] = WHITE_BACKGROUND_COLOR
plt.rcParams["text.color"] = TEXT_COLOR_DARK
plt.rcParams["axes.labelcolor"] = TEXT_COLOR_MEDIUM
plt.rcParams["xtick.color"] = TEXT_COLOR_MEDIUM
plt.rcParams["ytick.color"] = TEXT_COLOR_MEDIUM
plt.rcParams["axes.edgecolor"] = BORDER_COLOR_STANDARD

# --- Interfaz Principal ---
st.title("🚀 Herramienta de Estimación de Adopción SaaS")
st.markdown("**Plataforma interactiva para definir objetivos de adopción en software contable B2B para Latam.**")
st.markdown("---")

# --- Componentes de la Herramienta (Pestañas) ---
tab1, tab2, tab3 = st.tabs(["🧭 Explorador de Benchmarks", "🧮 Calculadora Predictiva", "📄 Generador de Informes"])

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
    
    if not benchmarks_df.empty:
        st.dataframe(benchmarks_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No se pudieron cargar los datos de benchmarks.")
    
    st.subheader("Evolución Histórica de Adopción (Ejemplos)")
    st.markdown("Tasas de adopción de funcionalidades lanzadas previamente (datos de ejemplo para ilustración).")
    
    if not historical_df.empty:
        line_chart_df = historical_df.copy()
        for col in ["Tasa Adopción 1 Mes", "Tasa Adopción 3 Meses", "Tasa Adopción 6 Meses"]:
            line_chart_df[col] = line_chart_df[col].str.rstrip("%").astype("float") / 100.0
        
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
            st.warning("No hay datos históricos procesados disponibles para graficar.")
    else:
        st.warning("No se pudieron cargar los datos históricos.")

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

    # --- Lógica de Predicción ---
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
        """, unsafe_allow_html=True)
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
        bar_colors = ["#fd7e14", PRIMARY_COLOR, "#28a745"]
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
    
    st.markdown("---")
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

# --- Pestaña Generador de Informes ---
with tab3:
    st.header("📄 Generador de Informes")
    st.info("Esta funcionalidad estará disponible próximamente. Permitirá generar un resumen de las estimaciones y benchmarks.")

# --- Footer ---
st.markdown("""
<div class="footer-custom">
    Hecho con ❤️ por un IA | Herramienta de Estimación de Adopción v10
</div>
""", unsafe_allow_html=True)
