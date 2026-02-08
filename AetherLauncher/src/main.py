import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
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
        self.root.title("Aether Launcher - Minecraft Elite Linux (Nativo)")
        
        # Centralizar a janela
        window_width = 1000
        window_height = 650
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg="#EAEAEA")
        
        # Design System (Moderno e Limpo)
        self.colors = {
            "bg": "#EAEAEA",      
            "sidebar": "#FFFFFF", 
            "card": "#FFFFFF",
            "accent": "#B43D3D",  
            "success": "#B43D3D", 
            "text": "#333333",
            "text_dim": "#666666",
            "border": "#DDDDDD",
            "selected": "#F0F0F0"
        }
        
        # Config Base
        self.config_dir = os.path.expanduser("~/.config/aetherlauncher")
        self.profiles_file = os.path.join(self.config_dir, "profiles_v2.json")
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Caminhos do Minecraft
        self.base_minecraft_dir = os.path.expanduser("~/.aetherlauncher/minecraft")
        os.makedirs(self.base_minecraft_dir, exist_ok=True)
        
        # Estado Inicial
        self.downloading = False
        self.settings = self.load_profiles_data()
        self.profiles = self.settings.get("profiles", [
            {"name": "Latest Release", "version": "latest-release", "type": "Vanilla", "id": "default_1"},
            {"name": "1.12.2 Forge", "version": "1.12.2", "type": "Forge", "id": "default_2"}
        ])
        self.selected_profile_id = self.settings.get("last_profile_id", self.profiles[0]["id"])
        self.username = self.settings.get("username", "DragonSCP")
        
        self.setup_ui()
        
    def load_profiles_data(self):
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, 'r') as f:
                    return json.load(f)
            except: return {}
        return {}

    def save_profiles_data(self):
        data = {
            "username": self.username,
            "last_profile_id": self.selected_profile_id,
            "profiles": self.profiles
        }
        try:
            with open(self.profiles_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar perfis: {e}")

    def setup_ui(self):
        # Layout Principal
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=250, bd=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        tk.Frame(self.root, bg=self.colors["border"], width=1).pack(side="left", fill="y")
        
        self.main_content = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_content.pack(side="right", fill="both", expand=True)
        
        # --- SIDEBAR ---
        # Perfil do Usuário
        self.profile_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar"], pady=20, padx=20)
        self.profile_frame.pack(fill="x")
        
        self.avatar_canvas = tk.Canvas(self.profile_frame, width=40, height=40, bg="#333", highlightthickness=0)
        self.avatar_canvas.pack(side="left")
        
        user_info = tk.Frame(self.profile_frame, bg=self.colors["sidebar"], padx=10)
        user_info.pack(side="left", fill="x")
        tk.Label(user_info, text="Logado como", font=("Segoe UI", 8), bg=self.colors["sidebar"], fg=self.colors["text_dim"]).pack(anchor="w")
        self.user_lbl = tk.Label(user_info, text=self.username, font=("Segoe UI", 10, "bold"), bg=self.colors["sidebar"], fg=self.colors["text"])
        self.user_lbl.pack(anchor="w")
        
        # Menu
        self.nav_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar"], pady=10)
        self.nav_frame.pack(fill="both", expand=True)
        
        self.create_sidebar_item("Configurações", "⚙")
        self.create_sidebar_item("Gerenciar Instalações", "+", is_action=True)
        
        tk.Frame(self.nav_frame, bg=self.colors["border"], height=1).pack(fill="x", pady=10, padx=20)
        
        # Lista de Perfis
        self.profile_list_frame = tk.Frame(self.nav_frame, bg=self.colors["sidebar"])
        self.profile_list_frame.pack(fill="both", expand=True)
        
        self.refresh_profile_list()
        
        # Botão JOGAR
        self.play_section = tk.Frame(self.sidebar, bg=self.colors["accent"], height=80)
        self.play_section.pack(side="bottom", fill="x")
        
        self.play_btn = tk.Button(self.play_section, text="JOGAR", font=("Segoe UI", 16, "bold"), 
                                 bg=self.colors["accent"], fg="white", bd=0, cursor="hand2",
                                 activebackground="#963232", command=self.start_launch_process)
        self.play_btn.pack(fill="both", expand=True, pady=(10,0))
        
        self.version_subtext = tk.Label(self.play_section, text="", font=("Segoe UI", 8), 
                                      bg=self.colors["accent"], fg="white")
        self.version_subtext.pack(fill="x", pady=(0, 10))
        self.update_selected_display()

        # --- CONTEÚDO ---
        self.banner_frame = tk.Frame(self.main_content, bg=self.colors["bg"], padx=40, pady=40)
        self.banner_frame.pack(fill="both", expand=True)
        
        self.image_container = tk.Frame(self.banner_frame, bg="#333", bd=0)
        self.image_container.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.85, relheight=0.6)
        
        # Barra de Progresso
        self.progress_container = tk.Frame(self.main_content, bg=self.colors["bg"], height=80)
        self.progress_container.pack(side="bottom", fill="x", padx=40, pady=20)
        
        self.progress_label = tk.Label(self.progress_container, text="Pronto para jogar", bg=self.colors["bg"], fg=self.colors["text_dim"], font=("Segoe UI", 9))
        self.progress_label.pack(anchor="w")
        
        self.progress_bar = ttk.Progressbar(self.progress_container, mode='determinate', length=100)
        self.progress_bar.pack(fill="x", pady=5)
        self.progress_container.pack_forget()

    def create_sidebar_item(self, text, icon, is_action=False):
        frame = tk.Frame(self.nav_frame, bg=self.colors["sidebar"], padx=20, pady=8)
        frame.pack(fill="x")
        tk.Label(frame, text=icon, font=("Segoe UI", 12), bg=self.colors["sidebar"], fg=self.colors["text_dim"], width=2).pack(side="left")
        tk.Label(frame, text=text, font=("Segoe UI", 10), bg=self.colors["sidebar"], fg=self.colors["text"]).pack(side="left", padx=10)
        
        if is_action:
            frame.bind("<Button-1>", lambda e: self.show_edit_installation())
            for child in frame.winfo_children(): child.bind("<Button-1>", lambda e: self.show_edit_installation())
        
        frame.bind("<Enter>", lambda e: frame.config(bg=self.colors["selected"]))
        frame.bind("<Leave>", lambda e: frame.config(bg=self.colors["sidebar"]))

    def refresh_profile_list(self):
        for widget in self.profile_list_frame.winfo_children(): widget.destroy()
        for p in self.profiles:
            is_selected = (p["id"] == self.selected_profile_id)
            bg = "#D0D0D0" if is_selected else self.colors["sidebar"]
            
            f = tk.Frame(self.profile_list_frame, bg=bg, padx=20, pady=8)
            f.pack(fill="x")
            
            canvas = tk.Canvas(f, width=20, height=20, bg="#5D8A3E", highlightthickness=0)
            canvas.pack(side="left")
            
            tk.Label(f, text=p["name"], font=("Segoe UI", 10), bg=bg, fg=self.colors["text"]).pack(side="left", padx=10)
            
            f.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))
            for child in f.winfo_children(): child.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))

    def select_profile(self, profile_id):
        self.selected_profile_id = profile_id
        self.update_selected_display()
        self.refresh_profile_list()
        self.save_profiles_data()

    def update_selected_display(self):
        profile = next((p for p in self.profiles if p["id"] == self.selected_profile_id), self.profiles[0])
        self.version_subtext.config(text=f"{profile['type']} {profile['version']}")

    def show_edit_installation(self, profile=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Instalação")
        dialog.geometry("500x550")
        dialog.configure(bg="white")
        dialog.transient(self.root)
        dialog.grab_set()

        # UI do Modal (Baseado na imagem de referência)
        tk.Label(dialog, text="Editar Instalação", font=("Segoe UI", 16, "bold"), bg="white", pady=20).pack()
        
        # Nome
        tk.Label(dialog, text="Nome da Instalação", bg="white", fg=self.colors["text_dim"], font=("Segoe UI", 9)).pack(anchor="w", padx=40)
        name_entry = tk.Entry(dialog, bg="#F0F0F0", bd=0, font=("Segoe UI", 11))
        name_entry.pack(fill="x", padx=40, pady=(5, 20), ipady=8)
        name_entry.insert(0, profile["name"] if profile else "Nova Instalação")

        # Tipo (Vanilla, Forge, Fabric)
        tk.Label(dialog, text="Versão", bg="white", fg=self.colors["text_dim"], font=("Segoe UI", 9)).pack(anchor="w", padx=40)
        type_frame = tk.Frame(dialog, bg="white")
        type_frame.pack(fill="x", padx=40, pady=5)
        
        type_var = tk.StringVar(value=profile["type"] if profile else "Vanilla")
        for t in ["Vanilla", "Forge", "Fabric"]:
            rb = tk.Radiobutton(type_frame, text=t, variable=type_var, value=t, bg="white", font=("Segoe UI", 10))
            rb.pack(side="left", padx=(0, 15))

        # Versão
        version_entry = tk.Entry(dialog, bg="#F0F0F0", bd=0, font=("Segoe UI", 11))
        version_entry.pack(fill="x", padx=40, pady=(5, 20), ipady=8)
        version_entry.insert(0, profile["version"] if profile else "1.20.1")

        # Diretório (Isolamento)
        tk.Label(dialog, text="Diretório do Jogo", bg="white", fg=self.colors["text_dim"], font=("Segoe UI", 9)).pack(anchor="w", padx=40)
        dir_var = tk.BooleanVar(value=True)
        tk.Checkbutton(dialog, text="Usar pasta separada (Instância)", variable=dir_var, bg="white").pack(anchor="w", padx=40)

        def save():
            new_profile = {
                "name": name_entry.get(),
                "version": version_entry.get(),
                "type": type_var.get(),
                "id": profile["id"] if profile else f"profile_{os.urandom(4).hex()}",
                "use_separate_dir": dir_var.get()
            }
            if profile:
                idx = next(i for i, p in enumerate(self.profiles) if p["id"] == profile["id"])
                self.profiles[idx] = new_profile
            else:
                self.profiles.append(new_profile)
            
            self.selected_profile_id = new_profile["id"]
            self.save_profiles_data()
            self.refresh_profile_list()
            self.update_selected_display()
            dialog.destroy()

        tk.Button(dialog, text="Salvar", bg=self.colors["accent"], fg="white", bd=0, font=("Segoe UI", 10, "bold"), 
                  padx=30, pady=10, command=save).pack(side="bottom", pady=30)

    def start_launch_process(self):
        if self.downloading: return
        self.downloading = True
        self.play_btn.config(state="disabled", text="AGUARDE...")
        self.progress_container.pack(side="bottom", fill="x", padx=40, pady=20)
        threading.Thread(target=self.run_minecraft, daemon=True).start()

    def run_minecraft(self):
        try:
            profile = next((p for p in self.profiles if p["id"] == self.selected_profile_id), self.profiles[0])
            version_id = profile["version"]
            
            # Tratar "latest"
            if version_id == "latest-release": version_id = minecraft_launcher_lib.utils.get_latest_version()["release"]
            elif version_id == "latest-snapshot": version_id = minecraft_launcher_lib.utils.get_latest_version()["snapshot"]

            # Definir diretório da instância
            instance_dir = os.path.join(self.base_minecraft_dir, "instances", profile["name"].replace(" ", "_")) if profile.get("use_separate_dir", True) else self.base_minecraft_dir
            os.makedirs(instance_dir, exist_ok=True)

            callback = {
                "setStatus": lambda text: self.root.after(0, lambda: self.progress_label.config(text=text)),
                "setProgress": lambda value: self.root.after(0, lambda: self.progress_bar.config(value=value)),
                "setMax": lambda value: self.root.after(0, lambda: self.progress_bar.config(maximum=value))
            }

            # 1. Download/Instalação do Vanilla Base
            self.root.after(0, lambda: self.progress_label.config(text=f"Baixando base {version_id}..."))
            minecraft_launcher_lib.install.install_minecraft_version(version_id, self.base_minecraft_dir, callback=callback)

            # 2. Lógica de Mod Loader (Forge/Fabric)
            final_version_id = version_id
            if profile["type"] == "Fabric":
                self.root.after(0, lambda: self.progress_label.config(text="Instalando Fabric..."))
                fabric_version = minecraft_launcher_lib.fabric.get_latest_loader_version()
                minecraft_launcher_lib.fabric.install_fabric(version_id, self.base_minecraft_dir, loader_version=fabric_version, callback=callback)
                final_version_id = minecraft_launcher_lib.fabric.get_fabric_version(version_id, fabric_version)
            elif profile["type"] == "Forge":
                self.root.after(0, lambda: self.progress_label.config(text="Instalando Forge..."))
                forge_version = minecraft_launcher_lib.forge.get_forge_version_list()[0] # Simplificado para o mais novo
                minecraft_launcher_lib.forge.install_forge_version(forge_version, self.base_minecraft_dir, callback=callback)
                final_version_id = forge_version

            # 3. Java Automático (O minecraft-launcher-lib já cuida disso se passarmos o executável correto)
            # Mas vamos garantir que temos o Java 17+ para versões novas
            java_path = "java" # Assume que está no path para Linux nativo, ou podemos baixar via runtime.install_jvm_runtime

            options = {
                "username": self.username,
                "uuid": "", "token": "",
                "launcherName": "AetherLauncher",
                "launcherVersion": "2.0",
                "gameDirectory": instance_dir,
                "jvmArguments": ["-Xmx2G", "-Xms1G"]
            }

            self.root.after(0, lambda: self.progress_label.config(text="Iniciando jogo nativo..."))
            cmd = minecraft_launcher_lib.command.get_minecraft_command(final_version_id, self.base_minecraft_dir, options)
            
            self.root.after(0, lambda: self.progress_container.pack_forget())
            subprocess.run(cmd)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Falha: {str(e)}"))
        finally:
            self.downloading = False
            self.root.after(0, lambda: self.play_btn.config(state="normal", text="JOGAR"))

if __name__ == "__main__":
    root = tk.Tk()
    app = AetherLauncherUI(root)
    root.mainloop()
