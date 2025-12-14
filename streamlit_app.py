import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import warnings
import os
from pathlib import Path
from init import connection_dict
from mysql_queries import queries_dict
import mysql.connector as mq

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="GreenScape Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_custom_css():
    css_file = Path(__file__).parent / "css" / "style.css"
    if css_file.exists():
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
        }
        </style>
        """, unsafe_allow_html=True)

apply_custom_css()

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'query_results' not in st.session_state:
    st.session_state.query_results = None
if 'selected_plant' not in st.session_state:
    st.session_state.selected_plant = None
if 'price_history' not in st.session_state:
    st.session_state.price_history = None

@st.cache_resource
def get_db_connection():
    return mq.connect(**connection_dict)

def run_query(query, params=None):
    connection = mq.connect(**connection_dict)
    if connection is None:
        return pd.DataFrame()
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        connection.commit()
        cursor.close()
        return pd.DataFrame(result)
    except Exception as e:
        st.error(f"Error en la consulta: {str(e)}")
        return pd.DataFrame()
    finally:
        if connection.is_connected():
            connection.close()

def query_selector_section():
    st.markdown("## 📊 Selector de Consultas SQL")
    st.markdown("Selecciona una consulta del ejercicio 3 para ejecutarla y visualizar los resultados.")

    examples = {
        "a) Listar todos los productos disponibles": "a",
        "b) Contar las reacciones por publicación": "b",
        "c) Tipos de plantas preferidos": "c",
        "d) Usuarios activos en contribuciones y reacciones": "d",
        "e) Publicaciones más populares": "e",
        "f) Contribuciones constantes": "f",
        "g) Promedio de actividad": "g",
        "h) Distribución de edades": "h",
        "i) Productos sin incremento en ventas mensuales": "i",
        "j) Tendencias de contribución según clima": "j",
        "k) Cambio de preferencia en categorías": "k",
        "l) Compras contradictorias": "l",
        "m) Usuarios de solo texto": "m",
        "n) Vendedores mejor calificados": "n",
        "ñ) Trigger de auditoría de precios": "ñ",
        "o) Procedimiento almacenado - Análisis de usuario": "o",
        "p) Análisis de influencers": "p",
        "q) Detección de patrones anómalos": "q"
    }
    
    selected_query = st.selectbox(
        "Selecciona una consulta:",
        list(examples.keys()),
        key="query_selector"
    )
    selected_query = examples[selected_query]
    selected_query = queries_dict[selected_query]
    col1, col2, col3 = st.columns(3)
    with col1: execute_button = st.button("🚀 Ejecutar Consulta", use_container_width=True)
    with col2: export_button = st.button("📤 Exportar Resultados", use_container_width=True)
    with col3: clear_button = st.button("🧹 Limpiar Resultados", use_container_width=True)
    if execute_button:
        with st.spinner("Ejecutando consulta..."):
            st.session_state.query_results = run_query(selected_query)
            st.success(f"✅ Consulta ejecutada correctamente.")
    if st.session_state.query_results is not None:
        st.markdown("### 📋 Resultados de la Consulta")
        st.dataframe(
            st.session_state.query_results,
            use_container_width=True,
            height=400
        )
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        with col_stats1:
            st.metric("Total Filas", len(st.session_state.query_results))
        with col_stats2:
            st.metric("Total Columnas", len(st.session_state.query_results.columns))
        with col_stats3:
            numeric_cols = len(st.session_state.query_results.select_dtypes(include=['int64', 'float64']).columns)
            st.metric("Columnas Numéricas", numeric_cols)
    if clear_button and st.session_state.query_results is not None:
        st.session_state.query_results = None
        st.rerun()

def user_analysis_section():
    pass

def conversation_management_section():
    pass

def document_explorer_section():
    pass

def price_manager_section():
    pass

def create_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="color: #0a5c36; margin-bottom: 0;">🌿</h1>
            <h2 style="color: #0a5c36; margin-top: 0;">GreenScape</h2>
            <p style="color: #2e7d32; font-size: 14px;">Plataforma de Análisis de Datos</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        page_options = {
            "🏠 Dashboard": "Dashboard",
            "📊 Consultas SQL": "Consultas SQL",
            "👤 Análisis de Usuario": "Análisis de Usuario",
            "💬 Conversaciones": "Conversaciones",
            "📚 Documentos": "Documentos",
            "💰 Gestor de Precios": "Gestor de Precios",
            "⚙️ Configuración": "Configuración"
        }
        
        for icon_text, page_name in page_options.items():
            if st.button(
                icon_text,
                key=f"nav_{page_name}",
                use_container_width=True,
                type="secondary" if st.session_state.current_page != page_name else "primary"
            ):
                st.session_state.current_page = page_name
                st.rerun()
        
        st.markdown("---")
        
        connection_status = "🟢 Conectado" if get_db_connection() else "🔴 Desconectado"
        st.markdown(f"**Base de datos:** {connection_status}")
        
        st.markdown("**Métricas:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("👥 **2,548**")
            st.caption("Usuarios")
        with col2:
            st.markdown("🌿 **1,235**")
            st.caption("Plantas")
        
        st.markdown("---")
        
        st.markdown(f"**Página actual:** {st.session_state.current_page}")
        
        if st.button("🔄 Recargar Página", use_container_width=True):
            st.rerun()

def main():
    create_sidebar()
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #23aa00, #00aa34); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px; color: white;">
        <h1 style="color: white; margin-bottom: 10px;">{st.session_state.current_page}</h1>
        <p style="color: rgba(255, 255, 255, 0.9); margin: 0;">
            Plataforma de análisis y gestión para la comunidad GreenScape
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.current_page == "Dashboard":
        show_dashboard()
    elif st.session_state.current_page == "Consultas SQL":
        query_selector_section()
    elif st.session_state.current_page == "Análisis de Usuario":
        user_analysis_section()
    elif st.session_state.current_page == "Conversaciones":
        conversation_management_section()
    elif st.session_state.current_page == "Documentos":
        document_explorer_section()
    elif st.session_state.current_page == "Gestor de Precios":
        price_manager_section()
    elif st.session_state.current_page == "Configuración":
        show_configuration()

def show_dashboard():
    pass

def show_configuration():
    pass

if __name__ == "__main__":
    main()