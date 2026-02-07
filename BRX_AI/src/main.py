import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import datetime
import os
import json
import threading
import time
import subprocess

# Nota: Em um ambiente real, estas seriam instaladas via install.sh
# import pyautogui 
# from PIL import Image, ImageTk

class BRX_AI_App_UI:
    def __init__(self, root):
        self.root = root
        self.root.title("BRX AI - Agente Autônomo Arch Linux")
        self.root.geometry("1200x850")
        self.root.configure(bg="#0B0E14")

        # Design System "Modo Prime" - Otimizado para Arch Linux
        self.colors = {
            "bg": "#0B0E14",
            "sidebar": "#10141B",
            "card": "#161B22",
            "accent": "#1793D1", # Azul Arch
            "success": "#00FF9C", # Verde Neon
            "warning": "#FFD700",
            "text": "#E6EDF3",
            "text_dim": "#7D8590",
            "border": "#30363D"
        }

        self.is_executing = False
        self.setup_ui()

    def setup_ui(self):
        # Sidebar Lateral
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar"], pady=40)
        logo_frame.pack(fill="x")
        tk.Label(logo_frame, text="BRX AI", font=("Segoe UI", 26, "bold"),
                 bg=self.colors["sidebar"], fg=self.colors["accent"]).pack()
        tk.Label(logo_frame, text="AGENTE AUTÔNOMO", font=("Segoe UI", 8, "bold"),
                 bg=self.colors["sidebar"], fg=self.colors["text_dim"]).pack()

        # Menu
        self.nav_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
        self.nav_frame.pack(fill="both", expand=True, pady=20)

        self.create_nav_btn("💬  CENTRAL DE COMANDO", self.show_chat_page)
        self.create_nav_btn("👁️  VISÃO DO SISTEMA", self.show_vision_page)
        self.create_nav_btn("🛠️  AUTOMAÇÃO", self.show_automation_page)
        self.create_nav_btn("⚙️  NÚCLEO (CONFIG)", self.show_settings_page)

        # Status
        footer = tk.Frame(self.sidebar, bg=self.colors["sidebar"], pady=20)
        footer.pack(side="bottom", fill="x")
        self.status_dot = tk.Label(footer, text="●", fg=self.colors["success"], bg=self.colors["sidebar"])
        self.status_dot.pack(side="left", padx=(25, 5))
        tk.Label(footer, text="AGENTE ATIVO", font=("Segoe UI", 8, "bold"),
                 bg=self.colors["sidebar"], fg=self.colors["text"]).pack(side="left")

        # Main Area
        self.main_area = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_area.pack(side="right", fill="both", expand=True)

        self.show_chat_page()

    def create_nav_btn(self, text, command):
        btn = tk.Button(self.nav_frame, text=text, font=("Segoe UI", 10, "bold"),
                        bg=self.colors["sidebar"], fg=self.colors["text"],
                        bd=0, padx=25, pady=18, anchor="w", cursor="hand2",
                        activebackground=self.colors["card"], activeforeground=self.colors["accent"],
                        command=command)
        btn.pack(fill="x")

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def show_chat_page(self):
        self.clear_main_area()
        
        header = tk.Frame(self.main_area, bg=self.colors["bg"], padx=30, pady=25)
        header.pack(fill="x")
        tk.Label(header, text="Interação em Tempo Real", font=("Segoe UI", 18, "bold"),
                 bg=self.colors["bg"], fg=self.colors["text"]).pack(side="left")

        # Chat Display
        self.chat_container = tk.Frame(self.main_area, bg=self.colors["bg"], padx=30)
        self.chat_container.pack(fill="both", expand=True)

        self.chat_display = scrolledtext.ScrolledText(self.chat_container, bg=self.colors["card"], 
                                                      fg=self.colors["text"], font=("Segoe UI", 11),
                                                      bd=0, padx=20, pady=20, state="disabled",
                                                      highlightthickness=1, highlightbackground=self.colors["border"])
        self.chat_display.pack(fill="both", expand=True)

        # Input
        input_frame = tk.Frame(self.main_area, bg=self.colors["bg"], padx=30, pady=25)
        input_frame.pack(fill="x")

        self.entry_bg = tk.Frame(input_frame, bg=self.colors["card"], padx=15, pady=12,
                                 highlightthickness=1, highlightbackground=self.colors["border"])
        self.entry_bg.pack(fill="x")

        self.msg_entry = tk.Entry(self.entry_bg, bg=self.colors["card"], fg=self.colors["text"],
                                  insertbackground=self.colors["accent"], bd=0, font=("Segoe UI", 12))
        self.msg_entry.pack(side="left", fill="x", expand=True)
        self.msg_entry.bind("<Return>", lambda e: self.send_message())

        send_btn = tk.Button(self.entry_bg, text="EXECUTAR", font=("Segoe UI", 9, "bold"),
                             bg=self.colors["accent"], fg="#FFFFFF", bd=0, padx=25,
                             cursor="hand2", command=self.send_message)
        send_btn.pack(side="right")

        self.append_message("BRX AI", "Aguardando comandos. Posso ver sua tela e interagir com o sistema.")

    def send_message(self):
        msg = self.msg_entry.get().strip()
        if msg:
            self.append_message("Você", msg)
            self.msg_entry.delete(0, tk.END)
            self.simulate_action(msg)

    def simulate_action(self, msg):
        self.append_message("BRX AI", f"Analisando ambiente para executar: '{msg}'...")
        # Simulação de "ver a tela" e "mexer no mouse"
        def run():
            time.sleep(1)
            self.append_message("SISTEMA", "Capturando tela... [OK]")
            time.sleep(1)
            self.append_message("SISTEMA", "Movendo cursor para coordenadas de interface... [OK]")
            time.sleep(1)
            self.append_message("BRX AI", "Ação concluída com sucesso no ambiente Arch Linux.")
        
        threading.Thread(target=run).start()

    def append_message(self, sender, message):
        self.chat_display.config(state="normal")
        time_str = datetime.datetime.now().strftime("%H:%M")
        color = self.colors["accent"] if sender == "BRX AI" else self.colors["text"]
        if sender == "SISTEMA": color = self.colors["warning"]
        
        self.chat_display.insert(tk.END, f"[{time_str}] {sender}: ", "header")
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.tag_configure("header", font=("Segoe UI", 11, "bold"), foreground=color)
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def show_vision_page(self):
        self.clear_main_area()
        container = tk.Frame(self.main_area, bg=self.colors["bg"], padx=40, pady=40)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Visão do Agente", font=("Segoe UI", 22, "bold"),
                 bg=self.colors["bg"], fg=self.colors["text"]).pack(anchor="w")
        
        # Placeholder para o Feed da Tela
        vision_card = tk.Frame(container, bg=self.colors["card"], height=400,
                               highlightthickness=1, highlightbackground=self.colors["border"])
        vision_card.pack(fill="both", expand=True, pady=30)
        vision_card.pack_propagate(False)

        tk.Label(vision_card, text="[ FEED DE TELA EM TEMPO REAL ]", bg=self.colors["card"], 
                 fg=self.colors["text_dim"], font=("Segoe UI", 14, "bold")).place(relx=0.5, rely=0.5, anchor="center")

    def show_automation_page(self):
        self.clear_main_area()
        container = tk.Frame(self.main_area, bg=self.colors["bg"], padx=40, pady=40)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Painel de Automação", font=("Segoe UI", 22, "bold"),
                 bg=self.colors["bg"], fg=self.colors["text"]).pack(anchor="w", pady=(0, 30))

        # Lista de Ferramentas
        tools = [
            ("Captura de Tela", "Permite que a IA veja o que está acontecendo."),
            ("Controle de Mouse", "Permite que a IA clique e mova janelas."),
            ("Injeção de Teclado", "Permite que a IA digite comandos e textos."),
            ("Terminal Root", "Acesso direto ao shell para tarefas complexas.")
        ]

        for title, desc in tools:
            card = tk.Frame(container, bg=self.colors["card"], padx=20, pady=15, mb=10,
                            highlightthickness=1, highlightbackground=self.colors["border"])
            card.pack(fill="x", pady=5)
            tk.Label(card, text=title, bg=self.colors["card"], fg=self.colors["accent"], font=("Segoe UI", 11, "bold")).pack(anchor="w")
            tk.Label(card, text=desc, bg=self.colors["card"], fg=self.colors["text_dim"], font=("Segoe UI", 9)).pack(anchor="w")

    def show_settings_page(self):
        self.clear_main_area()
        container = tk.Frame(self.main_area, bg=self.colors["bg"], padx=40, pady=40)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Configurações do Núcleo", font=("Segoe UI", 22, "bold"),
                 bg=self.colors["bg"], fg=self.colors["text"]).pack(anchor="w", pady=(0, 30))

        settings_card = tk.Frame(container, bg=self.colors["card"], padx=30, pady=30,
                                 highlightthickness=1, highlightbackground=self.colors["border"])
        settings_card.pack(fill="x")

        tk.Checkbutton(settings_card, text="Permitir Controle Total do Mouse/Teclado", 
                       bg=self.colors["card"], fg=self.colors["text"], selectcolor="#000000",
                       font=("Segoe UI", 11)).pack(anchor="w", pady=10)
        
        tk.Checkbutton(settings_card, text="Modo de Resposta Ultra-Rápida (Prime)", 
                       bg=self.colors["card"], fg=self.colors["text"], selectcolor="#000000",
                       font=("Segoe UI", 11)).pack(anchor="w", pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BRX_AI_App_UI(root)
    root.mainloop()
