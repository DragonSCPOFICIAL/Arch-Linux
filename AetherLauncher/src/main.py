import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import threading
import subprocess
import ssl
from PIL import Image, ImageTk
import minecraft_launcher_lib
import utils

# Configurações globais
ssl._create_default_https_context = ssl._create_unverified_context

class AetherLauncherUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aether Launcher v3.4 - Minecraft Elite Linux (Nativo)")
        
        # Configuração de Janela
        window_width, window_height = 1050, 680
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{window_width}x{window_height}+{(sw-window_width)//2}+{(sh-window_height)//2}")
        self.root.resizable(False, False)
        
        # Cores e Estilos
        self.colors = {
            "accent": "#B43D3D",  
            "text": "#FFFFFF",
            "sidebar_bg": "#121212",
            "content_overlay": "#1a1a1a"
        }
        
        # Pastas
        self.config_dir = os.path.expanduser("~/.config/aetherlauncher")
        self.data_file = os.path.join(self.config_dir, "launcher_data.json")
        self.mc_dir = os.path.expanduser("~/.aetherlauncher/minecraft")
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)))
        
        self.load_launcher_data()
        self.downloading = False
        self.mc_versions = [] # Cache de versões
        
        self.setup_ui()
        threading.Thread(target=self.fetch_versions, daemon=True).start()
        
    def load_launcher_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            except: self.data = self.get_default_data()
        else:
            self.data = self.get_default_data()
        self.profiles = self.data.get("profiles", [])
        self.selected_pid = self.data.get("last_profile", "p_default")
        self.username = self.data.get("username", "DragonSCP")

    def get_default_data(self):
        return {
            "username": "DragonSCP",
            "last_profile": "p_default",
            "profiles": [
                {"name": "Minecraft 1.12.2", "version": "1.12.2", "type": "Vanilla", "id": "p_default", "compatibility_mode": True}
            ]
        }

    def save_launcher_data(self):
        self.data["profiles"] = self.profiles
        self.data["last_profile"] = self.selected_pid
        self.data["username"] = self.username
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def fetch_versions(self):
        try:
            versions = minecraft_launcher_lib.utils.get_version_list()
            self.mc_versions = [v['id'] for v in versions if v['type'] == 'release']
        except:
            self.mc_versions = ["1.20.1", "1.19.4", "1.18.2", "1.12.2", "1.8.9"]

    def setup_ui(self):
        # Canvas Principal para Fundo Total
        self.canvas = tk.Canvas(self.root, width=1050, height=680, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.load_background()
        
        # Sidebar Transparente/Escura
        self.canvas.create_rectangle(0, 0, 250, 680, fill="#000000", stipple="gray50", outline="")
        
        # Header Perfil
        self.canvas.create_text(85, 45, text="BEM-VINDO,", font=("Segoe UI", 7), fill="#ccc", anchor="w")
        self.nick_text = self.canvas.create_text(85, 60, text=self.username, font=("Segoe UI", 11, "bold"), fill="white", anchor="w")
        self.canvas.create_rectangle(25, 35, 70, 70, fill="#333", outline="#555")

        # Botões Sidebar
        self.create_sidebar_btn(100, "Configurações", "⚙", self.show_settings)
        self.create_sidebar_btn(140, "Gerenciar Instalações", "+", self.show_install)
        self.canvas.create_line(25, 185, 225, 185, fill="#444")

        # Frame de Perfis (Transparente)
        self.profiles_frame = tk.Frame(self.root, bg="#121212", bd=0)
        self.canvas.create_window(125, 390, window=self.profiles_frame, width=230, height=360, anchor="center")
        self.refresh_profiles_list()

        # Rodapé JOGAR
        self.footer = tk.Frame(self.root, bg=self.colors["accent"], bd=0)
        self.canvas.create_window(125, 635, window=self.footer, width=250, height=90, anchor="center")
        
        self.btn_play = tk.Button(self.footer, text="JOGAR", font=("Segoe UI", 18, "bold"), 
                                 bg=self.colors["accent"], fg="white", bd=0, cursor="hand2",
                                 activebackground="#963232", command=self.launch_game)
        self.btn_play.pack(fill="both", expand=True, pady=(10,0))
        
        self.lbl_ver_info = tk.Label(self.footer, text="", font=("Segoe UI", 8), bg=self.colors["accent"], fg="white")
        self.lbl_ver_info.pack(fill="x", pady=(0, 10))
        self.update_selection_ui()

        # Área de Conteúdo Central (Transparente por padrão)
        self.content_container = tk.Frame(self.root, bg="", bd=0)
        self.content_window = self.canvas.create_window(650, 340, window=self.content_container, width=750, height=600, anchor="center")
        self.show_home()

    def load_background(self):
        bg_path = os.path.join(self.assets_dir, "background.png")
        if os.path.exists(bg_path):
            try:
                img = Image.open(bg_path).resize((1050, 680), Image.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
                self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
            except: self.canvas.config(bg="#1a1a1a")
        else: self.canvas.config(bg="#1a1a1a")

    def create_sidebar_btn(self, y, text, icon, cmd):
        txt_id = self.canvas.create_text(40, y, text=f"{icon}  {text}", font=("Segoe UI", 10, "bold"), fill="white", anchor="w")
        rect = self.canvas.create_rectangle(10, y-15, 240, y+15, fill="", outline="")
        self.canvas.tag_bind(txt_id, "<Button-1>", lambda e: cmd())
        self.canvas.tag_bind(rect, "<Button-1>", lambda e: cmd())

    def refresh_profiles_list(self):
        for w in self.profiles_frame.winfo_children(): w.destroy()
        self.profiles_frame.config(bg="#121212")
        for p in self.profiles:
            is_sel = (p["id"] == self.selected_pid)
            bg = "#333" if is_sel else "#121212"
            f = tk.Frame(self.profiles_frame, bg=bg, padx=10, pady=6)
            f.pack(fill="x", pady=2)
            tk.Canvas(f, width=16, height=16, bg="#5D8A3E" if is_sel else "#555", highlightthickness=0).pack(side="left")
            lbl = tk.Label(f, text=p["name"], font=("Segoe UI", 9), bg=bg, fg="white")
            lbl.pack(side="left", padx=8)
            if p["id"] != "p_default":
                del_btn = tk.Label(f, text="🗑", font=("Segoe UI", 9), bg=bg, fg="#666", cursor="hand2")
                del_btn.pack(side="right")
                del_btn.bind("<Button-1>", lambda e, pid=p["id"]: self.delete_profile(pid))
            f.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))
            lbl.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))

    def delete_profile(self, pid):
        if messagebox.askyesno("Confirmar", "Apagar instalação?"):
            self.profiles = [p for p in self.profiles if p["id"] != pid]
            if self.selected_pid == pid: self.selected_pid = "p_default"
            self.save_launcher_data()
            self.refresh_profiles_list()
            self.update_selection_ui()

    def select_profile(self, pid):
        self.selected_pid = pid
        self.update_selection_ui()
        self.refresh_profiles_list()
        self.save_launcher_data()
        self.show_home()

    def update_selection_ui(self):
        p = next((x for x in self.profiles if x["id"] == self.selected_pid), self.profiles[0])
        self.lbl_ver_info.config(text=f"{p['type']} {p['version']}")

    # --- TELAS ---
    def show_home(self):
        for w in self.content_container.winfo_children(): w.destroy()
        self.content_container.config(bg="") # Transparente
        
        # Texto sem fundo branco
        tk.Label(self.content_container, text="BEM-VINDO AO AETHER LINUX", font=("Segoe UI", 22, "bold"), fg="white", bg="#1a1a1a").pack(pady=(60, 20))
        
        # News Box com fundo escuro semi-transparente
        news = tk.Frame(self.content_container, bg="#000000", padx=20, pady=10)
        news.pack(fill="x", padx=100)
        tk.Label(news, text="Aether Launcher: Performance Nativa Ativada", font=("Segoe UI", 10), bg="#000000", fg="#ccc").pack()
        
        self.prog_ui = tk.Frame(self.content_container, bg="#000000", padx=20, pady=15)
        self.prog_ui.pack(side="bottom", fill="x", padx=100, pady=60)
        self.prog_lbl = tk.Label(self.prog_ui, text="Pronto", bg="#000000", fg="#888", font=("Segoe UI", 9))
        self.prog_lbl.pack(anchor="w")
        self.prog_bar = ttk.Progressbar(self.prog_ui, mode='determinate')
        self.prog_bar.pack(fill="x", pady=5)
        if not self.downloading: self.prog_ui.pack_forget()

    def show_settings(self):
        for w in self.content_container.winfo_children(): w.destroy()
        self.content_container.config(bg="#1a1a1a")
        
        tk.Label(self.content_container, text="CONFIGURAÇÕES", font=("Segoe UI", 18, "bold"), bg="#1a1a1a", fg="white").pack(pady=40)
        
        tk.Label(self.content_container, text="Nickname do Jogador", bg="#1a1a1a", fg="#aaa").pack(anchor="w", padx=150)
        e_nick = tk.Entry(self.content_container, font=("Segoe UI", 12), bg="#333", fg="white", bd=0, insertbackground="white")
        e_nick.pack(fill="x", padx=150, pady=10, ipady=8)
        e_nick.insert(0, self.username)
        
        def save():
            self.username = e_nick.get().strip()
            self.canvas.itemconfig(self.nick_text, text=self.username)
            self.save_launcher_data()
            self.show_home()
            
        tk.Button(self.content_container, text="SALVAR", bg=self.colors["accent"], fg="white", bd=0, 
                 font=("Segoe UI", 10, "bold"), padx=40, pady=10, command=save).pack(pady=40)

    def show_install(self):
        for w in self.content_container.winfo_children(): w.destroy()
        self.content_container.config(bg="#1a1a1a")
        
        tk.Label(self.content_container, text="GERENCIAR INSTALAÇÕES", font=("Segoe UI", 18, "bold"), bg="#1a1a1a", fg="white").pack(pady=40)
        
        container = tk.Frame(self.content_container, bg="#1a1a1a")
        container.pack(fill="both", expand=True, padx=150)
        
        tk.Label(container, text="Nome da Instalação", bg="#1a1a1a", fg="#aaa").pack(anchor="w")
        e_name = tk.Entry(container, bg="#333", fg="white", bd=0, font=("Segoe UI", 11), insertbackground="white")
        e_name.pack(fill="x", pady=(5, 15), ipady=8)
        e_name.insert(0, "Nova Versão")

        tk.Label(container, text="Versão do Minecraft", bg="#1a1a1a", fg="#aaa").pack(anchor="w")
        
        # COMBOBOX COM VERSÕES REAIS
        v_list = ttk.Combobox(container, values=self.mc_versions, state="readonly", font=("Segoe UI", 11))
        v_list.pack(fill="x", pady=(5, 15), ipady=5)
        if self.mc_versions: v_list.set(self.mc_versions[0])

        tk.Label(container, text="Mod Loader", bg="#1a1a1a", fg="#aaa").pack(anchor="w")
        type_var = tk.StringVar(value="Vanilla")
        tf = tk.Frame(container, bg="#1a1a1a")
        tf.pack(fill="x", pady=10)
        for t in ["Vanilla", "Forge", "Fabric"]:
            tk.Radiobutton(tf, text=t, variable=type_var, value=t, bg="#1a1a1a", fg="white", selectcolor="#333").pack(side="left", padx=(0, 15))

        def create():
            name, ver = e_name.get().strip(), v_list.get()
            if not name or not ver: return
            new_p = {"name": name, "version": ver, "type": type_var.get(), "id": f"p_{os.urandom(3).hex()}", "compatibility_mode": True}
            self.profiles.append(new_p)
            self.select_profile(new_p["id"])
            
        tk.Button(container, text="CRIAR INSTALAÇÃO", bg=self.colors["accent"], fg="white", bd=0, 
                 font=("Segoe UI", 11, "bold"), pady=12, command=create).pack(side="bottom", fill="x", pady=40)

    def launch_game(self):
        if self.downloading: return
        self.show_home()
        self.downloading = True
        self.btn_play.config(state="disabled", text="INICIANDO...")
        self.prog_ui.pack(side="bottom", fill="x", padx=100, pady=60)
        threading.Thread(target=self.engine_run, daemon=True).start()

    def engine_run(self):
        try:
            p = next((x for x in self.profiles if x["id"] == self.selected_pid), self.profiles[0])
            vid = p["version"]
            inst_path = utils.get_instance_path(self.mc_dir, p["name"])
            cb = {
                "setStatus": lambda t: self.root.after(0, lambda: self.prog_lbl.config(text=t)),
                "setProgress": lambda v: self.root.after(0, lambda: self.prog_bar.config(value=v)),
                "setMax": lambda v: self.root.after(0, lambda: self.prog_bar.config(maximum=v))
            }
            minecraft_launcher_lib.install.install_minecraft_version(vid, self.mc_dir, callback=cb)
            
            final_vid = vid
            if p["type"] == "Fabric":
                fv = minecraft_launcher_lib.fabric.get_latest_loader_version()
                minecraft_launcher_lib.fabric.install_fabric(vid, self.mc_dir, loader_version=fv, callback=cb)
                final_vid = minecraft_launcher_lib.fabric.get_fabric_version(vid, fv)
            elif p["type"] == "Forge":
                fv = minecraft_launcher_lib.forge.find_forge_version(vid)
                if fv:
                    minecraft_launcher_lib.forge.install_forge_version(fv, self.mc_dir, callback=cb)
                    final_vid = fv

            options = {"username": self.username, "uuid": "", "token": "", "gameDirectory": inst_path, "launcherName": "AetherLauncher", "launcherVersion": "3.4"}
            env = utils.get_compatibility_env() if p.get("compatibility_mode", True) else os.environ.copy()
            cmd = minecraft_launcher_lib.command.get_minecraft_command(final_vid, self.mc_dir, options)
            self.root.after(0, lambda: self.prog_ui.pack_forget())
            subprocess.run(cmd, env=env)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", str(e)))
        finally:
            self.downloading = False
            self.root.after(0, lambda: self.btn_play.config(state="normal", text="JOGAR"))

if __name__ == "__main__":
    root = tk.Tk()
    app = AetherLauncherUI(root)
    root.mainloop()
