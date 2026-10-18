import os
import google.generativeai as genai
import streamlit as st

# -------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -------------------------------------------------------------------
st.set_page_config(
    page_title="ChatbotJESS - Tutora de Ciencias Naturales",
    page_icon="💫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    /* Ocultar barra superior por defecto de Streamlit */
    header {visibility: hidden;}

    /* Estilo para la barra lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #f0f4f9;
        padding-top: 1rem;
    }

    /* Espacio inferior para evitar solapamiento */
    .main .block-container {
        padding-bottom: 120px !important;
    }

    /* Tamaño del avatar de la tutora */
    [data-testid="stChatMessageAvatar"] img {
        width: 55px !important;
        height: 55px !important;
        border-radius: 50% !important;
        object-fit: cover !important;
    }

    /* Alineación del chat */
    [data-testid="stChatMessage"] {
        align-items: flex-start !important;
    }

    /* Animación para hacer girar la estrella */
    @keyframes spin-star {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .shooting-star-icon {
        display: inline-block;
        font-size: 2.2rem;
        animation: spin-star 6s linear infinite;
        vertical-align: middle;
        margin-right: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# BARRA LATERAL (SIDEBAR)
# -------------------------------------------------------------------
with st.sidebar:
    try:
        st.image("avatar.png", use_container_width=True)
    except:
        st.image("https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=500", use_container_width=True)
    
    st.markdown("### 🎓 ChatbotJESS")
    st.caption("Tu tutora educativa: inteligente y cercana.")
    st.divider()
    st.markdown("### 📚 Áreas de aprendizaje")
    st.markdown("🌿 **Ciencias Naturales**")
    st.markdown("🔬 Cadenas Alimenticias y Redes Tróficas")

# -------------------------------------------------------------------
# CONTENIDO PRINCIPAL
# -------------------------------------------------------------------

# Título principal con la estrella animada
st.markdown('<h1><span class="shooting-star-icon">💫</span> ChatbotJESS: Tutora de Ciencias Naturales</h1>', unsafe_allow_html=True)
st.caption("Asistente educativo con IA para 8.º de EGB Superior | Nivel: Cadenas Alimenticias y Redes Tróficas")

# Advertencia DUA (Cerrado por defecto)
with st.expander("ℹ️ Información importante y reglas de uso (Transparencia)", expanded=False):
    st.markdown("""
    - **Propósito:** Guiarte a pensar y descubrir las respuestas por ti mismo/a.
    - **Límite de la IA:** Este es un asistente conversacional basado en IA. **No dará respuestas directas de tus tareas** ni reemplaza a tu docente.
    - **Privacidad:** No ingreses nombres, apellidos completos, ni datos personales.
    - **Verificación:** Las respuestas pueden contener errores; si persisten las dudas, consulta con tu profesor/a.
    """)

# -------------------------------------------------------------------
# CONTRATO PEDAGÓGICO / SYSTEM PROMPT
# -------------------------------------------------------------------
SYSTEM_PROMPT = """
Eres ChatbotJESS, una tutora virtual de Ciencias Naturales para estudiantes de 8.º año de EGB Superior (12-13 años).
Especialidad: Niveles Tróficos, Cadenas Alimenticias y Desequilibrios Ecológicos.

ROL Y PRINCIPIOS DUA (Diseño Universal para el Aprendizaje):
- Lenguaje muy claro, amable, cercano, empático, paciente y altamente motivador.
- Usa párrafos cortos, viñetas, negritas y emojis para facilitar la lectura.

RESTRICCIÓN DE LONGITUD DE RESPUESTA:
- Cada respuesta debe ser breve y concisa, de MÁXIMO 100 PALABRAS por interacción.

REGLAS ACCIONABLES DEL CONTRATO PEDAGÓGICO:
1. RECHAZAR Y NO DAR SOLUCIONES DIRECTAS: Jamás des la clasificación resuelta ni la tarea hecha.
2. PREGUNTAR Y DAR PISTAS: Ante dudas sobre la función de una especie, ofrece una PISTA simple.
3. EXPLICAR ERRORES: Explica los conceptos de manera sencilla.
4. MANEJAR AMBIGÜEDADES: Si hay confusión constante, deriva amablemente al docente.
5. CIERRE OBLIGATORIO: Toda interacción DEBE terminar con una pregunta abierta reflexiva.
6. CIENTIFICIDAD: Basado exclusivamente en ecología real.
7. SIN ESPECIES FICTICIAS: No inventes seres vivos irreales.
"""

# -------------------------------------------------------------------
# AUTENTICACIÓN Y CONFIGURACIÓN DE GEMINI API
# -------------------------------------------------------------------
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.sidebar.header("🔐 Configuración de la API")
    api_key = st.sidebar.text_input("Ingresa tu Gemini API Key aquí:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Intentar usar el nombre de modelo actualizado de Google Gemini
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", system_instruction=SYSTEM_PROMPT)
    except Exception:
        model = genai.GenerativeModel(model_name="gemini-1.5-pro", system_instruction=SYSTEM_PROMPT)

    # Inicializar historial de conversación
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "¡Hola! 👋 Soy **ChatbotJESS**, tu tutora de Ciencias Naturales. ¿Qué ejemplo o caso de cadena alimenticia estás analizando hoy?",
            }
        ]

    # Mostrar el historial de mensajes
    for message in st.session_state.messages:
        avatar_p = "avatar.png" if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar_p):
            st.markdown(message["content"])

    # Entrada de texto del estudiante
    if prompt := st.chat_input("Escribe tu consulta o respuesta aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="avatar.png"):
            message_placeholder = st.empty()
            try:
                history_gemini = [
                    {
                        "role": "user" if m["role"] == "user" else "model",
                        "parts": [m["content"]],
                    }
                    for m in st.session_state.messages[:-1]
                ]

                chat = model.start_chat(history=history_gemini)
                response = chat.send_message(prompt)

                message_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                message_placeholder.error(f"Error al conectar con la IA: {e}")
