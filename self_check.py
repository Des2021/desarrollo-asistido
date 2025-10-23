#!/usr/bin/env python
#
# Script de Auto-Verificación (Self-Check) para 'iot-secure-app'
#
# Propósito:
#   Este script está diseñado para que los alumnos lo ejecuten localmente
#   (usando 'python self_check.py' desde el directorio raíz del proyecto)
#   para verificar que los módulos 'core' principales están implementados
#   correctamente antes de intentar ejecutar la aplicación Streamlit.
#
#   Comprueba la lógica de negocio central (flujo de control de acceso,
#   lógica de UART, y criptografía de firmware) en memoria.
#

import sys
import os
from typing import List

# --- Configuración del Path ---
# Añadir el directorio raíz del proyecto al sys.path
# Esto permite que el script (ejecutado como 'python self_check.py')
# encuentre el directorio 'core' (como 'import core.uart_sim').
try:
    # __file__ es 'self_check.py'. parent es el directorio raíz.
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
except NameError:
    # Fallback por si se ejecuta en un REPL
    project_root = os.path.abspath('.')
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

# --- Importación de Módulos Core ---
try:
    from core import uart_sim
    from core import ledger_sim
    from core import ac_sim
    from core import actuator_sim
    from core import fw_sim
    from core import chain_sim_py
except ImportError as e:
    print(f"✖ ERROR CRÍTICO: No se pudieron importar los módulos 'core'.")
    print(f"  Asegúrate de ejecutar este script desde el directorio raíz del proyecto.")
    print(f"  Error detallado: {e}")
    sys.exit(1)

# Lista para almacenar los resultados
results: List[str] = []

# --- Definiciones de Pruebas ---

def check_uart_logic():
    """
    Verifica la lógica de estado del simulador UART:
    1. Prueba el bloqueo (lockout) después de MAX_FAILURES.
    2. Prueba el flujo de autenticación exitoso y el 'DUMP SECRETS'.
    """
    # 1. Prueba de bloqueo
    state = uart_sim.UARTState()
    
    # Asumimos que MAX_FAILURES es 3 (basado en el archivo uart_sim.py)
    # Si MAX_FAILURES no existe, esta prueba fallará (lo cual es bueno)
    max_fails = getattr(uart_sim, 'MAX_FAILURES', 3)
    
    for i in range(max_fails):
        uart_sim.handle_cmd(state, f"AUTH pass_fallido_{i}")
    
    if not state.locked:
        raise AssertionError(f"El estado UART no se bloqueó (state.locked=False) después de {max_fails} fallos.")
    
    # 2. Prueba de autenticación y DUMP
    state = uart_sim.UARTState() # Estado limpio
    correct_pass = state.pw
    
    resp_auth = uart_sim.handle_cmd(state, f"AUTH {correct_pass}")
    if "EXITOSA" not in resp_auth or state.secure:
        raise AssertionError("La autenticación UART falló con la contraseña correcta o no desactivó state.secure.")
        
    resp_dump = uart_sim.handle_cmd(state, "DUMP SECRETS")
    if "SECRETO REVELADO" not in resp_dump or correct_pass not in resp_dump:
        raise AssertionError("El comando 'DUMP SECRETS' no reveló los secretos después de la autenticación.")

def check_access_control_flow():
    """
    Verifica el flujo completo de Ledger -> AC -> Actuator.
    1. Instancia los tres módulos.
    2. Registra un dispositivo en el Ledger.
    3. Concede acceso a un usuario en el AC.
    4. Verifica que el actuador permite al usuario autorizado.
    5. Verifica que el actuador RECHAZA al usuario no autorizado.
    """
    DEVICE_ID = "actuator_001"
    AUTH_USER = "admin_user"
    UNAUTH_USER = "guest_user"

    # 1. Instanciar
    ledger = ledger_sim.Ledger()
    ac = ac_sim.AccessControl()
    # Asumimos la API: Actuator(device_id, ac_module, ledger_module)
    actuator = actuator_sim.Actuator(DEVICE_ID, ac, ledger)

    # 2. Registrar
    ledger.register_device(DEVICE_ID)
    # Asumimos la API: ledger.get_entry()
    if not ledger.get_entry(DEVICE_ID):
        raise AssertionError("Ledger.register_device() no creó una entrada verificable.")

    # 3. Conceder acceso
    ac.grant_access(AUTH_USER, DEVICE_ID)
    # Asumimos la API: ac.check_access()
    if not ac.check_access(AUTH_USER, DEVICE_ID):
        raise AssertionError("AccessControl.grant_access() no concedió el acceso correctamente.")

    # 4. Prueba de actuación (Éxito)
    try:
        # Asumimos la API: actuator.actuate(user_id, command)
        actuator.actuate(AUTH_USER, "SET_ON")
        # Si llega aquí, es un éxito
    except Exception as e:
        raise AssertionError(f"Actuator.actuate() (AUTORIZADO) lanzó una excepción inesperada: {e}")

    # 5. Prueba de actuación (Fallo esperado)
    try:
        actuator.actuate(UNAUTH_USER, "SET_ON")
        # Si llega aquí, es un fallo (debería haber lanzado una excepción)
        raise AssertionError("Actuator.actuate() (NO AUTORIZADO) NO lanzó una excepción.")
    except PermissionError:
        # ¡Éxito! Se lanzó la excepción de permisos esperada.
        pass
    except Exception as e:
        raise AssertionError(f"Actuator.actuate() (NO AUTORIZADO) lanzó una excepción incorrecta: {type(e).__name__} en lugar de PermissionError.")

