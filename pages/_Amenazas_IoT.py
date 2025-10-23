# Propósito: Página de Streamlit para demostrar amenazas comunes de IoT (UART/MQTT).
import streamlit as st
import time
from core.uart_sim import UARTSimulator
from core.mqtt_sim import GLOBAL_BROKER
import json

st.set_page_config(page_title="Amenazas IoT", page_icon="📡")
st.title("📡 Simulación de Amenazas Comunes en IoT")
st.markdown("Demostración de *sniffing* de comunicación y tráfico inseguro.")

# Inicializar simuladores
if "uart_sim" not in st.session_state:
    st.session_state.uart_sim = UARTSimulator()

# Limpiar el broker simulado al cargar la página
GLOBAL_BROKER.clear_log()

tab1, tab2 = st.tabs(["Sniffing de Hardware (UART)", "Sniffing de Red (MQTT)"])

with tab1:
    st.header("Simulación de Sniffing de UART")
    st.markdown(
        """
        Los dispositivos IoT a menudo exponen un puerto serie (UART) para depuración.
        Si no está deshabilitado en producción, un atacante con acceso físico
        puede "escuchar" (sniff) la comunicación o incluso enviar comandos.
        """
    )
    
    if st.button("Iniciar Sniffing de UART (5 segundos)"):
        with st.spinner("Escuchando puerto UART simulado..."):
            log_output = st.session_state.uart_sim.read_data_stream(duration_seconds=5)
            
            st.subheader("Resultados del Sniffing:")
            code_output = ""
            found_vuln = False
            for line in log_output:
                code_output += line + "\n"
                if "PASS:" in line or "MyPass" in line:
                    st.warning(f"¡Vulnerabilidad Encontrada! Credenciales expuestas: `{line}`")
                    found_vuln = True
            
            st.code(code_output, language="text")
            if not found_vuln:
                st.success("No se detectaron credenciales en este lote (intenta de nuevo).")
        st.success("Sniffing simulado completado.")

with tab2:
    st.header("Simulación de Tráfico MQTT Inseguro")
    st.markdown(
        """
        MQTT es un protocolo común en IoT. Si no está configurado con TLS y
        autenticación robusta, un atacante en la misma red puede suscribirse
        a tópicos sensibles (como `#` para todos los tópicos) y robar datos.
        """
    )
    
    if st.button("Simular Tráfico de Dispositivos MQTT"):
        with st.spinner("Simulando publicaciones MQTT..."):
            GLOBAL_BROKER.publish("device/123/temp", json.dumps({"t": 25.4}))
            time.sleep(0.5)
            GLOBAL_BROKER.publish("device/123/humidity", json.dumps({"h": 60.1}))
            time.sleep(0.5)
            # Publicación insegura (simulada automáticamente por el broker)
            GLOBAL_BROKER.publish("device/456/config/set", json.dumps({"ssid": "new_net"}))
            time.sleep(0.5)
            GLOBAL_BROKER.publish("device/789/status", "ONLINE")
        
        st.success("Tráfico simulado.")
        
    st.subheader("Log del Broker (Visión del Atacante)")
    log = GLOBAL_BROKER.get_log()
    if not log:
        st.info("No hay tráfico en el log. Presiona el botón para simular.")
    else:
        # Mostrar el log como JSON
        log_data = []
        for msg in log:
            log_data.append({
                "timestamp": f"{msg['timestamp']:.2f}",
                "topic": msg['topic'],
                "payload": msg['payload']
            })
        st.json(log_data)
        
        # Buscar vulnerabilidades
        found_vuln = False
        for msg in log:
            if "credentials" in msg["topic"]:
                st.error(f"¡Vulnerabilidad Crítica! Credenciales publicadas en el tópico: `{msg['topic']}`")
                st.json(msg['payload'])
                found_vuln = True
        
        if not found_vuln:
            st.success("No se detectaron credenciales hardcodeadas en este lote.")
