# Propósito: Simular el análisis de un archivo de firmware en busca de secretos.
import re

def create_dummy_firmware(include_vulnerability=True):
    """
    Crea un bloque de bytes que simula ser un firmware.
    Usamos bytes para simular datos binarios.
    """
    
    # Datos binarios aleatorios simulando código compilado
    firmware_data = b'\xDE\xAD\xBE\xEF' * 10
    firmware_data += b'Este es un firmware de prueba. ' * 5
    firmware_data += b'\x00\x01\x02\x03\x04' * 20
    firmware_data += b'CONFIG_START\n'
    firmware_data += b'SSID=MyDeviceNetwork\n'
    
    if include_vulnerability:
        # La vulnerabilidad: credenciales hardcodeadas
        firmware_data += b'API_KEY=key_a1b2c3d4e5f67890\n'
        firmware_data += b'ROOT_PASS=root_password_!@#\n'
    
    firmware_data += b'CONFIG_END\n'
    firmware_data += b'\xFF\xFE\xFD\xFC' * 15
    firmware_data += b'Cargador de arranque v1.2\n'
    
    return firmware_data

def analyze_firmware(firmware_bytes):
    """
    Simula un 'strings' y 'grep' en un binario de firmware.
    Busca patrones de texto comunes.
    """
    findings = {
        "passwords": [],
        "keys": [],
        "ssids": [],
        "total_size": len(firmware_bytes)
    }
    
    # Expresiones regulares simples para simular la búsqueda
    # Nota: En la vida real, esto sería mucho más complejo (ej. 'binwalk')
    
    # Convertir bytes a string, ignorando errores de decodificación
    firmware_text = ""
    if isinstance(firmware_bytes, bytes):
        firmware_text = firmware_bytes.decode('utf-8', errors='ignore')
    else:
        # Si ya es un string (ej. desde un st.file_uploader que lee como texto)
        firmware_text = firmware_bytes

    # Buscar contraseñas (ejemplos muy básicos)
    password_patterns = [r'(pass|password|pwd|PASSWD)\s*=\s*([a-zA-Z0-9_!@#$]+)', r'ROOT_PASS=([a-zA-Z0-9_!@#$]+)']
    for pattern in password_patterns:
        matches = re.findall(pattern, firmware_text, re.IGNORECASE)
        for match in matches:
            # match es una tupla, ej: ('PASS', '1234') o solo ('root_password_!@#')
            found_pass = match[1] if isinstance(match, tuple) and len(match) > 1 else match
            findings["passwords"].append(str(found_pass))
    
    # Buscar claves API
    key_patterns = [r'(api_key|KEY)\s*=\s*(key_[a-zA-Z0-9_]+)']
    for pattern in key_patterns:
        matches = re.findall(pattern, firmware_text, re.IGNORECASE)
        for match in matches:
            found_key = match[1] if isinstance(match, tuple) and len(match) > 1 else match
            findings["keys"].append(str(found_key))
            
    # Buscar SSIDs
    ssid_patterns = [r'SSID\s*=\s*([a-zA-Z0-9_]+)']
    for pattern in ssid_patterns:
        matches = re.findall(pattern, firmware_text, re.IGNORECASE)
        for match in matches:
            found_ssid = match[1] if isinstance(match, tuple) and len(match) > 1 else match
            findings["ssids"].append(str(found_ssid))
    
    return findings

if __name__ == "__main__":
    fw = create_dummy_firmware(include_vulnerability=True)
    results = analyze_firmware(fw)
    print(f"Firmware (tamaño: {len(fw)} bytes) creado.")
    print("--- Resultados del Análisis ---")
    print(results)
