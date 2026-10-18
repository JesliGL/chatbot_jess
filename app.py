import os
import google.generativeai as genai
import streamlit as st

# -------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA (DUA: Accesible, claro y estructurado)
# -------------------------------------------------------------------
st.set_page_config(
    page_title="ChatbotJESS - Tutora de Ciencias Naturales",
    page_icon="💫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados para la barra lateral, títulos y avatares grandes
st.markdown("""
    <style>
    /* Ocultar barra superior por defecto de Streamlit */
    header {visibility: hidden;}

    /* Estilo para la barra lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #f0f4f9;
        padding-top: 1rem;
    }

    /* Agrandar SOLO la foto del avatar sin apretar el texto del mensaje */
    [data-testid="stChatMessageAvatar"] img {
        width: 65px !important;
        height: 65px !important;
        max-width: 65px !important;
        max-height: 65px !important;
        border-radius: 50% !important;
        object-fit: cover !important;
    }

    /* Ajustar el alineamiento vertical del chat */
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
# BARRA LATERAL (SIDEBAR - IZQUIERDA CON LA TUTORA)
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
# CONTENIDO PRINCIPAL (DERECHA)
# -------------------------------------------------------------------

# Título principal con la estrella animada
st.markdown('<h1><span class="shooting-star-icon">💫</span> ChatbotJESS: Tutora de Ciencias Naturales</h1>', unsafe_allow_html=True)
st.caption("Asistente educativo con IA para 8.º de EGB Superior | Nivel: Cadenas Alimenticias y Redes Tróficas")

# Advertencia DUA y Contrato Pedagógico visible para el estudiante
with st.expander("ℹ️ Información importante y reglas de uso (Transparencia)"):
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
- Usa párrafos cortos, viñetas, negritas y emojis para facilitar la lectura y comprensión multimodal.

RESTRICCIÓN DE LONGITUD DE RESPUESTA:
- Cada respuesta debe ser breve y concisa, de MÁXIMO 100 PALABRAS por interacción.

REGLAS ACCIONABLES DEL CONTRATO PEDAGÓGICO:
1. RECHAZAR Y NO DAR SOLUCIONES DIRECTAS: Jamás des la clasificación resuelta, la lista completa ni la tarea hecha. Si te piden la respuesta, rechaza amablemente indicando que tu función es enseñarle a razonar.
2. PREGUNTAR Y DAR PISTAS: Ante dudas sobre la función o impacto de una especie, ofrece una PISTA simple sobre la dieta u origen de energía (ej. "¿De dónde obtiene su energía una planta?").
3. EXPLICAR ERRORES: Si el estudiante se equivoca, explica el concepto de manera sencilla y sin desanimarlo.
4. MANEJAR AMBIGÜEDADES / DERIVAR AL DOCENTE: Si el estudiante responde con ambigüedad repetida o muestra confusión constante, indícale amablemente que debe consultar directamente con su docente para revisar la ruta de aprendizaje.
5. CIERRE OBLIGATORIO: Toda interacción DEBE terminar con una pregunta abierta reflexiva para hacer pensar al estudiante.
6. CIENTIFICIDAD Y FUENTES: Basado exclusivamente en ecología real (SciELO, Redalyc, Scopus). Si solicita fuentes o justificaciones científicas, cita artículos/libros ecológicos reales con su código DOI o autor real.
7. SIN ESPECIES FICTICIAS: No inventes seres vivos irreales.
"""

# -------------------------------------------------------------------
# AUTENTICACIÓN Y CONFIGURACIÓN DE GEMINI API
# -------------------------------------------------------------------
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.sidebar.header("🔐 Configuración de la API")
    api_key = st.sidebar.text_input("Ingresa tu Gemini API Key aquí:", type="password")
    st.sidebar.info("Obtén tu clave gratuita en Google AI Studio para activar a ChatbotJESS.")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)

    # Inicializar historial
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "¡Hola! 👋 Soy **ChatbotJESS**, tu tutora de Ciencias Naturales. ¿Qué ejemplo o caso de cadena alimenticia estás analizando hoy?",
            }
        ]

    # Mostrar mensajes del historial con avatar correcto
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
