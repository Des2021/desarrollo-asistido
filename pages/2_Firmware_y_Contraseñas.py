# Propósito: Página de Streamlit para simular análisis de firmware y ataques de contraseña.
import streamlit as st
import time
import hashlib
from core.fw_sim import create_dummy_firmware, analyze_firmware

st.set_page_config(page_title="Firmware y Contraseñas", page_icon="🔐")
st.title("🔐 Análisis de Firmware y Ataques de Contraseña")

tab1, tab2 = st.tabs(["Análisis de Firmware", "Simulación de Fuerza Bruta"])

with tab1:
    st.header("Análisis de Firmware en busca de Secretos")
    st.markdown(
        """
        Muchos dispositivos IoT almacenan secretos (contraseñas, claves API,
        credenciales de WiFi) directamente en el firmware en texto plano.
        Un atacante puede extraer el firmware y analizarlo.
        """
    )
    
    # Generar firmware en el session state
    if "dummy_fw" not in st.session_state:
        st.session_state.dummy_fw = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generar Firmware Vulnerable (Simulado)"):
            st.session_state.dummy_fw = create_dummy_firmware(include_vulnerability=True)
            st.success(f"Firmware simulado generado ({len(st.session_state.dummy_fw)} bytes). Listo para analizar.")
    with col2:
        if st.button("Generar Firmware Seguro (Simulado)"):
            st.session_state.dummy_fw = create_dummy_firmware(include_vulnerability=False)
            st.success(f"Firmware simulado generado ({len(st.session_state.dummy_fw)} bytes). Listo para analizar.")

    if st.session_state.dummy_fw is not None:
        st.info("Firmware cargado en memoria. Haz clic en analizar.")
        
        if st.button("Analizar Firmware Cargado"):
            with st.spinner("Ejecutando 'strings' y 'grep' simulados..."):
                results = analyze_firmware(st.session_state.dummy_fw)
            
            st.subheader("Resultados del Análisis:")
            st.write(f"Tamaño total: {results['total_size']} bytes")
            
            if results["passwords"]:
                st.error("¡SECRETOS ENCONTRADOS! (Contraseñas)")
                st.json(results["passwords"])
            else:
                st.success("No se encontraron contraseñas hardcodeadas.")
                
            if results["keys"]:
                st.error("¡SECRETOS ENCONTRADOS! (Claves API)")
                st.json(results["keys"])
            else:
                st.success("No se encontraron claves API hardcodeadas.")
            
            if results["ssids"]:
                st.warning("Información encontrada (SSIDs)")
                st.json(results["ssids"])

with tab2:
    st.header("Simulación de Ataque de Fuerza Bruta")
    st.markdown(
        """
        Si un atacante captura un hash de contraseña (de una base de datos o
        del firmware), puede usar un "diccionario" de contraseñas comunes
        para adivinar la contraseña original.
        """
    )
    
    # Diccionarios simulados
    wordlists = {
        "Top 10": ["123456", "password", "123456789", "qwerty", "12345678", "111111", "12345", "admin", "123123", "root"],
        "Top 50 (Simulado)": ["123456", "password", "123456789", "qwerty", "12345678", "111111", "12345", "admin", "123123", "root"] + [f"pass{i}" for i in range(40)]
    }
    
    # Contraseña objetivo y su hash (SHA-256)
    target_password = "admin"
    target_hash = hashlib.sha256(target_password.encode()).hexdigest()
    
    st.info("Simulación de un hash de contraseña capturado:")
    st.code(f"Contraseña Original (Secreta): {target_password}\nHash SHA-256 (Capturado): {target_hash}", language="text")
    
    list_choice = st.selectbox("Seleccionar Diccionario", options=wordlists.keys())
    
    if st.button(f"Iniciar Ataque con '{list_choice}'"):
        wordlist = wordlists[list_choice]
        st.subheader("Log del Ataque:")
        
        progress_bar = st.progress(0)
        log_placeholder = st.empty()
        log_output = ""
        found = False
        
        for i, word in enumerate(wordlist):
            word_hash = hashlib.sha256(word.encode()).hexdigest()
            log_output += f"Probando: '{word}' -> Hash: {word_hash[:10]}...\n"
            
            if word_hash == target_hash:
                log_output += f"\n¡ÉXITO! Contraseña encontrada: '{word}'"
                log_placeholder.code(log_output, language="text")
                st.success(f"Contraseña encontrada: {word}")
                progress_bar.progress(100)
                found = True
                break
            
            # Actualizar UI
            time.sleep(0.1) # Simular esfuerzo
            progress_val = (i + 1) / len(wordlist)
            progress_bar.progress(progress_val)
            log_placeholder.code(log_output, language="text")
        
        if not found:
            st.error(f"Ataque fallido. La contraseña no estaba en el diccionario '{list_choice}'.")
