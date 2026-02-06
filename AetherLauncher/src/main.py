import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import threading
import subprocess
import ssl
import urllib.request
import shutil
from pathlib import Path
from PIL import Image, ImageTk

class AetherLauncherUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aether Launcher - Minecraft Elite Linux")
        self.root.geometry("1000x650")
        self.root.configure(bg="#0F111A")
        
        # Design System
        self.colors = {
            "bg": "#0F111A",
            "sidebar": "#161925",
            "card": "#1E2233",
            "accent": "#00E5FF",
            "success": "#00C853",
            "text": "#FFFFFF",
            "text_dim": "#8B949E"
        }
        
        # Caminhos Linux
        self.base_dir = "/opt/aetherlauncher"
        if not os.path.exists(self.base_dir):
            self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        self.config_dir = os.path.expanduser("~/.config/aetherlauncher")
        self.profiles_file = os.path.join(self.config_dir, "profiles.json")
        os.makedirs(self.config_dir, exist_ok=True)
        
        self.setup_ui()
        self.load_profiles()
        
        # Verificação de atualização silenciosa
        threading.Thread(target=self.silent_update_check, daemon=True).start()

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        tk.Label(self.sidebar, text="AETHER", font=("Segoe UI", 20, "bold"), 
                 bg=self.colors["sidebar"], fg=self.colors["accent"]).pack(pady=(40, 10))
        
        # Botões de Navegação (Simulados para esta v1.0.0)
        self.create_nav_btn("🎮  JOGAR")
        self.create_nav_btn("⚙️  AJUSTES")
        self.create_nav_btn("👤  PERFIS")
        
        # Footer Sidebar
        self.version_lbl = tk.Label(self.sidebar, text="v1.0.0", bg=self.colors["sidebar"], fg=self.colors["text_dim"])
        self.version_lbl.pack(side="bottom", pady=10)
        
        # Main Area
        self.main_area = tk.Frame(self.root, bg=self.colors["bg"], padx=40, pady=40)
        self.main_area.pack(side="right", fill="both", expand=True)
        
        tk.Label(self.main_area, text="BEM-VINDO AO AETHER LINUX", font=("Segoe UI", 24, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["text"]).pack(anchor="w")
        
        # Card de Jogo
        self.play_card = tk.Frame(self.main_area, bg=self.colors["card"], padx=30, pady=30)
        self.play_card.pack(fill="x", pady=40)
        
        tk.Label(self.play_card, text="NICKNAME:", bg=self.colors["card"], fg=self.colors["accent"]).pack(anchor="w")
        self.user_entry = tk.Entry(self.play_card, bg="#262B40", fg="white", insertbackground="white", bd=0, font=("Segoe UI", 12))
        self.user_entry.pack(fill="x", pady=(5, 20), ipady=8)
        self.user_entry.insert(0, "Player")
        
        # Botão Jogar
        self.play_btn = tk.Button(self.main_area, text="INICIAR MINECRAFT", font=("Segoe UI", 14, "bold"), 
                                 bg=self.colors["success"], fg="white", bd=0, cursor="hand2", command=self.launch_game)
        self.play_btn.pack(fill="x", side="bottom", ipady=15)

    def create_nav_btn(self, text):
        btn = tk.Button(self.sidebar, text=text, font=("Segoe UI", 10, "bold"), 
                       bg=self.colors["sidebar"], fg=self.colors["text"], bd=0, 
                       padx=20, pady=15, anchor="w", cursor="hand2", activebackground=self.colors["card"])
        btn.pack(fill="x")

    def load_profiles(self):
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, 'r') as f:
                    data = json.load(f)
                    self.user_entry.delete(0, tk.END)
                    self.user_entry.insert(0, data.get("username", "Player"))
            except: pass

    def save_profiles(self):
        data = {"username": self.user_entry.get()}
        with open(self.profiles_file, 'w') as f:
            json.dump(data, f, indent=4)

    def launch_game(self):
        self.save_profiles()
        messagebox.showinfo("Aether", "Iniciando Minecraft...\n(Lógica de download de assets será integrada na v1.1.0)")

    def get_remote_version(self):
        try:
            url = "https://raw.githubusercontent.com/DragonSCPOFICIAL/Arch-Linux/main/AetherLauncher/version.json"
            headers = {'User-Agent': 'Mozilla/5.0'}
            context = ssl._create_unverified_context()
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10, context=context) as response:
                return json.load(response)
        except: return None

    def silent_update_check(self):
        remote = self.get_remote_version()
        if remote and remote.get('build', 0) > 1: # Build 1 é a v1.0.0
            self.root.after(0, lambda: self.version_lbl.config(text="Nova versão disponível!", fg=self.colors["accent"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = AetherLauncherUI(root)
    root.mainloop()
