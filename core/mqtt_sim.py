# Propósito: Simular un broker y clientes MQTT para análisis de tráfico (sin red).
import random
import json
import time

class MQTTBrokerSim:
    """
    Simula un broker MQTT localmente usando un diccionario.
    No utiliza sockets ni red.
    """
    def __init__(self):
        # El "broker" es solo un diccionario que almacena el último mensaje por tópico.
        self.topics = {}
        self.log = []

    def publish(self, topic, payload, retain=False):
        """Simula la publicación de un mensaje."""
        message = {
            "timestamp": time.time(),
            "topic": topic,
            "payload": payload,
            "retain": retain
        }
        self.log.append(message)
        if retain:
            self.topics[topic] = message
        
        # Simular un dispositivo inseguro que envía credenciales
        if "config/set" in topic and random.random() < 0.5:
            self._sim_insecure_device()

    def get_log(self):
        """Obtiene el log completo de mensajes (para el 'sniffer')."""
        return self.log

    def get_retained_messages(self):
        """Obtiene los mensajes retenidos."""
        return self.topics

    def _sim_insecure_device(self):
        """Simula un dispositivo tonto publicando sus credenciales."""
        time.sleep(0.1) # Pausa simulada
        bad_topic = "device/12345/debug/credentials"
        bad_payload = json.dumps({
            "user": "device_admin",
            "pass": "admin_pass_123" # ¡Vulnerabilidad!
        })
        self.publish(bad_topic, bad_payload, retain=True)

    def clear_log(self):
        """Limpia el log y los tópicos para una nueva simulación."""
        self.log = []
        self.topics = {}

# Instancia global simulada para ser usada por la app Streamlit
GLOBAL_BROKER = MQTTBrokerSim()
