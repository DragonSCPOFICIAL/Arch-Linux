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
        self.root.title("Aether Launcher v4.6 - Minecraft Elite Linux (Nativo)")
        
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
        self.data_file = os.path.join(self.config_dir, "launcher_data.json")
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
        """Busca versões disponíveis, priorizando as mais recentes."""
        try:
            versions = minecraft_launcher_lib.utils.get_version_list()
            # Ordenar versões para que as mais novas apareçam primeiro
            releases = [v['id'] for v in versions if v['type'] == 'release']
            self.mc_versions = releases
        except Exception as e:
            print(f"Erro ao buscar versões: {e}")
            self.mc_versions = ["1.21", "1.20.1", "1.19.4", "1.18.2", "1.16.5", "1.12.2", "1.8.9"]

    def get_photo(self, name, path, size):
        """Carrega e mantém a imagem no cache para evitar coleta de lixo"""
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
        
        # Fundo com efeito de profundidade
        bg_path = os.path.join(self.base_dir, "background.png")
        bg_img = self.get_photo("bg", bg_path, (1050, 680))
        if bg_img: 
            self.canvas.create_image(0, 0, image=bg_img, anchor="nw")
        else:
            # Gradiente de fallback elegante
            self.canvas.create_rectangle(0, 0, 1050, 680, fill="#121212", outline="")
        
        # Sidebar
        self.canvas.create_rectangle(0, 0, 250, 680, fill="#000000", stipple="gray50", outline="")
        
        # Logo do Minecraft
        logo_path = os.path.join(self.icons_dir, "minecraft_logo.png")
        logo_img = self.get_photo("mc_logo", logo_path, (200, 52))
        if logo_img: self.canvas.create_image(650, 80, image=logo_img, anchor="center")
        self.canvas.create_text(85, 45, text="BEM-VINDO,", font=("Segoe UI", 7), fill="#ccc", anchor="w")
        self.nick_display = self.canvas.create_text(85, 60, text=self.username, font=("Segoe UI", 11, "bold"), fill="white", anchor="w")
        
        # Avatar (Usando Label simples para maior compatibilidade)
        self.avatar_lbl = tk.Label(self.root, bg="#333", bd=0)
        self.canvas.create_window(47, 52, window=self.avatar_lbl, width=45, height=45)
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
        """Atualiza o ícone do avatar na interface."""
        path = os.path.join(self.avatars_dir, self.selected_avatar)
        if not os.path.exists(path):
            # Fallback para steve se o avatar selecionado sumiu
            self.selected_avatar = "steve.png"
            path = os.path.join(self.avatars_dir, self.selected_avatar)
            
        # Limpa o cache antigo para forçar recarregamento
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
            
            if is_sel:
                opt = tk.Label(f, text="⋮", font=("Segoe UI", 12, "bold"), bg=bg, fg="white", cursor="hand2")
                opt.pack(side="right")
                opt.bind("<Button-1>", lambda e, profile=p: self.show_profile_menu(e, profile))
                
            f.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))
            lbl.bind("<Button-1>", lambda e, pid=p["id"]: self.select_profile(pid))

    def show_profile_menu(self, event, profile):
        menu = tk.Menu(self.root, tearoff=0, bg="#222", fg="white", activebackground=self.colors["accent"])
        menu.add_command(label="Abrir Pasta", command=lambda: subprocess.run(["xdg-open", utils.get_instance_path(self.mc_dir, profile["name"])]))
        menu.add_command(label="Editar", command=lambda: self.show_install(edit_profile=profile))
        menu.add_separator()
        menu.add_command(label="Apagar", command=lambda: self.delete_profile(profile["id"]))
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
        self.active_content_frame = tk.Frame(self.root, bg="#1a1a1a", padx=30, pady=20)
        self.active_content_id = self.canvas.create_window(650, 340, window=self.active_content_frame, width=800, height=600)
        
        # Notebook para Abas
        nb = ttk.Notebook(self.active_content_frame)
        nb.pack(fill="both", expand=True)
        
        # --- ABA PERFIL ---
        f_profile = tk.Frame(nb, bg="#1a1a1a", padx=20, pady=20)
        nb.add(f_profile, text=" Perfil ")
        
        tk.Label(f_profile, text="Nickname do Jogador", bg="#1a1a1a", fg="#aaa").pack(anchor="w")
        e_nick = tk.Entry(f_profile, font=("Segoe UI", 12), bg="#333", fg="white", bd=0, insertbackground="white")
        e_nick.pack(fill="x", pady=10, ipady=8); e_nick.insert(0, self.username)
        
        tk.Label(f_profile, text="URL da Skin (Opcional)", bg="#1a1a1a", fg="#aaa").pack(anchor="w", pady=(10, 0))
        e_skin = tk.Entry(f_profile, font=("Segoe UI", 10), bg="#333", fg="white", bd=0, insertbackground="white")
        e_skin.pack(fill="x", pady=5, ipady=5); e_skin.insert(0, self.data.get("skin_url", ""))
        
        tk.Label(f_profile, text="Escolha seu Avatar", bg="#1a1a1a", fg="#aaa").pack(anchor="w", pady=(20, 5))
        avatar_frame = tk.Frame(f_profile, bg="#1a1a1a")
        avatar_frame.pack(fill="x")
        
        self.avatar_var = tk.StringVar(value=self.selected_avatar)
        avatars = [("Steve", "steve.png"), ("Alex", "alex.png"), ("Herobrine", "herobrine.png")]
        for name, file in avatars:
            f = tk.Frame(avatar_frame, bg="#1a1a1a")
            f.pack(side="left", expand=True)
            img = self.get_photo(f"set_{file}", os.path.join(self.avatars_dir, file), (64, 64))
            l = tk.Label(f, bg="#1a1a1a")
            if img: l.config(image=img)
            l.pack()
            tk.Radiobutton(f, text=name, variable=self.avatar_var, value=file, bg="#1a1a1a", fg="white", selectcolor="#333").pack()

        # --- ABA PERFORMANCE ---
        f_perf = tk.Frame(nb, bg="#1a1a1a", padx=20, pady=20)
        nb.add(f_perf, text=" Performance ")
        
        sys_info = utils.get_system_info()
        tk.Label(f_perf, text="DETECÇÃO DE HARDWARE", font=("Segoe UI", 10, "bold"), bg="#1a1a1a", fg=self.colors["accent"]).pack(anchor="w", pady=(0, 10))
        tk.Label(f_perf, text=f"RAM Detectada: {sys_info['ram_gb']}GB | CPU: {sys_info['cpu_cores']} Cores | GPU: {sys_info['gpu_vendor'].upper()}", bg="#1a1a1a", fg="#888").pack(anchor="w")
        
        tk.Label(f_perf, text="Memória RAM (MB)", bg="#1a1a1a", fg="#aaa").pack(anchor="w", pady=(20, 5))
        ram_val = self.data.get("ram_mb", 4096)
        e_ram = tk.Scale(f_perf, from_=1024, to=sys_info['ram_gb']*1024 if sys_info['ram_gb'] > 1 else 2048, orient="horizontal", bg="#1a1a1a", fg="white", highlightthickness=0)
        e_ram.set(ram_val); e_ram.pack(fill="x")
        
        self.perf_vars = {
            "use_aikar": tk.BooleanVar(value=self.data.get("use_aikar", True)),
            "use_high_priority": tk.BooleanVar(value=self.data.get("use_high_priority", True)),
            "use_mesa_optim": tk.BooleanVar(value=self.data.get("use_mesa_optim", True))
        }
        
        tk.Checkbutton(f_perf, text="Usar Aikar's Flags (Estabilidade de FPS)", variable=self.perf_vars["use_aikar"], bg="#1a1a1a", fg="white", selectcolor="#333", activebackground="#1a1a1a").pack(anchor="w", pady=5)
        tk.Checkbutton(f_perf, text="Prioridade de Processo Alta (Nice/Ionice)", variable=self.perf_vars["use_high_priority"], bg="#1a1a1a", fg="white", selectcolor="#333", activebackground="#1a1a1a").pack(anchor="w", pady=5)
        tk.Checkbutton(f_perf, text="Otimizações de Driver Mesa (Latência Zero)", variable=self.perf_vars["use_mesa_optim"], bg="#1a1a1a", fg="white", selectcolor="#333", activebackground="#1a1a1a").pack(anchor="w", pady=5)
        
        self.perf_vars["use_autotune"] = tk.BooleanVar(value=self.data.get("use_autotune", True))
        tk.Checkbutton(f_perf, text="Auto-Tune Inteligente (Testar e selecionar melhor driver)", variable=self.perf_vars["use_autotune"], bg="#1a1a1a", fg="white", selectcolor="#333", activebackground="#1a1a1a").pack(anchor="w", pady=5)

        tk.Label(f_perf, text="Perfil de Driver (Manual)", bg="#1a1a1a", fg="#aaa").pack(anchor="w", pady=(10, 5))
        self.driver_profiles = utils.get_autotune_profiles()
        profile_names = [p["name"] for p in self.driver_profiles]
        self.driver_var = ttk.Combobox(f_perf, values=profile_names, state="readonly", font=("Segoe UI", 10))
        self.driver_var.pack(fill="x", pady=5)
        
        current_manual = self.data.get("manual_profile")
        if current_manual is not None and 0 <= current_manual < len(self.driver_profiles):
            self.driver_var.set(self.driver_profiles[current_manual]["name"])
        else:
            self.driver_var.set("Nativo (Mesa Otimizado)")

        # --- ABA PERSONALIZAÇÃO ---
        f_custom = tk.Frame(nb, bg="#1a1a1a", padx=20, pady=20)
        nb.add(f_custom, text=" Personalização ")
        
        tk.Label(f_custom, text="TEMA DO LAUNCHER", font=("Segoe UI", 10, "bold"), bg="#1a1a1a", fg=self.colors["accent"]).pack(anchor="w", pady=(0, 10))
        
        self.themes = utils.get_themes()
        self.theme_var = tk.StringVar(value=self.data.get("theme_name", "Aether (Padrão)"))
        
        for t_name in self.themes.keys():
            tk.Radiobutton(f_custom, text=t_name, variable=self.theme_var, value=t_name, bg="#1a1a1a", fg="white", selectcolor="#333", activebackground="#1a1a1a").pack(anchor="w", pady=2)

        # Botões de Ação
        btn_frame = tk.Frame(self.active_content_frame, bg="#1a1a1a")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="CANCELAR", bg="#444", fg="white", bd=0, font=("Segoe UI", 10, "bold"), padx=30, pady=10, command=self.show_home).pack(side="left", padx=10)
        
        def save():
            self.username = e_nick.get().strip() or "Jogador"
            self.selected_avatar = self.avatar_var.get()
            self.data["skin_url"] = e_skin.get().strip()
            self.data["ram_mb"] = e_ram.get()
            for k, v in self.perf_vars.items(): self.data[k] = v.get()
            
            # Salvar Perfil de Driver Manual
            selected_driver_name = self.driver_var.get()
            for p in self.driver_profiles:
                if p["name"] == selected_driver_name:
                    self.data["manual_profile"] = p["id"]
                    break
            
            # Aplicar Tema
            selected_theme = self.theme_var.get()
            self.data["theme_name"] = selected_theme
            theme_colors = self.themes[selected_theme]
            self.colors["accent"] = theme_colors["accent"]
            
            self.canvas.itemconfig(self.nick_display, text=self.username)
            self.update_avatar_display()
            self.save_launcher_data()
            # Reiniciar interface para aplicar cores
            self.show_home()
            
        tk.Button(btn_frame, text="SALVAR TUDO", bg=self.colors["accent"], fg="white", bd=0, font=("Segoe UI", 10, "bold"), padx=30, pady=10, command=save).pack(side="left", padx=10)

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
            
            # Verificar se já existe um perfil com esse nome (exceto o próprio perfil sendo editado)
            for p in self.profiles:
                if p["name"] == name and (not edit_profile or p["id"] != edit_profile["id"]):
                    messagebox.showwarning("Aviso", "Já existe uma instalação com este nome!")
                    return

            if edit_profile:
                # Atualizar perfil existente
                edit_profile["name"] = name
                edit_profile["version"] = ver
                edit_profile["type"] = t_v.get()
                # O ID permanece o mesmo, então não há duplicação
            else:
                # Criar novo perfil
                np = {"name": name, "version": ver, "type": t_v.get(), "id": f"p_{os.urandom(3).hex()}", "compatibility_mode": True}
                self.profiles.append(np)
                self.selected_pid = np["id"]
            
            self.save_launcher_data()
            self.select_profile(self.selected_pid)
        tk.Button(btn_frame, text="SALVAR" if edit_profile else "CRIAR", bg=self.colors["accent"], fg="white", bd=0, font=("Segoe UI", 11, "bold"), pady=12, command=action).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def launch_game(self):
        if self.downloading or not self.selected_pid: return
        self.downloading = True
        self.btn_play.config(state="disabled", text="PREPARANDO...")
        
        # Criar interface de progresso ANTES de iniciar o thread
        self.clear_content()
        self.active_content_frame = tk.Frame(self.root, bg="#000000", padx=20, pady=15)
        self.active_content_id = self.canvas.create_window(650, 580, window=self.active_content_frame, width=600)
        self.prog_lbl = tk.Label(self.active_content_frame, text="Iniciando...", bg="#000000", fg="#888", font=("Segoe UI", 9))
        self.prog_lbl.pack(anchor="w")
        self.prog_bar = ttk.Progressbar(self.active_content_frame, mode='determinate')
        self.prog_bar.pack(fill="x", pady=5)
        
        # Agora sim iniciar o download
        threading.Thread(target=self.engine_run, daemon=True).start()

    def engine_run(self):
        try:
            p = next((x for x in self.profiles if x["id"] == self.selected_pid), None)
            if not p: 
                self.root.after(0, lambda: messagebox.showerror("Erro", "Perfil nao encontrado!"))
                return
            
            vid = p["version"]
            inst = utils.get_instance_path(self.mc_dir, p["name"])
            
            print(f"\n{'='*60}")
            print(f"Iniciando launcher para versao: {vid}")
            print(f"Diretorio MC: {self.mc_dir}")
            print(f"Diretorio instancia: {inst}")
            print(f"{'='*60}\n")
            
            # Criar diretórios necessários
            if not os.path.exists(inst):
                os.makedirs(inst, exist_ok=True)
                print(f"Criado diretorio da instancia: {inst}")
            
            if not os.path.exists(self.mc_dir):
                os.makedirs(self.mc_dir, exist_ok=True)
                print(f"Criado diretorio minecraft: {self.mc_dir}")
            
            # Variáveis para controle de progresso
            download_info = {"current": 0, "max": 0, "files": 0}
            
            # Callback para atualizar progresso
            def set_status(status):
                print(f"[STATUS] {status}")
                def update():
                    if hasattr(self, 'prog_lbl'):
                        self.prog_lbl.config(text=status)
                self.root.after(0, update)
            
            def set_progress(progress):
                download_info["current"] = progress
                def update():
                    if hasattr(self, 'prog_bar'):
                        self.prog_bar.config(value=progress)
                self.root.after(0, update)
            
            def set_max(maximum):
                download_info["max"] = maximum
                download_info["files"] += 1
                def update():
                    if hasattr(self, 'prog_bar'):
                        self.prog_bar.config(maximum=maximum)
                        self.prog_bar.config(value=0)
                self.root.after(0, update)
            
            callback = {
                "setStatus": set_status,
                "setProgress": set_progress,
                "setMax": set_max
            }
            
            # Baixar e instalar Minecraft completo
            print(f"\n>>> Iniciando download do Minecraft {vid}...")
            set_status(f"Baixando Minecraft {vid}...")
            
            minecraft_launcher_lib.install.install_minecraft_version(
                version=vid,
                minecraft_directory=self.mc_dir,
                callback=callback
            )
            
            print(f">>> Download do Minecraft {vid} concluido!")
            
            final_vid = vid
            
            # Instalar modloader se necessário
            if p["type"] == "Fabric":
                print(f"\n>>> Instalando Fabric...")
                set_status("Instalando Fabric...")
                try:
                    fabric_loader = minecraft_launcher_lib.fabric.get_latest_loader_version()
                    print(f"Versao Fabric: {fabric_loader}")
                    
                    minecraft_launcher_lib.fabric.install_fabric(
                        minecraft_version=vid,
                        minecraft_directory=self.mc_dir,
                        loader_version=fabric_loader,
                        callback=callback
                    )
                    final_vid = f"fabric-loader-{fabric_loader}-{vid}"
                    print(f">>> Fabric instalado! ID final: {final_vid}")
                except Exception as e:
                    print(f"ERRO ao instalar Fabric: {e}")
                    import traceback
                    traceback.print_exc()
                    final_vid = vid
                    
            elif p["type"] == "Forge":
                print(f"\n>>> Instalando Forge...")
                set_status("Instalando Forge...")
                try:
                    forge_version = minecraft_launcher_lib.forge.find_forge_version(vid)
                    if forge_version:
                        print(f"Versao Forge: {forge_version}")
                        minecraft_launcher_lib.forge.install_forge_version(
                            forge_version,
                            self.mc_dir,
                            callback=callback
                        )
                        final_vid = forge_version
                        print(f">>> Forge instalado! ID final: {final_vid}")
                    else:
                        print(f"Forge nao disponivel para {vid}")
                except Exception as e:
                    print(f"ERRO ao instalar Forge: {e}")
                    import traceback
                    traceback.print_exc()
                    final_vid = vid
            
            # Instalar Java Runtime correto para a versão
            set_status("Verificando Java Runtime...")
            print(f"\n>>> Verificando Java Runtime necessario...")
            
            java_executable = None
            try:
                # Pegar informações da versão
                version_data = minecraft_launcher_lib.utils.get_version_list()
                version_info = next((v for v in version_data if v['id'] == vid), None)
                
                if version_info:
                    # Baixar JSON da versão
                    import requests
                    version_json_url = version_info.get('url')
                    if version_json_url:
                        response = requests.get(version_json_url)
                        version_details = response.json()
                        
                        # Verificar se tem especificação de Java
                        if 'javaVersion' in version_details:
                            java_major = version_details['javaVersion'].get('majorVersion', 8)
                            print(f">>> Versao Java necessaria: {java_major}")
                            
                            # Instalar o Java correto
                            set_status(f"Baixando Java {java_major}...")
                            print(f">>> Instalando Java Runtime {java_major}...")
                            
                            # Obter lista de runtimes disponíveis
                            try:
                                runtime_name = f"java-runtime-gamma" if java_major >= 17 else "java-runtime-alpha"
                                if java_major >= 21:
                                    runtime_name = "java-runtime-delta"
                                
                                print(f">>> Runtime selecionado: {runtime_name}")
                                
                                minecraft_launcher_lib.runtime.install_jvm_runtime(
                                    runtime_name,
                                    self.mc_dir,
                                    callback=callback
                                )
                                
                                java_executable = minecraft_launcher_lib.runtime.get_executable_path(runtime_name, self.mc_dir)
                                print(f">>> Java instalado em: {java_executable}")
                                
                            except Exception as e:
                                print(f"Aviso ao instalar Java: {e}")
                
            except Exception as e:
                print(f"Aviso ao verificar Java: {e}")
                import traceback
                traceback.print_exc()
            
            # Classificar era do Minecraft para configuração precisa
            era = utils.get_minecraft_era(vid)
            print(f"\n>>> Era detectada: {era.upper()} para versão {vid}")
            
            # Preparar opções de lançamento
            print(f"\n>>> Preparando para iniciar...")
            set_status("Preparando para iniciar...")
            
            options = {
                "username": self.username,
                "uuid": "",
                "token": "",
                "gameDirectory": inst,
                "launcherName": "AetherLauncher",
                "launcherVersion": "4.6"
            }
            
            # Suporte a skin via URL se configurado
            skin_url = self.data.get("skin_url")
            if skin_url:
                options["custom_skin"] = skin_url
            
            # Adicionar executável Java customizado se disponível
            if java_executable and os.path.exists(java_executable):
                options["executablePath"] = java_executable
                print(f">>> Usando Java: {java_executable}")
            
            # Obter comando de lançamento
            print(f">>> Gerando comando de execucao...")
            cmd = minecraft_launcher_lib.command.get_minecraft_command(
                version=final_vid,
                minecraft_directory=self.mc_dir,
                options=options
            )
            
            # Configurar ambiente Linux baseado na era
            if self.data.get("use_mesa_optim", True):
                env = utils.get_compatibility_env(is_recent=(era in ["v21", "modern"]))
            else:
                env = os.environ.copy()
            
            # Aplicar configurações extras de compatibilidade
            if p.get("compatibility_mode", True):
                print(f">>> Aplicando configuracoes de compatibilidade para era {era.upper()}...")
                
                # Java options baseadas nas configurações de performance e era
                java_opts = []
                
                # RAM Dinâmica
                ram_mb = self.data.get("ram_mb", 4096)
                java_opts.extend([f"-Xmx{ram_mb}M", f"-Xms{ram_mb//2}M"])
                
                # Aikar's Flags (Performance)
                if self.data.get("use_aikar", True):
                    java_opts.extend(utils.get_performance_args())
                
                # Flags de Compatibilidade Universais
                java_opts.extend([
                    "-Dsun.java2d.opengl=true",
                    "-Dorg.lwjgl.util.NoChecks=true",
                    "-Djava.net.preferIPv4Stack=true"
                ])
                
                    # Flags Específicas para Eras Modernas (Java 17/21+) - DESBLOQUEIO TOTAL LINUX
                if era in ["v21", "modern"]:
                    java_opts.extend([
                        "--add-modules", "java.base,java.desktop",
                        "--add-opens", "java.base/java.lang=ALL-UNNAMED",
                        "--add-opens", "java.base/java.util=ALL-UNNAMED",
                        "--add-opens", "java.base/java.io=ALL-UNNAMED",
                        "--add-opens", "java.base/java.net=ALL-UNNAMED",
                        "--add-opens", "java.base/java.nio=ALL-UNNAMED",
                        "--add-opens", "java.base/sun.nio.ch=ALL-UNNAMED",
                        "--add-opens", "java.base/sun.reflect.annotation=ALL-UNNAMED",
                        "--add-opens", "java.desktop/sun.awt=ALL-UNNAMED",
                        "--add-opens", "java.desktop/sun.java2d=ALL-UNNAMED",
                        "--add-opens", "jdk.unsupported/sun.misc=ALL-UNNAMED",
                        "-Dorg.lwjgl.util.NoChecks=true",
                        "-Dorg.lwjgl.util.Debug=false",
                        "-Dorg.lwjgl.system.allocator=system"
                    ])
                    if era == "v21":
                        java_opts.append("-Djava.awt.headless=false")
                        # Remover flags de performance se estiverem causando conflito na 1.21
                        if "-XX:MaxTenuringThreshold=1" in java_opts:
                            java_opts.remove("-XX:MaxTenuringThreshold=1")
                
                # Flags para Eras Antigas (Legado e Ancestral)
                if era in ["legacy", "ancient"]:
                    java_opts.extend([
                        "-Dfml.ignoreInvalidMinecraftCertificates=true",
                        "-Dfml.ignorePatchDiscrepancies=true"
                    ])
                    if era == "ancient":
                        env["LIBGL_ALWAYS_SOFTWARE"] = "1" # Forçar estabilidade em versões muito antigas
                        java_opts.append("-Dminecraft.applet.TargetDirectory=" + inst)
                
                # Aplicar opções ao ambiente
                env["_JAVA_OPTIONS"] = " ".join(java_opts)
                print(f"    - Java options da era {era.upper()} aplicadas")
            
            set_status("Iniciando Minecraft...")
            
            # Log resumido
            print(f"\n{'='*60}")
            print("INICIANDO MINECRAFT")
            print(f"{'='*60}")
            print(f"Versao: {final_vid}")
            print(f"Diretorio: {inst}")
            print(f"Java: {java_executable if java_executable else 'sistema'}")
            print(f"{'='*60}\n")
            
            # Iniciar processo
            # Adicionar flag para ignorar erros de inicialização de classes se necessário
            final_cmd = cmd
             # Sistema de Seleção de Driver (Manual ou Auto-Tune)
            manual_profile = self.data.get("manual_profile")
            
            if not self.data.get("use_autotune", True) and manual_profile is not None:
                print(f">>> Usando Perfil de Driver Manual: {manual_profile}")
                env = utils.get_compatibility_env(is_recent=(era in ["v21", "modern"]), profile_index=manual_profile)
            elif self.data.get("use_autotune", True) and self.data.get("best_profile") is None:
                print(">>> Iniciando Auto-Tune de Hardware...")
                profiles = utils.get_autotune_profiles()
                best_id = 0
                
                for profile in profiles:
                    print(f"    - Testando Perfil: {profile['name']}...")
                    test_env = utils.get_compatibility_env(is_recent=(era in ["v21", "modern"]), profile_index=profile['id'])
                    test_env.update(env) # Mantém as outras variáveis
                    
                    try:
                        p_test = subprocess.Popen(cmd, env=test_env, cwd=inst, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        time.sleep(3) # Espera 3 segundos para ver se crasha
                        if p_test.poll() is None:
                            print(f"    - SUCESSO: Perfil {profile['name']} funcionou!")
                            best_id = profile['id']
                            p_test.kill()
                            break
                        else:
                            print(f"    - FALHA: Perfil {profile['name']} incompatível.")
                            p_test.kill()
                    except: pass
                
                self.data["best_profile"] = best_id
                self.save_launcher_data()
                env = utils.get_compatibility_env(is_recent=(era in ["v21", "modern"]), profile_index=best_id)

            elif self.data.get("best_profile") is not None:
                env = utils.get_compatibility_env(is_recent=(era in ["v21", "modern"]), profile_index=self.data["best_profile"])

            # Iniciar processo final
            final_cmd = cmd
            if self.data.get("use_high_priority", True):
                final_cmd = ["nice", "-n", "0"] + cmd
                try: final_cmd = ["ionice", "-c", "2", "-n", "4"] + final_cmd
                except: pass

            process = subprocess.Popen(final_cmd, env=env, cwd=inst, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            
            print(f">>> Processo iniciado! PID: {process.pid}\n")
            
            # Monitorar saída
            def monitor_process():
                print("=== SAIDA DO MINECRAFT ===\n")
                error_lines = []
                
                for line in iter(process.stdout.readline, ''):
                    if line:
                        line_clean = line.rstrip()
                        print(f"[MC] {line_clean}")
                        
                        if "ERROR" in line_clean or "Exception" in line_clean or "FATAL" in line_clean:
                            error_lines.append(line_clean)
                
                process.wait()
                exit_code = process.returncode
                
                print(f"\n=== MINECRAFT ENCERRADO (codigo: {exit_code}) ===\n")
                
                if exit_code != 0:
                    error_msg = f"Minecraft encerrou com erro (codigo {exit_code})"
                    
                    if error_lines:
                        error_msg += f"\n\nErro principal:\n{error_lines[-1][:150]}"
                    
                    error_msg += "\n\nVerifique o console para detalhes."
                    self.root.after(0, lambda: messagebox.showerror("Erro", error_msg))
            
            threading.Thread(target=monitor_process, daemon=True).start()
            
            import time
            time.sleep(2)
            
        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            print(f"\n{'='*60}")
            print("ERRO FATAL")
            print(f"{'='*60}")
            print(error_msg)
            print(f"{'='*60}\n")
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro:\n{str(e)}\n\nVeja console para detalhes."))
            
        finally:
            self.downloading = False
            self.root.after(0, lambda: self.btn_play.config(state="normal", text="JOGAR"))
            self.root.after(0, lambda: self.show_home())

if __name__ == "__main__":
    root = tk.Tk(); app = AetherLauncherUI(root); root.mainloop()
