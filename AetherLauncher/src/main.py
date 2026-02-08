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
        self.root.title("Aether Launcher v3.3 - Minecraft Elite Linux (Nativo)")
        
        # Configuração de Janela
        window_width, window_height = 1050, 680
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{window_width}x{window_height}+{(sw-window_width)//2}+{(sh-window_height)//2}")
        self.root.resizable(False, False)
        
        # Cores e Estilos
        self.colors = {
            "accent": "#B43D3D",  
            "text": "#FFFFFF",
            "text_dark": "#333333",
            "sidebar_overlay": "rgba(0, 0, 0, 0.4)",
            "hover": "#444444"
        }
        
        # Pastas
        self.config_dir = os.path.expanduser("~/.config/aetherlauncher")
        self.data_file = os.path.join(self.config_dir, "launcher_data.json")
        self.mc_dir = os.path.expanduser("~/.aetherlauncher/minecraft")
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)))
        
        self.load_launcher_data()
        self.downloading = False
        self.current_screen = "home" # home, settings, install
        
        self.setup_ui()
        
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

    def setup_ui(self):
        # Canvas para Fundo Unificado
        self.canvas = tk.Canvas(self.root, width=1050, height=680, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Carregar Fundo
        self.load_background()
        
        # Sidebar Overlay (Semi-transparente)
        self.sidebar_bg = self.canvas.create_rectangle(0, 0, 250, 680, fill="#1a1a1a", stipple="gray50", outline="")
        
        # --- ELEMENTOS DA SIDEBAR ---
        # Perfil
        self.draw_sidebar_header()
        
        # Navegação
        self.create_sidebar_btn(100, "Configurações", "⚙", self.show_settings)
        self.create_sidebar_btn(140, "Gerenciar Instalações", "+", self.show_install)
        
        self.canvas.create_line(25, 190, 225, 190, fill="#444")
        
        # Lista de Perfis
        self.profiles_frame = tk.Frame(self.root, bg="#1a1a1a", bd=0)
        self.profiles_window = self.canvas.create_window(125, 400, window=self.profiles_frame, width=250, height=380, anchor="center")
        self.refresh_profiles_list()
        
        # Botão JOGAR
        self.footer = tk.Frame(self.root, bg=self.colors["accent"], bd=0)
        self.footer_window = self.canvas.create_window(125, 635, window=self.footer, width=250, height=90, anchor="center")
        
        self.btn_play = tk.Button(self.footer, text="JOGAR", font=("Segoe UI", 18, "bold"), 
                                 bg=self.colors["accent"], fg="white", bd=0, cursor="hand2",
                                 activebackground="#963232", command=self.launch_game)
        self.btn_play.pack(fill="both", expand=True, pady=(10,0))
        
        self.lbl_ver_info = tk.Label(self.footer, text="", font=("Segoe UI", 8), bg=self.colors["accent"], fg="white")
        self.lbl_ver_info.pack(fill="x", pady=(0, 10))
        self.update_selection_ui()

        # --- ÁREA DE CONTEÚDO CENTRAL ---
        self.content_frame = tk.Frame(self.root, bg="", bd=0)
        self.content_window = self.canvas.create_window(650, 340, window=self.content_frame, width=700, height=600, anchor="center")
        self.show_home()

    def load_background(self):
        bg_path = os.path.join(self.assets_dir, "background.png")
        if os.path.exists(bg_path):
            try:
                img = Image.open(bg_path).resize((1050, 680), Image.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
                self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
            except: self.canvas.config(bg="#2c3e50")
        else: self.canvas.config(bg="#2c3e50")

    def draw_sidebar_header(self):
        # Nickname e Avatar
        self.canvas.create_text(85, 45, text="BEM-VINDO,", font=("Segoe UI", 7), fill="#aaa", anchor="w")
        self.nick_text = self.canvas.create_text(85, 60, text=self.username, font=("Segoe UI", 11, "bold"), fill="white", anchor="w")
        # Placeholder Avatar
        self.canvas.create_rectangle(25, 35, 70, 70, fill="#333", outline="#555")

    def create_sidebar_btn(self, y, text, icon, cmd):
        btn_id = self.canvas.create_text(40, y, text=f"{icon}  {text}", font=("Segoe UI", 10, "bold"), fill="white", anchor="w")
        # Área clicável invisível
        rect = self.canvas.create_rectangle(0, y-15, 250, y+15, fill="", outline="")
        self.canvas.tag_bind(btn_id, "<Button-1>", lambda e: cmd())
        self.canvas.tag_bind(rect, "<Button-1>", lambda e: cmd())

    def refresh_profiles_list(self):
        for w in self.profiles_frame.winfo_children(): w.destroy()
        self.profiles_frame.config(bg="#1a1a1a")
        
        for p in self.profiles:
            is_sel = (p["id"] == self.selected_pid)
            bg = "#333" if is_sel else "#1a1a1a"
            f = tk.Frame(self.profiles_frame, bg=bg, padx=15, pady=8)
            f.pack(fill="x")
            
            # Ícone
            tk.Canvas(f, width=18, height=18, bg="#5D8A3E" if is_sel else "#555", highlightthickness=0).pack(side="left")
            
            # Nome
            lbl = tk.Label(f, text=p["name"], font=("Segoe UI", 10), bg=bg, fg="white")
            lbl.pack(side="left", padx=10)
            
            # Botão Deletar (Lixeira)
            if p["id"] != "p_default":
                del_btn = tk.Label(f, text="🗑", font=("Segoe UI", 10), bg=bg, fg="#888", cursor="hand2")
                del_btn.pack(side="right")
                del_btn.bind("<Button-1>", lambda e, pid=p["id"]: self.delete_profile(pid))
                del_btn.bind("<Enter>", lambda e, b=del_btn: b.config(fg="#B43D3D"))
                del_btn.bind("<Leave>", lambda e, b=del_btn: b.config(fg="#888"))

            f.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))
            lbl.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))

    def delete_profile(self, pid):
        if messagebox.askyesno("Confirmar", "Deseja realmente apagar esta instalação?"):
            self.profiles = [p for p in self.profiles if p["id"] != pid]
            if self.selected_pid == pid:
                self.selected_pid = "p_default"
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

    # --- NAVEGAÇÃO DE TELAS (INTEGRADA) ---
    def clear_content(self):
        for w in self.content_frame.winfo_children(): w.destroy()
        self.content_frame.config(bg="")

    def show_home(self):
        self.clear_content()
        self.current_screen = "home"
        
        # Título de Boas Vindas
        tk.Label(self.content_frame, text="BEM-VINDO AO AETHER LINUX", font=("Segoe UI", 24, "bold"), fg="white", bg="#2c3e50").pack(pady=(50, 20))
        
        # News Box
        news = tk.Frame(self.content_frame, bg="white", padx=20, pady=10)
        news.pack(fill="x", padx=50)
        tk.Label(news, text="Aether Launcher: Performance Nativa Ativada", font=("Segoe UI", 10), bg="white", fg="#333").pack()
        
        # Barra de Progresso (Sempre aqui, mas escondida se não baixando)
        self.prog_ui = tk.Frame(self.content_frame, bg="#1a1a1a", padx=20, pady=15)
        self.prog_ui.pack(side="bottom", fill="x", padx=50, pady=50)
        self.prog_lbl = tk.Label(self.prog_ui, text="Pronto para jogar", bg="#1a1a1a", fg="#aaa", font=("Segoe UI", 9))
        self.prog_lbl.pack(anchor="w")
        self.prog_bar = ttk.Progressbar(self.prog_ui, mode='determinate')
        self.prog_bar.pack(fill="x", pady=5)
        if not self.downloading: self.prog_ui.pack_forget()

    def show_settings(self):
        self.clear_content()
        self.current_screen = "settings"
        self.content_frame.config(bg="#ffffff")
        
        tk.Label(self.content_frame, text="CONFIGURAÇÕES", font=("Segoe UI", 18, "bold"), bg="white", fg="#333").pack(pady=30)
        
        tk.Label(self.content_frame, text="Nickname do Jogador", bg="white", fg="#666").pack(anchor="w", padx=100)
        e_nick = tk.Entry(self.content_frame, font=("Segoe UI", 12), bg="#f0f0f0", bd=0)
        e_nick.pack(fill="x", padx=100, pady=10, ipady=8)
        e_nick.insert(0, self.username)
        
        def save_settings():
            self.username = e_nick.get().strip()
            self.canvas.itemconfig(self.nick_text, text=self.username)
            self.save_launcher_data()
            messagebox.showinfo("Sucesso", "Configurações salvas!")
            self.show_home()
            
        tk.Button(self.content_frame, text="SALVAR", bg=self.colors["accent"], fg="white", bd=0, 
                 font=("Segoe UI", 10, "bold"), padx=40, pady=10, command=save_settings).pack(pady=30)

    def show_install(self):
        self.clear_content()
        self.current_screen = "install"
        self.content_frame.config(bg="#ffffff")
        
        tk.Label(self.content_frame, text="GERENCIAR INSTALAÇÕES", font=("Segoe UI", 18, "bold"), bg="white", fg="#333").pack(pady=30)
        
        container = tk.Frame(self.content_frame, bg="white")
        container.pack(fill="both", expand=True, padx=100)
        
        tk.Label(container, text="Nome da Instalação", bg="white", fg="#666").pack(anchor="w")
        e_name = tk.Entry(container, bg="#f0f0f0", bd=0, font=("Segoe UI", 11))
        e_name.pack(fill="x", pady=(5, 15), ipady=8)
        e_name.insert(0, "Nova Versão")

        tk.Label(container, text="Versão do Minecraft (ex: 1.20.1)", bg="white", fg="#666").pack(anchor="w")
        e_ver = tk.Entry(container, bg="#f0f0f0", bd=0, font=("Segoe UI", 11))
        e_ver.pack(fill="x", pady=(5, 15), ipady=8)
        e_ver.insert(0, "1.20.1")

        tk.Label(container, text="Mod Loader", bg="white", fg="#666").pack(anchor="w")
        type_var = tk.StringVar(value="Vanilla")
        tf = tk.Frame(container, bg="white")
        tf.pack(fill="x", pady=10)
        for t in ["Vanilla", "Forge", "Fabric"]:
            tk.Radiobutton(tf, text=t, variable=type_var, value=t, bg="white").pack(side="left", padx=(0, 15))

        def create():
            name, ver = e_name.get().strip(), e_ver.get().strip()
            if not name or not ver: return
            new_p = {"name": name, "version": ver, "type": type_var.get(), "id": f"p_{os.urandom(3).hex()}", "compatibility_mode": True}
            self.profiles.append(new_p)
            self.select_profile(new_p["id"])
            
        tk.Button(container, text="CRIAR INSTALAÇÃO", bg=self.colors["accent"], fg="white", bd=0, 
                 font=("Segoe UI", 11, "bold"), pady=12, command=create).pack(side="bottom", fill="x", pady=30)

    # --- MOTOR DE JOGO ---
    def launch_game(self):
        if self.downloading: return
        self.show_home()
        self.downloading = True
        self.btn_play.config(state="disabled", text="INICIANDO...")
        self.prog_ui.pack(side="bottom", fill="x", padx=50, pady=50)
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

            options = {"username": self.username, "uuid": "", "token": "", "gameDirectory": inst_path, "launcherName": "AetherLauncher", "launcherVersion": "3.3"}
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
