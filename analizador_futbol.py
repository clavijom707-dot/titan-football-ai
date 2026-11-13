import streamlit as st
import json
import urllib.request
import urllib.parse
import datetime
from openai import OpenAI

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Titan Football AI PRO", page_icon="⚽", layout="wide", initial_sidebar_state="collapsed")

# --- SISTEMA DE LOGIN SENCILLO ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_name = None

def login():
    st.title("🔒 Iniciar Sesión - Titan Football")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.button("Login", use_container_width=True):
            if username == st.secrets.get("ADMIN_USER") and password == st.secrets.get("ADMIN_PASS"):
                st.session_state.logged_in = True
                st.session_state.user_role = "admin"
                st.session_state.user_name = "Dueño (Admin)"
                st.rerun()
            elif username == st.secrets.get("CLIENTE_USER") and password == st.secrets.get("CLIENTE_PASS"):
                st.session_state.logged_in = True
                st.session_state.user_role = "cliente"
                st.session_state.user_name = "Cliente Afiliado"
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")

if not st.session_state.logged_in:
    login()
    st.stop() # Detiene la app aquí si no hay login

# --- DISEÑO VISUAL DEFINITIVO ---
st.markdown("""
    <style>
    [data-testid="stHeader"] { background-color: #0e1117 !important; background: #0e1117 !important; }
    [data-testid="stToolbar"] {display: none !important;}
    .stDeployButton {display: none !important;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="collapsedControl"], [data-testid="stSidebarCollapsedControl"] { display: block !important; visibility: visible !important; position: fixed !important; left: 15px !important; top: 15px !important; background-color: transparent !important; border: none !important; padding: 0px !important; z-index: 9999999 !important; }
    [data-testid="stSidebarCollapseButton"] { background-color: transparent !important; border: none !important; }
    [data-testid="stSidebarCollapseButton"] > div { background-color: transparent !important; border: none !important; }
    [data-testid="collapsedControl"] svg, [data-testid="stSidebarCollapsedControl"] svg, [data-testid="stSidebarCollapseButton"] svg { fill: #00ff87 !important; color: #00ff87 !important; width: 24px !important; height: 24px !important; }
    html, body, [data-testid="stAppViewContainer"], .stApp { background-color: #0e1117 !important; color: #ffffff !important; }
    h1, h2, h3, p, span, label { color: #ffffff !important; font-family: 'Helvetica Neue', sans-serif; }
    .big-title { font-size: 3.5rem; font-weight: 900; color: #00ff87 !important; text-align: center; margin-bottom: 0; }
    .sub-title { font-size: 1.2rem; color: #a0aab5 !important; text-align: center; margin-bottom: 30px; }
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"], .stNumberInput input { background-color: #1e2530 !important; color: #ffffff !important; border: 1px solid #00ff87 !important; border-radius: 8px !important; }
    ul[data-testid="stSelectboxVirtualDropdown"] { background-color: #1e2530 !important; }
    li[role="option"] { color: #ffffff !important; }
    li[role="option"]:hover { background-color: #00ff87 !important; color: #0e1117 !important; }
    .stButton > button { background-color: #00ff87 !important; color: #0e1117 !important; font-weight: bold !important; font-size: 1.2rem !important; border-radius: 8px !important; width: 100% !important; border: none !important; }
    .stButton > button:hover { background-color: #00cc6a !important; color: #0e1117 !important; border: none !important; }
    [data-testid="stSidebar"] { background-color: #161b22 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { font-size: 1.2rem; font-weight: bold; color: #ffffff; }
    .stTabs [aria-selected="true"] { color: #00ff87 !important; border-bottom-color: #00ff87 !important; }
    .contexto-box { background-color: #1e2530; border: 1px solid #00ff87; border-radius: 8px; padding: 10px 15px; margin-bottom: 15px; font-size: 0.9rem; color: #a0aab5 !important; }
    .sidebar-info { background-color: #1e2530; border-radius: 8px; padding: 10px; color: #a0aab5 !important; font-size: 0.9rem; }
    .stAlert > div { background-color: #1e2530 !important; color: #00ff87 !important; border: 1px solid #00ff87 !important; }
    .stAlert p { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# --- SEGURIDAD IA ---
try:
    api_key = st.secrets["DEEPSEEK_TOKEN"]
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
except Exception as e:
    st.error("🚨 Error crítico: No se encontró DEEPSEEK_TOKEN en los Secrets de Streamlit.")
    st.stop()

# --- MEMORIA ---
if "historial" not in st.session_state: st.session_state.historial = []
if "consultas" not in st.session_state: st.session_state.consultas = 0
if "ultimo_analisis" not in st.session_state: st.session_state.ultimo_analisis = None
if "partidos_liga" not in st.session_state: st.session_state.partidos_liga = []
if "liga_actual" not in st.session_state: st.session_state.liga_actual = "LigaPro (Ecuador)"
if "tokens_totales" not in st.session_state: st.session_state.tokens_totales = 0 

LIGAS_ESPN = {
    "LigaPro (Ecuador)": "ecu.1", "Champions League": "uefa.champions",
    "LaLiga (España)": "esp.1", "Premier League (Inglaterra)": "eng.1",
    "Serie A (Italia)": "ita.1", "Bundesliga (Alemania)": "ger.1",
    "Liga MX (México)": "mex.1", "MLS (EE.UU.)": "usa.1"
}

# --- FUNCIONES --- 
def buscar_noticias_reales(equipo, liga):
    query = urllib.parse.quote(f"{equipo} futbol {liga}")
    url = f"https://news.google.com/rss/search?q={query}&hl=es-419&gl=US&ceid=US:es-419"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml = response.read().decode('utf-8')
            titulares = []
            start = 0
            for _ in range(3):
                start = xml.find('<title>', start)
                if start == -1: break
                end = xml.find('</title>', start)
                titulo = xml[start+7:end].replace('<![CDATA[', '').replace(']]>', '')
                if "Google News" not in titulo: titulares.append(titulo)
                start = end
            return " | ".join(titulares) if titulares else "No hay noticias de última hora."
    except Exception: return "Servicio de noticias no disponible."

def obtener_partidos_liga(slug_liga):
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug_liga}/scoreboard?limit=100"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            partidos = []
            meses = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun", 7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
            for ev in data.get("events", []):
                competencias = ev.get("competitions", [])
                if competencias:
                    competidores = competencias[0].get("competitors", [])
                    if len(competencias[0].get("competitors", [])) == 2:
                        eq1 = competencias[0].get("competitors", [])[0].get("team", {}).get("displayName", "TBD")
                        eq2 = competencias[0].get("competitors", [])[1].get("team", {}).get("displayName", "TBD")
                        fecha_str = ev.get("date", "")
                        hora_formateada = "Hora TBD"
                        timestamp = 0
                        if fecha_str:
                            try:
                                dt = datetime.datetime.fromisoformat(fecha_str.replace("Z", "+00:00"))
                                dt_ec = dt - datetime.timedelta(hours=5)
                                hora_formateada = f"{dt_ec.day} {meses[dt_ec.month]} - {dt_ec.strftime('%H:%M')}"
                                timestamp = dt.timestamp()
                            except: pass
                        partidos.append({"local": eq1, "visitante": eq2, "fecha_hora": hora_formateada, "timestamp": timestamp})
            partidos.sort(key=lambda x: x['timestamp'])
            return partidos
    except Exception: return None

def analizar_con_ia(equipo_local, equipo_visitante, liga, contexto, modo_kalshi):
    noticias_local = buscar_noticias_reales(equipo_local, liga)
    noticias_visitante = buscar_noticias_reales(equipo_visitante, liga)
    
    # RESTAURADO: Prompts completos
    if modo_kalshi:
        system_prompt = """
        Eres un analista experto en mercados de predicción (Kalshi). 
        Responde con este formato exacto:
        📊 **Probabilidad Estimada:** [Ej: Local 45% | Empate 30% | Visitante 25%]
        🎯 **Recomendación de Contrato:** [Ej: Comprar SÍ al Local, o Comprar NO, o No operar]
        🔍 **Análisis Táctico:** [Explica en 3 líneas por qué crees que pasará esto]
        💡 **Value Bet (Kalshi):** [Dime si el precio en centavos está infravalorando alguna probabilidad].
        """
    else:
        system_prompt = """
        Eres un analista experto en fútbol y apuestas deportivas para el mercado latinoamericano (como Bet593, Betcris).
        Responde con este formato exacto:
        📊 **Probabilidad del Partido:** [Ej: Local 45% | Empate 30% | Visitante 25%]
        🎯 **Apuesta Recomendada:** [Ej: Gana Local, Doble Oportunidad, Más de 2.5 goles, o No apostar]
        🔍 **Análisis Táctico:** [Explica en 3 líneas por qué crees que pasará esto]
        💡 **Value Bet (Cuota con valor):** [Dime si la cuota de la casa de apuestas infravalora a algún equipo].
        """
    
    prompt = f"Partido: {equipo_local} vs {equipo_visitante}. Liga: {liga}. Contexto: {contexto}. Noticias {equipo_local}: {noticias_local}. Noticias {equipo_visitante}: {noticias_visitante}."
    
    try:
        respuesta = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        tokens_usados = respuesta.usage.total_tokens
        st.session_state.tokens_totales += tokens_usados 
        
        return {"noticias": noticias_local, "respuesta": respuesta.choices[0].message.content}
    except Exception as e:
        return {"noticias": "Error", "respuesta": f"La IA no pudo responder. Detalle: {e}"}

# --- BARRA LATERAL ---
with st.sidebar:
    st.write(f"👤 **{st.session_state.user_name}** ({st.session_state.user_role.upper()})")
    if st.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.user_name = None
        st.rerun()
    st.divider()
    
    if st.session_state.user_role == "admin":
        st.header("👑 Modo Dios (Admin)")
        st.write(f"**Tokens consumidos hoy:** {st.session_state.tokens_totales}")
        st.divider()

    st.header("⚙️ Panel Pro")
    st.write(f"**Tus consultas de hoy:** {st.session_state.consultas} / 5")
    if st.button("🗑️ Limpiar Historial"):
        st.session_state.historial = []
        st.session_state.ultimo_analisis = None
        st.session_state.consultas = 0
        st.session_state.partidos_liga = []
        st.rerun()
    st.divider()
    st.write("### 📊 Historial de Análisis")
    if not st.session_state.historial: 
        st.markdown('<div class="sidebar-info">Aún no has analizado ningún partido.</div>', unsafe_allow_html=True)
    else:
        for item in reversed(st.session_state.historial): st.write(f"• {item['local']} vs {item['visitante']} ({item['hora']})")

# --- ENCABEZADO Y PESTAÑAS ---
st.markdown('<p class="big-title">⚽ Titan Football AI PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">El centro de mando definitivo para el aficionado.</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🧠 Analizador IA", "📺 Marcadores en Vivo (ESPN)"])

with tab1:
    liga_seleccionada = st.selectbox("Selecciona una liga para ver los próximos partidos:", list(LIGAS_ESPN.keys()))
    
    if liga_seleccionada != st.session_state.liga_actual:
        st.session_state.liga_actual = liga_seleccionada
        st.session_state.partidos_liga = []
    
    if st.button("🔍 Buscar Próximos Partidos"):
        with st.spinner(f"Buscando encuentros de {liga_seleccionada}..."):
            resultados = obtener_partidos_liga(LIGAS_ESPN[liga_seleccionada])
            if resultados is None:
                st.session_state.partidos_liga = []
                st.error("⚠️ Los servidores de ESPN están saturados o sin conexión. Escribe los equipos manualmente abajo.")
            elif len(resultados) == 0:
                st.session_state.partidos_liga = []
                st.info(f"No se encontraron partidos programados para {liga_seleccionada}.")
            else:
                st.session_state.partidos_liga = resultados
                st.success(f"¡Se encontraron {len(resultados)} partidos!")

    partido_seleccionado = None
    if st.session_state.partidos_liga:
        opciones = [f"{p['local']} vs {p['visitante']} ({p['fecha_hora']})" for p in st.session_state.partidos_liga]
        partido_seleccionado = st.selectbox("Selecciona el partido a analizar:", opciones)

    col1, col2 = st.columns(2)
    with col1:
        local_default = st.session_state.partidos_liga[opciones.index(partido_seleccionado)]['local'] if partido_seleccionado else ""
        equipo_local = st.text_input("Equipo Local", value=local_default, placeholder="Ej: Barcelona SC")
    with col2:
        visitante_default = st.session_state.partidos_liga[opciones.index(partido_seleccionado)]['visitante'] if partido_seleccionado else ""
        equipo_visitante = st.text_input("Equipo Visitante", value=visitante_default, placeholder="Ej: Emelec")

    contexto_extra = st.text_area("Contexto Adicional (Opcional)", placeholder="Ej: Juegan en el Capwell, clima lluvioso...")
    modo_kalshi = st.checkbox("💡 Activar Modo Kalshi (Análisis para Mercados de Predicción)")

    if st.button("🧠 ANALIZAR PARTIDO"):
        if st.session_state.consultas >= 5:
            st.error("🚨 Límite de 5 análisis gratuitos alcanzado.")
        elif equipo_local and equipo_visitante:
            with st.spinner("Buscando noticias reales y analizando tácticas..."):
                resultado_ia = analizar_con_ia(equipo_local, equipo_visitante, liga_seleccionada, contexto_extra, modo_kalshi)
                st.session_state.ultimo_analisis = {
                    "local": equipo_local, "visitante": equipo_visitante,
                    "noticias": resultado_ia["noticias"], "respuesta": resultado_ia["respuesta"], "liga": liga_seleccionada
                }
                hora_actual = datetime.datetime.now().strftime("%H:%M")
                st.session_state.historial.append({"local": equipo_local, "visitante": equipo_visitante, "hora": hora_actual})
                st.session_state.consultas += 1
        else:
            st.warning("Por favor, ingresa el nombre de ambos equipos.")

    if st.session_state.ultimo_analisis:
        res = st.session_state.ultimo_analisis
        with st.container(border=True):
            st.markdown(f"### 🏆 {res['local']} vs {res['visitante']} ({res['liga']})")
            st.markdown(f'''
                <div class="contexto-box">
                    📰 <b>Contexto leído de las noticias:</b> {res['noticias'][:150]}...
                </div>
            ''', unsafe_allow_html=True)
            st.markdown(res['respuesta'])
        
        # RESTAURADO: Calculadora de Value Bet
        st.markdown("---")
        st.subheader("🧮 Calculadora de Value Bet (Bet593 / Betcris)")
        st.write("Ingresa los datos de tu casa de apuestas para saber si hay valor.")
        
        col_calc1, col_calc2 = st.columns(2)
        with col_calc1:
            cuota_casa = st.number_input("Cuota de la casa (Ej: 2.10)", min_value=1.01, value=2.00, step=0.01)
        with col_calc2:
            prob_ia = st.number_input("Probabilidad según IA (%) (Ej: 55)", min_value=1, max_value=100, value=50, step=1)
        
        if st.button("💰 Calcular si hay Valor"):
            prob_implicita = 100 / cuota_casa
            st.write(f"**Probabilidad implícita de la casa:** {prob_implicita:.1f}%")
            st.write(f"**Probabilidad estimada por la IA:** {prob_ia}%")
            
            if prob_ia > prob_implicita:
                st.success(f"✅ ¡HAY VALOR! La IA dice que la probabilidad real es mayor ({prob_ia}%) a la que paga la casa ({prob_implicita:.1f}%). ¡Apostar!")
            else:
                st.error(f"❌ NO HAY VALOR. La casa paga menos ({prob_implicita:.1f}%) de lo que realmente debería ser ({prob_ia}%). No apuestes.")

with tab2:
    st.subheader("🏆 UEFA Champions League (En Vivo / Próximos)")
    partidos_champions = obtener_partidos_liga("uefa.champions")
    if partidos_champions is None:
        st.error("⚠️ Los servidores de ESPN están caídos en este momento.")
    elif not partidos_champions:
        st.info("No hay partidos programados para hoy.")
    else:
        for partido in partidos_champions:
            st.info(f"**{partido['local']} vs {partido['visitante']}** | {partido['fecha_hora']}")
