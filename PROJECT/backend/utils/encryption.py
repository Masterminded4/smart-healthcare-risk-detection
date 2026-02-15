from cryptography.fernet import Fernet
from pathlib import Path
import os

class EncryptionService:
    """Service for encrypting sensitive health data."""
    
    def __init__(self, key_path='encryption_key.key'):
        self.key_path = Path(key_path)
        self._load_or_create_key()
    
    def _load_or_create_key(self):
        """Load existing key or create new one."""
        if self.key_path.exists():
            with open(self.key_path, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_path, 'wb') as f:
                f.write(self.key)
            os.chmod(self.key_path, 0o600)  # Restrict permissions
        
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data."""
        encrypted = self.cipher.encrypt(data.encode())
        return encrypted.decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data."""
        decrypted = self.cipher.decrypt(encrypted_data.encode())
        return decrypted.decode()