import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import threading
import subprocess
import ssl
import urllib.request
import shutil
from PIL import Image, ImageTk
import minecraft_launcher_lib

class AetherLauncherUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aether Launcher - Minecraft Elite Linux")
        
        # Centralizar a janela
        window_width = 1000
        window_height = 650
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg="#0F111A")
        
        # Design System (Baseado na referência e modernizado)
        self.colors = {
            "bg": "#EAEAEA",      # Fundo claro como na imagem
            "sidebar": "#FFFFFF", # Sidebar branca
            "card": "#FFFFFF",
            "accent": "#B43D3D",  # Tom de vermelho/rosa do botão JOGAR
            "success": "#B43D3D", # Botão jogar
            "text": "#333333",
            "text_dim": "#666666",
            "border": "#DDDDDD",
            "selected": "#F0F0F0"
        }
        
        # Config Base
        self.config_dir = os.path.expanduser("~/.config/aetherlauncher")
        self.profiles_file = os.path.join(self.config_dir, "profiles.json")
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Carregar Configurações
        self.settings = self.load_settings_data()
        
        # Caminhos do Minecraft
        self.minecraft_dir = self.settings.get("base_dir", os.path.expanduser("~/.aetherlauncher/minecraft"))
        os.makedirs(self.minecraft_dir, exist_ok=True)
        
        self.downloading = False
        self.selected_version = self.settings.get("last_version", "1.12.2")
        self.username = self.settings.get("username", "DragonSCP")
        
        self.setup_ui()
        
    def load_settings_data(self):
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, 'r') as f:
                    return json.load(f)
            except: return {}
        return {}

    def save_settings(self):
        self.settings["username"] = self.username
        self.settings["last_version"] = self.selected_version
        self.settings["base_dir"] = self.minecraft_dir
        try:
            with open(self.profiles_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar config: {e}")

    def setup_ui(self):
        # Layout Principal: Sidebar e Conteúdo
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=250, bd=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Divisor da sidebar
        tk.Frame(self.root, bg=self.colors["border"], width=1).pack(side="left", fill="y")
        
        self.main_content = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_content.pack(side="right", fill="both", expand=True)
        
        # --- SIDEBAR ---
        # Perfil do Usuário
        self.profile_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar"], pady=20, padx=20)
        self.profile_frame.pack(fill="x")
        
        # Ícone de perfil (simulado)
        self.avatar_canvas = tk.Canvas(self.profile_frame, width=40, height=40, bg="#333", highlightthickness=0)
        self.avatar_canvas.pack(side="left")
        
        user_info = tk.Frame(self.profile_frame, bg=self.colors["sidebar"], padx=10)
        user_info.pack(side="left", fill="x")
        tk.Label(user_info, text="Logado como", font=("Segoe UI", 8), bg=self.colors["sidebar"], fg=self.colors["text_dim"]).pack(anchor="w")
        self.user_lbl = tk.Label(user_info, text=self.username, font=("Segoe UI", 10, "bold"), bg=self.colors["sidebar"], fg=self.colors["text"])
        self.user_lbl.pack(anchor="w")
        
        # Menu de Navegação
        self.nav_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar"], pady=10)
        self.nav_frame.pack(fill="both", expand=True)
        
        self.create_sidebar_item("Configurações", "⚙")
        self.create_sidebar_item("Gerenciar Instalações", "+", is_action=True)
        
        tk.Frame(self.nav_frame, bg=self.colors["border"], height=1).pack(fill="x", pady=10, padx=20)
        
        # Lista de Versões (Como na imagem)
        self.version_list_frame = tk.Frame(self.nav_frame, bg=self.colors["sidebar"])
        self.version_list_frame.pack(fill="both", expand=True)
        
        self.refresh_version_list()
        
        # Botão JOGAR no rodapé da sidebar
        self.play_section = tk.Frame(self.sidebar, bg=self.colors["accent"], height=80)
        self.play_section.pack(side="bottom", fill="x")
        
        self.play_btn = tk.Button(self.play_section, text="JOGAR", font=("Segoe UI", 16, "bold"), 
                                 bg=self.colors["accent"], fg="white", bd=0, cursor="hand2",
                                 activebackground="#963232", command=self.start_game_process)
        self.play_btn.pack(fill="both", expand=True, pady=(10,0))
        
        self.version_subtext = tk.Label(self.play_section, text=self.selected_version, font=("Segoe UI", 8), 
                                      bg=self.colors["accent"], fg="white")
        self.version_subtext.pack(fill="x", pady=(0, 10))

        # --- CONTEÚDO PRINCIPAL ---
        # Área de Banner/Imagem central
        self.banner_frame = tk.Frame(self.main_content, bg=self.colors["bg"], padx=40, pady=40)
        self.banner_frame.pack(fill="both", expand=True)
        
        # Placeholder para a imagem do Minecraft (Penguin na neve da referência)
        self.image_container = tk.Frame(self.banner_frame, bg="#333", bd=2, relief="flat")
        self.image_container.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.8, relheight=0.5)
        
        # Texto de status/novidades (simulado)
        self.status_box = tk.Frame(self.banner_frame, bg="white", bd=1, relief="solid")
        self.status_box.place(relx=0.5, rely=0.1, anchor="center", relwidth=0.8, height=40)
        tk.Label(self.status_box, text="Novidades e Atualizações do Aether Launcher", bg="white", fg="#333").pack(pady=8)

        # Barra de Progresso (Invisível por padrão)
        self.progress_container = tk.Frame(self.main_content, bg=self.colors["bg"], height=60)
        self.progress_container.pack(side="bottom", fill="x", padx=40, pady=20)
        
        self.progress_label = tk.Label(self.progress_container, text="Pronto para jogar", bg=self.colors["bg"], fg=self.colors["text_dim"])
        self.progress_label.pack(anchor="w")
        
        self.progress_bar = ttk.Progressbar(self.progress_container, mode='determinate', length=100)
        self.progress_bar.pack(fill="x", pady=5)
        self.progress_container.pack_forget() # Esconder inicialmente

    def create_sidebar_item(self, text, icon, is_action=False):
        frame = tk.Frame(self.nav_frame, bg=self.colors["sidebar"], padx=20, pady=8)
        frame.pack(fill="x")
        
        tk.Label(frame, text=icon, font=("Segoe UI", 12), bg=self.colors["sidebar"], fg=self.colors["text_dim"], width=2).pack(side="left")
        tk.Label(frame, text=text, font=("Segoe UI", 10), bg=self.colors["sidebar"], fg=self.colors["text"]).pack(side="left", padx=10)
        
        if is_action:
            frame.bind("<Button-1>", lambda e: self.add_new_version())
            for child in frame.winfo_children():
                child.bind("<Button-1>", lambda e: self.add_new_version())
        
        frame.bind("<Enter>", lambda e: frame.config(bg=self.colors["selected"]))
        frame.bind("<Leave>", lambda e: frame.config(bg=self.colors["sidebar"]))

    def refresh_version_list(self):
        for widget in self.version_list_frame.winfo_children():
            widget.destroy()
            
        # Versões padrão como na imagem
        versions = ["Latest Release", "Latest Snapshot", "1.12.2", "mine"]
        
        for v in versions:
            is_selected = (v == self.selected_version)
            bg_color = "#D0D0D0" if is_selected else self.colors["sidebar"]
            
            f = tk.Frame(self.version_list_frame, bg=bg_color, padx=20, pady=8)
            f.pack(fill="x")
            
            # Ícone de grama/bloco simplificado
            canvas = tk.Canvas(f, width=20, height=20, bg="#5D8A3E", highlightthickness=0)
            canvas.pack(side="left")
            
            tk.Label(f, text=v, font=("Segoe UI", 10), bg=bg_color, fg=self.colors["text"]).pack(side="left", padx=10)
            
            # Bind de clique para selecionar
            f.bind("<Button-1>", lambda e, ver=v: self.select_version(ver))
            for child in f.winfo_children():
                child.bind("<Button-1>", lambda e, ver=v: self.select_version(ver))

    def select_version(self, version):
        self.selected_version = version
        self.version_subtext.config(text=version)
        self.refresh_version_list()
        self.save_settings()

    def add_new_version(self):
        # Simplesmente alterna para uma versão de teste para demonstrar
        v = filedialog.askstring("Nova Versão", "Digite a versão do Minecraft (ex: 1.20.1):")
        if v:
            self.select_version(v)

    def update_progress(self, progress):
        self.progress_bar["value"] = progress["current"]
        self.progress_bar["maximum"] = progress["max"]
        self.progress_label.config(text=f"Baixando: {progress['text']} ({progress['current']}/{progress['max']})")
        self.root.update_idletasks()

    def start_game_process(self):
        if self.downloading:
            return
            
        self.downloading = True
        self.play_btn.config(state="disabled", text="AGUARDE...")
        self.progress_container.pack(side="bottom", fill="x", padx=40, pady=20)
        
        # Thread para não travar a UI
        threading.Thread(target=self.run_minecraft, daemon=True).start()

    def run_minecraft(self):
        try:
            version = self.selected_version
            # Mapear nomes amigáveis para IDs reais do Minecraft
            version_id = version
            if version == "Latest Release":
                version_id = minecraft_launcher_lib.utils.get_latest_version()["release"]
            elif version == "Latest Snapshot":
                version_id = minecraft_launcher_lib.utils.get_latest_version()["snapshot"]
            elif version == "mine":
                version_id = "1.12.2" # Default para o perfil custom

            # Callbacks para o progresso
            callback = {
                "setStatus": lambda text: self.root.after(0, lambda: self.progress_label.config(text=text)),
                "setProgress": lambda value: self.root.after(0, lambda: self.progress_bar.config(value=value)),
                "setMax": lambda value: self.root.after(0, lambda: self.progress_bar.config(maximum=value))
            }

            # 1. Instalar (Isso baixa TUDO: jar, libraries, assets, natives)
            self.root.after(0, lambda: self.progress_label.config(text=f"Verificando arquivos de {version_id}..."))
            minecraft_launcher_lib.install.install_minecraft_version(version_id, self.minecraft_dir, callback=callback)

            # 2. Configurar Opções de Lançamento
            options = {
                "username": self.username,
                "uuid": "",
                "token": "",
                "launcherName": "AetherLauncher",
                "launcherVersion": "2.0",
                "jvmArguments": ["-Xmx2G", "-Xms1G"]
            }

            # 3. Obter comando de execução
            self.root.after(0, lambda: self.progress_label.config(text="Iniciando jogo..."))
            minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version_id, self.minecraft_dir, options)

            # 4. Executar
            self.root.after(0, lambda: self.progress_container.pack_forget())
            subprocess.run(minecraft_command)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Falha ao iniciar Minecraft: {str(e)}"))
        finally:
            self.downloading = False
            self.root.after(0, lambda: self.play_btn.config(state="normal", text="JOGAR"))

if __name__ == "__main__":
    root = tk.Tk()
    # Tenta carregar ícone se existir
    try:
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icon.png")
        if os.path.exists(icon_path):
            img = ImageTk.PhotoImage(Image.open(icon_path))
            root.iconphoto(True, img)
    except: pass
    
    app = AetherLauncherUI(root)
    root.mainloop()
