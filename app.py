import os
import streamlit as st
import base64
import numpy as np
import openai
from openai import OpenAI
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# --- CONFIGURACIÓN DE ESCENA ---
st.set_page_config(
    page_title="SketchMind AI | Personal Studio",
    page_icon="🎨",
    layout="wide"
)

# --- DISEÑO PREMIUM (PERSONALIZADO PARA TI) ---
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
    /* Contenedores con efecto cristal */
    div[data-testid="stExpander"], .result-box {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    /* Botón de Acción Principal */
    .stButton>button:first-child {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000 !important;
        font-weight: 800;
        border-radius: 15px;
        border: none;
        height: 3.5em;
        transition: 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    /* Botón Borrar */
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

# --- BARRA LATERAL (TU PANEL DE CONTROL) ---
with st.sidebar:
    st.title("Studio Tools")
    st.markdown("Configura tu entorno creativo.")
    
    with st.expander("Lienzo Personalizado", expanded=True):
        canvas_width = st.slider("Ancho", 400, 1000, 700, 50)
        canvas_height = st.slider("Alto", 300, 800, 450, 50)
    
    with st.expander("Estilos de Pincel", expanded=True):
        drawing_mode = st.selectbox("Herramienta", ("freedraw", "line", "rect", "circle", "transform"))
        stroke_width = st.slider("Grosor", 1, 30, 6)
        stroke_color = st.color_picker("Tinta", "#000000")
        bg_color = st.color_picker("Papel", "#FFFFFF")

    st.markdown("---")
    api_key = st.text_input("OpenAI Key", type="password", placeholder="Introduce tu clave sk-...")
    st.caption("Tus datos están seguros y no se almacenan.")

# --- INTERFAZ PRINCIPAL ---
st.title("SketchMind AI")
st.markdown("#### Convierte tus trazos en conceptos. Un espacio para tu creatividad.")

col_draw, col_ai = st.columns([1.6, 1])

with col_draw:
    # El Canvas con la lógica de tus imágenes originales
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode,
        key=f"sketch_mind_{canvas_width}", # Key dinámica para refrescar
    )
    
    # Botones de Acción
    c1, c2 = st.columns([3, 1])
    with c1:
        analyze_btn = st.button("ANALIZAR MI IDEA")
    with c2:
        if st.button("BORRAR TODO", key="reset_btn"):
            st.rerun()

with col_ai:
    st.subheader("Interpretación IA")
    
    # Panel de información que puedes colapsar (Meter y Sacar)
    with st.expander("Resultados del Análisis", expanded=True):
        info_area = st.empty()
        
        if analyze_btn:
            if not api_key:
                st.warning("Configura tu API Key en el panel de herramientas.")
            elif canvas_result.image_data is not None:
                with st.spinner("Decodificando tu creatividad..."):
                    try:
                        # Guardado y Codificación
                        img_arr = np.array(canvas_result.image_data)
                        img_obj = Image.fromarray(img_arr.astype('uint8'), 'RGBA')
                        img_obj.save("temp_idea.png")
                        
                        b64_img = encode_image("temp_idea.png")
                        
                        # Conexión con GPT-4o-mini
                        client = OpenAI(api_key=api_key)
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Analiza este boceto. Describe qué es y dame 3 ideas de cómo podría mejorar o evolucionar este concepto. Sé creativo y profesional en español."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_img}"}}
                                ]
                            }]
                        )
                        
                        # Resultado Final Estetizado
                        full_txt = response.choices[0].message.content
                        info_area.markdown(f"<div class='result-box'>{full_txt}</div>", unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Error de conexión: {e}")
            else:
                st.info("Dibuja algo en el lienzo para comenzar.")
        else:
            info_area.write("El análisis de IA aparecerá aquí.")

st.markdown("<br><center><p style='opacity: 0.5;'>SketchMind v4.0 | Tu espacio creativo digital</p></center>", unsafe_allow_html=True)
