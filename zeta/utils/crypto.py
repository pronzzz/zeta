from cryptography.fernet import Fernet
import os
from pathlib import Path
from typing import Optional
from zeta.utils.logger import logger

class CryptoUtils:
    def __init__(self, key_path: str = ".secret.key"):
        self.key_path = Path(key_path)
        self.key = self.load_or_create_key()
        self.cipher = Fernet(self.key)

    def load_or_create_key(self) -> bytes:
        if self.key_path.exists():
            with open(self.key_path, "rb") as f:
                return f.read()
        else:
            logger.info("Generating new encryption key...")
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as f:
                f.write(key)
            # Set permissions to read/write only by owner
            os.chmod(self.key_path, 0o600)
            return key

    def encrypt(self, data: str) -> bytes:
        return self.cipher.encrypt(data.encode())

    def decrypt(self, token: bytes) -> str:
        return self.cipher.decrypt(token).decode()

    def encrypt_file(self, file_path: str):
        path = Path(file_path)
        if not path.exists():
            return
        
        with open(path, "rb") as f:
            data = f.read()
        
        encrypted_data = self.cipher.encrypt(data)
        
        with open(path, "wb") as f:
            f.write(encrypted_data)

    def decrypt_file(self, file_path: str) -> bytes:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File {file_path} not found")
            
        with open(path, "rb") as f:
            data = f.read()
            
        return self.cipher.decrypt(data)
