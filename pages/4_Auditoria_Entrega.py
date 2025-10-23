# Propósito: Página de Streamlit con un checklist de auditoría de seguridad.
import streamlit as st

st.set_page_config(page_title="Auditoría de Entrega", page_icon="📋")
st.title("📋 Checklist de Auditoría de Entrega Segura")
st.markdown(
    """
    Antes de lanzar un producto IoT, es crucial realizar una auditoría de seguridad.
    Este checklist (no exhaustivo) cubre los puntos vulnerables más comunes
    demostrados en esta aplicación.
    """
)

st.header("Hardware y Acceso Físico")
st.checkbox("Puertos de depuración (UART, JTAG) están deshabilitados en el firmware de producción.", value=False, key="h1")
st.checkbox("El hardware está protegido contra la extracción fácil del firmware (ej. 'epoxy blob').", value=False, key="h2")

st.header("Red y Comunicación")
st.checkbox("Toda la comunicación de red (MQTT, HTTP) utiliza cifrado (TLS).", value=False, key="r1")
st.checkbox("El broker MQTT requiere autenticación robusta (usuario/contraseña o certificados).", value=True, key="r2")
st.checkbox("Los tópicos MQTT siguen un control de acceso (ACL) estricto (ej. el dispositivo 'A' no puede leer/escribir en el tópico del dispositivo 'B').", value=False, key="r3")
st.checkbox("No se utilizan servicios inseguros (Telnet, FTP). Se prefiere SSH con claves.", value=True, key="r4")

st.header("Firmware y Software")
st.checkbox("No existen contraseñas, claves API o secretos hardcodeados en el binario.", value=False, key="f1")
st.checkbox("Todas las contraseñas de administrador por defecto (ej. 'admin', 'root') deben ser cambiadas por el usuario en la primera configuración.", value=True, key="f2")
st.checkbox("Se utiliza un 'booteo seguro' (Secure Boot) para verificar la firma del firmware.", value=False, key="f3")
st.checkbox("Se implementa un mecanismo de actualización de firmware segura (OTA) (firmware firmado).", value=False, key="f4")

st.header("Datos")
st.checkbox("Los datos sensibles del usuario se almacenan cifrados en el dispositivo.", value=False, key="d1")
st.checkbox("Se utiliza un registro de integridad (como una blockchain simulada) para auditorías críticas.", value=False, key="d2")

st.info("Usa este checklist para evaluar los riesgos en las simulaciones anteriores.")
