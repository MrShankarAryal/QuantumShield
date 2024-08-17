import unittest
from core.quantum_defense import QuantumDefense

class TestQuantumDefense(unittest.TestCase):
    def setUp(self):
        self.q_defense = QuantumDefense()
        self.plaintext = "Sensitive information"

    def test_encryption_decryption(self):
        encrypted = self.q_defense.encrypt_data(self.plaintext)
        decrypted = self.q_defense.decrypt_data(encrypted)
        self.assertEqual(self.plaintext, decrypted)

if __name__ == "__main__":
    unittest.main()
