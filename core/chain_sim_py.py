# Propósito: Simular una blockchain simple para el registro inmutable de datos.
import hashlib
import time
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

class Block:
    """Define la estructura de un bloque en la blockchain."""
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data # Datos del dispositivo IoT
        self.previous_hash = previous_hash
        self.nonce = nonce # Para la prueba de trabajo (Proof-of-Work)
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calcula el hash SHA-256 del bloque."""
        block_string = json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "data": self.data,
                "previous_hash": self.previous_hash,
                "nonce": self.nonce
            },
            sort_keys=True,
        ).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        """Simula la minería (PoW) encontrando un hash con 'difficulty' ceros."""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        # print(f"Bloque minado: {self.hash}") # Descomentar para depurar

class BlockchainSimulator:
    """Simula la cadena de bloques completa."""
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty # Ceros iniciales para la PoW

    def create_genesis_block(self):
        """Crea el primer bloque (génesis) de la cadena."""
        return Block(0, time.time(), "Bloque Génesis", "0")

    def get_latest_block(self):
        """Obtiene el último bloque de la cadena."""
        return self.chain[-1]

    def add_block(self, data):
        """Añade un nuevo bloque a la cadena después de minarlo."""
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            timestamp=time.time(),
            data=data,
            previous_hash=latest_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        """Verifica la integridad de toda la cadena."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # 1. Verificar si el hash almacenado es correcto
            if current_block.hash != current_block.calculate_hash():
                return False, f"Hash del bloque {i} es incorrecto (los datos fueron alterados)."

            # 2. Verificar si el bloque apunta al hash anterior correcto
            if current_block.previous_hash != previous_block.hash:
                return False, f"El bloque {i} no apunta al hash del bloque {i-1} (enlace roto)."
            
            # 3. Verificar si el hash minado cumple la dificultad
            target = "0" * self.difficulty
            if current_block.hash[:self.difficulty] != target:
                 return False, f"El hash del bloque {i} no cumple la dificultad."

        return True, "La cadena es válida."

    def tamper_block(self, block_index, new_data):
        """Simula la alteración de datos en un bloque (para demostrar la invalidación)."""
        if 0 < block_index < len(self.chain):
            self.chain[block_index].data = new_data
            # No recalcula el hash, solo altera los datos.
            return True
        return False

# --- Simulación de Firma Digital ---
# (Usando 'cryptography' de requirements.txt)

def generate_keys():
    """Genera un par de claves RSA (privada y pública) simuladas."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def sign_data(private_key, data):
    """Firma datos (ej. un hash de datos IoT) con la clave privada."""
    if not isinstance(data, bytes):
        data = str(data).encode('utf-8')
    
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(public_key, data, signature):
    """Verifica una firma con la clave pública."""
    if not isinstance(data, bytes):
        data = str(data).encode('utf-8')
    
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

if __name__ == "__main__":
    # 1. Prueba de Blockchain
    print("--- Prueba de Blockchain ---")
    bc = BlockchainSimulator(difficulty=3)
    bc.add_block({"sensor": "temp", "valor": 22.5})
    bc.add_block({"sensor": "hum", "valor": 60.1})
    
    print(f"Cadena válida: {bc.is_chain_valid()}")
    print("Alterando el bloque 1...")
    bc.tamper_block(1, {"sensor": "temp", "valor": 500.0}) # Alteración
    print(f"Cadena válida: {bc.is_chain_valid()}")
    
    # 2. Prueba de Firma Digital
    print("\n--- Prueba de Firma Digital ---")
    priv, pub = generate_keys()
    datos_iot = "ID_DISPOSITIVO: 789, DATOS: 42.0"
    firma = sign_data(priv, datos_iot)
    
    print(f"Datos: {datos_iot}")
    print(f"Firma (hex): {firma.hex()[:40]}...")
    
    es_valida_ok = verify_signature(pub, datos_iot, firma)
    print(f"Verificación (datos correctos): {es_valida_ok}")
    
    datos_falsos = "ID_DISPOSITIVO: 789, DATOS: 99.9" # Datos alterados
    es_valida_fail = verify_signature(pub, datos_falsos, firma)
    print(f"Verificación (datos falsos): {es_valida_fail}")
