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

# Configurações de SSL para evitar erros de certificado em downloads
ssl._create_default_https_context = ssl._create_unverified_context

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
        self.root.resizable(False, False)
        
        # Design System (Baseado na referência moderna)
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
        self.profiles_file = os.path.join(self.config_dir, "profiles_v3.json")
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Caminhos do Minecraft
        self.base_minecraft_dir = os.path.expanduser("~/.aetherlauncher/minecraft")
        os.makedirs(self.base_minecraft_dir, exist_ok=True)
        
        # Estado Inicial
        self.downloading = False
        self.data = self.load_data()
        self.profiles = self.data.get("profiles", [
            {"name": "Latest Release", "version": "latest-release", "type": "Vanilla", "id": "p1"},
            {"name": "1.12.2 Forge", "version": "1.12.2", "type": "Forge", "id": "p2"}
        ])
        self.selected_profile_id = self.data.get("last_profile_id", self.profiles[0]["id"])
        self.username = self.data.get("username", "DragonSCP")
        
        self.setup_ui()
        
    def load_data(self):
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, 'r') as f:
                    return json.load(f)
            except: return {}
        return {}

    def save_data(self):
        data = {
            "username": self.username,
            "last_profile_id": self.selected_profile_id,
            "profiles": self.profiles
        }
        try:
            with open(self.profiles_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar: {e}")

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
        
        self.create_sidebar_btn("Configurações", "⚙", self.show_settings)
        self.create_sidebar_btn("Gerenciar Instalações", "+", self.show_edit_installation)
        
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
                                 activebackground="#963232", command=self.start_launch)
        self.play_btn.pack(fill="both", expand=True, pady=(10,0))
        
        self.version_subtext = tk.Label(self.play_section, text="", font=("Segoe UI", 8), 
                                      bg=self.colors["accent"], fg="white")
        self.version_subtext.pack(fill="x", pady=(0, 10))
        self.update_display()

        # --- CONTEÚDO ---
        self.banner_frame = tk.Frame(self.main_content, bg=self.colors["bg"], padx=40, pady=40)
        self.banner_frame.pack(fill="both", expand=True)
        
        # Imagem Central (Placeholder)
        self.img_box = tk.Frame(self.banner_frame, bg="#333", bd=0)
        self.img_box.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.85, relheight=0.6)
        
        # Barra de Progresso
        self.progress_container = tk.Frame(self.main_content, bg=self.colors["bg"], height=80)
        self.progress_container.pack(side="bottom", fill="x", padx=40, pady=20)
        
        self.progress_label = tk.Label(self.progress_container, text="Pronto", bg=self.colors["bg"], fg=self.colors["text_dim"], font=("Segoe UI", 9))
        self.progress_label.pack(anchor="w")
        
        self.progress_bar = ttk.Progressbar(self.progress_container, mode='determinate', length=100)
        self.progress_bar.pack(fill="x", pady=5)
        self.progress_container.pack_forget()

    def create_sidebar_btn(self, text, icon, command):
        f = tk.Frame(self.nav_frame, bg=self.colors["sidebar"], padx=20, pady=8)
        f.pack(fill="x")
        tk.Label(f, text=icon, font=("Segoe UI", 12), bg=self.colors["sidebar"], fg=self.colors["text_dim"], width=2).pack(side="left")
        tk.Label(f, text=text, font=("Segoe UI", 10), bg=self.colors["sidebar"], fg=self.colors["text"]).pack(side="left", padx=10)
        f.bind("<Button-1>", lambda e: command())
        for c in f.winfo_children(): c.bind("<Button-1>", lambda e: command())
        f.bind("<Enter>", lambda e: f.config(bg=self.colors["selected"]))
        f.bind("<Leave>", lambda e: f.config(bg=self.colors["sidebar"]))

    def refresh_profile_list(self):
        for w in self.profile_list_frame.winfo_children(): w.destroy()
        for p in self.profiles:
            sel = (p["id"] == self.selected_profile_id)
            bg = "#D0D0D0" if sel else self.colors["sidebar"]
            f = tk.Frame(self.profile_list_frame, bg=bg, padx=20, pady=8)
            f.pack(fill="x")
            canvas = tk.Canvas(f, width=20, height=20, bg="#5D8A3E", highlightthickness=0)
            canvas.pack(side="left")
            tk.Label(f, text=p["name"], font=("Segoe UI", 10), bg=bg, fg=self.colors["text"]).pack(side="left", padx=10)
            f.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))
            for c in f.winfo_children(): c.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))

    def select_profile(self, pid):
        self.selected_profile_id = pid
        self.update_display()
        self.refresh_profile_list()
        self.save_data()

    def update_display(self):
        p = next((x for x in self.profiles if x["id"] == self.selected_profile_id), self.profiles[0])
        self.version_subtext.config(text=f"{p['type']} {p['version']}")

    def show_settings(self):
        new_nick = filedialog.askstring("Ajustes", "Mudar Nickname:", initialvalue=self.username)
        if new_nick:
            self.username = new_nick
            self.user_lbl.config(text=self.username)
            self.save_data()

    def show_edit_installation(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Instalação")
        dialog.geometry("500x550")
        dialog.configure(bg="white")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Editar Instalação", font=("Segoe UI", 16, "bold"), bg="white", pady=20).pack()
        
        tk.Label(dialog, text="Nome da Instalação", bg="white", fg=self.colors["text_dim"], font=("Segoe UI", 9)).pack(anchor="w", padx=40)
        name_ent = tk.Entry(dialog, bg="#F0F0F0", bd=0, font=("Segoe UI", 11))
        name_ent.pack(fill="x", padx=40, pady=(5, 15), ipady=8)
        name_ent.insert(0, "Nova Instalação")

        tk.Label(dialog, text="Loader", bg="white", fg=self.colors["text_dim"], font=("Segoe UI", 9)).pack(anchor="w", padx=40)
        type_var = tk.StringVar(value="Vanilla")
        tf = tk.Frame(dialog, bg="white")
        tf.pack(fill="x", padx=40, pady=5)
        for t in ["Vanilla", "Forge", "Fabric"]:
            tk.Radiobutton(tf, text=t, variable=type_var, value=t, bg="white").pack(side="left", padx=10)

        tk.Label(dialog, text="Versão do Minecraft", bg="white", fg=self.colors["text_dim"], font=("Segoe UI", 9)).pack(anchor="w", padx=40)
        ver_ent = tk.Entry(dialog, bg="#F0F0F0", bd=0, font=("Segoe UI", 11))
        ver_ent.pack(fill="x", padx=40, pady=(5, 15), ipady=8)
        ver_ent.insert(0, "1.20.1")

        def save():
            p = {"name": name_ent.get(), "version": ver_ent.get(), "type": type_var.get(), "id": f"p_{os.urandom(3).hex()}"}
            self.profiles.append(p)
            self.select_profile(p["id"])
            dialog.destroy()

        tk.Button(dialog, text="SALVAR", bg=self.colors["accent"], fg="white", bd=0, font=("Segoe UI", 10, "bold"), padx=40, pady=10, command=save).pack(side="bottom", pady=30)

    def start_launch(self):
        if self.downloading: return
        self.downloading = True
        self.play_btn.config(state="disabled", text="BAIXANDO...")
        self.progress_container.pack(side="bottom", fill="x", padx=40, pady=20)
        threading.Thread(target=self.run_logic, daemon=True).start()

    def run_logic(self):
        try:
            p = next((x for x in self.profiles if x["id"] == self.selected_profile_id), self.profiles[0])
            vid = p["version"]
            if vid == "latest-release": vid = minecraft_launcher_lib.utils.get_latest_version()["release"]
            
            # Isolamento de Instância
            inst_dir = os.path.join(self.base_minecraft_dir, "instances", p["name"].replace(" ", "_"))
            os.makedirs(inst_dir, exist_ok=True)

            # Callbacks
            cb = {
                "setStatus": lambda t: self.root.after(0, lambda: self.progress_label.config(text=t)),
                "setProgress": lambda v: self.root.after(0, lambda: self.progress_bar.config(value=v)),
                "setMax": lambda v: self.root.after(0, lambda: self.progress_bar.config(maximum=v))
            }

            # 1. Download Java Automático
            self.root.after(0, lambda: self.progress_label.config(text="Verificando Java Runtime..."))
            # O launcher lib gerencia runtimes se configurado, mas vamos usar o nativo do sistema ou baixar se necessário
            # Para simplificar e garantir sucesso no Linux, usamos o java do sistema ou instalamos via lib
            
            # 2. Instalação Base
            self.root.after(0, lambda: self.progress_label.config(text=f"Baixando Minecraft {vid}..."))
            minecraft_launcher_lib.install.install_minecraft_version(vid, self.base_minecraft_dir, callback=cb)

            # 3. Mod Loaders
            final_vid = vid
            if p["type"] == "Fabric":
                self.root.after(0, lambda: self.progress_label.config(text="Instalando Fabric Loader..."))
                fab_v = minecraft_launcher_lib.fabric.get_latest_loader_version()
                minecraft_launcher_lib.fabric.install_fabric(vid, self.base_minecraft_dir, loader_version=fab_v, callback=cb)
                final_vid = minecraft_launcher_lib.fabric.get_fabric_version(vid, fab_v)
            elif p["type"] == "Forge":
                self.root.after(0, lambda: self.progress_label.config(text="Instalando Forge..."))
                forge_v = minecraft_launcher_lib.forge.find_forge_version(vid)
                if forge_v:
                    minecraft_launcher_lib.forge.install_forge_version(forge_v, self.base_minecraft_dir, callback=cb)
                    final_vid = forge_v

            # 4. Launch
            options = {
                "username": self.username,
                "uuid": "", "token": "",
                "gameDirectory": inst_dir, # Pasta isolada para mods/configs
                "launcherName": "AetherLauncher",
                "launcherVersion": "3.0"
            }
            
            self.root.after(0, lambda: self.progress_label.config(text="Abrindo Minecraft Nativo..."))
            cmd = minecraft_launcher_lib.command.get_minecraft_command(final_vid, self.base_minecraft_dir, options)
            
            self.root.after(0, lambda: self.progress_container.pack_forget())
            subprocess.run(cmd)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro no Launcher: {str(e)}"))
        finally:
            self.downloading = False
            self.root.after(0, lambda: self.play_btn.config(state="normal", text="JOGAR"))

if __name__ == "__main__":
    root = tk.Tk()
    app = AetherLauncherUI(root)
    root.mainloop()
