import os
import streamlit as st
import base64
import numpy as np
from openai import OpenAI
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="SketchMind AI | Creative Studio",
    page_icon="🎨",
    layout="wide"
)

# --- DISEÑO ESTÉTICO (GLASSMORPHISM) ---
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
        text-transform: uppercase;
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

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# --- PANEL LATERAL (PROPIEDADES DEL TABLERO) ---
with st.sidebar:
    st.header("Propiedades del Tablero")
    
    with st.expander("Dimensiones del Tablero", expanded=True):
        canvas_width = st.slider("Ancho del tablero", 300, 1000, 700, 50)
        canvas_height = st.slider("Alto del tablero", 200, 800, 450, 50)
    
    with st.expander("Herramientas de Estilo", expanded=True):
        drawing_mode = st.selectbox("Herramienta de Dibujo:", 
            ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"))
        stroke_width = st.slider('Selecciona el ancho de línea', 1, 30, 6)
        stroke_color = st.color_picker("Color de trazo", "#000000")
        bg_color = st.color_picker("Color de fondo", "#FFFFFF")

    st.markdown("---")
    api_key = st.text_input("OpenAI Key", type="password")

# --- INTERFAZ PRINCIPAL ---
st.title("SketchMind AI")
st.markdown("#### Un espacio para tu creatividad e investigación interactiva.")

col_draw, col_ai = st.columns([1.6, 1])

with col_draw:
    # Canvas con los parámetros exactos de tu código original
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode,
        key=f"canvas_{canvas_width}_{canvas_height}", # Key dinámica
    )
    
    c1, c2 = st.columns([3, 1])
    with c1:
        analyze_btn = st.button("ANALIZAR CONCEPTO")
    with c2:
        if st.button("BORRAR TODO", key="reset_btn"):
            st.rerun()

with col_ai:
    st.subheader("Interpretación IA")
    
    with st.expander("Resultados del Análisis", expanded=True):
        info_area = st.empty()
        
        if analyze_btn:
            if not api_key:
                st.warning("Configura tu API Key en el panel lateral.")
            elif canvas_result.image_data is not None:
                with st.spinner("La IA está analizando tu boceto..."):
                    try:
                        img_arr = np.array(canvas_result.image_data)
                        img_obj = Image.fromarray(img_arr.astype('uint8'), 'RGBA')
                        img_obj.save("temp_idea.png")
                        
                        b64_img = encode_image("temp_idea.png")
                        
                        client = OpenAI(api_key=api_key)
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Describe brevemente este dibujo en español y sugiere cómo mejorarlo desde el diseño interactivo."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_img}"}}
                                ]
                            }]
                        )
                        
                        full_txt = response.choices[0].message.content
                        info_area.markdown(f"<div class='result-box'>{full_txt}</div>", unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.info("Dibuja algo antes de analizar.")
        else:
            info_area.write("Tu análisis aparecerá aquí.")

st.markdown("<br><center><p style='opacity: 0.5;'>SketchMind v4.0 | Creado para el diseño interactivo</p></center>", unsafe_allow_html=True)
