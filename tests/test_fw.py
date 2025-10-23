# Propósito: Pruebas unitarias para el simulador de análisis de firmware.
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.fw_sim import create_dummy_firmware, analyze_firmware

class TestFirmwareSimulator(unittest.TestCase):

    def test_create_vulnerable_firmware(self):
        """Prueba que el firmware vulnerable contiene secretos."""
        fw = create_dummy_firmware(include_vulnerability=True)
        self.assertIn(b"ROOT_PASS=root_password_!@#", fw)
        self.assertIn(b"API_KEY=key_a1b2c3d4e5f67890", fw)

    def test_create_safe_firmware(self):
        """Prueba que el firmware seguro no contiene esos secretos."""
        fw = create_dummy_firmware(include_vulnerability=False)
        self.assertNotIn(b"ROOT_PASS=root_password_!@#", fw)
        self.assertNotIn(b"API_KEY=key_a1b2c3d4e5f67890", fw)

    def test_analyze_vulnerable_firmware(self):
        """Prueba que el análisis encuentra los secretos en el firmware vulnerable."""
        fw = create_dummy_firmware(include_vulnerability=True)
        results = analyze_firmware(fw)
        
        self.assertIsInstance(results, dict)
        self.assertIn("root_password_!@#", results["passwords"])
        self.assertIn("key_a1b2c3d4e5f67890", results["keys"])
        self.assertIn("MyDeviceNetwork", results["ssids"])

    def test_analyze_safe_firmware(self):
        """Prueba que el análisis no encuentra secretos en el firmware seguro."""
        fw = create_dummy_firmware(include_vulnerability=False)
        results = analyze_firmware(fw)
        
        self.assertEqual(len(results["passwords"]), 0)
        self.assertEqual(len(results["keys"]), 0)
        self.assertIn("MyDeviceNetwork", results["ssids"]) # El SSID está bien

if __name__ == '__main__':
    unittest.main()
