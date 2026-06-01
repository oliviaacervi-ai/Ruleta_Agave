import streamlit as st
import plotly.graph_objects as go
import random
import time
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Ruleta Agave", layout="centered")

# --- DISEÑO ---
st.markdown("""
    <style>
    .stApp { background-color: #C06C4C !important; }
    h1 { color: white !important; text-align: center; font-weight: bold; }
    .premio-final { 
        background-color: #2D55A6; color: white; padding: 40px; 
        border-radius: 20px; text-align: center; font-size: 30px; margin-top: 20px;
        border: 4px solid white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎡 RULETA AGAVE</h1>", unsafe_allow_html=True)

# --- VALIDACIÓN MAIL ---
email = st.text_input("ESCRIBE TU EMAIL PARA JUGAR:")
if not email:
    st.stop()

# --- LÓGICA DE RULETA ---
premios_display = ["Taco Dulce", "Margarita Frozen", "Pinta de Cerveza", "No estas de suerte", 
                   "10% de Descuento", "Taco Dulce ", "La proxima sera", "¡Margarita Frozen! "]

container = st.empty()

def dibujar_ruleta(rotacion=0):
    fig = go.Figure(data=[go.Pie(labels=premios_display, values=[1]*8, marker_colors=['#D9C3A6', '#2D55A6'] * 4, rotation=rotacion)])
    fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0))
    return fig

# --- BOTÓN CENTRADO (ARRIBA DE LA RULETA) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    btn_girar = st.button("¡GIRAR RULETA!")

# Mostrar ruleta inicial
with container.container():
    st.plotly_chart(dibujar_ruleta(), use_container_width=True)

# Acción de giro
if btn_girar:
    for i in range(20):
        with container.container():
            st.plotly_chart(dibujar_ruleta(i * 30), use_container_width=True)
        time.sleep(0.05)
    
    resultado = random.choice([p.strip() for p in premios_display])
    container.empty()
    st.markdown(f"<div class='premio-final'>🎉 GANASTE: {resultado.upper()} 🎉</div>", unsafe_allow_html=True)
