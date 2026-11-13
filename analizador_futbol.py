import streamlit as st
from openai import OpenAI

# 1. Configuración inicial (Lo que ya tenías)
st.set_page_config(page_title="Titan Football AI", page_icon="⚽", layout="wide")

# Ocultar menús
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 2. Conexión segura a DeepSeek
# Usamos st.secrets para leer el token que guardaste en la nube
try:
    api_key = st.secrets["DEEPSEEK_TOKEN"]
    # DeepSeek usa la misma librería que OpenAI
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
except Exception as e:
    st.error(f"Error de configuración: Asegúrate de tener DEEPSEEK_TOKEN en los Secrets. Detalle: {e}")
    st.stop() # Detiene la app si no hay clave, evitando pantallas negras

# 3. Interfaz de usuario
st.title("⚽ Analizador de Fútbol IA")
st.write("Ingresa los datos del partido para generar un análisis profundo.")

col1, col2 = st.columns(2)
with col1:
    equipo_local = st.text_input("Equipo Local", placeholder="Ej: Real Madrid")
with col2:
    equipo_visitante = st.text_input("Equipo Visitante", placeholder="Ej: Barcelona")

# 4. Botón de acción y llamado a la IA
if st.button("Generar Análisis", type="primary"):
    if not equipo_local or not equipo_visitante:
        st.warning("Por favor, escribe el nombre de ambos equipos.")
    else:
        with st.spinner("Analizando tácticas, estadísticas y jugadores..."):
            try:
                # Llamada a la API de DeepSeek
                respuesta = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "Eres un analista experto de fútbol. Da pronósticos tácticos, estadísticas y posibles resultados."},
                        {"role": "user", "content": f"Analiza el partido entre {equipo_local} y {equipo_visitante}."}
                    ]
                )
                # Mostrar el resultado
                st.success("¡Análisis completado!")
                st.markdown(respuesta.choices[0].message.content)
                
            except Exception as e:
                # Si hay un error con la API, se muestra aquí y no se congela la pantalla
                st.error(f"Hubo un error al conectar con DeepSeek: {e}")
