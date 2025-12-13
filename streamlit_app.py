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
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="GreenScape Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar CSS personalizado
def apply_custom_css():
    css_file = Path(__file__).parent / "css" / "style.css"
    if css_file.exists():
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # CSS por defecto en caso de que no exista el archivo
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

# Inicializar sesión state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'query_results' not in st.session_state:
    st.session_state.query_results = None
if 'selected_plant' not in st.session_state:
    st.session_state.selected_plant = None
if 'price_history' not in st.session_state:
    st.session_state.price_history = None

# Conexión a la base de datos
@st.cache_resource
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=st.secrets.get("DB_HOST", "localhost"),
            user=st.secrets.get("DB_USER", "root"),
            password=st.secrets.get("DB_PASSWORD", ""),
            database=st.secrets.get("DB_NAME", "GreenScape"),
            port=st.secrets.get("DB_PORT", 3306)
        )
        return connection
    except Exception as e:
        st.error(f"Error de conexión a la base de datos: {str(e)}")
        return None

# Ejecutar consulta SQL
def run_query(query, params=None):
    connection = get_db_connection()
    if connection is None:
        return pd.DataFrame()
    
    try:
        cursor = connection.cursor(dictionary=True)
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

# ==================== SECCIÓN 1: SELECTOR DE CONSULTAS ====================
def query_selector_section():
    st.markdown("## 📊 Selector de Consultas SQL")
    st.markdown("Selecciona una consulta del ejercicio 3 para ejecutarla y visualizar los resultados.")
    
    col1, col2 = st.columns([3, 1])
    
    # Lista de consultas disponibles (se cargarán del archivo queries.py)
    queries = {
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
        list(queries.keys()),
        key="query_selector"
    )
    
    col1, col2, col3 = st.columns(3)
    with col1: execute_button = st.button("🚀 Ejecutar Consulta", use_container_width=True)
    with col2: export_button = st.button("📤 Exportar Resultados", use_container_width=True)
    with col3: clear_button = st.button("🧹 Limpiar Resultados", use_container_width=True)

    if execute_button:
        with st.spinner("Ejecutando consulta..."):
            # Aquí se cargaría la consulta específica desde queries.py
            # Por ahora, mostramos un placeholder
            placeholder_data = pd.DataFrame({
                'Columna1': [1, 2, 3, 4, 5],
                'Columna2': ['A', 'B', 'C', 'D', 'E'],
                'Columna3': [10.5, 20.3, 30.1, 40.7, 50.9]
            })
            st.session_state.query_results = placeholder_data
            
            # Mostrar estadísticas
            st.success(f"✅ Consulta ejecutada correctamente. Resultados: {len(placeholder_data)} filas")
    
    # Mostrar resultados si existen
    if st.session_state.query_results is not None:
        st.markdown("### 📋 Resultados de la Consulta")
        
        st.dataframe(
            st.session_state.query_results,
            use_container_width=True,
            height=400
        )
        
        # Estadísticas rápidas
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

