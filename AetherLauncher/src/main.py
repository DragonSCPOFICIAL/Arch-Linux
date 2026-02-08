import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import threading
import subprocess
import ssl
from PIL import Image, ImageTk
import minecraft_launcher_lib
import utils # Nosso novo módulo

# Configurações globais
ssl._create_default_https_context = ssl._create_unverified_context

class AetherLauncherUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aether Launcher v3.0 - Minecraft Elite Linux (Nativo)")
        
        # Configuração de Janela
        window_width, window_height = 1050, 680
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{window_width}x{window_height}+{(sw-window_width)//2}+{(sh-window_height)//2}")
        self.root.configure(bg="#F5F5F5")
        self.root.resizable(False, False)
        
        # Design System Expandido
        self.colors = {
            "bg": "#F5F5F5",      
            "sidebar": "#FFFFFF", 
            "accent": "#B43D3D",  
            "text": "#2C3E50",
            "text_dim": "#7F8C8D",
            "border": "#E0E0E0",
            "hover": "#F8F9FA",
            "success": "#27AE60"
        }
        
        # Estrutura de Pastas e Dados
        self.config_dir = os.path.expanduser("~/.config/aetherlauncher")
        self.data_file = os.path.join(self.config_dir, "launcher_data.json")
        self.mc_dir = os.path.expanduser("~/.aetherlauncher/minecraft")
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.mc_dir, exist_ok=True)
        
        # Carregamento de Dados
        self.load_launcher_data()
        
        self.downloading = False
        self.setup_ui()
        
    def load_launcher_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "username": "DragonSCP",
                "last_profile": "p_default",
                "profiles": [
                    {"name": "Minecraft 1.12.2", "version": "1.12.2", "type": "Vanilla", "id": "p_default", "compatibility_mode": True}
                ],
                "settings": {"ram": "2G", "auto_compatibility": True}
            }
        self.profiles = self.data["profiles"]
        self.selected_pid = self.data["last_profile"]
        self.username = self.data["username"]

    def save_launcher_data(self):
        self.data["profiles"] = self.profiles
        self.data["last_profile"] = self.selected_pid
        self.data["username"] = self.username
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=260, bd=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Divisor Sutil
        tk.Frame(self.root, bg=self.colors["border"], width=1).pack(side="left", fill="y")
        
        # Área Principal
        self.main = tk.Frame(self.root, bg=self.colors["bg"])
        self.main.pack(side="right", fill="both", expand=True)
        
        # --- COMPONENTES SIDEBAR ---
        # Header Perfil
        p_header = tk.Frame(self.sidebar, bg=self.colors["sidebar"], pady=25, padx=20)
        p_header.pack(fill="x")
        self.avatar = tk.Canvas(p_header, width=45, height=45, bg="#34495E", highlightthickness=0)
        self.avatar.pack(side="left")
        
        u_info = tk.Frame(p_header, bg=self.colors["sidebar"], padx=12)
        u_info.pack(side="left", fill="x")
        tk.Label(u_info, text="BEM-VINDO,", font=("Segoe UI", 7, "bold"), bg=self.colors["sidebar"], fg=self.colors["text_dim"]).pack(anchor="w")
        self.u_name_lbl = tk.Label(u_info, text=self.username, font=("Segoe UI", 11, "bold"), bg=self.colors["sidebar"], fg=self.colors["text"])
        self.u_name_lbl.pack(anchor="w")

        # Navegação
        self.nav = tk.Frame(self.sidebar, bg=self.colors["sidebar"])
        self.nav.pack(fill="both", expand=True)
        
        self.add_nav_item("Configurações", "⚙", self.open_settings)
        self.add_nav_item("Gerenciar Instalações", "+", self.open_profile_editor)
        
        tk.Frame(self.nav, bg=self.colors["border"], height=1).pack(fill="x", pady=15, padx=25)
        
        # Lista de Instalações
        self.inst_list = tk.Frame(self.nav, bg=self.colors["sidebar"])
        self.inst_list.pack(fill="both", expand=True)
        self.refresh_profiles()
        
        # Rodapé JOGAR
        self.footer = tk.Frame(self.sidebar, bg=self.colors["accent"], height=90)
        self.footer.pack(side="bottom", fill="x")
        
        self.btn_play = tk.Button(self.footer, text="JOGAR", font=("Segoe UI", 18, "bold"), 
                                 bg=self.colors["accent"], fg="white", bd=0, cursor="hand2",
                                 activebackground="#922B2B", command=self.launch_game)
        self.btn_play.pack(fill="both", expand=True, pady=(12,0))
        
        self.lbl_ver_info = tk.Label(self.footer, text="", font=("Segoe UI", 8), bg=self.colors["accent"], fg="white")
        self.lbl_ver_info.pack(fill="x", pady=(0, 12))
        self.update_selection_ui()

        # --- COMPONENTES PRINCIPAIS ---
        # Banner de Destaque
        self.banner = tk.Frame(self.main, bg="#2C3E50", bd=0)
        self.banner.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.9, relheight=0.6)
        
        # News/Status Box
        self.news = tk.Frame(self.main, bg="white", bd=1, relief="flat")
        self.news.place(relx=0.5, rely=0.08, anchor="center", relwidth=0.9, height=45)
        tk.Label(self.news, text="Aether Launcher: Performance Nativa Linux Ativada", font=("Segoe UI", 9), bg="white", fg=self.colors["text"]).pack(pady=12)

        # Barra de Progresso Avançada
        self.prog_box = tk.Frame(self.main, bg=self.colors["bg"])
        self.prog_box.pack(side="bottom", fill="x", padx=50, pady=30)
        
        self.prog_lbl = tk.Label(self.prog_box, text="Sistema Pronto", bg=self.colors["bg"], fg=self.colors["text_dim"], font=("Segoe UI", 9))
        self.prog_lbl.pack(anchor="w")
        
        style = ttk.Style()
        style.configure("Aether.Horizontal.TProgressbar", thickness=10, bordercolor=self.colors["border"], lightcolor=self.colors["accent"], pcolor=self.colors["accent"])
        self.prog_bar = ttk.Progressbar(self.prog_box, mode='determinate', style="Aether.Horizontal.TProgressbar")
        self.prog_bar.pack(fill="x", pady=8)
        self.prog_box.pack_forget()

    def add_nav_item(self, text, icon, cmd):
        f = tk.Frame(self.nav, bg=self.colors["sidebar"], padx=25, pady=10)
        f.pack(fill="x")
        tk.Label(f, text=icon, font=("Segoe UI", 13), bg=self.colors["sidebar"], fg=self.colors["text_dim"], width=3).pack(side="left")
        tk.Label(f, text=text, font=("Segoe UI", 10, "bold"), bg=self.colors["sidebar"], fg=self.colors["text"]).pack(side="left", padx=10)
        f.bind("<Button-1>", lambda e: cmd())
        for c in f.winfo_children(): c.bind("<Button-1>", lambda e: cmd())
        f.bind("<Enter>", lambda e: f.config(bg=self.colors["hover"]))
        f.bind("<Leave>", lambda e: f.config(bg=self.colors["sidebar"]))

    def refresh_profiles(self):
        for w in self.inst_list.winfo_children(): w.destroy()
        for p in self.profiles:
            is_sel = (p["id"] == self.selected_pid)
            bg = "#F0F0F0" if is_sel else self.colors["sidebar"]
            f = tk.Frame(self.inst_list, bg=bg, padx=25, pady=12)
            f.pack(fill="x")
            # Ícone de bloco
            tk.Canvas(f, width=22, height=22, bg="#5D8A3E", highlightthickness=0).pack(side="left")
            tk.Label(f, text=p["name"], font=("Segoe UI", 10), bg=bg, fg=self.colors["text"]).pack(side="left", padx=12)
            f.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))
            for c in f.winfo_children(): c.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))

    def select_profile(self, pid):
        self.selected_pid = pid
        self.update_selection_ui()
        self.refresh_profiles()
        self.save_launcher_data()

    def update_selection_ui(self):
        p = next((x for x in self.profiles if x["id"] == self.selected_pid), self.profiles[0])
        self.lbl_ver_info.config(text=f"{p['type']} {p['version']}")

    def open_settings(self):
        nick = filedialog.askstring("Ajustes", "Nickname do Jogador:", initialvalue=self.username)
        if nick:
            self.username = nick
            self.u_name_lbl.config(text=self.username)
            self.save_launcher_data()

    def open_profile_editor(self):
        ed = tk.Toplevel(self.root)
        ed.title("Nova Instalação")
        ed.geometry("520x580")
        ed.configure(bg="white")
        ed.transient(self.root)
        ed.grab_set()

        tk.Label(ed, text="Configurar Instalação", font=("Segoe UI", 18, "bold"), bg="white", pady=25).pack()
        
        # Campos
        tk.Label(ed, text="Nome da Instalação", bg="white", fg=self.colors["text_dim"], font=("Segoe UI", 9)).pack(anchor="w", padx=45)
        e_name = tk.Entry(ed, bg="#F7F9FB", bd=0, font=("Segoe UI", 11))
        e_name.pack(fill="x", padx=45, pady=(5, 15), ipady=10)
        e_name.insert(0, "Nova Instância")

        tk.Label(ed, text="Versão do Minecraft", bg="white", fg=self.colors["text_dim"], font=("Segoe UI", 9)).pack(anchor="w", padx=45)
        e_ver = tk.Entry(ed, bg="#F7F9FB", bd=0, font=("Segoe UI", 11))
        e_ver.pack(fill="x", padx=45, pady=(5, 15), ipady=10)
        e_ver.insert(0, "1.20.1")

        tk.Label(ed, text="Mod Loader", bg="white", fg=self.colors["text_dim"], font=("Segoe UI", 9)).pack(anchor="w", padx=45)
        t_var = tk.StringVar(value="Vanilla")
        tf = tk.Frame(ed, bg="white")
        tf.pack(fill="x", padx=45, pady=5)
        for t in ["Vanilla", "Forge", "Fabric"]:
            tk.Radiobutton(tf, text=t, variable=t_var, value=t, bg="white", font=("Segoe UI", 10)).pack(side="left", padx=10)

        # Opção de Compatibilidade
        c_var = tk.BooleanVar(value=True)
        tk.Checkbutton(ed, text="Modo de Compatibilidade (Hardware Antigo)", variable=c_var, bg="white", font=("Segoe UI", 9)).pack(anchor="w", padx=45, pady=10)

        def save():
            new_p = {
                "name": e_name.get(),
                "version": e_ver.get(),
                "type": t_var.get(),
                "id": f"p_{os.urandom(4).hex()}",
                "compatibility_mode": c_var.get()
            }
            self.profiles.append(new_p)
            self.select_profile(new_p["id"])
            ed.destroy()

        tk.Button(ed, text="CRIAR INSTALAÇÃO", bg=self.colors["accent"], fg="white", bd=0, font=("Segoe UI", 11, "bold"), padx=50, pady=12, command=save).pack(side="bottom", pady=40)

    def launch_game(self):
        if self.downloading: return
        self.downloading = True
        self.btn_play.config(state="disabled", text="INICIANDO...")
        self.prog_box.pack(side="bottom", fill="x", padx=50, pady=30)
        threading.Thread(target=self.engine_run, daemon=True).start()

    def engine_run(self):
        try:
            p = next((x for x in self.profiles if x["id"] == self.selected_pid), self.profiles[0])
            vid = p["version"]
            
            # 1. Preparar Instância Isolada
            inst_path = utils.get_instance_path(self.mc_dir, p["name"])
            
            # Callbacks
            cb = {
                "setStatus": lambda t: self.root.after(0, lambda: self.prog_lbl.config(text=t)),
                "setProgress": lambda v: self.root.after(0, lambda: self.prog_bar.config(value=v)),
                "setMax": lambda v: self.root.after(0, lambda: self.prog_bar.config(maximum=v))
            }

            # 2. Instalação Base e Loader
            self.root.after(0, lambda: self.prog_lbl.config(text=f"Sincronizando Minecraft {vid}..."))
            minecraft_launcher_lib.install.install_minecraft_version(vid, self.mc_dir, callback=cb)
            
            final_vid = vid
            if p["type"] == "Fabric":
                self.root.after(0, lambda: self.prog_lbl.config(text="Integrando Fabric..."))
                fv = minecraft_launcher_lib.fabric.get_latest_loader_version()
                minecraft_launcher_lib.fabric.install_fabric(vid, self.mc_dir, loader_version=fv, callback=cb)
                final_vid = minecraft_launcher_lib.fabric.get_fabric_version(vid, fv)
            elif p["type"] == "Forge":
                self.root.after(0, lambda: self.prog_lbl.config(text="Integrando Forge..."))
                fv = minecraft_launcher_lib.forge.find_forge_version(vid)
                if fv:
                    minecraft_launcher_lib.forge.install_forge_version(fv, self.mc_dir, callback=cb)
                    final_vid = fv

            # 3. Configurações de Lançamento
            options = {
                "username": self.username,
                "uuid": "", "token": "",
                "gameDirectory": inst_path,
                "launcherName": "AetherLauncher",
                "launcherVersion": "3.0",
                "jvmArguments": ["-Xmx2G", "-Xms1G"]
            }
            
            # 4. Modo de Compatibilidade (O diferencial do nosso Launcher)
            env = os.environ.copy()
            if p.get("compatibility_mode", True):
                self.root.after(0, lambda: self.prog_lbl.config(text="Ativando Engine de Compatibilidade Linux..."))
                env = utils.get_compatibility_env()

            # 5. Execução
            cmd = minecraft_launcher_lib.command.get_minecraft_command(final_vid, self.mc_dir, options)
            self.root.after(0, lambda: self.prog_box.pack_forget())
            
            # Rodar processo com ambiente de compatibilidade
            subprocess.run(cmd, env=env)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro Crítico", f"Falha no Engine: {str(e)}"))
        finally:
            self.downloading = False
            self.root.after(0, lambda: self.btn_play.config(state="normal", text="JOGAR"))

if __name__ == "__main__":
    root = tk.Tk()
    app = AetherLauncherUI(root)
    root.mainloop()
