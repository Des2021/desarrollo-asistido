# Propósito: Simular un flujo de datos de un puerto serie (UART) para análisis.
import time
import random

class UARTSimulator:
    """Simula un dispositivo que envía datos por UART (sin hardware real)."""

    def __init__(self):
        self.buffer = []
        self.comandos_comunes = [
            "AT+STATUS?",
            "AT+RESET",
            "AT+SEND=DATA,10,ABCDEFGHIJ",
            "LOGIN:admin,PASS:1234", # Vulnerabilidad
            "SENSOR_READ=25.5C",
            "SET_CONFIG=WIFI,MyNet,MyPass" # Vulnerabilidad
        ]

    def read_data_stream(self, duration_seconds=5):
        """Genera un flujo de datos simulado durante un tiempo."""
        data_log = []
        start_time = time.time()
        while time.time() - start_time < duration_seconds:
            if random.random() < 0.3: # 30% de probabilidad de un comando
                line = random.choice(self.comandos_comunes)
            else: # 70% de datos binarios/ruido simulado
                # Usamos random.randint para generar bytes simulados (como hex)
                simulated_bytes = "".join([f"{random.randint(0, 255):02x}" for _ in range(random.randint(4, 16))])
                line = f"BIN:{simulated_bytes}"
            
            data_log.append(f"[{time.time():.2f}] RX: {line}")
            time.sleep(random.uniform(0.1, 0.5))
        return data_log

    def send_command(self, cmd):
        """Simula el envío de un comando y obtiene una respuesta."""
        response = "OK"
        if "STATUS" in cmd:
            response = "STATUS: OK, TEMP: 25.5C, V: 3.3V"
        elif "LOGIN" in cmd:
            response = "ERROR: INVALID_PASS"
        return f"CMD: {cmd}\nRES: {response}"

if __name__ == "__main__":
    # Prueba rápida de la simulación
    sim = UARTSimulator()
    print("--- Stream de Datos Simulado ---")
    log = sim.read_data_stream(2)
    for line in log:
        print(line)
    
    print("\n--- Envío de Comando Simulado ---")
    print(sim.send_command("AT+STATUS?"))
