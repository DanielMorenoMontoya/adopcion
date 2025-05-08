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

# --- Estilos CSS Mejorados (v7 - Revertir color sliders/radios a morado) ---
st.markdown("""
<style>
    /* --- General --- */
    body {
        font-family: 'Inter', sans-serif;
    }
    .main {
        background-color: #f0f2f5;
        padding: 2rem;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a;
        font-weight: 600;
    }
    h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    h2 {
        font-size: 1.75rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.5rem;
    }
    h3 {
        font-size: 1.3rem;
        margin-bottom: 0.8rem;
        color: #333;
    }
    p, .stMarkdown p {
        color: #4f4f4f;
        line-height: 1.6;
    }
    .stCaption {
        color: #666;
        font-style: italic;
    }

    /* --- Pestañas --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0;
    }
    .stTabs [data-baseweb="tab"] {
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
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e9ecef;
        color: #333;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #6f42c1 !important; /* Morado primario */
        border-bottom: 3px solid #6f42c1 !important;
        font-weight: 600;
    }

    /* --- Botones --- */
    .stButton>button {
        background-color: #6f42c1; /* Morado primario */
        color: white !important; /* Asegurar texto blanco */
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        border: none;
        transition: background-color 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:hover {
        background-color: #5a32a3; /* Morado más oscuro */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    /* Unificar botón descarga */
    .stDownloadButton>button {
        background-color: #6f42c1; /* Morado primario */
        color: white !important; /* Asegurar texto blanco */
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        border: none;
        transition: background-color 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stDownloadButton>button:hover {
        background-color: #5a32a3; /* Morado más oscuro */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }

    /* --- Tarjetas y Cajas de Información --- */
    .metric-card, .info-box, .warning-box, .success-box, .pessimistic-box {
        background-color: white;
        border-radius: 8px;
        padding: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        border-left: 5px solid;
    }
    .metric-card {
        border-left-color: #6f42c1; /* Morado */
    }
    .info-box {
        border-left-color: #17a2b8; /* Cyan */
        background-color: #e8f7f9;
    }
    .warning-box {
        border-left-color: #ffc107; /* Amarillo */
        background-color: #fff9e6;
    }
    /* Cambiado a naranja */
    .pessimistic-box {
        border-left-color: #fd7e14; /* Naranja */
        background-color: #fff3e0; /* Fondo naranja claro */
    }
    .success-box {
        border-left-color: #28a745; /* Verde */
        background-color: #eaf6ec;
    }
    .metric-card h3, .info-box h4, .warning-box h4, .success-box h4, .pessimistic-box h4 {
        margin-top: 0;
        font-weight: 600;
    }
    .metric-card h2 {
        color: #6f42c1; /* Morado */
        margin-bottom: 5px;
        font-size: 2.2rem;
        border-bottom: none;
    }
    .metric-card p {
        color: #5f6368;
        margin: 0;
        font-size: 0.95rem;
    }

    /* --- Entradas (Inputs) --- */
    .stTextInput>div>div>input {
        border-radius: 6px;
        border: 1px solid #ced4da;
        background-color: white;
        padding: 0.5rem;
    }
    .stSelectbox>div>div, .stMultiSelect>div>div {
        border-radius: 6px;
        border: 1px solid #ced4da;
        background-color: white;
    }
    /* Revertir color sliders a morado */
    .stSlider [data-baseweb="slider"] > div:nth-child(2) > div {
        background-color: #6f42c1 !important; /* Morado primario */
    }
    .stSlider [data-baseweb="slider"] > div:nth-child(3) > div {
        background-color: #6f42c1 !important; /* Morado primario - círculo */
    }
    /* Asegurar que el texto del valor del slider (ej. 'Media') no se coloree */
    .stSlider > div > div[style*="text-align: center;"],
    .stSlider > div > div[style*="text-align: center;"] > div { /* Cubre el div contenedor y si el texto está en un div anidado */
        color: #495057 !important; /* Color de texto estándar, igual que las etiquetas */
        background-color: transparent !important; /* Sin fondo de color */
    }
    .stRadio>div {
        background-color: white;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #ced4da;
    }
    /* Revertir color radio buttons a morado */
    .stRadio input[type="radio"]:checked + div {
        background-color: #f3eefc !important; /* Fondo morado muy claro */
        border-color: #6f42c1 !important;
        color: #5a32a3; /* Texto morado oscuro para contraste */
    }
    .stSelectbox label, .stSlider label, .stMultiSelect label, .stRadio label, .stTextInput label {
        color: #495057;
        font-weight: 500;
        font-size: 0.9rem;
        margin-bottom: 0.3rem;
    }

    /* --- DataFrames y Gráficos --- */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    .stPlotlyChart {
        border-radius: 8px;
        padding: 10px;
        background-color: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
    }

    /* --- Contenedores y Columnas --- */
    .stVerticalBlock, .stHorizontalBlock {
        gap: 1.5rem;
    }

    /* --- Footer --- */
    footer {
        visibility: hidden;
    }
    .footer-custom {
        text-align: center;
        padding: 1.5rem 0;
        margin-top: 3rem;
        font-size: 0.9rem;
        color: #6c757d;
        border-top: 1px solid #e0e0e0;
    }

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

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.family'] = 'sans-serif'

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
            
            # Funcionalidades actualizadas
            tipo_funcionalidad = st.selectbox(
                'Tipo de Funcionalidad:',
                ['Facturación electrónica', 'Reportes fiscales', 'Inventarios', 'Contabilidad', 'Ventas en POS', 'Nómina electrónica'],
                index=0, help="Categoría principal de la funcionalidad.")
            
            complejidad = st.select_slider(
                'Nivel de Complejidad Percibida:',
                options=['Muy Baja', 'Baja', 'Media', 'Alta', 'Muy Alta'],
                value='Media', help="¿Qué tan difícil es para el usuario entender y usar la funcionalidad?")
            
            # Selección única por defecto
            segmento = st.multiselect(
                'Segmento(s) de Usuario Objetivo:',
                ['Pequeña empresa', 'Mediana empresa', 'Contador', 'Auxiliar contable', 'Dueño de negocio', 'Usuario final POS'],
                default=['Pequeña empresa'], help="¿A quién va dirigida principalmente?")
            
            # Países actualizados
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
    
    # Ajuste por país (Estimado)
    country_impact = 0
    # Factores estimados: MX/CO (+), CR/DO (neutral o -) - Basado en madurez/regulación
    country_factors = {'México': 3, 'Colombia': 3, 'Costa Rica': -1, 'República Dominicana': -2}
    for pais in paises:
        country_impact += country_factors.get(pais, 0) # Sumar factor si el país está en el dict
    if len(paises) > 0:
        country_impact = country_impact / len(paises) # Promediar impacto
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
    
    # Tarjetas métricas
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        # Usar help para el tooltip
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
        # Usar clase pessimistic-box con color naranja
        st.markdown(f"""
        <div class="pessimistic-box">
            <h4>📉 Escenario Pesimista</h4>
            <h3 style="color:#fd7e14; margin:0; font-size: 1.8rem;">{rango_objetivo_pesimista}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráfico de comparación
    with st.container():
        st.markdown("#### Comparación Visual de Escenarios")
        fig, ax = plt.subplots(figsize=(8, 4))
        scenarios = ['Pesimista', 'Base', 'Optimista']
        values = [pesimista_medio, base_medio, optimista_medio]
        # Colores: Naranja para pesimista, Morado primario para base, Verde para optimista
        colors = ['#fd7e14', '#6f42c1', '#28a745'] 
        
        bars = ax.bar(scenarios, values, color=colors, width=0.5)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1.5,
                    f'{int(height)}%', ha='center', va='bottom', fontsize=11, fontweight='medium')
        
        ax.set_ylim(0, 105)
        ax.set_ylabel('Tasa de Adopción (%)', fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        sns.despine(left=True, bottom=True)
        plt.tight_layout()
        st.pyplot(fig)
    
    # Factores de influencia y Recomendaciones
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
        # Añadir impacto país si es significativo
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
        if integracion_compleja == 'Sí': recomendaciones.append("Ofrecer asistencia técnica para la integración.")
        if 'Dueño de negocio' in segmento: recomendaciones.append("Crear materiales específicos para dueños (beneficios negocio).")
        if 'Usuario final POS' in segmento: recomendaciones.append("Desarrollar capacitación específica para usuarios POS.")
        if country_impact < 0: recomendaciones.append("Considerar estrategias de localización o soporte adicional para países con menor adopción estimada.")
        recomendaciones.append("Implementar recordatorios y notificaciones in-app.")
        recomendaciones.append("Considerar incentivos para adopción temprana.")
        
        if recomendaciones:
            st.markdown("<ul>" + "".join([f"<li>{rec}</li>" for rec in recomendaciones]) + "</ul>", unsafe_allow_html=True)
        else:
            st.info("No hay recomendaciones específicas basadas en los parámetros seleccionados.")

# --- Pestaña Explorador de Benchmarks (Adaptada y Gráficos Eliminados) ---
with tab1:
    st.header("🧭 Explorador de Benchmarks y Datos Históricos")
    st.markdown("""
    <div class="info-box">
    <h4 style="margin-top:0">📊 ¿Qué encontrarás aquí?</h4>
    Consulta benchmarks estimados para la industria del software contable en Latam, explora datos históricos de adopción 
    y compara el rendimiento pasado con los estándares de la industria.
    </div>
    """, unsafe_allow_html=True)

    benchmark_tab1, benchmark_tab2, benchmark_tab3 = st.tabs(["📈 Benchmarks Industria", "⏳ Datos Históricos", "🔍 Análisis Comparativo"])
    
    with benchmark_tab1:
        st.subheader("Benchmarks Estimados (Software Contable Latam)")
        with st.expander("Filtrar Benchmarks", expanded=False):
             # Filtros simplificados ya que los datos son generales para Latam
            filtro_metrica = st.multiselect("Tipo Métrica:", options=['Activación', 'Adopción', 'Retención', 'Rotación', 'CAC', 'LTV', 'Todos'], default=['Todos'])
        
        filtered_df = benchmarks_df.copy()
        if 'Todos' not in filtro_metrica:
            mask = pd.Series(False, index=filtered_df.index)
            for metrica in filtro_metrica:
                mask = mask | filtered_df['Métrica'].str.contains(metrica, case=False)
            filtered_df = filtered_df[mask]
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        # Gráfico "Visualización de Benchmarks Clave" eliminado

    with benchmark_tab2:
        st.subheader("Datos Históricos de Adopción (Ejemplos)")
        with st.expander("Filtrar Datos Históricos", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                # Usar nueva lista de funcionalidades
                filtro_tipo = st.multiselect("Tipo Funcionalidad:", options=historical_df['Tipo'].unique(), default=list(historical_df['Tipo'].unique()))
            with col2:
                # Usar nueva lista de países
                filtro_pais_hist = st.multiselect("País:", options=historical_df['País'].unique(), default=list(historical_df['País'].unique()))
            with col3:
                filtro_complejidad = st.multiselect("Complejidad:", options=historical_df['Complejidad'].unique(), default=list(historical_df['Complejidad'].unique()))
        
        hist_filtered_df = historical_df[historical_df['Tipo'].isin(filtro_tipo) & historical_df['País'].isin(filtro_pais_hist) & historical_df['Complejidad'].isin(filtro_complejidad)]
        st.dataframe(hist_filtered_df, use_container_width=True, hide_index=True)
        
        if not hist_filtered_df.empty:
            st.markdown("#### Visualización de Datos Históricos")
            for col in ['Tasa Adopción 1 Mes', 'Tasa Adopción 3 Meses', 'Tasa Adopción 6 Meses']:
                hist_filtered_df[col] = hist_filtered_df[col].str.replace('%', '').astype(float)
            
            # Gráfico "Evolución de Adopción por Tiempo" eliminado
            
            col_vis1, col_vis2 = st.columns(2)
            with col_vis1:
                st.markdown("##### Comparación por Tipo")
                fig, ax = plt.subplots(figsize=(6, 4))
                tipo_avg = hist_filtered_df.groupby('Tipo')[['Tasa Adopción 3 Meses']].mean().reset_index()
                sns.barplot(x='Tipo', y='Tasa Adopción 3 Meses', data=tipo_avg, ax=ax, palette='viridis')
                ax.set_ylabel('Adopción Promedio 3 Meses (%)', fontsize=9)
                ax.set_xlabel('Tipo de Funcionalidad', fontsize=9)
                ax.set_ylim(0, 100)
                plt.xticks(rotation=45, ha='right', fontsize=9)
                ax.tick_params(axis='y', labelsize=9)
                for i, v in enumerate(tipo_avg['Tasa Adopción 3 Meses']):
                    ax.text(i, v + 2, f'{v:.1f}%', ha='center', fontsize=9)
                sns.despine()
                plt.tight_layout()
                st.pyplot(fig)
            
            with col_vis2:
                st.markdown("##### Comparación por País")
                fig, ax = plt.subplots(figsize=(6, 4))
                pais_avg = hist_filtered_df.groupby('País')[['Tasa Adopción 3 Meses']].mean().reset_index()
                sns.barplot(x='País', y='Tasa Adopción 3 Meses', data=pais_avg, ax=ax, palette='magma')
                ax.set_ylabel('Adopción Promedio 3 Meses (%)', fontsize=9)
                ax.set_xlabel('País', fontsize=9)
                ax.set_ylim(0, 100)
                plt.xticks(rotation=30, ha='right', fontsize=9)
                ax.tick_params(axis='y', labelsize=9)
                for i, v in enumerate(pais_avg['Tasa Adopción 3 Meses']):
                    ax.text(i, v + 2, f'{v:.1f}%', ha='center', fontsize=9)
                sns.despine()
                plt.tight_layout()
                st.pyplot(fig)
        else:
            st.info("No hay datos históricos que cumplan con los filtros seleccionados.")
        
        st.markdown("--- ")
        st.markdown("#### Cargar Datos Propios")
        st.info("Próximamente: Funcionalidad para cargar y analizar tus propios datos históricos de adopción.")
        # Botón de descarga ahora usa st.button y se aplica estilo CSS
        st.download_button(
            label="📄 Descargar Plantilla CSV",
            data="Funcionalidad,Tipo,Complejidad,País,Tasa Adopción 1 Mes,Tasa Adopción 3 Meses,Tasa Adopción 6 Meses,Requisito Regulatorio,Año Lanzamiento\nEjemplo Funcionalidad,Facturación electrónica,Media,México,25%,50%,75%,Sí,2023",
            file_name="plantilla_datos_adopcion.csv",
            mime="text/csv"
        )

    with benchmark_tab3:
        st.subheader("Análisis Comparativo: Histórico vs. Benchmark")
        
        col1, col2 = st.columns(2)
        with col1:
            # Usar nueva lista de funcionalidades
            tipo_comparar = st.selectbox("Seleccionar Tipo de Funcionalidad:", options=historical_df['Tipo'].unique())
        with col2:
            # Usar nueva lista de países
            pais_comparar = st.selectbox("Seleccionar País (Opcional):", options=['Todos'] + list(historical_df['País'].unique()))
        
        hist_tipo_df = historical_df[historical_df['Tipo'] == tipo_comparar]
        if pais_comparar != 'Todos':
            hist_pais_tipo_df = hist_tipo_df[hist_tipo_df['País'] == pais_comparar]
        else:
            hist_pais_tipo_df = hist_tipo_df
        
        hist_avg = hist_tipo_df['Tasa Adopción 3 Meses'].str.replace('%', '').astype(float).mean()
        hist_pais_avg = hist_pais_tipo_df['Tasa Adopción 3 Meses'].str.replace('%', '').astype(float).mean() if not hist_pais_tipo_df.empty else None
        
        # Buscar benchmark correspondiente (puede ser más genérico)
        benchmark_row = benchmarks_df[benchmarks_df['Métrica'].str.contains(tipo_comparar, case=False)]
        if benchmark_row.empty: # Si no hay específico, usar el general
             benchmark_row = benchmarks_df[benchmarks_df['Métrica'] == 'Tasa Adopción Funcionalidad - Software Contable Latam']

        if not benchmark_row.empty:
            benchmark_correspondiente = benchmark_row['Valor Benchmark (Promedio/Rango)'].iloc[0]
            benchmark_range = str(benchmark_correspondiente).replace('%', '').split('-')
            if len(benchmark_range) == 2:
                benchmark_low = float(benchmark_range[0])
                benchmark_high = float(benchmark_range[1])
                benchmark_avg = (benchmark_low + benchmark_high) / 2
            else:
                benchmark_avg = extract_avg(benchmark_correspondiente)
                benchmark_low = benchmark_avg - 3
                benchmark_high = benchmark_avg + 3
        else:
            benchmark_avg, benchmark_low, benchmark_high = None, None, None
        
        if benchmark_avg is not None and not np.isnan(hist_avg):
            st.markdown(f"#### Comparación para: {tipo_comparar}")
            fig, ax = plt.subplots(figsize=(8, 5))
            
            categories = ['Benchmark Industria', f'Promedio Histórico ({tipo_comparar})']
            values = [benchmark_avg, hist_avg]
            colors = ['#6c757d', '#6f42c1'] # Gris para benchmark, morado para histórico
            
            if pais_comparar != 'Todos' and hist_pais_avg is not None and not np.isnan(hist_pais_avg):
                categories.append(f'Histórico {pais_comparar}')
                values.append(hist_pais_avg)
                colors.append('#17a2b8')
            
            bars = ax.bar(categories, values, color=colors, width=0.5)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{height:.1f}%', ha='center', va='bottom', fontsize=10)
            
            if benchmark_low is not None and benchmark_high is not None:
                 ax.fill_between([-0.5, len(categories)-0.5], benchmark_low, benchmark_high, 
                                color='#6c757d', alpha=0.1, label=f'Rango Benchmark ({benchmark_low:.0f}%-{benchmark_high:.0f}%)')
                 ax.legend(fontsize=9)
            
            ax.set_ylim(0, max(values + [benchmark_high if benchmark_high else 0]) * 1.2)
            ax.set_ylabel('Tasa de Adopción a 3 Meses (%)', fontsize=10)
            plt.xticks(rotation=15, ha='right', fontsize=10)
            ax.tick_params(axis='y', labelsize=10)
            sns.despine()
            plt.tight_layout()
            st.pyplot(fig)
            
            st.markdown("##### Análisis")
            if hist_avg > benchmark_high:
                st.markdown(f"<div class='success-box'><p>🚀 El promedio histórico ({hist_avg:.1f}%) está <strong>por encima</strong> del benchmark ({benchmark_low:.0f}%-{benchmark_high:.0f}%).</p></div>", unsafe_allow_html=True)
            elif hist_avg >= benchmark_low:
                st.markdown(f"<div class='info-box'><p>✅ El promedio histórico ({hist_avg:.1f}%) está <strong>dentro</strong> del benchmark ({benchmark_low:.0f}%-{benchmark_high:.0f}%).</p></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='warning-box'><p>⚠️ El promedio histórico ({hist_avg:.1f}%) está <strong>por debajo</strong> del benchmark ({benchmark_low:.0f}%-{benchmark_high:.0f}%).</p></div>", unsafe_allow_html=True)
            
            if pais_comparar != 'Todos' and hist_pais_avg is not None and not np.isnan(hist_pais_avg):
                if hist_pais_avg > hist_avg:
                    st.markdown(f"<div class='success-box'><p>👍 El desempeño en <strong>{pais_comparar}</strong> ({hist_pais_avg:.1f}%) es <strong>superior</strong> al promedio general.</p></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='warning-box'><p>👎 El desempeño en <strong>{pais_comparar}</strong> ({hist_pais_avg:.1f}%) es <strong>inferior</strong> al promedio general.</p></div>", unsafe_allow_html=True)
        else:
            st.info("No hay suficientes datos (históricos o de benchmark) para realizar la comparación seleccionada.")

# --- Pestaña Generador de Informes (Texto botón corregido) ---
with tab3:
    st.header("📄 Generador de Informes")
    st.markdown("""
    <div class="info-box">
    <h4 style="margin-top:0">📝 Crea tu Resumen</h4>
    Genera un informe ejecutivo con los resultados clave de la calculadora o el análisis comparativo para compartir con tu equipo.
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.subheader("Configuración del Informe")
        col1, col2 = st.columns(2)
        with col1:
            informe_tipo = st.selectbox("Tipo de Informe:", ["Predicción de Nueva Funcionalidad", "Análisis Comparativo de Benchmarks"])
            informe_formato = st.selectbox("Formato de Salida:", ["Markdown", "HTML", "PDF (Próximamente)"])
        with col2:
            informe_incluir = st.multiselect("Incluir Secciones:", ["Resumen Ejecutivo", "Gráficos", "Tablas de Datos", "Factores Clave", "Recomendaciones", "Metodología"], default=["Resumen Ejecutivo", "Gráficos", "Recomendaciones"])
        
        # Botón usa estilo CSS para texto blanco
        if st.button("✨ Generar Informe", type="primary"):
            with st.spinner("Generando informe..."):
                time.sleep(1) # Simular generación
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                report_content_md = f"""
# Informe de Adopción SaaS - {informe_tipo}
*Generado el {time_now}*

---
"""
                if "Resumen Ejecutivo" in informe_incluir:
                    if informe_tipo == "Predicción de Nueva Funcionalidad":
                        report_content_md += f"""
## Resumen Ejecutivo
Predicción de tasa de adopción para: **{nombre_funcionalidad if nombre_funcionalidad else "Nueva Funcionalidad"}**.
- **Tasa Objetivo Base (3 Meses):** {rango_objetivo_base}
- Escenario Optimista: {rango_objetivo_optimista}
- Escenario Pesimista: {rango_objetivo_pesimista}

"""
                    else:
                        report_content_md += f"""
## Resumen Ejecutivo
Análisis comparativo de benchmarks de la industria (Software Contable Latam) con datos históricos.
- **Tipo de Funcionalidad Analizada:** {tipo_comparar}
- **Benchmark Industria (3 Meses):** {benchmark_correspondiente if benchmark_avg is not None else 'N/A'}
- **Promedio Histórico (3 Meses):** {hist_avg:.1f}% {f'(País: {pais_comparar} - {hist_pais_avg:.1f}%)' if pais_comparar != 'Todos' and hist_pais_avg is not None else ''}

"""
                
                if "Factores Clave" in informe_incluir and informe_tipo == "Predicción de Nueva Funcionalidad":
                     report_content_md += "## Factores Clave de Influencia\n"
                     if factores:
                         for factor in factores:
                             report_content_md += f"- {factor[0]}: {factor[1]} ({factor[2]})\n"
                     report_content_md += "\n"
                
                if "Recomendaciones" in informe_incluir:
                    report_content_md += "## Recomendaciones\n"
                    if informe_tipo == "Predicción de Nueva Funcionalidad":
                        if recomendaciones:
                            for rec in recomendaciones:
                                report_content_md += f"- {rec}\n"
                        else:
                             report_content_md += "- No hay recomendaciones específicas.\n"
                    else:
                        report_content_md += "- Identificar causas de desviaciones respecto al benchmark.\n"
                        report_content_md += "- Replicar estrategias exitosas de funcionalidades/países con alto desempeño.\n"
                        report_content_md += "- Ajustar estrategias en áreas con bajo desempeño.\n"
                    report_content_md += "\n"
                
                if "Metodología" in informe_incluir:
                    report_content_md += "## Metodología\n"
                    if informe_tipo == "Predicción de Nueva Funcionalidad":
                        report_content_md += "- Estimación basada en benchmarks de software contable Latam y modelo predictivo ponderado con ajustes estimados por país.\n"
                    else:
                        report_content_md += "- Comparación de promedios históricos con benchmarks estimados de la industria.\n"
                    report_content_md += "\n"
                
                st.success(f"Informe generado exitosamente.")
                st.markdown("### Vista Previa (Markdown)")
                st.markdown(f"```markdown\n{report_content_md}\n```")
                
                # Botón de descarga ahora usa st.button y se aplica estilo CSS
                st.download_button(
                    label=f"⬇️ Descargar Informe ({informe_formato})",
                    data=report_content_md,
                    file_name=f"informe_adopcion_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )

# --- Footer Personalizado ---
st.markdown("--- ")
st.markdown("""
<div class="footer-custom">
    Herramienta de Estimación de Adopción SaaS B2B Latam | Versión 1.6 - Abril 2025
</div>
""", unsafe_allow_html=True)