# ==================== SECCIÓN 2: ANÁLISIS DE USUARIO ====================
def user_analysis_section():
    st.markdown("## 👤 Análisis de Usuario con Procedimiento Almacenado")
    st.markdown("Utiliza el procedimiento almacenado `sp_analisis_usuario` para obtener métricas detalladas de actividad.")
    
    col_left, col_right = st.columns([2, 3])
    
    with col_left:
        st.markdown("### Parámetros de Entrada")
        
        # Selector de usuario (simulando datos de la BD)
        users_data = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'Nombre': ['Juan Perez', 'María García', 'Luis Torres', 'Ana Sánchez', 
                      'Carlos Martínez', 'Laura López', 'Pedro Ramírez', 'Sonia Ruiz',
                      'Jorge Rodríguez', 'Elena Gómez'],
            'Email': ['juan@email.com', 'maria@email.com', 'luis@email.com', 'ana@email.com',
                     'carlos@email.com', 'laura@email.com', 'pedro@email.com', 'sonia@email.com',
                     'jorge@email.com', 'elena@email.com']
        })
        
        selected_user = st.selectbox(
            "Seleccionar Usuario:",
            users_data.apply(lambda x: f"{x['ID']} - {x['Nombre']} ({x['Email']})", axis=1)
        )
        user_id = int(selected_user.split(" - ")[0])
        
        # Selector de fechas
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            start_date = st.date_input(
                "Fecha Inicio:",
                value=datetime.now() - timedelta(days=90),
                max_value=datetime.now()
            )
        with col_date2:
            end_date = st.date_input(
                "Fecha Fin:",
                value=datetime.now(),
                min_value=start_date,
                max_value=datetime.now()
            )
        
        # Botón para ejecutar análisis
        analyze_button = st.button(
            "🔍 Ejecutar Análisis de Usuario",
            use_container_width=True,
            type="primary"
        )
    
    with col_right:
        st.markdown("### Resultados del Análisis")
        
        if analyze_button:
            # Simulación de resultados del procedimiento almacenado
            with st.spinner("Analizando actividad del usuario..."):
                # Simular tiempo de procesamiento
                import time
                time.sleep(1)
                
                # Resultados simulados
                results = {
                    "TotalPublicaciones": 24,
                    "ReaccionesDadas": 156,
                    "ReaccionesRecibidas": 89,
                    "TotalComentarios": 42,
                    "TotalCompras": 8,
                    "MontoGastado": 1256.75,
                    "TotalContribuciones": 15,
                    "PlantaMasComprada": "Planta Araña",
                    "PlantaMasContribuida": "Potos Dorado"
                }
                
                # Mostrar métricas principales
                st.markdown("#### 📈 Métricas Principales")
                cols = st.columns(4)
                metrics = [
                    ("Publicaciones", results["TotalPublicaciones"], "📝"),
                    ("Reacciones Dadas", results["ReaccionesDadas"], "👍"),
                    ("Reacciones Recibidas", results["ReaccionesRecibidas"], "❤️"),
                    ("Comentarios", results["TotalComentarios"], "💬"),
                    ("Compras", results["TotalCompras"], "🛒"),
                    ("Monto Gastado", f"${results['MontoGastado']:,.2f}", "💰"),
                    ("Contribuciones", results["TotalContribuciones"], "🌱"),
                    ("Actividad Total", results["TotalPublicaciones"] + results["TotalComentarios"] + results["TotalContribuciones"], "📊")
                ]
                
                for i, (label, value, icon) in enumerate(metrics):
                    with cols[i % 4]:
                        st.metric(label=f"{icon} {label}", value=value)
                
                # Gráficos de actividad
                st.markdown("#### 📊 Visualización de Actividad")
                
                # Simular datos de actividad mensual
                months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
                activity_data = pd.DataFrame({
                    'Mes': months,
                    'Publicaciones': [3, 4, 5, 4, 5, 3],
                    'Comentarios': [5, 7, 6, 8, 7, 9],
                    'Reacciones': [20, 25, 30, 28, 32, 21]
                })
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=activity_data['Mes'],
                    y=activity_data['Publicaciones'],
                    name='Publicaciones',
                    line=dict(color='#4CAF50', width=3),
                    mode='lines+markers'
                ))
                fig.add_trace(go.Scatter(
                    x=activity_data['Mes'],
                    y=activity_data['Comentarios'],
                    name='Comentarios',
                    line=dict(color='#2196F3', width=3),
                    mode='lines+markers'
                ))
                fig.add_trace(go.Scatter(
                    x=activity_data['Mes'],
                    y=activity_data['Reacciones'],
                    name='Reacciones',
                    line=dict(color='#FF9800', width=3),
                    mode='lines+markers'
                ))
                
                fig.update_layout(
                    title="Actividad Mensual del Usuario",
                    plot_bgcolor='rgba(240, 255, 240, 0.8)',
                    paper_bgcolor='rgba(255, 255, 255, 0.9)',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Detalles adicionales
                with st.expander("📋 Detalles Completos del Análisis"):
                    st.json(results)
                    
                    st.markdown("**Planta más comprada:**")
                    st.info(f"🌿 {results['PlantaMasComprada']}")
                    
                    st.markdown("**Planta más contribuida:**")
                    st.info(f"🌱 {results['PlantaMasContribuida']}")

# ==================== SECCIÓN 3: GESTIÓN DE CONVERSACIONES ====================
def conversation_management_section():
    st.markdown("## 💬 Gestión de Conversaciones")
    st.markdown("Crea y navega por hilos de conversación en los comentarios.")
    
    tab1, tab2 = st.tabs(["📝 Crear Comentario", "🌳 Navegar Conversaciones"])
    
    with tab1:
        st.markdown("### Crear Nuevo Comentario")
        
        col1, col2 = st.columns(2)
        with col1:
            # Selector de publicación
            publications = pd.DataFrame({
                'ID': [1, 2, 3, 4, 5],
                'Texto': [
                    "Mi opinión sobre el último lanzamiento tecnológico",
                    "Rutinas de ejercicio para hacer en casa",
                    "Mi primera receta de pan casero",
                    "Hermoso día en el parque!",
                    "Viajar solo: mi experiencia y consejos"
                ],
                'Autor': ['Juan Perez', 'María García', 'Luis Torres', 'Ana Sánchez', 'Carlos Martínez']
            })
            
            selected_publication = st.selectbox(
                "Publicación:",
                publications.apply(lambda x: f"ID {x['ID']}: {x['Texto'][:50]}...", axis=1)
            )
            pub_id = int(selected_publication.split(":")[0].replace("ID ", ""))
        
        with col2:
            # Selector de comentario padre (para respuestas)
            comment_threads = pd.DataFrame({
                'ID': [None, 1, 2, 3],
                'Texto': [
                    "Nuevo comentario (sin respuesta)",
                    "¡Excelente publicación!",
                    "Totalmente de acuerdo",
                    "¿Podrías explicar más sobre esto?"
                ]
            })
            
            parent_comment = st.selectbox(
                "Responder a (opcional):",
                comment_threads.apply(lambda x: f"{x['ID']}: {x['Texto']}" if pd.notna(x['ID']) else "Nuevo comentario", axis=1)
            )
        
        # Editor de comentario
        comment_text = st.text_area(
            "Tu comentario:",
            placeholder="Escribe tu comentario aquí...",
            height=150
        )
        
        # Botones de acción
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("💾 Guardar Comentario", use_container_width=True):
                if comment_text.strip():
                    st.success("✅ Comentario guardado exitosamente")
                    st.balloons()
                else:
                    st.error("Por favor, escribe un comentario")
        
        with col_btn2:
            preview = st.button("👁️ Vista Previa", use_container_width=True)
        
        with col_btn3:
            clear = st.button("🗑️ Limpiar", use_container_width=True)
        
        if preview and comment_text:
            with st.expander("Vista previa del comentario"):
                st.markdown(f"**Tu comentario:**")
                st.markdown(f"> {comment_text}")
    
    with tab2:
        st.markdown("### Navegación Jerárquica de Conversaciones")
        
        # Selector de conversación inicial
        initial_comments = pd.DataFrame({
            'ID': [1, 2, 3],
            'Texto': [
                "Increíble atardecer visto desde mi ventana",
                "Los mejores cafés para comenzar tu día",
                "Explorando nuevos senderos de montaña"
            ],
            'Respuestas': [5, 3, 7]
        })
        
        selected_conversation = st.selectbox(
            "Seleccionar conversación:",
            initial_comments.apply(lambda x: f"💬 {x['Texto'][:60]}... ({x['Respuestas']} respuestas)", axis=1)
        )
        
        if st.button("🔍 Cargar Conversación", type="primary"):
            # Simular árbol de conversación
            conversation_tree = {
                'root': {
                    'id': 1,
                    'text': "Increíble atardecer visto desde mi ventana",
                    'author': "Juan Perez",
                    'date': "2024-01-15",
                    'replies': [
                        {
                            'id': 2,
                            'text': "¡Qué hermosa vista! ¿En qué ciudad estás?",
                            'author': "María García",
                            'date': "2024-01-15",
                            'replies': [
                                {
                                    'id': 3,
                                    'text': "Estoy en Barcelona, la vista es desde mi apartamento",
                                    'author': "Juan Perez",
                                    'date': "2024-01-16"
                                }
                            ]
                        },
                        {
                            'id': 4,
                            'text': "Me encantaría ver más fotos",
                            'author': "Carlos Martínez",
                            'date': "2024-01-16"
                        }
                    ]
                }
            }
            
            # Función para mostrar árbol recursivamente
            def display_conversation(node, level=0):
                indent = "&nbsp;" * (level * 40) + ("↳ " if level > 0 else "")
                author_badge = f"👤 **{node['author']}**" if level == 0 else f"👥 **{node['author']}**"
                
                st.markdown(f"""
                <div style="margin-left: {level * 20}px; padding: 10px; border-left: {'3px solid #4CAF50' if level > 0 else 'none'}; margin-bottom: 10px;">
                    <div style="color: #0a5c36; font-size: {'18px' if level == 0 else '16px'};">
                        {indent}{author_badge} · 📅 {node['date']}
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.8); padding: 15px; border-radius: 10px; margin-top: 5px; border: 1px solid #81c784;">
                        {node['text']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if 'replies' in node:
                    for reply in node['replies']:
                        display_conversation(reply, level + 1)
            
            # Mostrar conversación
            display_conversation(conversation_tree['root'])

# ==================== SECCIÓN 4: EXPLORADOR DE DOCUMENTOS ====================
def document_explorer_section():
    st.markdown("## 📚 Explorador de Documentos de Plantas")
    st.markdown("Visualiza todos los documentos asociados a una planta de forma organizada y jerárquica.")
    
    # Lista de plantas disponibles
    plants_data = pd.DataFrame({
        'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Nombre': [
            'Planta Araña', 'Planta Serpiente', 'Potos', 'Planta ZZ', 'Filodendro',
            'Hiedra Inglesa', 'Aglaonema', 'Lirio de Paz', 'Planta de Caucho', 'Aloe Vera'
        ],
        'Categoría': ['Ornamental', 'Ornamental', 'Ornamental', 'Ornamental', 'Ornamental',
                     'Ornamental', 'Ornamental', 'Ornamental', 'Ornamental', 'Medicinal'],
        'Documentos': [5, 4, 6, 3, 5, 4, 3, 6, 4, 5]
    })
    
    # Seleccionar planta
    selected_plant = st.selectbox(
        "Seleccionar Planta:",
        plants_data.apply(lambda x: f"{x['ID']}: {x['Nombre']} ({x['Categoría']}) - {x['Documentos']} documentos", axis=1)
    )
    
    plant_id = int(selected_plant.split(":")[0])
    plant_name = selected_plant.split(":")[1].split("(")[0].strip()
    
    if st.button("🌿 Cargar Documentos", type="primary"):
        st.session_state.selected_plant = {
            'id': plant_id,
            'name': plant_name,
            'documents': load_plant_documents(plant_id)  # Función simulada
        }
    
    # Mostrar documentos si hay una planta seleccionada
    if st.session_state.selected_plant:
        plant = st.session_state.selected_plant
        
        st.markdown(f"### 📖 Documentos de: **{plant['name']}**")
        
        # Mostrar jerarquía de documentos
        documents = plant['documents']
        
        # Pestañas para diferentes vistas
        tab_tree, tab_list, tab_details = st.tabs(["🌳 Vista de Árbol", "📋 Lista de Documentos", "🔍 Detalles"])
        
        with tab_tree:
            st.markdown("#### Estructura Jerárquica de Documentos")
            
            # Función recursiva para mostrar árbol
            def display_document_tree(doc, level=0):
                icon = "📄" if doc['type'] == 'principal' else "📑"
                badge_color = "#4CAF50" if doc['type'] == 'principal' else "#2196F3"
                
                st.markdown(f"""
                <div style="margin-left: {level * 30}px; padding: 8px; border-left: 2px solid {badge_color}; margin-bottom: 5px;">
                    <div style="background: {badge_color}; color: white; padding: 5px 10px; border-radius: 5px; display: inline-block; margin-right: 10px;">
                        {icon} {doc['type'].upper()}
                    </div>
                    <strong>{doc['title']}</strong>
                    <div style="color: #666; font-size: 14px; margin-top: 5px;">
                        📅 {doc['date']} · 📏 {doc['size']} · 📂 {doc['format']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if 'children' in doc:
                    for child in doc['children']:
                        display_document_tree(child, level + 1)
            
            # Mostrar documentos principales
            for doc in documents:
                display_document_tree(doc)
        
        with tab_list:
            st.markdown("#### Lista Completa de Documentos")
            
            # Crear tabla de documentos
            doc_list = flatten_documents(documents)
            df_docs = pd.DataFrame(doc_list)
            
            if not df_docs.empty:
                st.dataframe(
                    df_docs,
                    column_config={
                        "type": st.column_config.TextColumn("Tipo"),
                        "title": st.column_config.TextColumn("Título"),
                        "date": st.column_config.TextColumn("Fecha"),
                        "size": st.column_config.TextColumn("Tamaño"),
                        "format": st.column_config.TextColumn("Formato")
                    },
                    use_container_width=True
                )
        
        with tab_details:
            st.markdown("#### Información Detallada")
            
            # Mostrar estadísticas
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📄 Total Documentos", len(flatten_documents(documents)))
            with col2:
                st.metric("📑 Documentos Secundarios", len([d for d in flatten_documents(documents) if d['type'] != 'principal']))
            with col3:
                total_size = sum([d['size_num'] for d in flatten_documents(documents)])
                st.metric("📏 Tamaño Total", f"{total_size} MB")
            with col4:
                formats = set([d['format'] for d in flatten_documents(documents)])
                st.metric("📂 Formatos", len(formats))
            
            # Gráfico de distribución por tipo
            doc_types = pd.DataFrame(flatten_documents(documents))['type'].value_counts()
            fig = px.pie(
                values=doc_types.values,
                names=doc_types.index,
                title="Distribución de Tipos de Documentos",
                color_discrete_sequence=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

# ==================== SECCIÓN 5: GESTOR DE PRECIOS ====================
def price_manager_section():
    st.markdown("## 💰 Gestor de Precios de Productos")
    st.markdown("Modifica precios de productos y visualiza el historial de cambios.")
    
    # Obtener lista de productos
    products = pd.DataFrame({
        'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Nombre': [
            'Planta Araña', 'Planta Serpiente', 'Potos', 'Planta ZZ', 'Filodendro',
            'Hiedra Inglesa', 'Aglaonema', 'Lirio de Paz', 'Planta de Caucho', 'Aloe Vera'
        ],
        'Precio Actual': [100.0, 102.3, 123.2, 123.0, 364.0, 922.3, 83.1, 1.5, 10.2, 2.3],
        'Última Modificación': ['2024-01-15', '2024-02-10', '2024-01-22', '2024-03-05',
                               '2024-02-28', '2024-01-30', '2024-03-12', '2024-02-15',
                               '2024-01-18', '2024-03-08']
    })
    
    # Layout principal
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown("### 📦 Seleccionar Producto")
        
        selected_product = st.selectbox(
            "Producto:",
            products.apply(lambda x: f"{x['ID']}: {x['Nombre']} - ${x['Precio Actual']}", axis=1)
        )
        
        product_id = int(selected_product.split(":")[0])
        product_info = products[products['ID'] == product_id].iloc[0]
        
        # Mostrar información del producto seleccionado
        st.markdown("#### Información del Producto")
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 10px; border: 2px solid #4CAF50;">
            <h4 style="color: #0a5c36; margin-top: 0;">{product_info['Nombre']}</h4>
            <div style="font-size: 28px; color: #2e7d32; font-weight: bold;">
                ${product_info['Precio Actual']:.2f}
            </div>
            <div style="color: #666; margin-top: 10px;">
                📅 Última modificación: {product_info['Última Modificación']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Formulario para modificar precio
        st.markdown("#### ✏️ Modificar Precio")
        
        with st.form("price_update_form"):
            new_price = st.number_input(
                "Nuevo precio:",
                min_value=0.01,
                max_value=10000.0,
                value=float(product_info['Precio Actual']),
                step=0.01
            )
            
            change_reason = st.text_area(
                "Motivo del cambio (opcional):",
                placeholder="Ej: Actualización por temporada, corrección de precio, etc.",
                height=100
            )
            
            submitted = st.form_submit_button("💾 Actualizar Precio", type="primary")
            
            if submitted:
                if new_price != product_info['Precio Actual']:
                    # Simular actualización en base de datos
                    st.success(f"✅ Precio actualizado de ${product_info['Precio Actual']} a ${new_price}")
                    
                    # Simular trigger de auditoría
                    audit_record = {
                        'producto': product_info['Nombre'],
                        'precio_anterior': product_info['Precio Actual'],
                        'precio_nuevo': new_price,
                        'porcentaje_cambio': ((new_price - product_info['Precio Actual']) / product_info['Precio Actual']) * 100,
                        'fecha_cambio': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'motivo': change_reason if change_reason else "Sin motivo especificado"
                    }
                    
                    st.session_state.price_history = audit_record
                    st.rerun()
                else:
                    st.warning("El nuevo precio es igual al precio actual")
    
    with col_right:
        st.markdown("### 📜 Historial de Auditoría")
        
        if st.session_state.price_history:
            audit = st.session_state.price_history
            
            # Mostrar último cambio
            st.markdown("#### Último Cambio Registrado")
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(255, 255, 240, 0.9), rgba(240, 255, 240, 0.9)); 
                        padding: 20px; border-radius: 10px; border: 2px solid #FF9800; margin-bottom: 20px;">
                <div style="color: #0a5c36; font-weight: bold; font-size: 18px;">
                    {audit['producto']}
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                    <div style="text-align: center;">
                        <div style="color: #666; font-size: 14px;">Precio Anterior</div>
                        <div style="color: #f44336; font-size: 22px; font-weight: bold;">
                            ${audit['precio_anterior']:.2f}
                        </div>
                    </div>
                    <div style="text-align: center; align-self: center;">
                        <div style="font-size: 24px;">→</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #666; font-size: 14px;">Precio Nuevo</div>
                        <div style="color: #4CAF50; font-size: 22px; font-weight: bold;">
                            ${audit['precio_nuevo']:.2f}
                        </div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 15px;">
                    <div style="color: #666; font-size: 14px;">Cambio</div>
                    <div style="color: {'#f44336' if audit['porcentaje_cambio'] < 0 else '#4CAF50'}; 
                                font-size: 20px; font-weight: bold;">
                        {audit['porcentaje_cambio']:+.2f}%
                    </div>
                </div>
                <div style="margin-top: 15px; color: #666;">
                    📅 {audit['fecha_cambio']}
                </div>
                <div style="margin-top: 10px; padding: 10px; background: rgba(255, 255, 255, 0.7); 
                            border-radius: 5px; border-left: 4px solid #2196F3;">
                    💡 <strong>Motivo:</strong> {audit['motivo']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Tabla de historial completo (simulado)
        st.markdown("#### Historial Completo de Cambios")
        
        history_data = pd.DataFrame({
            'Fecha': ['2024-03-15 14:30:00', '2024-02-10 10:15:00', '2024-01-05 16:45:00', '2023-12-20 09:30:00'],
            'Precio Anterior': [95.0, 90.0, 85.0, 80.0],
            'Precio Nuevo': [100.0, 95.0, 90.0, 85.0],
            'Cambio %': [+5.26, +5.56, +5.88, +6.25],
            'Usuario': ['admin', 'admin', 'admin', 'admin']
        })
        
        st.dataframe(
            history_data,
            column_config={
                "Fecha": st.column_config.DatetimeColumn("Fecha"),
                "Precio Anterior": st.column_config.NumberColumn("Precio Anterior", format="$%.2f"),
                "Precio Nuevo": st.column_config.NumberColumn("Precio Nuevo", format="$%.2f"),
                "Cambio %": st.column_config.NumberColumn("Cambio %", format="%.2f%%"),
                "Usuario": st.column_config.TextColumn("Usuario")
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Gráfico de evolución de precios
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(history_data['Fecha']),
            y=history_data['Precio Nuevo'],
            mode='lines+markers',
            name='Precio',
            line=dict(color='#4CAF50', width=3),
            marker=dict(size=10, color='#2e7d32')
        ))
        
        fig.update_layout(
            title="Evolución del Precio",
            xaxis_title="Fecha",
            yaxis_title="Precio ($)",
            plot_bgcolor='rgba(240, 255, 240, 0.8)',
            paper_bgcolor='rgba(255, 255, 255, 0.9)',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==================== FUNCIONES AUXILIARES ====================
def load_plant_documents(plant_id):
    """Cargar documentos de una planta (simulación)"""
    # Datos de ejemplo
    documents = [
        {
            'type': 'principal',
            'title': 'Ficha Técnica - Planta Araña',
            'date': '2024-01-15',
            'size': '2.5 MB',
            'size_num': 2.5,
            'format': 'PDF',
            'children': [
                {
                    'type': 'secundario',
                    'title': 'Certificado Fitosanitario',
                    'date': '2024-01-16',
                    'size': '1.2 MB',
                    'size_num': 1.2,
                    'format': 'PDF'
                },
                {
                    'type': 'secundario',
                    'title': 'Guía de Riego Estacional',
                    'date': '2024-01-17',
                    'size': '0.8 MB',
                    'size_num': 0.8,
                    'format': 'PDF',
                    'children': [
                        {
                            'type': 'anexo',
                            'title': 'Tabla de Riego por Mes',
                            'date': '2024-01-18',
                            'size': '0.3 MB',
                            'size_num': 0.3,
                            'format': 'Excel'
                        }
                    ]
                },
                {
                    'type': 'secundario',
                    'title': 'Manual de Tratamiento de Plagas',
                    'date': '2024-01-20',
                    'size': '1.5 MB',
                    'size_num': 1.5,
                    'format': 'PDF'
                }
            ]
        }
    ]
    return documents

def flatten_documents(documents):
    """Aplanar estructura jerárquica de documentos"""
    flat_list = []
    
    def flatten(doc):
        flat_list.append({
            'type': doc['type'],
            'title': doc['title'],
            'date': doc['date'],
            'size': doc['size'],
            'size_num': doc.get('size_num', 0),
            'format': doc['format']
        })
        if 'children' in doc:
            for child in doc['children']:
                flatten(child)
    
    for doc in documents:
        flatten(doc)
    
    return flat_list

# ==================== BARRA LATERAL ====================
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
        
        # Navegación principal
        st.markdown("### 📍 Navegación")
        
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
        
        # Información del sistema
        st.markdown("### ℹ️ Estado del Sistema")
        
        # Simular estado de conexión
        connection_status = "🟢 Conectado" if get_db_connection() else "🔴 Desconectado"
        st.markdown(f"**Base de datos:** {connection_status}")
        
        # Métricas rápidas
        st.markdown("**Métricas:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("👥 **2,548**")
            st.caption("Usuarios")
        with col2:
            st.markdown("🌿 **1,235**")
            st.caption("Plantas")
        
        st.markdown("---")
        
        # Información de la sesión
        st.markdown("### 👤 Sesión")
        st.markdown(f"**Página actual:** {st.session_state.current_page}")
        
        if st.button("🔄 Recargar Página", use_container_width=True):
            st.rerun()

# ==================== PÁGINA PRINCIPAL ====================
def main():
    create_sidebar()
    
    # Encabezado principal
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #4CAF50, #2e7d32); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px; color: white;">
        <h1 style="color: white; margin-bottom: 10px;">{st.session_state.current_page}</h1>
        <p style="color: rgba(255, 255, 255, 0.9); margin: 0;">
            Plataforma de análisis y gestión para la comunidad GreenScape
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contenido según página seleccionada
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
    """Mostrar dashboard principal"""
    st.markdown("## 📈 Dashboard de GreenScape")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Usuarios Activos", "2,548", "+125 (5.2%)")
    with col2:
        st.metric("🌿 Plantas Registradas", "1,235", "+42 (3.5%)")
    with col3:
        st.metric("💬 Publicaciones", "8,942", "+327 (3.8%)")
    with col4:
        st.metric("💰 Ventas Totales", "$124,580", "+$8,420 (7.2%)")
    
    st.markdown("---")
    
    # Gráficos principales
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### 📊 Actividad Mensual")
        
        # Datos de ejemplo
        months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
        activity_data = {
            'Publicaciones': [450, 520, 600, 580, 620, 550],
            'Comentarios': [1200, 1350, 1500, 1420, 1600, 1450],
            'Reacciones': [3200, 3500, 3800, 3700, 3900, 3600]
        }
        
        fig = go.Figure()
        colors = ['#4CAF50', '#2196F3', '#FF9800']
        
        for i, (key, values) in enumerate(activity_data.items()):
            fig.add_trace(go.Bar(
                x=months,
                y=values,
                name=key,
                marker_color=colors[i]
            ))
        
        fig.update_layout(
            barmode='group',
            plot_bgcolor='rgba(240, 255, 240, 0.8)',
            paper_bgcolor='rgba(255, 255, 255, 0.9)',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_chart2:
        st.markdown("### 🌿 Plantas Más Populares")
        
        plants = ['Planta Araña', 'Planta Serpiente', 'Potos', 'Planta ZZ', 'Filodendro']
        popularity = [1250, 980, 850, 720, 650]
        
        fig = px.pie(
            values=popularity,
            names=plants,
            color_discrete_sequence=['#4CAF50', '#8BC34A', '#CDDC39', '#FFEB3B', '#FFC107']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Accesos rápidos
    st.markdown("### ⚡ Acciones Rápidas")
    
    col_quick1, col_quick2, col_quick3, col_quick4 = st.columns(4)
    
    with col_quick1:
        if st.button("📊 Ejecutar Consultas", use_container_width=True):
            st.session_state.current_page = "Consultas SQL"
            st.rerun()
    
    with col_quick2:
        if st.button("👤 Analizar Usuario", use_container_width=True):
            st.session_state.current_page = "Análisis de Usuario"
            st.rerun()
    
    with col_quick3:
        if st.button("📚 Ver Documentos", use_container_width=True):
            st.session_state.current_page = "Documentos"
            st.rerun()
    
    with col_quick4:
        if st.button("💰 Gestionar Precios", use_container_width=True):
            st.session_state.current_page = "Gestor de Precios"
            st.rerun()

def show_configuration():
    """Mostrar página de configuración"""
    st.markdown("## ⚙️ Configuración del Sistema")
    
    tab1, tab2, tab3 = st.tabs(["🔧 Conexión BD", "🎨 Apariencia", "🔐 Seguridad"])
    
    with tab1:
        st.markdown("### Configuración de Base de Datos")
        
        with st.form("db_config_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                db_host = st.text_input("Host", value="localhost")
                db_user = st.text_input("Usuario", value="root")
            
            with col2:
                db_name = st.text_input("Base de Datos", value="GreenScape")
                db_port = st.number_input("Puerto", value=3306, min_value=1, max_value=65535)
            
            db_password = st.text_input("Contraseña", type="password")
            
            if st.form_submit_button("💾 Guardar Configuración"):
                st.success("✅ Configuración guardada exitosamente")
    
    with tab2:
        st.markdown("### Personalización de Apariencia")
        
        theme = st.selectbox("Tema", ["Frutiger Aero", "Oscuro", "Claro"])
        primary_color = st.color_picker("Color Primario", "#4CAF50")
        font_size = st.slider("Tamaño de Fuente", 12, 24, 16)
        
        if st.button("Aplicar Cambios"):
            st.success("✅ Cambios aplicados exitosamente")
    
    with tab3:
        st.markdown("### Configuración de Seguridad")
        
        st.checkbox("Requerir autenticación de dos factores")
        st.checkbox("Registrar todas las operaciones")
        st.checkbox("Limitar acceso por IP")
        
        session_timeout = st.slider("Tiempo de expiración de sesión (minutos)", 15, 240, 60)
        
        if st.button("💾 Guardar Configuración de Seguridad"):
            st.success("✅ Configuración de seguridad guardada")

# ==================== EJECUCIÓN PRINCIPAL ====================
if __name__ == "__main__":
    main()