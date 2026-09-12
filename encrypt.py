import base64
import os
from Crypto.Cipher import AES

class Encryption:
    def __init__(self):
        # מפתח הצפנה בגודל 256 ביט
        self.AES_KEY = b"\xa5\\\xb9\xdf\xaa\xc9M\xb5\xf7\xaf\x03\x96k,^S+\x1f\x07w\x7f\xe6\xe6\xe8\x07\x81\xca\x99'\xc4\x8f\xb6"

    def encrypt_data(self, data: bytes) -> str:
        """הצפנת נתונים ב-AES-GCM עם Nonce אקראי לכל הודעה (מתקן כשל אבטחה)"""
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        nonce = os.urandom(12)  # ייצור Nonce דינמי ייחודי
        cipher = AES.new(self.AES_KEY, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        # הרכבת המבנה: Nonce (12B) + Tag (16B) + Ciphertext
        payload = nonce + tag + ciphertext
        return base64.b64encode(payload).decode('utf-8')

    def decrypt_data(self, data: str) -> bytes:
        """פיענוח נתוני Base64 המוצפנים"""
        raw_data = base64.b64decode(data)
        nonce = raw_data[:12]
        tag = raw_data[12:28]
        ciphertext = raw_data[28:]
        
        cipher = AES.new(self.AES_KEY, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag)