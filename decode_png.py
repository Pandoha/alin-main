import os

class ImageExtractor:
    def __init__(self, media_path: str):
        self.media_path = media_path
        self.jpeg_start = b'\xff\xd8'
        self.jpeg_end = b'\xff\xd9'

    def extract_images(self, output_folder: str = ".") -> list:
        """חילוץ מדויק של תמונות מוסתרות שצורפו לאחר תמונת הבסיס"""
        if not os.path.exists(self.media_path):
            print(f"[!] File not found: {self.media_path}")
            return []

        with open(self.media_path, 'rb') as f:
            media_data = f.read()

        # מציאת סוף תמונת הבסיס המקורית
        first_end = media_data.find(self.jpeg_end)
        if first_end == -1:
            print("[!] No valid JPEG end boundary found.")
            return []

        # המידע המוסתר מתחיל מיד לאחר ה-EOF של תמונת הבסיס
        hidden_data = media_data[first_end + len(self.jpeg_end):]
        
        extracted_files = []
        count = 1
        pos = 0

        while True:
            start_index = hidden_data.find(self.jpeg_start, pos)
            if start_index == -1:
                break
                
            end_index = hidden_data.find(self.jpeg_end, start_index)
            if end_index == -1:
                break

            end_index += len(self.jpeg_end)
            image_bytes = hidden_data[start_index:end_index]

            output_filename = os.path.join(output_folder, f"extracted_{count}.jpg")
            with open(output_filename, 'wb') as img_out:
                img_out.write(image_bytes)

            extracted_files.append(output_filename)
            count += 1
            pos = end_index

        return extracted_files