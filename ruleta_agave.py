import streamlit as st
import plotly.graph_objects as go
import random
import time
import pandas as pd
import datetime
import os

# Configuración inicial
st.set_page_config(page_title="Ruleta Agave", layout="centered")

# Estilos CSS para el diseño terracota y animaciones
st.markdown("""
    <style>
    .stApp { background-color: #C06C4C !important; }
    h1 { color: white !important; text-align: center; font-weight: bold; }
    .premio-final { 
        background-color: #2D55A6; color: white; padding: 40px; 
        border-radius: 20px; text-align: center; font-size: 30px; margin-top: 20px;
        border: 4px solid white; animation: zoomIn 0.5s;
    }
    .perdedor { background-color: #8B0000; color: #FFD700; border: 4px solid #FFD700; }
    @keyframes zoomIn { from {transform: scale(0.5); opacity: 0;} to {transform: scale(1); opacity: 1;} }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎡 RULETA AGAVE</h1>", unsafe_allow_html=True)

# Lógica de datos (Registro)
ARCHIVO_DATOS = "datos_clientes.csv"
if not os.path.exists(ARCHIVO_DATOS):
    pd.DataFrame(columns=["email", "fecha_hora", "premio"]).to_csv(ARCHIVO_DATOS, index=False)

def guardar_giro(email, premio):
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fecha_solo = str(datetime.date.today())
    nuevo_registro = pd.DataFrame({"email": [email], "fecha_hora": [fecha_hora], "premio": [premio]})
    df = pd.read_csv(ARCHIVO_DATOS)
    df = pd.concat([df, nuevo_registro], ignore_index=True)
    df.to_csv(ARCHIVO_DATOS, index=False)

# Captura de Email
email = st.text_input("ESCRIBE TU EMAIL PARA JUGAR:")
if not email:
    st.stop() 

# Validación diaria
df = pd.read_csv(ARCHIVO_DATOS)
hoy = str(datetime.date.today())
if not df[df["email"] == email].empty:
    registros_hoy = df[(df["email"] == email) & (df["fecha_hora"].str.contains(hoy))]
    if not registros_hoy.empty:
        st.error("⚠️ Ya participaste hoy. ¡Te esperamos mañana!")
        st.stop()

# Ruleta
premios_display = ["Taco Dulce", "Margarita Frozen", "Pinta de Cerveza", "No estas de suerte", 
                   "10% de Descuento", "Taco Dulce ", "La proxima sera", "¡Margarita Frozen! "]
container = st.empty()

def dibujar_ruleta(rotacion=0):
    fig = go.Figure(data=[go.Pie(
        labels=premios_display, values=[1]*8, 
        marker_colors=['#D9C3A6', '#2D55A6'] * 4,
        textinfo='label', textfont_size=14, rotation=rotacion,
        marker=dict(line=dict(color='white', width=3))
    )])
    fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0))
    return fig

with container.container():
    st.plotly_chart(dibujar_ruleta(), use_container_width=True, key="ruleta_ini")

if st.button("¡GIRAR RULETA!"):
    for i in range(20):
        with container.container():
            st.plotly_chart(dibujar_ruleta(i * 30), use_container_width=True, key=f"giro_{i}")
        time.sleep(0.05)
    
    resultado = random.choice([p.strip() for p in premios_display])
    container.empty()
    guardar_giro(email, resultado)
    
    if resultado in ["No estas de suerte", "La proxima sera"]:
        st.markdown(f"<div class='premio-final perdedor'>✨ ¡Casi sale! ✨<br>{resultado.upper()}<br><br><span style='font-size: 18px;'>¡No te desanimes, la próxima será tuya!</span></div>", unsafe_allow_html=True)
    else:
        st.balloons()
        st.markdown(f"<div class='premio-final'>🎉 ¡FELICIDADES! 🎉<br>Ganaste: {resultado.upper()}<br><br><span style='font-size: 18px;'>Muestra esta pantalla al camarero.</span></div>", unsafe_allow_html=True)
