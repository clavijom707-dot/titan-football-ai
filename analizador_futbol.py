import streamlit as st
from openai import OpenAI

# 1. Configuración de la página (Debe ser lo primero)
st.set_page_config(page_title="Titan Football AI", page_icon="⚽", layout="wide")

# 2. Estilos CSS para el diseño oscuro y elegante
st.markdown("""
    <style>
    /* Fondo general oscuro */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Ocultar menús de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Estilo del título principal */
    .titulo-principal {
        text-align: center;
        color: #00ffcc;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0px;
    }
    
    .subtitulo {
        text-align: center;
        color: #a0a0a0;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }

    /* Cuadros de texto */
    .stTextInput>div>div>input {
        background-color: #1e2130;
        color: white;
        border: 1px solid #00ffcc;
        border-radius: 8px;
    }
    
    /* Botón principal */
    .stButton>button {
        background-color: #00ffcc;
        color: black;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        height: 50px;
        font-size: 1.2rem;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00ccaa;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Conexión segura a DeepSeek
try:
    api_key = st.secrets["DEEPSEEK_TOKEN"]
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
except Exception as e:
    st.error(f"Error de configuración: Falta DEEPSEEK_TOKEN en los Secrets de Streamlit.")
    st.stop()

# 4. Interfaz visual de usuario
st.markdown('<div class="titulo-principal">⚽ Titan Football AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Ingresa los equipos para generar un análisis táctico profundo con Inteligencia Artificial.</div>', unsafe_allow_html=True)

# Columnas para los equipos
col1, col2 = st.columns(2)
with col1:
    equipo_local = st.text_input("🏠 Equipo Local", placeholder="Ej: Real Madrid")
with col2:
    equipo_visitante = st.text_input("✈️ Equipo Visitante", placeholder="Ej: Barcelona")

st.markdown("<br>", unsafe_allow_html=True)

# 5. Botón de acción y llamado a la IA
if st.button("GENERAR ANÁLISIS TÁCTICO"):
    if not equipo_local or not equipo_visitante:
        st.warning("Por favor, escribe el nombre de ambos equipos.")
    else:
        with st.spinner("Analizando tácticas, estadísticas y jugadores..."):
            try:
                # Llamada a la API de DeepSeek
                respuesta = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "Eres un analista experto de fútbol. Da pronósticos tácticos, estadísticas y posibles resultados. Usa un tono profesional."},
                        {"role": "user", "content": f"Analiza el partido entre {equipo_local} y {equipo_visitante}."}
                    ]
                )
                
                # Mostrar el resultado con éxito
                st.success("¡Análisis completado!")
                st.markdown("---")
                st.markdown(respuesta.choices[0].message.content)
                
            except Exception as e:
                # Si hay un error con la API, se muestra aquí y no se congela la pantalla
                st.error(f"Hubo un error al conectar con DeepSeek: {e}")
