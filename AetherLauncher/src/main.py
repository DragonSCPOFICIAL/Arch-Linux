import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import threading
import subprocess
import ssl
import platform
from PIL import Image, ImageTk
import minecraft_launcher_lib
import utils

# Configurações globais
ssl._create_default_https_context = ssl._create_unverified_context

class AetherLauncherUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aether Launcher v4.3 - Minecraft Elite Linux (Nativo)")
        
        # Configuração de Janela
        window_width, window_height = 1050, 680
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{window_width}x{window_height}+{(sw-window_width)//2}+{(sh-window_height)//2}")
        self.root.resizable(False, False)
        
        # Cores
        self.colors = {"accent": "#B43D3D"}
        
        # Pastas e Ativos
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.config_dir = os.path.expanduser("~/.config/aetherlauncher")
        self.data_file = os.path.join(self.config_dir, "launcher_data.json")
        self.mc_dir = os.path.expanduser("~/.aetherlauncher/minecraft")
        self.assets_dir = os.path.join(self.base_dir, "assets")
        self.avatars_dir = os.path.join(self.assets_dir, "avatars")
        
        self.load_launcher_data()
        self.downloading = False
        self.mc_versions = []
        self.cached_images = {}
        
        self.setup_ui()
        
        # Se for o primeiro acesso (sem username salvo), mostra tela de boas-vindas
        if self.username == "Jogador":
            self.show_welcome_screen()
        else:
            self.show_home()
            
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
        self.selected_pid = self.data.get("last_profile", "")
        if not self.selected_pid and self.profiles:
            self.selected_pid = self.profiles[0]["id"]
        self.username = self.data.get("username", "Jogador")
        self.selected_avatar = self.data.get("avatar", "steve.png")

    def get_default_data(self):
        return {
            "username": "Jogador",
            "last_profile": "p_default",
            "avatar": "steve.png",
            "profiles": [
                {"name": "Minecraft 1.12.2", "version": "1.12.2", "type": "Vanilla", "id": "p_default", "compatibility_mode": True}
            ]
        }

    def save_launcher_data(self):
        self.data["profiles"] = self.profiles
        self.data["last_profile"] = self.selected_pid
        self.data["username"] = self.username
        self.data["avatar"] = self.selected_avatar
        if not os.path.exists(self.config_dir): os.makedirs(self.config_dir)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def fetch_versions(self):
        try:
            versions = minecraft_launcher_lib.utils.get_version_list()
            self.mc_versions = [v['id'] for v in versions if v['type'] == 'release']
        except:
            self.mc_versions = ["1.20.1", "1.19.4", "1.12.2"]

    def get_image(self, path, size):
        key = f"{path}_{size[0]}x{size[1]}"
        if key in self.cached_images: return self.cached_images[key]
        if os.path.exists(path):
            try:
                img = Image.open(path).resize(size, Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.cached_images[key] = photo
                return photo
            except: pass
        return None

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=1050, height=680, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)
        self.load_background()
        
        # Sidebar Overlay
        self.canvas.create_rectangle(0, 0, 250, 680, fill="#000000", stipple="gray50", outline="")
        self.canvas.create_text(85, 45, text="BEM-VINDO,", font=("Segoe UI", 7), fill="#ccc", anchor="w")
        self.nick_display = self.canvas.create_text(85, 60, text=self.username, font=("Segoe UI", 11, "bold"), fill="white", anchor="w")
        
        # Avatar do Usuário (Imagem Real)
        self.avatar_label = tk.Label(self.root, bg="#333", bd=0)
        self.canvas.create_window(47, 52, window=self.avatar_label, width=45, height=45)
        self.update_avatar_display()
        
        self.create_sidebar_btn(100, "Configurações", "⚙", self.show_settings)
        self.create_sidebar_btn(140, "Gerenciar Instalações", "+", self.show_install)
        self.canvas.create_line(25, 185, 225, 185, fill="#444")
        
        self.profiles_frame = tk.Frame(self.root, bg="#121212", bd=0)
        self.canvas.create_window(125, 390, window=self.profiles_frame, width=240, height=360, anchor="center")
        self.refresh_profiles_list()
        
        self.footer = tk.Frame(self.root, bg=self.colors["accent"], bd=0)
        self.canvas.create_window(125, 635, window=self.footer, width=250, height=90, anchor="center")
        self.btn_play = tk.Button(self.footer, text="JOGAR", font=("Segoe UI", 18, "bold"), bg=self.colors["accent"], fg="white", bd=0, cursor="hand2", activebackground="#963232", command=self.launch_game)
        self.btn_play.pack(fill="both", expand=True, pady=(10,0))
        self.lbl_ver_info = tk.Label(self.footer, text="", font=("Segoe UI", 8), bg=self.colors["accent"], fg="white")
        self.lbl_ver_info.pack(fill="x", pady=(0, 10))
        self.update_selection_ui()
        
        self.active_content_id = None
        self.active_content_frame = None

    def update_avatar_display(self):
        path = os.path.join(self.avatars_dir, self.selected_avatar)
        img = self.get_image(path, (45, 45))
        if img: self.avatar_label.config(image=img)

    def load_background(self):
        bg_path = os.path.join(self.base_dir, "background.png")
        img = self.get_image(bg_path, (1050, 680))
        if img: self.canvas.create_image(0, 0, image=img, anchor="nw")

    def create_sidebar_btn(self, y, text, icon, cmd):
        t_id = self.canvas.create_text(40, y, text=f"{icon}  {text}", font=("Segoe UI", 10, "bold"), fill="white", anchor="w")
        r_id = self.canvas.create_rectangle(10, y-15, 240, y+15, fill="", outline="")
        self.canvas.tag_bind(t_id, "<Button-1>", lambda e: cmd())
        self.canvas.tag_bind(r_id, "<Button-1>", lambda e: cmd())

    def refresh_profiles_list(self):
        for w in self.profiles_frame.winfo_children(): w.destroy()
        if not self.profiles:
            tk.Label(self.profiles_frame, text="Nenhuma instalação", bg="#121212", fg="#555").pack(pady=20)
            return
            
        grass_path = os.path.join(self.assets_dir, "grass_block.png")
        grass_img = self.get_image(grass_path, (16, 16))
        
        for p in self.profiles:
            is_sel = (p["id"] == self.selected_pid)
            bg = "#B43D3D" if is_sel else "#121212"
            f = tk.Frame(self.profiles_frame, bg=bg, padx=10, pady=8)
            f.pack(fill="x", pady=2)
            
            # Ícone de Bloco de Grama Real
            icon_lbl = tk.Label(f, bg=bg, bd=0)
            if grass_img: icon_lbl.config(image=grass_img)
            icon_lbl.pack(side="left")
            
            lbl = tk.Label(f, text=p["name"], font=("Segoe UI", 9, "bold" if is_sel else "normal"), bg=bg, fg="white")
            lbl.pack(side="left", padx=8)
            
            if is_sel:
                opt = tk.Label(f, text="⋮", font=("Segoe UI", 12, "bold"), bg=bg, fg="white", cursor="hand2")
                opt.pack(side="right")
                opt.bind("<Button-1>", lambda e, profile=p: self.show_profile_menu(e, profile))
                
            f.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))
            lbl.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))

    def show_profile_menu(self, event, profile):
        menu = tk.Menu(self.root, tearoff=0, bg="#222", fg="white", activebackground=self.colors["accent"])
        menu.add_command(label="📂 Abrir Pasta", command=lambda: subprocess.run(["xdg-open", utils.get_instance_path(self.mc_dir, profile["name"])]))
        menu.add_command(label="✏️ Editar", command=lambda: self.show_install(edit_profile=profile))
        menu.add_separator()
        menu.add_command(label="🗑️ Apagar", command=lambda: self.delete_profile(profile["id"]))
        menu.post(event.x_root, event.y_root)

    def delete_profile(self, pid):
        if messagebox.askyesno("Confirmar", "Deseja realmente apagar esta instalação?"):
            self.profiles = [p for p in self.profiles if p["id"] != pid]
            if self.selected_pid == pid:
                self.selected_pid = self.profiles[0]["id"] if self.profiles else ""
            self.save_launcher_data(); self.refresh_profiles_list(); self.update_selection_ui()

    def select_profile(self, pid):
        self.selected_pid = pid
        self.update_selection_ui(); self.refresh_profiles_list(); self.save_launcher_data(); self.show_home()

    def update_selection_ui(self):
        p = next((x for x in self.profiles if x["id"] == self.selected_pid), None)
        if p:
            self.lbl_ver_info.config(text=f"{p['type']} {p['version']}")
            self.btn_play.config(state="normal")
        else:
            self.lbl_ver_info.config(text="Selecione ou crie uma versão")
            self.btn_play.config(state="disabled")

    def clear_content(self):
        if self.active_content_id:
            self.canvas.delete(self.active_content_id)
            self.active_content_id = None
        if self.active_content_frame:
            self.active_content_frame.destroy()
            self.active_content_frame = None

    def show_home(self):
        self.clear_content()
        if self.downloading:
            self.active_content_frame = tk.Frame(self.root, bg="#000000", padx=20, pady=15)
            self.active_content_id = self.canvas.create_window(650, 580, window=self.active_content_frame, width=600)
            self.prog_lbl = tk.Label(self.active_content_frame, text="Pronto", bg="#000000", fg="#888", font=("Segoe UI", 9))
            self.prog_lbl.pack(anchor="w")
            self.prog_bar = ttk.Progressbar(self.active_content_frame, mode='determinate')
            self.prog_bar.pack(fill="x", pady=5)

    def show_welcome_screen(self):
        self.clear_content()
        self.active_content_frame = tk.Frame(self.root, bg="#1a1a1a", padx=50, pady=50)
        self.active_content_id = self.canvas.create_window(650, 340, window=self.active_content_frame, width=600, height=400)
        
        tk.Label(self.active_content_frame, text="BEM-VINDO AO AETHER", font=("Segoe UI", 20, "bold"), bg="#1a1a1a", fg="white").pack(pady=30)
        tk.Label(self.active_content_frame, text="Como devemos chamar você?", bg="#1a1a1a", fg="#aaa").pack(pady=5)
        
        e_name = tk.Entry(self.active_content_frame, font=("Segoe UI", 14), bg="#333", fg="white", bd=0, insertbackground="white", justify="center")
        e_name.pack(fill="x", padx=100, pady=20, ipady=10)
        e_name.focus_set()
        
        def start():
            name = e_name.get().strip()
            if name:
                self.username = name
                self.canvas.itemconfig(self.nick_display, text=self.username)
                self.save_launcher_data()
                self.show_home()
            else: messagebox.showwarning("Aviso", "Por favor, digite um nome.")
            
        tk.Button(self.active_content_frame, text="COMEÇAR", bg=self.colors["accent"], fg="white", bd=0, font=("Segoe UI", 12, "bold"), padx=50, pady=12, command=start).pack(pady=20)

    def show_settings(self):
        self.clear_content()
        self.active_content_frame = tk.Frame(self.root, bg="#1a1a1a", padx=50, pady=30)
        self.active_content_id = self.canvas.create_window(650, 340, window=self.active_content_frame, width=750, height=550)
        
        tk.Label(self.active_content_frame, text="CONFIGURAÇÕES", font=("Segoe UI", 18, "bold"), bg="#1a1a1a", fg="white").pack(pady=20)
        
        # Nickname
        tk.Label(self.active_content_frame, text="Nickname do Jogador", bg="#1a1a1a", fg="#aaa").pack(anchor="w", padx=50)
        e_nick = tk.Entry(self.active_content_frame, font=("Segoe UI", 12), bg="#333", fg="white", bd=0, insertbackground="white")
        e_nick.pack(fill="x", padx=50, pady=10, ipady=8); e_nick.insert(0, self.username)
        
        # Seleção de Avatar
        tk.Label(self.active_content_frame, text="Escolha seu Avatar", bg="#1a1a1a", fg="#aaa").pack(anchor="w", padx=50, pady=(20, 5))
        avatar_frame = tk.Frame(self.active_content_frame, bg="#1a1a1a")
        avatar_frame.pack(fill="x", padx=50)
        
        self.avatar_var = tk.StringVar(value=self.selected_avatar)
        avatars = [("Steve", "steve.png"), ("Alex", "alex.png"), ("Herobrine", "herobrine.png")]
        
        for name, file in avatars:
            f = tk.Frame(avatar_frame, bg="#1a1a1a")
            f.pack(side="left", expand=True)
            
            img = self.get_image(os.path.join(self.avatars_dir, file), (64, 64))
            l = tk.Label(f, image=img, bg="#1a1a1a")
            l.pack()
            tk.Radiobutton(f, text=name, variable=self.avatar_var, value=file, bg="#1a1a1a", fg="white", selectcolor="#333").pack()
        
        btn_frame = tk.Frame(self.active_content_frame, bg="#1a1a1a")
        btn_frame.pack(pady=30)
        tk.Button(btn_frame, text="VOLTAR", bg="#444", fg="white", bd=0, font=("Segoe UI", 10, "bold"), padx=30, pady=10, command=self.show_home).pack(side="left", padx=10)
        
        def save():
            self.username = e_nick.get().strip() or "Jogador"
            self.selected_avatar = self.avatar_var.get()
            self.canvas.itemconfig(self.nick_display, text=self.username)
            self.update_avatar_display()
            self.save_launcher_data()
            self.show_home()
            
        tk.Button(btn_frame, text="SALVAR", bg=self.colors["accent"], fg="white", bd=0, font=("Segoe UI", 10, "bold"), padx=30, pady=10, command=save).pack(side="left", padx=10)

    def show_install(self, edit_profile=None):
        self.clear_content()
        self.active_content_frame = tk.Frame(self.root, bg="#1a1a1a", padx=50, pady=40)
        self.active_content_id = self.canvas.create_window(650, 340, window=self.active_content_frame, width=700, height=550)
        
        title = "EDITAR INSTALAÇÃO" if edit_profile else "NOVA INSTALAÇÃO"
        tk.Label(self.active_content_frame, text=title, font=("Segoe UI", 18, "bold"), bg="#1a1a1a", fg="white").pack(pady=(20, 10))
        
        c = tk.Frame(self.active_content_frame, bg="#1a1a1a")
        c.pack(fill="both", expand=True, padx=100)
        tk.Label(c, text="Nome", bg="#1a1a1a", fg="#aaa").pack(anchor="w")
        e_n = tk.Entry(c, bg="#333", fg="white", bd=0, font=("Segoe UI", 11), insertbackground="white")
        e_n.pack(fill="x", pady=5, ipady=8); e_n.insert(0, edit_profile["name"] if edit_profile else "Nova Versão")
        tk.Label(c, text="Versão", bg="#1a1a1a", fg="#aaa").pack(anchor="w", pady=(10,0))
        v_l = ttk.Combobox(c, values=self.mc_versions, state="readonly", font=("Segoe UI", 11))
        v_l.pack(fill="x", pady=5, ipady=5)
        if edit_profile: v_l.set(edit_profile["version"])
        elif self.mc_versions: v_l.set(self.mc_versions[0])
        t_v = tk.StringVar(value=edit_profile["type"] if edit_profile else "Vanilla")
        tf = tk.Frame(c, bg="#1a1a1a")
        tf.pack(fill="x", pady=15)
        for t in ["Vanilla", "Forge", "Fabric"]: tk.Radiobutton(tf, text=t, variable=t_v, value=t, bg="#1a1a1a", fg="white", selectcolor="#333").pack(side="left", padx=10)
        
        btn_frame = tk.Frame(c, bg="#1a1a1a")
        btn_frame.pack(side="bottom", fill="x", pady=20)
        tk.Button(btn_frame, text="CANCELAR", bg="#444", fg="white", bd=0, font=("Segoe UI", 11, "bold"), pady=12, command=self.show_home).pack(side="left", expand=True, fill="x", padx=(0, 5))
        def action():
            name, ver = e_n.get().strip(), v_l.get()
            if not name or not ver: return
            if edit_profile: edit_profile["name"], edit_profile["version"], edit_profile["type"] = name, ver, t_v.get()
            else:
                np = {"name": name, "version": ver, "type": t_v.get(), "id": f"p_{os.urandom(3).hex()}", "compatibility_mode": True}
                self.profiles.append(np); self.selected_pid = np["id"]
            self.save_launcher_data(); self.select_profile(self.selected_pid)
        tk.Button(btn_frame, text="SALVAR" if edit_profile else "CRIAR", bg=self.colors["accent"], fg="white", bd=0, font=("Segoe UI", 11, "bold"), pady=12, command=action).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def launch_game(self):
        if self.downloading or not self.selected_pid: return
        self.show_home(); self.downloading = True; self.btn_play.config(state="disabled", text="INICIANDO...")
        threading.Thread(target=self.engine_run, daemon=True).start()

    def engine_run(self):
        try:
            p = next((x for x in self.profiles if x["id"] == self.selected_pid), None)
            if not p: return
            vid = p["version"]; inst = utils.get_instance_path(self.mc_dir, p["name"])
            cb = {"setStatus": lambda t: self.root.after(0, lambda: self.prog_lbl.config(text=t)), "setProgress": lambda v: self.root.after(0, lambda: self.prog_bar.config(value=v)), "setMax": lambda v: self.root.after(0, lambda: self.prog_bar.config(maximum=v))}
            minecraft_launcher_lib.install.install_minecraft_version(vid, self.mc_dir, callback=cb)
            final_vid = vid
            if p["type"] == "Fabric":
                fv = minecraft_launcher_lib.fabric.get_latest_loader_version()
                minecraft_launcher_lib.fabric.install_fabric(vid, self.mc_dir, loader_version=fv, callback=cb)
                final_vid = minecraft_launcher_lib.fabric.get_fabric_version(vid, fv)
            elif p["type"] == "Forge":
                fv = minecraft_launcher_lib.forge.find_forge_version(vid)
                if fv: minecraft_launcher_lib.forge.install_forge_version(fv, self.mc_dir, callback=cb); final_vid = fv
            cmd = minecraft_launcher_lib.command.get_minecraft_command(final_vid, self.mc_dir, {"username": self.username, "uuid": "", "token": "", "gameDirectory": inst, "launcherName": "AetherLauncher", "launcherVersion": "4.3"})
            env = utils.get_compatibility_env() if p.get("compatibility_mode", True) else os.environ.copy()
            self.root.after(0, lambda: self.show_home())
            subprocess.run(cmd, env=env)
        except Exception as e: self.root.after(0, lambda: messagebox.showerror("Erro", str(e)))
        finally: self.downloading = False; self.root.after(0, lambda: self.btn_play.config(state="normal", text="JOGAR"))

if __name__ == "__main__":
    root = tk.Tk(); app = AetherLauncherUI(root); root.mainloop()