def check_firmware_and_ota():
    """
    Verifica la lógica del firmware:
    1. El 'first_boot_check' (simulado).
    2. El flujo de firma y verificación OTA (usando chain_sim_py).
    """
    
    # 1. Prueba de First Boot
    # Asumimos la API: fw_sim.first_boot_check() devuelve True/False
    if not fw_sim.first_boot_check():
        raise AssertionError("fw_sim.first_boot_check() devolvió False (falló).")

    # 2. Prueba de Firma/Verificación OTA
    # Asumimos que la criptografía está en chain_sim_py
    try:
        priv_key, pub_key = chain_sim_py.generate_keys()
    except Exception as e:
        raise AssertionError(f"chain_sim_py.generate_keys() falló. ¿Está 'cryptography' instalado? Error: {e}")

    dummy_firmware = b"DatosDelFirmwareVersion3.1"
    
    # Firma
    signature = chain_sim_py.sign_data(priv_key, dummy_firmware)
    if not signature or not isinstance(signature, bytes):
        raise AssertionError("chain_sim_py.sign_data() no devolvió una firma válida (bytes).")
        
    # Verificación (Éxito)
    if not chain_sim_py.verify_signature(pub_key, dummy_firmware, signature):
        raise AssertionError("chain_sim_py.verify_signature() falló con una firma y datos válidos.")
        
    # Verificación (Fallo por datos alterados)
    tampered_firmware = b"DatosDelFirmwareVersion3.1-ALTERADO"
    if chain_sim_py.verify_signature(pub_key, tampered_firmware, signature):
        raise AssertionError("chain_sim_py.verify_signature() TUVO ÉXITO con datos alterados (¡Error de seguridad!).")
    
    # Verificación (Fallo por firma alterada)
    tampered_signature = signature[::-1] # Firma invertida
    if chain_sim_py.verify_signature(pub_key, dummy_firmware, tampered_signature):
        raise AssertionError("chain_sim_py.verify_signature() TUVO ÉXITO con una firma alterada (¡Error de seguridad!).")

# --- Ejecutor de Pruebas ---

def run_test(name: str, test_function):
    """
    Función helper para ejecutar una prueba y almacenar su resultado.
    """
    try:
        test_function()
        results.append(f"✔ {name}")
    except Exception as e:
        results.append(f"✖ {name}\n    -> ERROR: {e}")

def main():
    """
    Punto de entrada principal del script.
    """
    print(f"--- Iniciando Auto-Verificación (Self-Check) para 'iot-secure-app' ---")
    print(f"Cargando módulos desde: {project_root}\n")

    # Ejecutar todas las pruebas
    run_test("UART: Lógica de autenticación y bloqueo (lockout)", check_uart_logic)
    run_test("Flujo: Ledger -> AccessControl -> Actuator", check_access_control_flow)
    run_test("Firmware: First Boot y Criptografía OTA (Sign/Verify)", check_firmware_and_ota)

    # Imprimir resumen
    print("--- Resumen de Resultados ---")
    all_passed = True
    for res in results:
        print(res)
        if res.startswith("✖"):
            all_passed = False
    
    print("-" * 29)
    if all_passed:
        print("\n🎉 ¡ÉXITO! Todos los checks locales han pasado.")
    else:
        print("\n❌ FALLIDO. Revisa los errores (✖) de arriba.")
        sys.exit(1) # Salir con código de error

if __name__ == "__main__":
    main()
