# Propósito: Pruebas unitarias para el simulador de blockchain y firma.
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.chain_sim_py import BlockchainSimulator, generate_keys, sign_data, verify_signature

class TestBlockchainSimulator(unittest.TestCase):

    def setUp(self):
        # Usar dificultad baja para pruebas rápidas
        self.bc = BlockchainSimulator(difficulty=1) 

    def test_initialization(self):
        """Prueba que la cadena se inicializa con un bloque génesis."""
        self.assertEqual(len(self.bc.chain), 1)
        self.assertEqual(self.bc.chain[0].index, 0)
        self.assertEqual(self.bc.chain[0].data, "Bloque Génesis")

    def test_add_block(self):
        """Prueba que añadir un bloque incrementa la longitud de la cadena."""
        self.bc.add_block("Datos de prueba 1")
        self.bc.add_block("Datos de prueba 2")
        self.assertEqual(len(self.bc.chain), 3)
        self.assertEqual(self.bc.chain[2].data, "Datos de prueba 2")
        self.assertEqual(self.bc.chain[2].previous_hash, self.bc.chain[1].hash)

    def test_is_chain_valid_success(self):
        """Prueba que una cadena recién creada es válida."""
        self.bc.add_block("Datos 1")
        is_valid, msg = self.bc.is_chain_valid()
        self.assertTrue(is_valid)
        self.assertEqual(msg, "La cadena es válida.")

    def test_is_chain_valid_failure_on_tamper(self):
        """Prueba que la cadena es inválida después de alterar un bloque."""
        self.bc.add_block("Datos buenos")
        self.bc.add_block("Más datos buenos")
        
        # Alterar el bloque 1 (el segundo bloque)
        self.bc.tamper_block(1, "Datos FALSOS")
        
        is_valid, msg = self.bc.is_chain_valid()
        self.assertFalse(is_valid)
        # El primer error que debe encontrar es el hash incorrecto del bloque 1
        self.assertIn("Hash del bloque 1 es incorrecto", msg)

    def test_is_chain_valid_failure_on_link(self):
        """Prueba que la cadena es inválida si los hashes no enlazan."""
        self.bc.add_block("Datos 1")
        # Alterar manualmente el hash anterior del bloque 1
        self.bc.chain[1].previous_hash = "hash_falso_12345"
        
        is_valid, msg = self.bc.is_chain_valid()
        self.assertFalse(is_valid)
        self.assertIn("no apunta al hash del bloque 0", msg)

class TestDigitalSignatures(unittest.TestCase):

    def setUp(self):
        self.private_key, self.public_key = generate_keys()

    def test_sign_verify_success(self):
        """Prueba que una firma válida se verifica correctamente."""
        data = "Datos importantes del sensor"
        signature = sign_data(self.private_key, data)
        is_valid = verify_signature(self.public_key, data, signature)
        self.assertTrue(is_valid)

    def test_verify_failure_wrong_data(self):
        """Prueba que una firma falla si los datos cambian."""
        data = "Datos originales"
        tampered_data = "Datos alterados"
        signature = sign_data(self.private_key, data)
        is_valid = verify_signature(self.public_key, tampered_data, signature)
        self.assertFalse(is_valid)
    
    def test_verify_failure_wrong_key(self):
        """Prueba que una firma falla si la clave pública es incorrecta."""
        data = "Datos"
        signature = sign_data(self.private_key, data)
        
        # Generar un par de claves completamente diferente
        _, other_public_key = generate_keys()
        
        is_valid = verify_signature(other_public_key, data, signature)
        self.assertFalse(is_valid)

if __name__ == '__main__':
    unittest.main()
