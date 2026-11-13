import streamlit as st
from openai import OpenAI

# 1. Configuración de la página (Diseño ancho)
st.set_page_config(page_title="Titan Football AI", page_icon="⚽", layout="wide")

# 2. Estilos CSS para replicar tu diseño original (Verde neón y fondo oscuro)
st.markdown("""
    <style>
    /* Fondo general oscuro */
    .stApp {
        background-color: #0b131e;
        color: #ffffff;
    }
    
    /* Ocultar menús */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Cuadros de texto con borde verde */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #0b131e !important;
        color: #ffffff !important;
        border: 1px solid #34d399 !important;
        border-radius: 8px;
    }
    
    /* Botones verdes neón */
    .stButton>button {
        background-color: #34d399 !important; /* Color verde de tu foto */
        color: black !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
    }
    .stButton>button:hover {
        background-color: #10b981 !important;
    }
    
    /* Color del texto de los labels */
    .stTextInput label, .stTextArea label, .stCheckbox label {
        color: #ffffff !important;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Conexión a DeepSeek
try:
    api_key = st.secrets["DEEPSEEK_TOKEN"]
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
except Exception as e:
    st.error("Error: Falta DEEPSEEK_TOKEN en los Secrets.")
    st.stop()

# 4. Interfaz visual (Idéntica a tu foto)
# Botón superior (Si tenías una función para esto, agrégala después)
st.button("🔍 Buscar Próximos Partidos")

# Fila de equipos
col1, col2 = st.columns(2)
with col1:
    equipo_local = st.text_input("Equipo Local")
with col2:
    equipo_visitante = st.text_input("Equipo Visitante")

# Contexto y Modo Kalshi
contexto = st.text_area("Contexto Adicional (Opcional)")
modo_kalshi = st.checkbox("💡 Activar Modo Kalshi (Análisis para Mercados de Predicción)")

st.markdown("<br>", unsafe_allow_html=True)

# Botón de análisis principal
if st.button("🔴 ANALIZAR PARTIDO"):
    if not equipo_local or not equipo_visitante:
        st.warning("Por favor, ingresa el nombre de ambos equipos.")
    else:
        with st.spinner("Analizando el partido..."):
            try:
                # Creamos las instrucciones dependiendo de si Kalshi está activo
                system_prompt = "Eres un analista experto de fútbol. Da pronósticos tácticos, estadísticas y posibles resultados."
                
                if modo_kalshi:
                    system_prompt += " Además, eres un experto en mercados de predicción (como Kalshi). Proporciona probabilidades estimadas, valor esperado y sugerencias de trading/apuestas basadas en el partido."
                
                user_prompt = f"Analiza el partido entre {equipo_local} y {equipo_visitante}."
                if contexto:
                    user_prompt += f" Ten en cuenta este contexto adicional: {contexto}"

                # Llamada a DeepSeek
                respuesta = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                
                # Mostrar resultado
                st.success("¡Análisis completado!")
                st.markdown("---")
                st.markdown(respuesta.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Hubo un error al conectar con DeepSeek: {e}")
