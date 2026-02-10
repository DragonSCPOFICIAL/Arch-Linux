import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import threading
import subprocess
import ssl
import time
from PIL import Image, ImageTk
import minecraft_launcher_lib
import utils_extreme as utils
from execution_builder_extreme import ExecutionBuilderExtreme as ExecutionBuilder

# Configurações globais
ssl._create_default_https_context = ssl._create_unverified_context

class AetherLauncherUIExtreme:
    def __init__(self, root):
        self.root = root
        self.root.title("Aether Launcher v7.0-EXTREME - Minecraft Elite Linux (Absurd Performance)")
        
        # Configuração de Janela
        window_width, window_height = 1050, 680
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{window_width}x{window_height}+{(sw-window_width)//2}+{(sh-window_height)//2}")
        self.root.resizable(False, False)
        
        # Cores
        self.colors = {"accent": "#B43D3D"}
        
        # Pastas e Ativos
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.dirname(self.script_dir)
        self.config_dir = os.path.expanduser("~/.config/aetherlauncher")
        self.data_file = os.path.join(self.config_dir, "launcher_data_extreme.json")
        self.mc_dir = os.path.expanduser("~/.aetherlauncher/minecraft")
        self.assets_dir = os.path.join(self.base_dir, "assets")
        self.icons_dir = os.path.join(self.assets_dir, "icons")
        self.avatars_dir = os.path.join(self.assets_dir, "avatars")
        
        # Garantir que pastas de assets existam
        os.makedirs(self.icons_dir, exist_ok=True)
        os.makedirs(self.avatars_dir, exist_ok=True)
        
        # Cache de Imagens persistente
        self.img_cache = {}
        
        self.load_launcher_data()
        self.downloading = False
        self.mc_versions = []
        
        # === EXTREME: Ativar modo performance no sistema ===
        print("\n[PERF] Ativando modo de performance EXTREMO do sistema...")
        try:
            utils.enable_performance_mode()
        except:
            print("[PERF] Modo performance não disponível (permissões)")
        
        self.setup_ui()
        
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
                {"name": "Minecraft 1.21", "version": "1.21", "type": "Vanilla", "id": "p_default", "compatibility_mode": True}
            ],
            "use_autotune": True,
            "use_aikar": True,
            "use_high_priority": True,
            "use_mesa_optim": True,
            "use_zgc_extreme": True,
            "use_io_scheduler": True,
            "use_sysctl_tweaks": True,
            "ram_mb": 4096
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
            releases = [v['id'] for v in versions if v['type'] == 'release']
            self.mc_versions = releases
            print(f"[INFO] {len(self.mc_versions)} versões disponíveis")
        except Exception as e:
            print(f"[WARN] Erro ao buscar versões: {e}")
            self.mc_versions = ["1.21.4", "1.21", "1.20.1", "1.19.4", "1.18.2", "1.16.5", "1.12.2", "1.8.9"]

    def get_photo(self, name, path, size):
        if name in self.img_cache: return self.img_cache[name]
        try:
            if os.path.exists(path):
                img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.img_cache[name] = photo
                return photo
        except: pass
        return None

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=1050, height=680, highlightthickness=0, bg="#0a0a0a")
        self.canvas.pack(fill="both", expand=True)
        
        bg_path = os.path.join(self.base_dir, "background.png")
        bg_img = self.get_photo("bg", bg_path, (1050, 680))
        if bg_img: 
            self.canvas.create_image(0, 0, image=bg_img, anchor="nw")
        else:
            self.canvas.create_rectangle(0, 0, 1050, 680, fill="#121212", outline="")
        
        self.canvas.create_rectangle(0, 0, 250, 680, fill="#000000", stipple="gray50", outline="")
        
        logo_path = os.path.join(self.icons_dir, "minecraft_logo.png")
        logo_img = self.get_photo("mc_logo", logo_path, (200, 52))
        if logo_img: self.canvas.create_image(650, 80, image=logo_img, anchor="center")
        
        self.canvas.create_text(85, 45, text="BEM-VINDO AO MODO EXTREMO,", font=("Segoe UI", 7), fill="#ccc", anchor="w")
        self.nick_display = self.canvas.create_text(85, 60, text=self.username, font=("Segoe UI", 11, "bold"), fill="white", anchor="w")
        
        self.avatar_lbl = tk.Label(self.root, bg="#333", bd=0)
        self.canvas.create_window(47, 52, window=self.avatar_lbl, width=45, height=45)
        self.update_avatar_display()
        
        gpu_info = utils.get_gpu_info()
        self.canvas.create_text(125, 600, text=gpu_info, font=("Segoe UI", 7), fill="#888", anchor="center")
        
        self.create_sidebar_btn(100, "Configurações", "⚙", self.show_settings)
        self.create_sidebar_btn(140, "Gerenciar Instalações", "+", self.show_install)
        self.canvas.create_line(25, 185, 225, 185, fill="#444")
        
        self.profiles_frame = tk.Frame(self.root, bg="#121212", bd=0)
        self.canvas.create_window(125, 390, window=self.profiles_frame, width=240, height=360, anchor="center")
        self.refresh_profiles_list()
        
        self.footer = tk.Frame(self.root, bg=self.colors["accent"], bd=0)
        self.canvas.create_window(125, 635, window=self.footer, width=250, height=90, anchor="center")
        self.btn_play = tk.Button(self.footer, text="JOGAR EXTREME", font=("Segoe UI", 18, "bold"), bg=self.colors["accent"], fg="white", bd=0, cursor="hand2", activebackground="#963232", command=self.launch_game)
        self.btn_play.pack(fill="both", expand=True, pady=(10,0))
        self.lbl_ver_info = tk.Label(self.footer, text="", font=("Segoe UI", 8), bg=self.colors["accent"], fg="white")
        self.lbl_ver_info.pack(fill="x", pady=(0, 10))
        self.update_selection_ui()
        
    def update_avatar_display(self):
        path = os.path.join(self.avatars_dir, self.selected_avatar)
        if not os.path.exists(path):
            self.selected_avatar = "steve.png"
            path = os.path.join(self.avatars_dir, self.selected_avatar)
            
        if "current_avatar" in self.img_cache: del self.img_cache["current_avatar"]
        img = self.get_photo("current_avatar", path, (45, 45))
        if img: 
            self.avatar_lbl.config(image=img)
        else:
            self.avatar_lbl.config(image="", text="👤", fg="white", font=("Segoe UI", 12))

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
            
        grass_path = os.path.join(self.icons_dir, "grass_block.png")
        grass_img = self.get_photo("grass_icon", grass_path, (16, 16))
        
        for p in self.profiles:
            is_sel = (p["id"] == self.selected_pid)
            bg = "#B43D3D" if is_sel else "#121212"
            f = tk.Frame(self.profiles_frame, bg=bg, padx=10, pady=8)
            f.pack(fill="x", pady=2)
            
            icon_lbl = tk.Label(f, bg=bg, bd=0)
            if grass_img: icon_lbl.config(image=grass_img)
            icon_lbl.pack(side="left")
            
            lbl = tk.Label(f, text=p["name"], font=("Segoe UI", 9, "bold" if is_sel else "normal"), bg=bg, fg="white")
            lbl.pack(side="left", padx=8)
            
            f.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))
            lbl.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))

    def select_profile(self, pid):
        self.selected_pid = pid
        self.refresh_profiles_list()
        self.update_selection_ui()
        self.save_launcher_data()

    def update_selection_ui(self):
        p = next((x for x in self.profiles if x["id"] == self.selected_pid), None)
        if p:
            self.lbl_ver_info.config(text=f"{p['version']} ({p['type']})")

    def show_welcome_screen(self):
        self.clear_content()
        self.active_content_frame = tk.Frame(self.root, bg="#1a1a1a", padx=40, pady=40)
        self.active_content_id = self.canvas.create_window(650, 340, window=self.active_content_frame, width=500)
        
        tk.Label(self.active_content_frame, text="BEM-VINDO AO AETHER EXTREME", font=("Segoe UI", 18, "bold"), bg="#1a1a1a", fg="white").pack(pady=(0, 20))
        tk.Label(self.active_content_frame, text="Qual seu nick para o jogo?", font=("Segoe UI", 11), bg="#1a1a1a", fg="#aaa").pack()
        
        nick_entry = tk.Entry(self.active_content_frame, font=("Segoe UI", 14), bg="#333", fg="white", bd=0, insertbackground="white")
        nick_entry.pack(fill="x", pady=20, ipady=8)
        nick_entry.insert(0, self.username)
        
        tk.Button(self.active_content_frame, text="CONTINUAR", bg=self.colors["accent"], fg="white", font=("Segoe UI", 12, "bold"), bd=0, pady=10, cursor="hand2", command=lambda: self.set_username(nick_entry.get())).pack(fill="x")

    def set_username(self, nick):
        if not nick.strip(): return
        self.username = nick.strip()
        self.canvas.itemconfig(self.nick_display, text=self.username)
        self.save_launcher_data()
        self.show_home()

    def show_home(self):
        self.clear_content()
        # Home screen can show news or stats

    def show_settings(self):
        self.clear_content()
        self.active_content_frame = tk.Frame(self.root, bg="#1a1a1a", padx=30, pady=30)
        self.active_content_id = self.canvas.create_window(650, 340, window=self.active_content_frame, width=600, height=500)
        
        tk.Label(self.active_content_frame, text="CONFIGURAÇÕES EXTREMAS", font=("Segoe UI", 16, "bold"), bg="#1a1a1a", fg="white").pack(anchor="w", pady=(0, 20))
        
        # RAM Slider
        tk.Label(self.active_content_frame, text="Memória RAM (MB):", bg="#1a1a1a", fg="#ccc").pack(anchor="w")
        ram_val = tk.IntVar(value=self.data.get("ram_mb", 4096))
        ram_slider = tk.Scale(self.active_content_frame, from_=1024, to=16384, orient="horizontal", variable=ram_val, bg="#1a1a1a", fg="white", highlightthickness=0)
        ram_slider.pack(fill="x", pady=(0, 20))
        
        # Checkboxes for optimizations
        opts = [
            ("use_zgc_extreme", "Usar Generational ZGC (Java 21+)"),
            ("use_io_scheduler", "Otimizar I/O Scheduler (NVMe/SSD)"),
            ("use_sysctl_tweaks", "Aplicar Tweaks de Kernel (Sysctl)"),
            ("use_mesa_optim", "Otimizações Mesa/NVIDIA Turbo"),
            ("use_autotune", "Auto-Tune de Hardware na Inicialização")
        ]
        
        self.opt_vars = {}
        for key, text in opts:
            var = tk.BooleanVar(value=self.data.get(key, True))
            self.opt_vars[key] = var
            tk.Checkbutton(self.active_content_frame, text=text, variable=var, bg="#1a1a1a", fg="white", selectcolor="#333", activebackground="#1a1a1a", activeforeground="white").pack(anchor="w")
            
        tk.Button(self.active_content_frame, text="SALVAR E APLICAR", bg=self.colors["accent"], fg="white", font=("Segoe UI", 11, "bold"), bd=0, pady=10, command=lambda: self.save_settings(ram_val.get())).pack(side="bottom", fill="x")

    def save_settings(self, ram):
        self.data["ram_mb"] = ram
        for key, var in self.opt_vars.items():
            self.data[key] = var.get()
        self.save_launcher_data()
        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        self.show_home()

    def show_install(self):
        self.clear_content()
        self.active_content_frame = tk.Frame(self.root, bg="#1a1a1a", padx=30, pady=30)
        self.active_content_id = self.canvas.create_window(650, 340, window=self.active_content_frame, width=600, height=500)
        
        tk.Label(self.active_content_frame, text="NOVA INSTALAÇÃO EXTREME", font=("Segoe UI", 16, "bold"), bg="#1a1a1a", fg="white").pack(anchor="w", pady=(0, 20))
        
        tk.Label(self.active_content_frame, text="Nome da Instância:", bg="#1a1a1a", fg="#ccc").pack(anchor="w")
        name_entry = tk.Entry(self.active_content_frame, bg="#333", fg="white", bd=0)
        name_entry.pack(fill="x", pady=(0, 15), ipady=5)
        
        tk.Label(self.active_content_frame, text="Versão:", bg="#1a1a1a", fg="#ccc").pack(anchor="w")
        ver_combo = ttk.Combobox(self.active_content_frame, values=self.mc_versions)
        ver_combo.pack(fill="x", pady=(0, 15))
        if self.mc_versions: ver_combo.current(0)
        
        tk.Label(self.active_content_frame, text="Modloader:", bg="#1a1a1a", fg="#ccc").pack(anchor="w")
        type_combo = ttk.Combobox(self.active_content_frame, values=["Vanilla", "Forge", "Fabric", "Quilt", "NeoForge"])
        type_combo.pack(fill="x", pady=(0, 20))
        type_combo.current(0)
        
        tk.Button(self.active_content_frame, text="CRIAR INSTÂNCIA", bg=self.colors["accent"], fg="white", font=("Segoe UI", 11, "bold"), bd=0, pady=10, command=lambda: self.create_profile(name_entry.get(), ver_combo.get(), type_combo.get())).pack(fill="x")

    def create_profile(self, name, ver, type):
        if not name or not ver: return
        pid = f"p_{int(time.time())}"
        self.profiles.append({"name": name, "version": ver, "type": type, "id": pid, "compatibility_mode": True})
        self.selected_pid = pid
        self.save_launcher_data()
        self.refresh_profiles_list()
        self.update_selection_ui()
        self.show_home()

    def clear_content(self):
        if hasattr(self, 'active_content_id') and self.active_content_id:
            self.canvas.delete(self.active_content_id)
        if hasattr(self, 'active_content_frame') and self.active_content_frame:
            self.active_content_frame.destroy()

    def launch_game(self):
        if self.downloading or not self.selected_pid: return
        self.downloading = True
        self.btn_play.config(state="disabled", text="PREPARANDO EXTREME...")
        
        self.clear_content()
        self.active_content_frame = tk.Frame(self.root, bg="#000000", padx=20, pady=15)
        self.active_content_id = self.canvas.create_window(650, 580, window=self.active_content_frame, width=600)
        self.prog_lbl = tk.Label(self.active_content_frame, text="Iniciando motor extremo...", bg="#000000", fg="#888", font=("Segoe UI", 9))
        self.prog_lbl.pack(anchor="w")
        self.prog_bar = ttk.Progressbar(self.active_content_frame, mode='determinate')
        self.prog_bar.pack(fill="x", pady=5)
        
        threading.Thread(target=self.engine_run, daemon=True).start()

    def engine_run(self):
        try:
            p = next((x for x in self.profiles if x["id"] == self.selected_pid), None)
            if not p: return
            
            vid = p["version"]
            inst = utils.get_instance_path(self.mc_dir, p["name"])
            
            def set_status(status):
                self.root.after(0, lambda: self.prog_lbl.config(text=status))
            
            def set_progress(progress):
                self.root.after(0, lambda: self.prog_bar.config(value=progress))
            
            def set_max(maximum):
                self.root.after(0, lambda: self.prog_bar.config(maximum=maximum, value=0))
            
            callback = {"setStatus": set_status, "setProgress": set_progress, "setMax": set_max}
            
            final_vid = vid
            # Lógica de instalação (simplificada para este exemplo, usa a lib)
            if p["type"] == "Forge":
                forge_id = minecraft_launcher_lib.forge.find_forge_version(vid)
                if forge_id:
                    minecraft_launcher_lib.forge.install_forge_version(forge_id, self.mc_dir, callback=callback)
                    final_vid = forge_id
            elif p["type"] == "Fabric":
                fabric_loader = minecraft_launcher_lib.fabric.get_latest_loader_version()
                minecraft_launcher_lib.fabric.install_fabric(vid, self.mc_dir, loader_version=fabric_loader, callback=callback)
                final_vid = f"fabric-loader-{fabric_loader}-{vid}"
            elif p["type"] == "Vanilla":
                minecraft_launcher_lib.install.install_minecraft_version(vid, self.mc_dir, callback=callback)
            
            # Preparar opções
            options = {
                "username": self.username,
                "uuid": "",
                "token": "",
                "gameDirectory": inst,
                "jvmArguments": [f"-Xmx{self.data.get('ram_mb', 4096)}M", f"-Xms{self.data.get('ram_mb', 4096)}M"]
            }
            
            # Gerar comando EXTREMO
            cmd = ExecutionBuilder.build_command(final_vid, self.mc_dir, options)
            
            # Configurar ambiente EXTREMO
            env = ExecutionBuilder.get_environment_variables(profile_index=self.data.get("best_profile"))
            
            # Aplicar Tweaks de Sistema
            utils.apply_linux_tweaks(self.data)
            
            set_status("MOTOR EXTREMO INICIADO! BOM JOGO!")
            time.sleep(2)
            
            subprocess.Popen(cmd, env=env, cwd=inst)
            self.root.after(0, self.reset_play_btn)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro Fatal", str(e)))
            self.root.after(0, self.reset_play_btn)

    def reset_play_btn(self):
        self.downloading = False
        self.btn_play.config(state="normal", text="JOGAR EXTREME")
        self.clear_content()

if __name__ == "__main__":
    root = tk.Tk()
    app = AetherLauncherUIExtreme(root)
    root.mainloop()
