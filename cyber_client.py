import socket
import os
import random
import string
import tkinter as tk
from tkinter import filedialog, messagebox
from encrypt import Encryption
from hide_png import DataHider

class CyberClientGUI:
    def __init__(self, server_ip='localhost', server_port=5555):
        self.server_ip = server_ip
        self.server_port = server_port
        self.crypto = Encryption()
        self.client_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        self.cover_path = ""
        self.secret_path = ""

        # Tkinter Setup
        self.root = tk.Tk()
        self.root.title("Cyber Stego Client")
        self.root.geometry("450x350")
        
        self.build_gui()

    def build_gui(self):
        tk.Label(self.root, text="Steganography Client Tool", font=("Arial", 14, "bold")).pack(pady=10)

        # Cover Image Select
        btn_cover = tk.Button(self.root, text="1. Select Cover Image (Base)", command=self.select_cover)
        btn_cover.pack(fill='x', padx=30, pady=5)
        self.lbl_cover = tk.Label(self.root, text="No file selected", fg="gray")
        self.lbl_cover.pack()

        # Secret Image Select
        btn_secret = tk.Button(self.root, text="2. Select Secret Image to Hide", command=self.select_secret)
        btn_secret.pack(fill='x', padx=30, pady=5)
        self.lbl_secret = tk.Label(self.root, text="No file selected", fg="gray")
        self.lbl_secret.pack()

        # Send Button
        btn_send = tk.Button(self.root, text="Process & Upload to Server", bg="green", fg="white", font=("Arial", 10, "bold"), command=self.process_and_send)
        btn_send.pack(fill='x', padx=30, pady=20)

    def select_cover(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if path:
            self.cover_path = path
            self.lbl_cover.config(text=os.path.basename(path), fg="black")

    def select_secret(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if path:
            self.secret_path = path
            self.lbl_secret.config(text=os.path.basename(path), fg="black")

    def process_and_send(self):
        if not self.cover_path or not self.secret_path:
            messagebox.showwarning("Missing Files", "Please select both cover and secret images.")
            return

        stego_output = "stego_temp.jpg"
        hider = DataHider(self.cover_path, self.secret_path)
        
        if not hider.hide_data(stego_output):
            messagebox.showerror("Error", "Failed to perform steganography.")
            return

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.server_ip, self.server_port))

            # 1. שליחת Client ID מוצפן
            enc_id = self.crypto.encrypt_data(self.client_id)
            sock.sendall(enc_id.encode('utf-8'))

            # 2. שליחת פקודה
            enc_cmd = self.crypto.encrypt_data("DECODE")
            sock.sendall(enc_cmd.encode('utf-8'))

            # 3. שליחת גודל קובץ
            file_size = os.path.getsize(stego_output)
            enc_size = self.crypto.encrypt_data(str(file_size))
            sock.sendall(enc_size.encode('utf-8'))

            # 4. שליחת נתוני הקובץ
            with open(stego_output, "rb") as f:
                sock.sendall(f.read())

            messagebox.showinfo("Success", "Stego image successfully generated and uploaded to server!")

        except Exception as e:
            messagebox.showerror("Network Error", f"Could not connect or send data: {e}")
        finally:
            sock.close()
            if os.path.exists(stego_output):
                os.remove(stego_output)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    client = CyberClientGUI()
    client.run()