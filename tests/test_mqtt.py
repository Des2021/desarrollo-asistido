# Propósito: Pruebas unitarias para el simulador MQTT.
import unittest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.mqtt_sim import MQTTBrokerSim

class TestMQTTBrokerSim(unittest.TestCase):

    def setUp(self):
        self.broker = MQTTBrokerSim()

    def test_publish_to_log(self):
        """Prueba que un publish normal se añade al log."""
        self.broker.publish("test/topic", "payload1")
        log = self.broker.get_log()
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]["topic"], "test/topic")
        self.assertEqual(log[0]["payload"], "payload1")
        self.assertFalse(log[0]["retain"])

    def test_publish_retained(self):
        """Prueba que un publish retenido se añade al log y a los tópicos."""
        self.broker.publish("test/retained", "payload2", retain=True)
        log = self.broker.get_log()
        retained = self.broker.get_retained_messages()
        
        self.assertEqual(len(log), 1)
        self.assertIn("test/retained", retained)
        self.assertEqual(retained["test/retained"]["payload"], "payload2")

    def test_insecure_device_simulation(self):
        """Prueba que un 'config/set' dispara la simulación de credenciales."""
        self.broker.publish("config/set", "data")
        
        # El broker debería haber añadido automáticamente el tópico de credenciales
        log = self.broker.get_log()
        retained = self.broker.get_retained_messages()
        
        # Debería haber 2 mensajes en el log (config + credenciales)
        self.assertEqual(len(log), 2)
        
        # El mensaje de credenciales debería estar retenido
        found = any("credentials" in topic for topic in retained.keys())
        self.assertTrue(found, "No se encontró el tópico de credenciales retenido.")
        
        # Verificar el payload
        cred_topic = next(topic for topic in retained.keys() if "credentials" in topic)
        payload = json.loads(retained[cred_topic]["payload"])
        self.assertIn("user", payload)
        self.assertIn("pass", payload)

    def test_clear_log(self):
        """Prueba que clear_log limpia el log y los tópicos."""
        self.broker.publish("test/topic", "payload1", retain=True)
        self.broker.clear_log()
        log = self.broker.get_log()
        retained = self.broker.get_retained_messages()
        self.assertEqual(len(log), 0)
        self.assertEqual(len(retained), 0)

if __name__ == '__main__':
    unittest.main()
