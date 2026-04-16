import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="SketchStudio | Interactive Design",
    page_icon="🎨",
    layout="wide"
)

# --- DISEÑO ESTÉTICO ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    div[data-testid="stExpander"], .result-box {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
    }
    .stButton>button:first-child {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000 !important;
        font-weight: 800;
        border-radius: 15px;
        border: none;
        height: 3.5em;
    }
    button[key="reset_btn"] {
        background: rgba(255, 75, 75, 0.1) !important;
        border: 1px solid #ff4b4b !important;
        color: #ff4b4b !important;
        border-radius: 15px;
    }
    .stCanvas {
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL LATERAL ---
with st.sidebar:
    st.title("Studio Tools")
    
    with st.expander("Dimensiones del Lienzo", expanded=True):
        canvas_width = st.slider("Ancho", 300, 1000, 700, 50)
        canvas_height = st.slider("Alto", 200, 800, 450, 50)
    
    with st.expander("Herramientas de Estilo", expanded=True):
        drawing_mode = st.selectbox("Herramienta:", 
            ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"))
        stroke_width = st.slider('Grosor de línea', 1, 30, 6)
        stroke_color = st.color_picker("Color de trazo", "#000000")
        bg_color = st.color_picker("Color de fondo", "#FFFFFF")

# --- INTERFAZ PRINCIPAL ---
st.title("SketchStudio AI")
st.markdown("#### Herramienta de prototipado para Diseño Interactivo")

col_draw, col_info = st.columns([1.6, 1])

with col_draw:
    # Canvas con tu configuración original de key dinámica
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode,
        key=f"canvas_{canvas_width}_{canvas_height}",
    )
    
    if st.button("BORRAR TODO EL TABLERO", key="reset_btn"):
        st.rerun()

with col_info:
    st.subheader("Formulario Ludificado") # Aplicando tu corrección de términos
    
    with st.expander("Notas de Ergonomía Cognitiva", expanded=True):
        st.markdown("Utiliza este espacio para documentar hallazgos del usuario.")
        
        # Campos para tus proyectos de EAFIT
        user_obs = st.text_area("Observaciones del usuario:", placeholder="Escribe aquí qué valoró el usuario...")
        st.info("Este sistema está diseñado para ser valorado por el usuario final.") # Siguiendo tus guías de estilo
        
        if st.button("GUARDAR SESIÓN"):
            if canvas_result.image_data is not None:
                st.success("Boceto y notas listas para documentar.")
            else:
                st.warning("El lienzo está vacío.")

st.markdown("<br><center><p style='opacity: 0.5;'>SketchStudio v5.0 | Universidad EAFIT</p></center>", unsafe_allow_html=True)
