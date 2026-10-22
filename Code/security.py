import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KEY_FILE = "secret.key"


class SecurityManager:

  def __init__(self):
    self.key = self._load_or_generate_key()
    self.cipher = Fernet(self.key)

  def _load_or_generate_key(self) -> bytes:
    """Generates or loads a secure 256-bit encryption key."""
    if os.path.exists(KEY_FILE):
      with open(KEY_FILE, "rb") as k_file:
        return k_file.read()
    else:
      key = Fernet.generate_key()
      with open(KEY_FILE, "wb") as k_file:
        k_file.write(key)
      return key

  def encrypt_data(self, data: str) -> str:
    """Encrypts plain text string using AES-256 (Fernet)."""
    if not data:
      return ""
    encrypted = self.cipher.encrypt(data.encode())
    return encrypted.decode()

  def decrypt_data(self, encrypted_data: str) -> str:
    """Decrypts ciphertext back into plain text string."""
    if not encrypted_data:
      return ""
    try:
      decrypted = self.cipher.decrypt(encrypted_data.encode())
      return decrypted.decode()
    except Exception:
      return "[Decryption Failed]"

  @staticmethod
  def hash_sensitive_id(identity_str: str) -> str:
    """Creates a one-way SHA-256 hash for privacy-preserving user tracking."""
    digest = hashes.Hash(hashes.SHA256())
    digest.update(identity_str.encode())
    return digest.finalize().hex()[:16]
