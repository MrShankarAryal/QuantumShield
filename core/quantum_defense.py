from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class QuantumDefense:
    def __init__(self):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()

    def encrypt_data(self, plaintext):
        ciphertext = self.public_key.encrypt(
            plaintext.encode(),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(), label=None))
        return ciphertext

    def decrypt_data(self, ciphertext):
        plaintext = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(), label=None))
        return plaintext.decode()

if __name__ == "__main__":
    q_defense = QuantumDefense()
    secret = "Sensitive information"
    encrypted = q_defense.encrypt_data(secret)
    print("Encrypted:", encrypted)
    decrypted = q_defense.decrypt_data(encrypted)
    print("Decrypted:", decrypted)
