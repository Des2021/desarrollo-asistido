# Propósito: Punto de entrada principal y página de bienvenida de la app Streamlit.
import streamlit as st

st.set_page_config(
    page_title="IoT Secure App",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Aplicación de Simulación de Seguridad IoT")
st.sidebar.success("Selecciona una simulación arriba.")

st.markdown(
    """
    Bienvenido a la aplicación de simulación de seguridad en el Internet de las Cosas (IoT).
    Esta herramienta está diseñada para demostrar conceptos clave de seguridad en un
    entorno **completamente local y simulado**.

    **👈 Selecciona una de las páginas en la barra lateral** para explorar diferentes
    escenarios de seguridad:

    1.  **Amenazas IoT:** Explora vectores de ataque comunes (sniffing de UART y MQTT).
    2.  **Firmware y Contraseñas:** Simula ataques de fuerza bruta y análisis de firmware.
    3.  **Blockchain y Seguridad:** Demuestra cómo un ledger inmutable puede asegurar datos.
    4.  **Auditoría y Entrega:** Revisa un checklist de entrega segura.

    *Nota: Todas las operaciones son simulaciones locales y no se realiza ninguna
    comunicación de red real ni se descargan binarios.*
    """
)
