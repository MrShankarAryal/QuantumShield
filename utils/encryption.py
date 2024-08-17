from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class Encryption:
    def __init__(self):
        self.backend = default_backend()

    def encrypt(self, plaintext):
        key = os.urandom(32)
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return ciphertext, key, iv

    def decrypt(self, ciphertext, key, iv):
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

if __name__ == "__main__":
    encryption = Encryption()
    secret = "Highly sensitive data"
    encrypted, key, iv = encryption.encrypt(secret)
    print("Encrypted:", encrypted)
    decrypted = encryption.decrypt(encrypted, key, iv)
    print("Decrypted:", decrypted.decode())
