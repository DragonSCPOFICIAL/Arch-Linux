import tkinter as tk
from tkinter import messagebox
import os
import sys
import subprocess

# Importar as interfaces
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from main import AetherLauncherUI
from main_extreme import AetherLauncherUIExtreme

class LauncherManager:
    def __init__(self):
        self.root = tk.Tk()
        self.current_app = None
        self.mode = "standard" # standard ou extreme
        
        # Iniciar com o modo padrão
        self.launch_standard()
        
    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        # Limpar o cache de imagens se necessário (as classes já cuidam disso em seus inits)

    def launch_standard(self):
        self.clear_root()
        self.mode = "standard"
        # Criar um frame container para a interface
        self.container = tk.Frame(self.root, bg="#0a0a0a")
        self.container.pack(fill="both", expand=True)
        self.current_app = AetherLauncherUI(self.container)
        self.add_switch_button()
        
    def launch_extreme(self):
        self.clear_root()
        self.mode = "extreme"
        self.container = tk.Frame(self.root, bg="#0a0a0a")
        self.container.pack(fill="both", expand=True)
        self.current_app = AetherLauncherUIExtreme(self.container)
        self.add_switch_button()

    def add_switch_button(self):
        btn_text = "➔ MODO EXTREME (FORGE)" if self.mode == "standard" else "➔ MODO PADRÃO"
        btn_color = "#B43D3D" if self.mode == "standard" else "#1a1a1a"
        
        # O botão será colocado diretamente no root para ficar por cima de tudo
        self.switch_btn = tk.Button(
            self.root, 
            text=btn_text, 
            command=self.switch_mode,
            bg=btn_color, 
            fg="white", 
            font=("Segoe UI", 8, "bold"),
            bd=1,
            relief="flat",
            highlightthickness=0,
            cursor="hand2",
            activebackground="#963232"
        )
        # Posicionado na parte inferior da sidebar para não atrapalhar
        self.switch_btn.place(x=20, y=560, width=210, height=30)

    def switch_mode(self):
        if self.mode == "standard":
            self.launch_extreme()
        else:
            self.launch_standard()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    manager = LauncherManager()
    manager.run()
