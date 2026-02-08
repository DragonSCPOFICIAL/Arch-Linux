import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
        self.root.title("Aether Launcher v3.2 - Minecraft Elite Linux (Nativo)")
        
        # Configuração de Janela
        window_width, window_height = 1050, 680
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{window_width}x{window_height}+{(sw-window_width)//2}+{(sh-window_height)//2}")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        
        # Design System
        self.colors = {
            "bg": "#EAEAEA",      
            "sidebar": "#FFFFFF", 
            "accent": "#B43D3D",  
            "text": "#333333",
            "text_dim": "#666666",
            "border": "#DDDDDD",
            "hover": "#F5F5F5"
        }
        
        # Pastas
        self.config_dir = os.path.expanduser("~/.config/aetherlauncher")
        self.data_file = os.path.join(self.config_dir, "launcher_data.json")
        self.mc_dir = os.path.expanduser("~/.aetherlauncher/minecraft")
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)))
        
        self.load_launcher_data()
        self.downloading = False
        self.setup_ui()
        
    def load_launcher_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            except: self.data = self.get_default_data()
        else:
            self.data = self.get_default_data()
        self.profiles = self.data["profiles"]
        self.selected_pid = self.data["last_profile"]
        self.username = self.data["username"]

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

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=250, bd=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Área Principal
        self.main = tk.Frame(self.root, bg=self.colors["bg"])
        self.main.pack(side="right", fill="both", expand=True)
        
        # --- BACKGROUND TOTAL NA ÁREA PRINCIPAL ---
        self.bg_label = tk.Label(self.main, bg=self.colors["bg"], bd=0)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.load_full_background()

        # --- COMPONENTES SIDEBAR ---
        p_header = tk.Frame(self.sidebar, bg=self.colors["sidebar"], pady=20, padx=20)
        p_header.pack(fill="x")
        
        self.avatar_label = tk.Label(p_header, bg="#333", width=5, height=2)
        self.avatar_label.pack(side="left")
        self.load_image_into_label(os.path.join(self.assets_dir, "icon.png"), self.avatar_label, (40, 40))
        
        u_info = tk.Frame(p_header, bg=self.colors["sidebar"], padx=10)
        u_info.pack(side="left", fill="x")
        tk.Label(u_info, text="BEM-VINDO,", font=("Segoe UI", 7), bg=self.colors["sidebar"], fg=self.colors["text_dim"]).pack(anchor="w")
        self.u_name_lbl = tk.Label(u_info, text=self.username, font=("Segoe UI", 10, "bold"), bg=self.colors["sidebar"], fg=self.colors["text"])
        self.u_name_lbl.pack(anchor="w")

        self.nav = tk.Frame(self.sidebar, bg=self.colors["sidebar"], pady=10)
        self.nav.pack(fill="both", expand=True)
        
        self.create_nav_item("Configurações", "⚙", self.open_settings)
        self.create_nav_item("Gerenciar Instalações", "+", self.open_profile_editor)
        
        tk.Frame(self.nav, bg=self.colors["border"], height=1).pack(fill="x", pady=10, padx=20)
        
        self.inst_list = tk.Frame(self.nav, bg=self.colors["sidebar"])
        self.inst_list.pack(fill="both", expand=True)
        self.refresh_profiles()
        
        self.footer = tk.Frame(self.sidebar, bg=self.colors["accent"], height=85)
        self.footer.pack(side="bottom", fill="x")
        
        self.btn_play = tk.Button(self.footer, text="JOGAR", font=("Segoe UI", 16, "bold"), 
                                 bg=self.colors["accent"], fg="white", bd=0, cursor="hand2",
                                 activebackground="#963232", command=self.launch_game)
        self.btn_play.pack(fill="both", expand=True, pady=(10,0))
        
        self.lbl_ver_info = tk.Label(self.footer, text="", font=("Segoe UI", 8), bg=self.colors["accent"], fg="white")
        self.lbl_ver_info.pack(fill="x", pady=(0, 10))
        self.update_selection_ui()

        # --- COMPONENTES SOBRE O BACKGROUND ---
        self.news = tk.Frame(self.main, bg="white", bd=0)
        self.news.place(relx=0.5, rely=0.1, anchor="center", relwidth=0.85, height=40)
        tk.Label(self.news, text="Aether Launcher: Performance Nativa Ativada", bg="white", fg=self.colors["text"]).pack(pady=8)

        self.prog_box = tk.Frame(self.main, bg="#FFFFFF", bd=1, relief="flat")
        self.prog_box.place(relx=0.5, rely=0.9, anchor="center", relwidth=0.85, height=60)
        self.prog_lbl = tk.Label(self.prog_box, text="Pronto", bg="white", fg=self.colors["text_dim"], font=("Segoe UI", 9))
        self.prog_lbl.pack(anchor="w", padx=10, pady=(5,0))
        self.prog_bar = ttk.Progressbar(self.prog_box, mode='determinate', length=100)
        self.prog_bar.pack(fill="x", padx=10, pady=5)
        self.prog_box.place_forget()

    def load_full_background(self):
        bg_path = os.path.join(self.assets_dir, "background.png")
        if os.path.exists(bg_path):
            try:
                img = Image.open(bg_path).resize((800, 680), Image.LANCZOS)
                self.full_bg = ImageTk.PhotoImage(img)
                self.bg_label.config(image=self.full_bg)
            except: pass

    def load_image_into_label(self, path, label, size):
        try:
            if os.path.exists(path):
                img = Image.open(path).resize(size, Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                label.config(image=photo, bg=self.colors["sidebar"])
                label.image = photo
        except: pass

    def create_nav_item(self, text, icon, cmd):
        f = tk.Frame(self.nav, bg=self.colors["sidebar"], padx=20, pady=8)
        f.pack(fill="x")
        tk.Label(f, text=icon, font=("Segoe UI", 12), bg=self.colors["sidebar"], fg=self.colors["text_dim"], width=2).pack(side="left")
        tk.Label(f, text=text, font=("Segoe UI", 10), bg=self.colors["sidebar"], fg=self.colors["text"]).pack(side="left", padx=10)
        f.bind("<Button-1>", lambda e: cmd())
        for c in f.winfo_children(): c.bind("<Button-1>", lambda e: cmd())
        f.bind("<Enter>", lambda e: f.config(bg=self.colors["hover"]))
        f.bind("<Leave>", lambda e: f.config(bg=self.colors["sidebar"]))

    def refresh_profiles(self):
        for w in self.inst_list.winfo_children(): w.destroy()
        for p in self.profiles:
            is_sel = (p["id"] == self.selected_pid)
            bg = "#D0D0D0" if is_sel else self.colors["sidebar"]
            f = tk.Frame(self.inst_list, bg=bg, padx=20, pady=8)
            f.pack(fill="x")
            tk.Canvas(f, width=20, height=20, bg="#5D8A3E" if is_sel else "#777", highlightthickness=0).pack(side="left")
            tk.Label(f, text=p["name"], font=("Segoe UI", 10), bg=bg, fg=self.colors["text"]).pack(side="left", padx=10)
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
        nick = filedialog.askstring("Ajustes", "Mudar Nickname:", initialvalue=self.username)
        if nick:
            self.username = nick
            self.u_name_lbl.config(text=self.username)
            self.save_launcher_data()

    def open_profile_editor(self):
        # Janela de Nova Instalação - Refatorada para evitar tela branca
        ed = tk.Toplevel(self.root)
        ed.title("Nova Instalação")
        ed.geometry("480x550")
        ed.configure(bg="#FFFFFF")
        ed.transient(self.root)
        ed.grab_set()
        
        # Forçar atualização para garantir que a janela não fique branca
        ed.update_idletasks()
        
        container = tk.Frame(ed, bg="white", padx=30, pady=30)
        container.pack(fill="both", expand=True)
        
        tk.Label(container, text="Criar Nova Instalação", font=("Segoe UI", 16, "bold"), bg="white", fg=self.colors["text"]).pack(pady=(0, 20))
        
        # Nome
        tk.Label(container, text="Nome da Instalação", bg="white", fg=self.colors["text_dim"], font=("Segoe UI", 9)).pack(anchor="w")
        e_name = tk.Entry(container, bg="#F0F0F0", bd=0, font=("Segoe UI", 11))
        e_name.pack(fill="x", pady=(5, 20), ipady=8)
        e_name.insert(0, "Nova Instância")

        # Versão
        tk.Label(container, text="Versão do Minecraft (ex: 1.20.1)", bg="white", fg=self.colors["text_dim"], font=("Segoe UI", 9)).pack(anchor="w")
        e_ver = tk.Entry(container, bg="#F0F0F0", bd=0, font=("Segoe UI", 11))
        e_ver.pack(fill="x", pady=(5, 20), ipady=8)
        e_ver.insert(0, "1.20.1")

        # Loader
        tk.Label(container, text="Mod Loader", bg="white", fg=self.colors["text_dim"], font=("Segoe UI", 9)).pack(anchor="w")
        type_var = tk.StringVar(value="Vanilla")
        tf = tk.Frame(container, bg="white")
        tf.pack(fill="x", pady=10)
        for t in ["Vanilla", "Forge", "Fabric"]:
            tk.Radiobutton(tf, text=t, variable=type_var, value=t, bg="white", font=("Segoe UI", 10)).pack(side="left", padx=(0, 15))

        def save_profile():
            name = e_name.get().strip()
            ver = e_ver.get().strip()
            if not name or not ver:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            new_p = {
                "name": name,
                "version": ver,
                "type": type_var.get(),
                "id": f"p_{os.urandom(3).hex()}",
                "compatibility_mode": True
            }
            self.profiles.append(new_p)
            self.select_profile(new_p["id"])
            ed.destroy()

        btn_save = tk.Button(container, text="SALVAR INSTALAÇÃO", bg=self.colors["accent"], fg="white", bd=0, 
                             font=("Segoe UI", 11, "bold"), cursor="hand2", command=save_profile)
        btn_save.pack(side="bottom", fill="x", ipady=12, pady=20)

    def launch_game(self):
        if self.downloading: return
        self.downloading = True
        self.btn_play.config(state="disabled", text="INICIANDO...")
        self.prog_box.place(relx=0.5, rely=0.9, anchor="center", relwidth=0.85, height=60)
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

            options = {"username": self.username, "uuid": "", "token": "", "gameDirectory": inst_path, "launcherName": "AetherLauncher", "launcherVersion": "3.2"}
            env = utils.get_compatibility_env() if p.get("compatibility_mode", True) else os.environ.copy()
            cmd = minecraft_launcher_lib.command.get_minecraft_command(final_vid, self.mc_dir, options)
            self.root.after(0, lambda: self.prog_box.place_forget())
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
