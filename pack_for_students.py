#!/usr/bin/env python
#
# Script de Empaquetado del Proyecto 'iot-secure-app'
#
# Propósito:
#   1. Verifica que todos los archivos esenciales del proyecto existen.
#   2. Si es así, crea un archivo 'iot-secure-app.zip' que contiene
#      todo el contenido del proyecto (excepto él mismo y el zip resultante).
#   3. Imprime la ruta absoluta al .zip creado o un error si faltan archivos.
#
# Uso:
#   Ejecutar desde el directorio raíz del proyecto:
#   > python pack_for_students.py
#

import os
import sys
import zipfile

# --- Configuración ---

# El nombre del archivo .zip que se generará
ZIP_FILENAME = "iot-secure-app.zip"

# El nombre de este script, para excluirlo del .zip
SCRIPT_NAME = "pack_for_students.py"

# Lista de archivos y directorios esenciales que DEBEN existir
# para que el empaquetado se considere válido.
ESSENTIAL_FILES = [
    'app.py',
    'requirements.txt',
    'ENTREGA.md',
    'self_check.py',
    'core',
    'core/uart_sim.py',
    'core/mqtt_sim.py',
    'core/fw_sim.py',
    'core/chain_sim_py.py',
    'core/ledger_sim.py',
    'core/ac_sim.py',
    'core/actuator_sim.py',
    'pages',
    'pages/1_Amenazas_IoT.py',
    'pages/2_Firmware_y_Contraseñas.py',
    'pages/3_Blockchain_Seguridad.py',
    'pages/4_Auditoria_Entrega.py',
    'tests',
    'tests/test_uart.py',
    'tests/test_mqtt.py',
    'tests/test_fw.py',
    'tests/test_chain_py.py',
]

# Directorios que se excluirán recursivamente del .zip
EXCLUDE_DIRS = {
    '.git',
    '.venv',
    'venv',
    '__pycache__',
    '.vscode',
}

# --- Lógica del Script ---

def verify_files(project_root: str) -> (bool, list):
    """Verifica que todos los archivos esenciales existen."""
    missing = []
    for f in ESSENTIAL_FILES:
        path = os.path.join(project_root, f)
        if not os.path.exists(path):
            missing.append(f)
    
    if missing:
        return False, missing
    return True, []

def create_zip(project_root: str, zip_path: str) -> int:
    """
    Crea el archivo .zip caminando por el project_root.
    Excluye este script, el .zip resultante y los directorios en EXCLUDE_DIRS.
    """
    files_packaged = 0
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(project_root, topdown=True):
            # 1. Modificar 'dirs' in-place para podar la búsqueda de os.walk
            # Esto evita que 'os.walk' entre en estos directorios.
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                # 2. Excluir archivos de empaquetado
                if file == SCRIPT_NAME or file == ZIP_FILENAME:
                    continue
                
                # 3. Obtener la ruta completa y la ruta relativa (para el .zip)
                file_path = os.path.join(root, file)
                
                # arcname es el path *dentro* del zip.
                # os.path.relpath asegura que la estructura de carpetas sea correcta.
                archive_name = os.path.relpath(file_path, project_root)

                # 4. Escribir en el .zip
                zf.write(file_path, arcname=archive_name)
                files_packaged += 1
                
    return files_packaged

def main():
    """Punto de entrada principal del script."""
    
    # Asumimos que el script se ejecuta desde el directorio raíz del proyecto
    project_root = os.getcwd()
    
    # 1. Verificar archivos
    print("Verificando la estructura del proyecto...")
    success, missing = verify_files(project_root)
    
    if not success:
        print("\n--- ✖ ERROR: Faltan archivos esenciales ---", file=sys.stderr)
        for f in missing:
            print(f"  - {f}", file=sys.stderr)
        print("Empaquetado cancelado.", file=sys.stderr)
        sys.exit(1)
        
    print("✔ Verificación completada.")
    
    # 2. Crear el Zip
    zip_path_full = os.path.join(project_root, ZIP_FILENAME)
    print(f"Creando {ZIP_FILENAME}...")
    
    try:
        count = create_zip(project_root, zip_path_full)
    except Exception as e:
        print(f"\n--- ✖ ERROR: No se pudo crear el archivo .zip ---", file=sys.stderr)
        print(f"  Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    # 3. Éxito
    print(f"✔ Éxito: Se empaquetaron {count} archivos.")
    print("\n--- Ubicación del Paquete ---")
    print(os.path.abspath(zip_path_full))

if __name__ == "__main__":
    main()
