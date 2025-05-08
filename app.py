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

# --- Estilos CSS Mejorados (v8 - Correcciones modo claro y colores) ---
NEW_PRIMARY_COLOR = "#00535E"
LIGHT_BACKGROUND_COLOR = "#f0f2f5"
TEXT_COLOR_ON_LIGHT_BG = "#1a1a1a"
SECONDARY_TEXT_COLOR = "#4f4f4f"
DEFAULT_TEXT_COLOR_INPUT_LABELS = "#495057"

st.markdown(f"""
<style>
    /* --- Forzar Tema Claro --- */
    html, body {{
        background-color: {LIGHT_BACKGROUND_COLOR} !important;
    }}
    div[data-testid="stAppViewContainer"],
    div[data-testid="stReportViewContainer"],
    div.main {{
        background-color: {LIGHT_BACKGROUND_COLOR} !important;
    }}
    section[data-testid="stHeader"] {{
        background-color: #FFFFFF !important;
        border-bottom: 1px solid #e0e0e0;
    }}
    section[data-testid="stHeader"] h1,
    section[data-testid="stHeader"] p,
    section[data-testid="stHeader"] .stToolbar {{
        color: {TEXT_COLOR_ON_LIGHT_BG} !important;
    }}
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {{
        color: {SECONDARY_TEXT_COLOR} !important; /* Color de texto en la barra lateral si es necesario */
    }}

    /* --- General --- */
    body {{
        font-family: 'Inter', sans-serif;
        color: {TEXT_COLOR_ON_LIGHT_BG};
    }}
    .main {{
        padding: 2rem;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {TEXT_COLOR_ON_LIGHT_BG};
        font-weight: 600;
    }}
    h1 {{
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }}
    h2 {{
        font-size: 1.75rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.5rem;
    }}
    h3 {{
        font-size: 1.3rem;
        margin-bottom: 0.8rem;
        color: #333;
    }}
    p, .stMarkdown p {{
        color: {SECONDARY_TEXT_COLOR};
        line-height: 1.6;
    }}
    .stCaption {{
        color: #666;
        font-style: italic;
    }}

    /* --- Pestañas --- */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 12px;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: auto;
        white-space: normal;
        border-radius: 8px 8px 0 0;
        padding: 12px 20px;
        background-color: transparent;
        font-weight: 500;
        color: #666;
        border: none;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: #e9ecef;
        color: #333;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: transparent !important;
        color: {NEW_PRIMARY_COLOR} !important; /* Color primario nuevo */
        border-bottom: 3px solid {NEW_PRIMARY_COLOR} !important;
        font-weight: 600;
    }}

    /* --- Botones --- */
    .stButton>button {{
        background-color: {NEW_PRIMARY_COLOR};
        color: white !important;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        border: none;
        transition: background-color 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}
    .stButton>button:hover {{
        background-color: color-mix(in srgb, {NEW_PRIMARY_COLOR} 80%, black);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }}
    .stDownloadButton>button {{
        background-color: {NEW_PRIMARY_COLOR};
        color: white !important;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        border: none;
        transition: background-color 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}
    .stDownloadButton>button:hover {{
        background-color: color-mix(in srgb, {NEW_PRIMARY_COLOR} 80%, black);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }}

    /* --- Tarjetas y Cajas de Información --- */
    .metric-card, .info-box, .warning-box, .success-box, .pessimistic-box {{
        background-color: white;
        border-radius: 8px;
        padding: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        border-left: 5px solid;
    }}
    .metric-card {{
        border-left-color: {NEW_PRIMARY_COLOR};
    }}
    .info-box {{
        border-left-color: #17a2b8;
        background-color: #e8f7f9;
    }}
    .warning-box {{
        border-left-color: #ffc107;
        background-color: #fff9e6;
    }}
    .pessimistic-box {{
        border-left-color: #fd7e14;
        background-color: #fff3e0;
    }}
    .success-box {{
        border-left-color: #28a745;
        background-color: #eaf6ec;
    }}
    .metric-card h3, .info-box h4, .warning-box h4, .success-box h4, .pessimistic-box h4 {{
        margin-top: 0;
        font-weight: 600;
    }}
    .metric-card h2 {{
        color: {NEW_PRIMARY_COLOR};
        margin-bottom: 5px;
        font-size: 2.2rem;
        border-bottom: none;
    }}
    .metric-card p {{
        color: #5f6368;
        margin: 0;
        font-size: 0.95rem;
    }}

    /* --- Entradas (Inputs) --- */
    .stTextInput>div>div>input,
    .stSelectbox>div>div,
    .stMultiSelect>div>div[data-baseweb="select"] /* Contenedor principal del multiselect */
    {{
        border-radius: 6px;
        border: 1px solid #ced4da;
        background-color: white !important; /* Fondo blanco para inputs */
        color: {TEXT_COLOR_ON_LIGHT_BG} !important; /* Texto oscuro para inputs */
    }}
    .stTextInput>div>div>input {{
        padding: 0.5rem;
    }}

    /* Estilos para Sliders (st.slider y st.select_slider) */
    .stSlider [data-baseweb="slider"] > div:nth-child(1) /* Track inactivo */
    {{
        background-color: #D3D3D3 !important; /* Gris claro para track inactivo */
    }}
    .stSlider [data-baseweb="slider"] > div:nth-child(2) > div, /* Barra activa de st.slider */
    .stSlider div[data-testid="stTickBar"] > div[style*="background: rgb(111, 66, 193)"] /* Barra activa de st.select_slider (color morado original) */
    {{
        background-color: {NEW_PRIMARY_COLOR} !important;
    }}
    .stSlider [data-baseweb="slider"] > div:nth-child(3) > div /* Círculo/Thumb */
    {{
        background-color: {NEW_PRIMARY_COLOR} !important;
        border: 2px solid {NEW_PRIMARY_COLOR} !important; /* Borde del mismo color */
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
    /* Quitarles el fondo morado y asegurar texto normal */
    .stSlider div[data-testid="stTickBar"] > div,
    .stSlider div[data-testid="stTickBar"] span,
    .stSlider div[role="listbox"] div[role="option"] > div /* Opciones de st.select_slider */
    {{
        background-color: transparent !important;
        color: {DEFAULT_TEXT_COLOR_INPUT_LABELS} !important;
        padding: 2px 4px !important; /* Ajustar padding si es necesario */
        border-radius: 0px !important;
        font-weight: normal !important;
    }}

    /* Radio Buttons */
    .stRadio>div {{
        background-color: white;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #ced4da;
    }}
    .stRadio label span {{
        color: {DEFAULT_TEXT_COLOR_INPUT_LABELS} !important;
    }}
    .stRadio input[type="radio"]:checked + div {{
        background-color: color-mix(in srgb, {NEW_PRIMARY_COLOR} 15%, white) !important; /* Fondo primario muy claro */
        border-color: {NEW_PRIMARY_COLOR} !important;
        color: color-mix(in srgb, {NEW_PRIMARY_COLOR} 80%, black) !important; /* Texto primario oscuro para contraste */
    }}

    /* Etiquetas de todos los inputs */
    .stSelectbox label, .stSlider label, .stMultiSelect label, .stRadio label, .stTextInput label {{
        color: {DEFAULT_TEXT_COLOR_INPUT_LABELS};
        font-weight: 500;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }}

    /* Chips/Tags de st.multiselect */
    .stMultiSelect span[data-baseweb="tag"],
    .stMultiSelect span[data-baseweb="tag"] span /* Para el texto dentro del tag */
    {{
        background-color: {NEW_PRIMARY_COLOR} !important;
        color: white !important;
        border-radius: 0.25rem;
    }}
    .stMultiSelect span[data-baseweb="tag"] svg /* Icono 'x' de cierre */
    {{
        fill: white !important;
    }}

    /* --- DataFrames y Gráficos --- */
    .stDataFrame {{
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }}
    .stPlotlyChart {{
        border-radius: 8px;
        padding: 10px;
        background-color: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
    }}

    /* --- Contenedores y Columnas --- */
    .stVerticalBlock, .stHorizontalBlock {{
        gap: 1.5rem;
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
# --- Datos de Benchmarks (Ajustados para Latam General, ya que específicos son difíciles) ---
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
        '28-35%',
        '26-32%',
        '45-60%', # Alto por regulación
        '35-45%', # Alto por necesidad de cumplimiento fiscal
        '30-50%', # Variable según país
        '25-35%', # Core pero no siempre urgente
        '20-30%', # Depende del tipo de negocio
        '20-28%', # Depende de implementación
        '50-55%',
        '4-6%',
        '3.5:1'
    ],
    'Fuente': [
        'Estimación Industria Latam',
        'Estimación Industria Latam',
        'Estimación Industria Latam (Regulatorio)',
        'Estimación Industria Latam (Regulatorio)',
        'Estimación Industria Latam (Regulatorio)',
        'Estimación Industria Latam',
        'Estimación Industria Latam',
        'Estimación Industria Latam',
        'Estimación Industria Latam',
        'Estimación Industria Latam',
        'Estimación Industria Latam'
    ],
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
benchmarks_df = pd.DataFrame(benchmark_data)

# Datos históricos de ejemplo (Adaptados a nuevas funcionalidades y países)
historical_data = {
    'Funcionalidad': [
        'Facturación Electrónica México',
        'Facturación Electrónica Colombia',
        'Reportes Fiscales México',
        'Reportes Fiscales Colombia',
        'Nómina Electrónica Colombia',
        'Inventarios México',
        'Contabilidad General Colombia',
        'Ventas en POS México',
        'Ventas en POS Costa Rica'
    ],
    'Tipo': [
        'Facturación electrónica',
        'Facturación electrónica',
        'Reportes fiscales',
        'Reportes fiscales',
        'Nómina electrónica',
        'Inventarios',
        'Contabilidad',
        'Ventas en POS',
        'Ventas en POS'
    ],
    'Complejidad': [
        'Media', 'Media', 'Media', 'Media', 'Alta', 'Media', 'Baja', 'Media', 'Media'
    ],
    'País': [
        'México', 'Colombia', 'México', 'Colombia', 'Colombia', 'México', 'Colombia', 'México', 'Costa Rica'
    ],
    'Tasa Adopción 1 Mes': [
        '25%', '22%', '20%', '18%', '15%', '12%', '18%', '10%', '8%'
    ],
    'Tasa Adopción 3 Meses': [
        '55%', '48%', '40%', '38%', '35%', '28%', '30%', '25%', '20%'
    ],
    'Tasa Adopción 6 Meses': [
        '78%', '72%', '60%', '58%', '55%', '45%', '50%', '40%', '35%'
    ],
    'Requisito Regulatorio': [
        'Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'No', 'No', 'No', 'No'
    ],
    'Año Lanzamiento': [
        '2022', '2022', '2022', '2023', '2023', '2023', '2022', '2023', '2024'
    ]
}
historical_df = pd.DataFrame(historical_data)

# --- Título y Descripción ---
st.title("🚀 Herramienta de Estimación de Adopción SaaS")
st.markdown("**Plataforma interactiva para definir objetivos de adopción en software contable B2B para Latam.**")
st.markdown("--- ")

# --- Componentes de la Herramienta (Pestañas) ---
tab2, tab1, tab3 = st.tabs(["🧮 Calculadora Predictiva", "🧭 Explorador de Benchmarks", "📄 Generador de Informes"])

# --- Funciones Auxiliares ---
def extract_avg(range_str):
    try:
        parts = str(range_str).replace('%', '').replace('$', '').split('-')
        if len(parts) == 2:
            return (float(parts[0]) + float(parts[1])) / 2
        elif len(parts) == 1 and parts[0] != '':
            if ':' in parts[0]:
                return float(parts[0].split(':')[0])
            return float(parts[0])
        else:
            return np.nan
    except:
        return np.nan

sns.set_theme(style="whitegrid", palette="muted") # Esto podría influir en los colores de Matplotlib
# Para asegurar que Matplotlib use el tema claro para los gráficos:
plt.style.use('seaborn-v0_8-whitegrid') # Usar un estilo claro explícito de Matplotlib
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.facecolor'] = 'white' # Fondo de los ejes del gráfico
plt.rcParams['figure.facecolor'] = 'white' # Fondo de la figura del gráfico
plt.rcParams['text.color'] = TEXT_COLOR_ON_LIGHT_BG # Color de texto en gráficos
plt.rcParams['axes.labelcolor'] = SECONDARY_TEXT_COLOR # Color de etiquetas de ejes
plt.rcParams['xtick.color'] = SECONDARY_TEXT_COLOR # Color de ticks en X
plt.rcParams['ytick.color'] = SECONDARY_TEXT_COLOR # Color de ticks en Y

# --- Pestaña Calculadora Predictiva (Layout Revertido a 1 Columna) ---
with tab2:
    st.header("🧮 Calculadora Predictiva de Tasa de Adopción")
    st.markdown("""
    <div class="info-box">
    <h4 style="margin-top:0">💡 ¿Cómo funciona?</h4>
    Introduce las características de tu nueva funcionalidad y observa la estimación del rango de adopción
    esperado a los 3 meses.
    </div>
    """, unsafe_allow_html=True)

    # --- Inputs --- 
    st.subheader("1. Define tu Funcionalidad")
    with st.container(): # Contenedor para inputs
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            nombre_funcionalidad = st.text_input('Nombre de la Funcionalidad:', placeholder="Ej: Facturación Electrónica 4.0", help="Nombre descriptivo para identificarla.")
            
            tipo_funcionalidad = st.selectbox(
                'Tipo de Funcionalidad:',
                ['Facturación electrónica', 'Reportes fiscales', 'Inventarios', 'Contabilidad', 'Ventas en POS', 'Nómina electrónica'],
                index=0, help="Categoría principal de la funcionalidad.")
            
            complejidad = st.select_slider(
                'Nivel de Complejidad Percibida:',
                options=['Muy Baja', 'Baja', 'Media', 'Alta', 'Muy Alta'],
                value='Media', help="¿Qué tan difícil es para el usuario entender y usar la funcionalidad?")
            
            segmento = st.multiselect(
                'Segmento(s) de Usuario Objetivo:',
                ['Pequeña empresa', 'Mediana empresa', 'Contador', 'Auxiliar contable', 'Dueño de negocio', 'Usuario final POS'],
                default=['Pequeña empresa'], help="¿A quién va dirigida principalmente?")
            
            paises = st.multiselect(
                'País(es) Objetivo(s):',
                ['Colombia', 'México', 'Costa Rica', 'República Dominicana'],
                default=['Colombia'], help="Mercados principales de lanzamiento.")

        with col_in2:
            valor_percibido = st.select_slider(
                'Valor Percibido / Urgencia:',
                options=['Muy Bajo', 'Bajo', 'Medio', 'Alto', 'Muy Alto'],
                value='Medio', help="¿Cuánto valor aporta al usuario y qué tan urgente es su necesidad?")
            
            regulatorio = st.radio("¿Es un Requisito Regulatorio?", ('No', 'Sí'), horizontal=True, help="¿Es obligatorio por ley o normativa en el país/países objetivo?")
            
            esfuerzo_mkt = st.select_slider(
                'Esfuerzo de Marketing/Comunicación Planeado:',
                options=['Muy Bajo', 'Bajo', 'Medio', 'Alto', 'Muy Alto'],
                value='Medio', help="Nivel de inversión en promoción y comunicación.")
            
            esfuerzo_soporte = st.select_slider(
                'Esfuerzo de Soporte/Capacitación Planeado:',
                options=['Muy Bajo', 'Bajo', 'Medio', 'Alto', 'Muy Alto'],
                value='Medio', help="Nivel de inversión en documentación, tutoriales y soporte.")
            
            integracion_compleja = st.radio("¿Requiere Integración Compleja por parte del Usuario?", ('No', 'Sí'), horizontal=True, help="¿Necesita el usuario configurar conexiones complejas con otros sistemas?")

    # --- Lógica de Predicción (Adaptada a nuevos países y funcionalidades) ---
    # Base score por funcionalidad
    if tipo_funcionalidad == 'Facturación electrónica': base_score = 45
    elif tipo_funcionalidad == 'Reportes fiscales': base_score = 40
    elif tipo_funcionalidad == 'Nómina electrónica': base_score = 38 # Similar a reportes, pero puede variar más
    elif tipo_funcionalidad == 'Contabilidad': base_score = 30 # Core, pero menos urgente que regulatorio
    elif tipo_funcionalidad == 'Inventarios': base_score = 28 # Depende del segmento
    elif tipo_funcionalidad == 'Ventas en POS': base_score = 25 # Puede requerir hardware/setup
    else: base_score = 30

    # Ajustes
    complejidad_map = {'Muy Baja': 15, 'Baja': 10, 'Media': 0, 'Alta': -10, 'Muy Alta': -20}
    base_score += complejidad_map[complejidad]
    valor_map = {'Muy Bajo': -15, 'Bajo': -10, 'Medio': 0, 'Alto': 10, 'Muy Alto': 20}
    base_score += valor_map[valor_percibido]
    if regulatorio == 'Sí': base_score += 25
    esfuerzo_mkt_map = {'Muy Bajo': -10, 'Bajo': -5, 'Medio': 0, 'Alto': 8, 'Muy Alto': 15}
    base_score += esfuerzo_mkt_map[esfuerzo_mkt]
    esfuerzo_soporte_map = {'Muy Bajo': -10, 'Bajo': -5, 'Medio': 0, 'Alto': 8, 'Muy Alto': 15}
    base_score += esfuerzo_soporte_map[esfuerzo_soporte]
    if integracion_compleja == 'Sí': base_score -= 15
    
    segment_impact = 0
    if 'Pequeña empresa' in segmento: segment_impact += 2
    if 'Mediana empresa' in segmento: segment_impact -= 3
    if 'Contador' in segmento: segment_impact += 8
    if 'Auxiliar contable' in segmento: segment_impact += 5
    if 'Dueño de negocio' in segmento: segment_impact -= 5
    if 'Usuario final POS' in segmento: segment_impact -= 2
    base_score += segment_impact
    
    country_impact = 0
    country_factors = {'México': 3, 'Colombia': 3, 'Costa Rica': -1, 'República Dominicana': -2}
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

    # --- Resultados --- 
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
        scenarios = ['Pesimista', 'Base', 'Optimista']
        values = [pesimista_medio, base_medio, optimista_medio]
        # Colores: Naranja para pesimista, NUEVO_PRIMARY_COLOR para base, Verde para optimista
        bar_colors = ['#fd7e14', NEW_PRIMARY_COLOR, '#28a745'] 
        
        bars = ax.bar(scenarios, values, color=bar_colors, width=0.5)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1.5,
                    f'{int(height)}%', ha='center', va='bottom', fontsize=11, fontweight='medium', color=SECONDARY_TEXT_COLOR)
        
        ax.set_ylim(0, 105)
        ax.set_ylabel('Tasa de Adopción (%)', fontsize=10, color=SECONDARY_TEXT_COLOR)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#DDDDDD')
        ax.spines['bottom'].set_color('#DDDDDD')
        ax.tick_params(axis='x', labelsize=10, colors=SECONDARY_TEXT_COLOR)
        ax.tick_params(axis='y', labelsize=10, colors=SECONDARY_TEXT_COLOR)
        # sns.despine(left=True, bottom=True) # Despine puede quitar los ejes que acabamos de colorear
        plt.tight_layout()
        st.pyplot(fig)
    
    st.markdown("--- ")
    st.subheader("3. Análisis y Recomendaciones")
    with st.container():
        st.markdown("#### Factores Clave de Influencia")
        factores = []
        if regulatorio == 'Sí': factores.append(("✅ Requisito Regulatorio", "Muy Positivo", "+25%"))
        if complejidad in ['Muy Baja', 'Baja']: factores.append(("👍 Baja Complejidad", "Positivo", "+10-15%"))
        elif complejidad in ['Alta', 'Muy Alta']: factores.append(("👎 Alta Complejidad", "Negativo", "-10-20%"))
        if valor_percibido in ['Alto', 'Muy Alto']: factores.append(("⭐ Alto Valor Percibido", "Positivo", "+10-20%"))
        elif valor_percibido in ['Bajo', 'Muy Bajo']: factores.append(("📉 Bajo Valor Percibido", "Negativo", "-10-15%"))
        if esfuerzo_mkt in ['Alto', 'Muy Alto']: factores.append(("📢 Alto Esfuerzo Marketing", "Positivo", "+8-15%"))
        if esfuerzo_soporte in ['Alto', 'Muy Alto']: factores.append(("🎓 Alto Esfuerzo Soporte", "Positivo", "+8-15%"))
        if integracion_compleja == 'Sí': factores.append(("🔗 Integración Compleja", "Negativo", "-15%"))
        if 'Contador' in segmento: factores.append(("👨‍💼 Segmento Contador", "Positivo", "+8%"))
        if 'Dueño de negocio' in segmento: factores.append(("🏢 Segmento Dueño Negocio", "Negativo", "-5%"))
        if abs(country_impact) > 1: 
             factores.append(("🌍 Impacto País (Promedio)", "Positivo" if country_impact > 0 else "Negativo", f"{country_impact:+.1f}%"))
        
        if factores:
            factores_df = pd.DataFrame(factores, columns=["Factor", "Impacto", "Efecto Aprox."])
            st.dataframe(factores_df, use_container_width=True, hide_index=True)
        else:
            st.info("No se identificaron factores con impacto significativo.")

        st.markdown("#### Recomendaciones Accionables")
        recomendaciones = []
        if complejidad in ['Alta', 'Muy Alta']: recomendaciones.append("Simplificar onboarding y crear tutoriales claros.")
        if valor_percibido in ['Bajo', 'Muy Bajo', 'Medio']: recomendaciones.append("Comunicar beneficios y ROI de forma efectiva.")
        if esfuerzo_mkt in ['Bajo', 'Muy Bajo', 'Medio']: recomendaciones.append("Intensificar comunicación y marketing.")
        if esfuerzo_soporte in ['Bajo', 'Muy Bajo', 'Medio']: recomendaciones.append("Mejorar recursos de capacitación y soporte.")
        if integracion_compleja == 'Sí': recomendaciones.append("Ofrecer asistencia para la integración o simplificarla.")
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
    
    # Preparar datos para gráfico de líneas múltiples
    line_chart_df = historical_df.copy()
    for col in ['Tasa Adopción 1 Mes', 'Tasa Adopción 3 Meses', 'Tasa Adopción 6 Meses']:
        line_chart_df[col] = line_chart_df[col].str.rstrip('%').astype('float') / 100.0
    
    line_chart_df_melted = line_chart_df.melt(
        id_vars=['Funcionalidad', 'País'], 
        value_vars=['Tasa Adopción 1 Mes', 'Tasa Adopción 3 Meses', 'Tasa Adopción 6 Meses'],
        var_name='Meses', 
        value_name='Tasa de Adopción'
    )
    line_chart_df_melted['Meses'] = line_chart_df_melted['Meses'].map({
        'Tasa Adopción 1 Mes': 1,
        'Tasa Adopción 3 Meses': 3,
        'Tasa Adopción 6 Meses': 6
    })
    line_chart_df_melted['Etiqueta'] = line_chart_df_melted['Funcionalidad'] + " (" + line_chart_df_melted['País'] + ")"

    if not line_chart_df_melted.empty:
        fig_line, ax_line = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=line_chart_df_melted, x='Meses', y='Tasa de Adopción', hue='Etiqueta', marker='o', ax=ax_line, palette="viridis")
        ax_line.set_title('Curva de Adopción Histórica por Funcionalidad y País', fontsize=15, color=TEXT_COLOR_ON_LIGHT_BG)
        ax_line.set_xlabel('Meses desde Lanzamiento', fontsize=12, color=SECONDARY_TEXT_COLOR)
        ax_line.set_ylabel('Tasa de Adopción Acumulada', fontsize=12, color=SECONDARY_TEXT_COLOR)
        ax_line.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y))) # Formato porcentaje
        ax_line.legend(title='Funcionalidad (País)', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax_line.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout(rect=[0, 0, 0.85, 1]) # Ajustar para leyenda fuera
        st.pyplot(fig_line)
    else:
        st.warning("No hay datos históricos disponibles para graficar.")

# --- Pestaña Generador de Informes (Placeholder) ---
with tab3:
    st.header("📄 Generador de Informes")
    st.info("Esta funcionalidad estará disponible próximamente. Permitirá generar un resumen de las estimaciones y benchmarks.")
    # Aquí iría la lógica para tomar los inputs de la calculadora y generar un informe.

# --- Footer Personalizado ---
st.markdown("""
<div class="footer-custom">
    Hecho con ❤️ por un IA | Herramienta de Estimación de Adopción v8
</div>
""", unsafe_allow_html=True)

