# Propósito: Página de Streamlit para demostrar el uso de blockchain para integridad de datos.
import streamlit as st
import json
import time
from core.chain_sim_py import BlockchainSimulator

st.set_page_config(page_title="Blockchain e Integridad", page_icon="⛓️")
st.title("⛓️ Blockchain para la Integridad de Datos IoT")
st.markdown(
    """
    Una blockchain puede usarse como un registro (ledger) inmutable.
    Cada bloque de datos (ej. lecturas de sensores) está criptográficamente
    ligado al anterior. Alterar un bloque invalida toda la cadena.
    """
)

# Inicializar la blockchain en el estado de la sesión
if "blockchain" not in st.session_state:
    st.session_state.blockchain = BlockchainSimulator(difficulty=3) # Dificultad 3 para rapidez

def display_chain():
    """Función helper para mostrar la cadena."""
    st.subheader("Estado Actual de la Cadena")
    chain_data = []
    for block in st.session_state.blockchain.chain:
        chain_data.append(
            {
                "index": block.index,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp)),
                "data": block.data,
                "hash": block.hash[:15] + "...",
                "previous_hash": block.previous_hash[:15] + "...",
                "nonce": block.nonce
            }
        )
    st.json(json.dumps(chain_data, indent=2))

# --- Columna 1: Añadir Bloques ---
col1, col2 = st.columns(2)
with col1:
    st.header("1. Registrar Datos (Minar)")
    sensor_data = st.text_input("Datos del Sensor (ej. 'temp: 22.5')", "temp: 22.5")
    
    if st.button("Añadir Bloque a la Cadena"):
        with st.spinner(f"Minando bloque (dificultad={st.session_state.blockchain.difficulty})..."):
            new_block = st.session_state.blockchain.add_block(sensor_data)
        st.success(f"¡Bloque {new_block.index} minado y añadido!")
        st.write(f"Hash: `{new_block.hash}`")
        display_chain()

# --- Columna 2: Verificar y Alterar ---
with col2:
    st.header("2. Verificar y Alterar")
    
    st.subheader("Verificar Integridad")
    if st.button("Verificar la Cadena Completa"):
        is_valid, message = st.session_state.blockchain.is_chain_valid()
        if is_valid:
            st.success(f"¡Éxito! {message}")
        else:
            st.error(f"¡Fallo de Integridad! {message}")
    
    st.subheader("Simular Ataque (Alteración)")
    chain_length = len(st.session_state.blockchain.chain)
    if chain_length > 1:
        block_to_tamper = st.number_input(
            "Índice del bloque a alterar", 
            min_value=1, 
            max_value=chain_length - 1, 
            value=1,
            step=1
        )
        new_data = st.text_input("Nuevos datos fraudulentos", "temp: 99.9")
        
        if st.button("Alterar Datos del Bloque (¡Ataque!)"):
            if st.session_state.blockchain.tamper_block(int(block_to_tamper), new_data):
                st.warning(f"¡Datos del bloque {block_to_tamper} alterados en memoria!")
                st.info("La cadena ahora debería ser inválida. Intenta verificarla.")
                display_chain()
            else:
                st.error("No se pudo alterar el bloque (índice inválido).")
    else:
        st.info("Añade más bloques para poder simular una alteración.")

# Mostrar la cadena al final si no se mostró ya
if 'new_block' not in locals() and 'block_to_tamper' not in locals():
    display_chain()
