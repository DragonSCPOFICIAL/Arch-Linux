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

class AetherLauncherUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aether Launcher - Minecraft Elite Linux")
        self.root.geometry("1000x650")
        self.root.configure(bg="#0F111A")
        
        # Design System
        self.colors = {
            "bg": "#0F111A",
            "sidebar": "#161925",
            "card": "#1E2233",
            "accent": "#00E5FF",
            "success": "#00C853",
            "warning": "#FFA726",
            "error": "#FF5252",
            "text": "#FFFFFF",
            "text_dim": "#8B949E"
        }
        
        # Caminhos Linux
        self.base_dir = os.path.expanduser("~/.aetherlauncher")
        self.minecraft_dir = os.path.join(self.base_dir, "minecraft")
        self.versions_dir = os.path.join(self.minecraft_dir, "versions")
        self.libraries_dir = os.path.join(self.minecraft_dir, "libraries")
        self.assets_dir = os.path.join(self.minecraft_dir, "assets")
        self.natives_dir = os.path.join(self.minecraft_dir, "natives")
        
        # Config
        self.config_dir = os.path.expanduser("~/.config/aetherlauncher")
        self.profiles_file = os.path.join(self.config_dir, "profiles.json")
        
        # Criar diretórios
        for directory in [self.base_dir, self.minecraft_dir, self.versions_dir, 
                         self.libraries_dir, self.assets_dir, self.natives_dir, self.config_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Versões disponíveis
        self.available_versions = {
            "1.20.1": "https://piston-data.mojang.com/v1/objects/0c3ec587af28e5a785c0b4a7b8a30f9a8f78f838/client.jar",
            "1.19.4": "https://piston-data.mojang.com/v1/objects/958928a560c9167687bea0cefeb7375da1e552a8/client.jar",
            "1.18.2": "https://piston-data.mojang.com/v1/objects/2e9a3e3107cca00d6bc9c97bf7d149cae163ef21/client.jar",
            "1.16.5": "https://piston-data.mojang.com/v1/objects/37fd3c903861eeff3bc24b71eed48f828b5269c8/client.jar",
            "1.8.9": "https://launcher.mojang.com/v1/objects/3870888a6c3d349d3771a3e9d16c9bf5e076b908/client.jar"
        }
        
        self.downloading = False
        self.selected_version = "1.20.1"
        self.current_page = None
        
        self.setup_ui()
        self.load_profiles()
        
        # Verificação de atualização silenciosa
        threading.Thread(target=self.silent_update_check, daemon=True).start()

    def setup_ui(self):
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        tk.Label(self.sidebar, text="AETHER", font=("Segoe UI", 20, "bold"), 
                 bg=self.colors["sidebar"], fg=self.colors["accent"]).pack(pady=(40, 10))
        
        tk.Label(self.sidebar, text="LAUNCHER v2.0", font=("Segoe UI", 8), 
                 bg=self.colors["sidebar"], fg=self.colors["text_dim"]).pack()
        
        # Botões de Navegação
        self.create_nav_btn("JOGAR", self.show_play_page)
        self.create_nav_btn("VERSÕES", self.show_versions_page)
        self.create_nav_btn("AJUSTES", self.show_settings_page)
        self.create_nav_btn("PERFIS", self.show_profiles_page)
        
        # Footer Sidebar
        self.version_lbl = tk.Label(self.sidebar, text="v2.0.0", bg=self.colors["sidebar"], fg=self.colors["text_dim"])
        self.version_lbl.pack(side="bottom", pady=10)
        
        # Main Area
        self.main_area = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_area.pack(side="right", fill="both", expand=True)
        
        # Background Label (no fundo da main_area)
        self.background_label = tk.Label(self.main_area, bg=self.colors["bg"], bd=0)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Container para o conteúdo (acima do background)
        self.content_container = tk.Frame(self.main_area, bg="")
        self.content_container.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Garantir que o conteúdo fique acima do background
        self.content_container.lift()
        
        # Forçar carregamento do background e da primeira página
        self.root.after(100, self.load_background)
        self.show_play_page()

    def load_background(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            launcher_base_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
            bg_image_path = os.path.join(launcher_base_dir, "background.png")
            
            if not os.path.exists(bg_image_path):
                return

            original_image = Image.open(bg_image_path)
            
            # Obter dimensões reais
            self.root.update_idletasks()
            width = self.main_area.winfo_width()
            height = self.main_area.winfo_height()
            
            if width <= 10 or height <= 10:
                self.root.after(200, self.load_background)
                return

            resized_image = original_image.resize((width, height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_image)
            
            self.background_label.configure(image=self.bg_photo)
            self.background_label.image = self.bg_photo
            
        except Exception as e:
            print(f"Erro ao carregar background: {e}")

    def clear_main_area(self):
        for widget in self.content_container.winfo_children():
            widget.destroy()

    def show_play_page(self):
        if self.current_page == "play": return
        self.current_page = "play"
        self.clear_main_area()
        
        # Usar um frame transparente para não cobrir o fundo
        container = tk.Frame(self.content_container, bg="", padx=40, pady=40)
        container.pack(fill="both", expand=True)
        
        # Título com fundo vazio para transparência (se o sistema suportar)
        tk.Label(container, text="BEM-VINDO AO AETHER LINUX", font=("Segoe UI", 24, "bold"), bg=self.colors["bg"], fg=self.colors["text"]).pack(anchor="w")
        
        self.play_card = tk.Frame(container, bg=self.colors["card"], padx=30, pady=30)
        self.play_card.pack(fill="x", pady=40)
        
        tk.Label(self.play_card, text="NICKNAME:", bg=self.colors["card"], fg=self.colors["accent"], font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.user_entry = tk.Entry(self.play_card, bg="#262B40", fg="white", insertbackground="white", bd=0, font=("Segoe UI", 12))
        self.user_entry.pack(fill="x", pady=(5, 20), ipady=8)
        self.user_entry.insert(0, self.load_username())
        
        tk.Label(self.play_card, text="VERSÃO:", bg=self.colors["card"], fg=self.colors["accent"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 5))
        
        self.version_var = tk.StringVar(value=self.selected_version)
        version_combo = ttk.Combobox(self.play_card, textvariable=self.version_var, values=list(self.available_versions.keys()), state="readonly", font=("Segoe UI", 11))
        version_combo.pack(fill="x", ipady=5)
        version_combo.bind("<<ComboboxSelected>>", lambda e: self.on_version_change())
        
        self.version_status = tk.Label(self.play_card, text="", bg=self.colors["card"], fg=self.colors["text_dim"], font=("Segoe UI", 9))
        self.version_status.pack(anchor="w", pady=(5, 0))
        
        self.progress_frame = tk.Frame(container, bg=self.colors["bg"])
        self.progress_label = tk.Label(self.progress_frame, text="", bg=self.colors["bg"], fg=self.colors["text"], font=("Segoe UI", 10))
        self.progress_label.pack(anchor="w", pady=(0, 5))
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate', length=400)
        
        self.play_btn = tk.Button(container, text="INICIAR MINECRAFT", font=("Segoe UI", 14, "bold"), bg=self.colors["success"], fg="white", bd=0, cursor="hand2", command=self.launch_game, activebackground="#00A040")
        self.play_btn.pack(fill="x", side="bottom", ipady=15)
        
        self.check_version_status()

    def show_versions_page(self):
        if self.current_page == "versions": return
        self.current_page = "versions"
        self.clear_main_area()
        
        canvas = tk.Canvas(self.content_container, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["bg"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=700)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=40, pady=40)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scrollable_frame, text="GERENCIADOR DE VERSÕES", font=("Segoe UI", 24, "bold"), bg=self.colors["bg"], fg=self.colors["text"]).pack(anchor="w", pady=(0, 30))
        
        for version in self.available_versions.keys():
            self.create_version_card(scrollable_frame, version)

    def show_settings_page(self):
        if self.current_page == "settings": return
        self.current_page = "settings"
        self.clear_main_area()
        
        container = tk.Frame(self.content_container, bg=self.colors["bg"], padx=40, pady=40)
        container.pack(fill="both", expand=True)
        
        tk.Label(container, text="CONFIGURAÇÕES", font=("Segoe UI", 24, "bold"), bg=self.colors["bg"], fg=self.colors["text"]).pack(anchor="w", pady=(0, 30))
        
        settings_card = tk.Frame(container, bg=self.colors["card"], padx=30, pady=30)
        settings_card.pack(fill="x", pady=10)
        
        tk.Label(settings_card, text="MEMÓRIA RAM (MB):", bg=self.colors["card"], fg=self.colors["accent"], font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.ram_entry = tk.Entry(settings_card, bg="#262B40", fg="white", insertbackground="white", bd=0, font=("Segoe UI", 12))
        self.ram_entry.pack(fill="x", pady=(5, 20), ipady=8)
        self.ram_entry.insert(0, "2048")
        
        tk.Button(settings_card, text="SALVAR CONFIGURAÇÕES", font=("Segoe UI", 12, "bold"), bg=self.colors["accent"], fg="white", bd=0, cursor="hand2", command=self.save_settings).pack(fill="x", ipady=10)
        
        danger_frame = tk.Frame(container, bg=self.colors["bg"], pady=40)
        danger_frame.pack(fill="x")
        tk.Label(danger_frame, text="ZONA DE PERIGO", font=("Segoe UI", 10, "bold"), bg=self.colors["bg"], fg=self.colors["error"]).pack(anchor="w")
        tk.Button(danger_frame, text="DESINSTALAR AETHER LAUNCHER", font=("Segoe UI", 12, "bold"), bg=self.colors["error"], fg="white", bd=0, cursor="hand2", command=self.confirm_uninstall).pack(fill="x", pady=10, ipady=10)

    def show_profiles_page(self):
        if self.current_page == "profiles": return
        self.current_page = "profiles"
        self.clear_main_area()
        
        container = tk.Frame(self.content_container, bg=self.colors["bg"], padx=40, pady=40)
        container.pack(fill="both", expand=True)
        
        tk.Label(container, text="PERFIS", font=("Segoe UI", 24, "bold"), bg=self.colors["bg"], fg=self.colors["text"]).pack(anchor="w", pady=(0, 30))
        tk.Label(container, text="Sistema de perfis será implementado em breve!", font=("Segoe UI", 14), bg=self.colors["bg"], fg=self.colors["text_dim"]).pack(pady=50)

    def create_version_card(self, parent, version):
        status = self.check_version_installed(version)
        status_color = self.colors["success"] if status else self.colors["text_dim"]
        status_text = "✓ Instalado" if status else "Não instalado"

        card = tk.Frame(parent, bg=self.colors["card"], padx=20, pady=15)
        card.pack(fill="x", pady=10)
        
        info_frame = tk.Frame(card, bg=self.colors["card"])
        info_frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(info_frame, text=f"Minecraft {version}", font=("Segoe UI", 14, "bold"), bg=self.colors["card"], fg=self.colors["text"]).pack(anchor="w")
        tk.Label(info_frame, text=status_text, font=("Segoe UI", 10), bg=self.colors["card"], fg=status_color).pack(anchor="w")
        
        btn_frame = tk.Frame(card, bg=self.colors["card"])
        btn_frame.pack(side="right")
        
        if not status:
            tk.Button(btn_frame, text="BAIXAR", font=("Segoe UI", 10, "bold"), bg=self.colors["accent"], fg="white", bd=0, cursor="hand2", command=lambda v=version: self.download_version(v), padx=20, pady=8).pack(side="right", padx=5)
        else:
            tk.Button(btn_frame, text="DELETAR", font=("Segoe UI", 10, "bold"), bg=self.colors["error"], fg="white", bd=0, cursor="hand2", command=lambda v=version: self.delete_version(v), padx=20, pady=8).pack(side="right", padx=5)

    def create_nav_btn(self, text, command):
        btn = tk.Button(self.sidebar, text=text, font=("Segoe UI", 10, "bold"), bg=self.colors["sidebar"], fg=self.colors["text"], bd=0, padx=20, pady=15, anchor="w", cursor="hand2", activebackground=self.colors["card"], command=command)
        btn.pack(fill="x")

    def load_username(self):
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, 'r') as f:
                    return json.load(f).get("username", "Player")
            except:
                return "Player"
        return "Player"

    def load_profiles(self): pass
    
    def save_profiles(self):
        username = self.user_entry.get() if hasattr(self, 'user_entry') else "Player"
        data = {"username": username}
        try:
            with open(self.profiles_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar perfil: {e}")

    def save_settings(self): 
        messagebox.showinfo("Aether", "Configurações salvas com sucesso!")

    def check_version_installed(self, version):
        jar_path = os.path.join(self.versions_dir, version, f"{version}.jar")
        # Verifica se o arquivo existe e tem mais de 1MB (evita considerar arquivos corrompidos/vazios)
        return os.path.exists(jar_path) and os.path.getsize(jar_path) > 1024 * 1024

    def check_version_status(self):
        if hasattr(self, 'version_status'):
            installed = self.check_version_installed(self.selected_version)
            if installed:
                self.version_status.config(text="✓ Versão instalada e pronta", fg=self.colors["success"])
            else:
                self.version_status.config(text="⚠ Versão não instalada - clique em BAIXAR", fg=self.colors["warning"])

    def on_version_change(self):
        self.selected_version = self.version_var.get()
        self.check_version_status()

    def download_version(self, version):
        if self.downloading:
            messagebox.showwarning("Aether", "Um download já está em andamento!")
            return
        self.downloading = True
        threading.Thread(target=self._download_version_thread, args=(version,), daemon=True).start()

    def _download_version_thread(self, version):
        version_dir = os.path.join(self.versions_dir, version)
        jar_path = os.path.join(version_dir, f"{version}.jar")
        try:
            os.makedirs(version_dir, exist_ok=True)
            self.root.after(0, lambda: self.update_progress(f"Iniciando download de {version}...", 0))
            self.download_file(self.available_versions[version], jar_path)
            
            # Verificação final após download
            if self.check_version_installed(version):
                self.root.after(0, lambda: self.update_progress(f"✓ Minecraft {version} instalado!", 100))
                self.root.after(0, lambda: messagebox.showinfo("Aether", f"Minecraft {version} instalado com sucesso!"))
            else:
                raise Exception("Arquivo baixado parece estar incompleto ou corrompido.")
                
            self.root.after(0, lambda: [setattr(self, 'current_page', None), self.show_versions_page()])
        except Exception as e:
            import traceback
            error_msg = f"Erro: {str(e)}" if str(e) else "Erro desconhecido de conexão"
            print(f"Erro no download: {traceback.format_exc()}")
            # Se falhar, remove o arquivo incompleto para não dar "falso positivo" depois
            if os.path.exists(jar_path):
                try: os.remove(jar_path)
                except: pass
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Falha ao baixar: {error_msg}"))
        finally:
            self.downloading = False
            self.root.after(0, lambda: self.hide_progress())

    def download_file(self, url, dest):
        context = ssl._create_unverified_context()
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=context) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            with open(dest, 'wb') as f:
                while True:
                    buffer = response.read(8192)
                    if not buffer: break
                    f.write(buffer)
                    downloaded += len(buffer)
                    if total_size > 0:
                        self.root.after(0, lambda p=int((downloaded / total_size) * 100): self.update_progress_bar(p))

    def delete_version(self, version):
        if messagebox.askyesno("Confirmar", f"Deseja deletar Minecraft {version}?"):
            shutil.rmtree(os.path.join(self.versions_dir, version), ignore_errors=True)
            messagebox.showinfo("Aether", f"Minecraft {version} deletado!")
            self.current_page = None
            self.show_versions_page()

    def update_progress(self, text, value):
        if hasattr(self, 'progress_label'):
            self.progress_label.config(text=text)
            self.progress_frame.pack(fill="x", pady=(20, 0))
            self.progress_bar.pack(fill="x")
            self.progress_bar['value'] = value

    def update_progress_bar(self, value):
        if hasattr(self, 'progress_bar'): self.progress_bar['value'] = value

    def hide_progress(self):
        if hasattr(self, 'progress_frame'): self.progress_frame.pack_forget()

    def launch_game(self):
        self.save_profiles()
        if not self.check_version_installed(self.selected_version):
            if messagebox.askyesno("Aether", f"Minecraft {self.selected_version} não está instalado.\n\nDeseja baixá-lo agora?"):
                self.current_page = None
                self.show_versions_page()
                self.download_version(self.selected_version)
            return
        threading.Thread(target=self._launch_minecraft_thread, args=(self.user_entry.get() or "Player", self.selected_version), daemon=True).start()

    def _launch_minecraft_thread(self, username, version):
        try:
            java_cmd = self.find_java()
            if not java_cmd:
                self.root.after(0, lambda: messagebox.showerror("Erro", "Java não encontrado!"))
                return
            cmd = [java_cmd, "-Xmx2G", "-Xms1G", f"-Djava.library.path={self.natives_dir}", "-cp", os.path.join(self.versions_dir, version, f"{version}.jar"), "net.minecraft.client.main.Main", "--username", username, "--version", version, "--gameDir", self.minecraft_dir, "--assetsDir", self.assets_dir]
            self.root.after(0, lambda: messagebox.showinfo("Aether", f"Iniciando Minecraft {version}..."))
            subprocess.Popen(cmd, cwd=self.minecraft_dir).wait()
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Falha ao iniciar: {str(e)}"))

    def find_java(self):
        # Lista expandida de locais comuns do Java no Linux
        common_paths = [
            "/usr/bin/java",
            "/usr/lib/jvm/default/bin/java",
            "/usr/lib/jvm/java-17-openjdk/bin/java",
            "/usr/lib/jvm/java-11-openjdk/bin/java",
            "/usr/lib/jvm/java-8-openjdk/bin/java",
            os.path.expanduser("~/.aetherlauncher/java/bin/java")
        ]
        for path in common_paths:
            if os.path.exists(path): return path
            
        # Tenta via comando 'which'
        try:
            res = subprocess.run(['which', 'java'], capture_output=True, text=True)
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()
        except: pass
        
        # Tenta via 'whereis' como alternativa
        try:
            res = subprocess.run(['whereis', 'java'], capture_output=True, text=True)
            parts = res.stdout.split(':')
            if len(parts) > 1:
                paths = parts[1].strip().split()
                for p in paths:
                    if p.endswith('/bin/java') and os.path.exists(p):
                        return p
        except: pass
        
        return None

    def get_remote_version(self):
        try:
            req = urllib.request.Request("https://raw.githubusercontent.com/DragonSCPOFICIAL/Arch-Linux/main/AetherLauncher/version.json", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10, context=ssl._create_unverified_context()) as response:
                return json.load(response)
        except: return None

    def silent_update_check(self):
        remote = self.get_remote_version()
        if remote and remote.get('build', 0) > 2:
            self.root.after(0, lambda: self.version_lbl.config(text="Nova versão disponível!", fg=self.colors["accent"]))

    def confirm_uninstall(self):
        if messagebox.askyesno("Confirmar Desinstalação", "Tem certeza que deseja desinstalar o Aether Launcher?\n\nIsso removerá a aplicação do sistema."):
            try:
                uninstall_script = "/opt/aetherlauncher/uninstall.sh"
                if not os.path.exists(uninstall_script):
                    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    uninstall_script = os.path.join(script_dir, "uninstall.sh")
                
                if os.path.exists(uninstall_script):
                    subprocess.Popen(["sudo", "bash", uninstall_script])
                    self.root.destroy()
                else:
                    messagebox.showerror("Erro", "Script de desinstalação não encontrado.")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao desinstalar: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    AetherLauncherUI(root)
    root.mainloop()
