import socket
import threading
import sqlite3
import os
import sys
import tkinter as tk
from tkinter import messagebox
import pygame
from encrypt import Encryption
from decode_png import ImageExtractor

class CyberServer:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.crypto = Encryption()
        self.setup_db()
        self.setup_audio()
        
        # Tkinter Root
        self.root = tk.Tk()
        self.root.title("Cyber Server Management System")
        self.root.geometry("600x500")
        
        self.build_gui()

    def setup_audio(self):
        try:
            pygame.mixer.init()
            if os.path.exists("intro.mp3"):
                pygame.mixer.music.load("intro.mp3")
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"[!] Audio init error: {e}")

    def setup_db(self):
        conn = sqlite3.connect('server_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def register_client(self, client_id: str, ip: str):
        conn = sqlite3.connect('server_data.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clients (client_id, ip_address) VALUES (?, ?)", (client_id, ip))
        conn.commit()
        conn.close()

    def build_gui(self):
        label = tk.Label(self.root, text="Server Monitor Log", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        self.log_box = tk.Text(self.root, state='disabled', width=70, height=20)
        self.log_box.pack(padx=10, pady=10)

    def log(self, message: str):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.config(state='disabled')
        self.log_box.see(tk.END)

    def handle_client(self, conn, addr):
        self.log(f"[+] Incoming connection from {addr[0]}:{addr[1]}")
        try:
            # 1. קבלת ID
            encrypted_id = conn.recv(1024).decode('utf-8')
            client_id = self.crypto.decrypt_data(encrypted_id).decode('utf-8')
            self.register_client(client_id, addr[0])
            self.log(f"[*] Client authenticated: {client_id}")

            # 2. קבלת פקודה
            encrypted_cmd = conn.recv(1024).decode('utf-8')
            cmd = self.crypto.decrypt_data(encrypted_cmd).decode('utf-8')

            if cmd == "DECODE":
                # קבלת גודל הקובץ המוצפן
                file_size_enc = conn.recv(1024).decode('utf-8')
                file_size = int(self.crypto.decrypt_data(file_size_enc).decode('utf-8'))
                
                # איסוף בינארי נקי של הקובץ
                received_data = b""
                while len(received_data) < file_size:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    received_data += chunk
                
                temp_path = f"received_{client_id}.jpg"
                with open(temp_path, "wb") as f:
                    f.write(received_data)
                
                extractor = ImageExtractor(temp_path)
                extracted = extractor.extract_images()
                
                self.log(f"[+] Successfully extracted {len(extracted)} hidden file(s) for {client_id}")
                
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        except Exception as e:
            self.log(f"[!] Error processing client {addr}: {e}")
        finally:
            conn.close()

    def start_network_listener(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        self.log(f"[*] Server listening on {self.host}:{self.port}")

        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def run(self):
        threading.Thread(target=self.start_network_listener, daemon=True).start()
        self.root.mainloop()

if __name__ == "__main__":
    server = CyberServer()
    server.run()