import os

class DataHider:
    def __init__(self, cover_path: str, secret_path: str):
        self.cover_path = cover_path
        self.secret_path = secret_path

    def hide_data(self, output_path: str) -> bool:
        """הסתרת תמונה בשיטת EOF Steganography"""
        if not os.path.exists(self.cover_path) or not os.path.exists(self.secret_path):
            print("[!] One or both input files do not exist.")
            return False

        try:
            with open(self.cover_path, 'rb') as f_cover:
                cover_bytes = f_cover.read()

            with open(self.secret_path, 'rb') as f_secret:
                secret_bytes = f_secret.read()

            # הדבקת תמונת הסתר בסוף תמונת הבסיס
            combined = cover_bytes + secret_bytes

            with open(output_path, 'wb') as f_out:
                f_out.write(combined)

            return True
        except Exception as e:
            print(f"[!] Steganography error: {e}")
            return False