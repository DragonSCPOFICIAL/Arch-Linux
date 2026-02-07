import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import threading
import subprocess
import ssl
import urllib.request
import shutil
import zipfile
import hashlib
from pathlib import Path
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
            "1.20.1": "https://piston-data.mojang.com/v1/objects/84194a2f286ef7c14ed60ce89ce1596734fd4f85/client.jar",
            "1.19.4": "https://piston-data.mojang.com/v1/objects/fd19469fed4a4b4c15b2d5133985f0e3e7816a8a/client.jar",
            "1.18.2": "https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/client.jar",
            "1.16.5": "https://piston-data.mojang.com/v1/objects/37fd3c903861eeff3bc24b71eed48f828b5269c8/client.jar",
            "1.8.9": "https://piston-data.mojang.com/v1/objects/2e9a3e07f61bf4f52bf69e6c3e33b4e3e0e0e0f9/client.jar"
        }
        
        self.downloading = False
        self.selected_version = "1.20.1"
        
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
        self.create_nav_btn("🎮  JOGAR", self.show_play_page)
        self.create_nav_btn("📦  VERSÕES", self.show_versions_page)
        self.create_nav_btn("⚙️  AJUSTES", self.show_settings_page)
        self.create_nav_btn("👤  PERFIS", self.show_profiles_page)
        
        # Footer Sidebar
        self.version_lbl = tk.Label(self.sidebar, text="v2.0.0", bg=self.colors["sidebar"], fg=self.colors["text_dim"])
        self.version_lbl.pack(side="bottom", pady=10)
        
        # Main Area
        # Carregar imagem de fundo
        try:
            bg_image_path = os.path.join(self.base_dir, "background.png")
            original_image = Image.open(bg_image_path)
            # Redimensionar a imagem para preencher a área principal
            # Obter as dimensões da janela principal (root)
            self.root.update_idletasks() # Atualiza para obter as dimensões corretas
            main_area_width = self.root.winfo_width() - self.sidebar.winfo_width()
            main_area_height = self.root.winfo_height()

            resized_image = original_image.resize((main_area_width, main_area_height), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_image)

            self.background_label = tk.Label(self.root, image=self.bg_photo)
            self.background_label.place(x=self.sidebar.winfo_width(), y=0, relwidth=1, relheight=1)
            self.background_label.image = self.bg_photo # Manter referência

            self.main_area = tk.Frame(self.root, bg="") # Fundo transparente para o frame
            self.main_area.place(x=self.sidebar.winfo_width(), y=0, relwidth=1, relheight=1)

        except FileNotFoundError:
            print("Arquivo de background.png não encontrado. Usando cor de fundo padrão.")
            self.main_area = tk.Frame(self.root, bg=self.colors["bg"])
            self.main_area.pack(side="right", fill="both", expand=True)
        except Exception as e:
            print(f"Erro ao carregar imagem de fundo: {e}")
            self.main_area = tk.Frame(self.root, bg=self.colors["bg"])
            self.main_area.pack(side="right", fill="both", expand=True)
        
        # Mostrar página inicial
        self.show_play_page()

    def show_play_page(self):
        self.clear_main_area()
        
        container = tk.Frame(self.main_area, bg="", padx=40, pady=40)
        container.pack(fill="both", expand=True)
        
        tk.Label(container, text="BEM-VINDO AO AETHER LINUX", font=("Segoe UI", 24, "bold"), 
                 bg="", fg=self.colors["text"]).pack(anchor="w")
        
        # Card de Jogo
        self.play_card = tk.Frame(container, bg=self.colors["card"], padx=30, pady=30)
        self.play_card.pack(fill="x", pady=40)
        
        tk.Label(self.play_card, text="NICKNAME:", bg=self.colors["card"], 
                fg=self.colors["accent"], font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.user_entry = tk.Entry(self.play_card, bg="#262B40", fg="white", 
                                   insertbackground="white", bd=0, font=("Segoe UI", 12))
        self.user_entry.pack(fill="x", pady=(5, 20), ipady=8)
        self.user_entry.insert(0, self.load_username())
        
        # Seletor de Versão
        tk.Label(self.play_card, text="VERSÃO:", bg=self.colors["card"], 
                fg=self.colors["accent"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 5))
        
        version_frame = tk.Frame(self.play_card, bg=self.colors["card"])
        version_frame.pack(fill="x", pady=(0, 20))
        
        self.version_var = tk.StringVar(value=self.selected_version)
        version_combo = ttk.Combobox(version_frame, textvariable=self.version_var, 
                                     values=list(self.available_versions.keys()),
                                     state="readonly", font=("Segoe UI", 11))
        version_combo.pack(fill="x", ipady=5)
        version_combo.bind("<<ComboboxSelected>>", lambda e: self.on_version_change())
        
        # Status da versão
        self.version_status = tk.Label(self.play_card, text="", bg=self.colors["card"], 
                                       fg=self.colors["text_dim"], font=("Segoe UI", 9))
        self.version_status.pack(anchor="w")
        
        # Barra de progresso
        self.progress_frame = tk.Frame(container, bg="")
        self.progress_label = tk.Label(self.progress_frame, text="", bg="", 
                                       fg=self.colors["text"], font=("Segoe UI", 10))
        self.progress_label.pack(anchor="w", pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate', length=400)
        
        # Botão Jogar
        self.play_btn = tk.Button(container, text="INICIAR MINECRAFT", font=("Segoe UI", 14, "bold"), 
                                 bg=self.colors["success"], fg="white", bd=0, cursor="hand2", 
                                 command=self.launch_game, activebackground="#00A040")
        self.play_btn.pack(fill="x", side="bottom", ipady=15)
        
        self.check_version_status()

    def show_versions_page(self):
        self.clear_main_area()
        
        container = tk.Frame(self.main_area, bg="", padx=40, pady=40)
        container.pack(fill="both", expand=True)
        
        tk.Label(container, text="GERENCIADOR DE VERSÕES", font=("Segoe UI", 24, "bold"), 
                 bg="", fg=self.colors["text"]).pack(anchor="w", pady=(0, 30))
        
        for version, url in self.available_versions.items():
            self.create_version_card(container, version)

    def show_settings_page(self):
        self.clear_main_area()
        
        container = tk.Frame(self.main_area, bg="", padx=40, pady=40)
        container.pack(fill="both", expand=True)
        
        tk.Label(container, text="CONFIGURAÇÕES", font=("Segoe UI", 24, "bold"), 
                 bg="", fg=self.colors["text"]).pack(anchor="w", pady=(0, 30))
        
        settings_card = tk.Frame(container, bg=self.colors["card"], padx=30, pady=30)
        settings_card.pack(fill="x", pady=10)
        
        tk.Label(settings_card, text="MEMÓRIA RAM (MB):", bg=self.colors["card"], 
                fg=self.colors["accent"], font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        self.ram_entry = tk.Entry(settings_card, bg="#262B40", fg="white", 
                                 insertbackground="white", bd=0, font=("Segoe UI", 12))
        self.ram_entry.pack(fill="x", pady=(5, 20), ipady=8)
        self.ram_entry.insert(0, "2048")
        
        tk.Button(settings_card, text="SALVAR CONFIGURAÇÕES", font=("Segoe UI", 12, "bold"), 
                 bg=self.colors["accent"], fg="white", bd=0, cursor="hand2",
                 command=self.save_settings).pack(fill="x", ipady=10)

    def show_profiles_page(self):
        self.clear_main_area()
        
        container = tk.Frame(self.main_area, bg="", padx=40, pady=40)
        container.pack(fill="both", expand=True)
        
        tk.Label(container, text="PERFIS", font=("Segoe UI", 24, "bold"), 
                 bg="", fg=self.colors["text"]).pack(anchor="w", pady=(0, 30))
        
        tk.Label(container, text="🎮 Sistema de perfis será implementado em breve!", 
                font=("Segoe UI", 14), bg="", fg=self.colors["text_dim"]).pack(pady=50)

    def create_version_card(self, parent, version):
        card = tk.Frame(parent, bg=self.colors["card"], padx=20, pady=15)
        card.pack(fill="x", pady=10)
        
        info_frame = tk.Frame(card, bg=self.colors["card"])
        info_frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(info_frame, text=f"Minecraft {version}", font=("Segoe UI", 14, "bold"), 
                bg=self.colors["card"], fg=self.colors["text"]).pack(anchor="w")
        
        status = self.check_version_installed(version)
        status_color = self.colors["success"] if status else self.colors["text_dim"]
        status_text = "✓ Instalado" if status else "Não instalado"
        
        tk.Label(info_frame, text=status_text, font=("Segoe UI", 10), 
                bg=self.colors["card"], fg=status_color).pack(anchor="w")
        
        btn_frame = tk.Frame(card, bg=self.colors["card"])
        btn_frame.pack(side="right")
        
        if not status:
            tk.Button(btn_frame, text="BAIXAR", font=("Segoe UI", 10, "bold"), 
                     bg=self.colors["accent"], fg="white", bd=0, cursor="hand2",
                     command=lambda v=version: self.download_version(v),
                     padx=20, pady=8).pack(side="right", padx=5)
        else:
            tk.Button(btn_frame, text="DELETAR", font=("Segoe UI", 10, "bold"), 
                     bg="#FF5252", fg="white", bd=0, cursor="hand2",
                     command=lambda v=version: self.delete_version(v),
                     padx=20, pady=8).pack(side="right", padx=5)

    def create_nav_btn(self, text, command):
        btn = tk.Button(self.sidebar, text=text, font=("Segoe UI", 10, "bold"), 
                       bg=self.colors["sidebar"], fg=self.colors["text"], bd=0, 
                       padx=20, pady=15, anchor="w", cursor="hand2", 
                       activebackground=self.colors["card"], command=command)
        btn.pack(fill="x")

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def load_username(self):
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, 'r') as f:
                    data = json.load(f)
                    return data.get("username", "Player")
            except:
                return "Player"
        return "Player"

    def load_profiles(self):
        pass  # Username é carregado diretamente

    def save_profiles(self):
        data = {"username": self.user_entry.get() if hasattr(self, 'user_entry') else "Player"}
        with open(self.profiles_file, 'w') as f:
            json.dump(data, f, indent=4)

    def save_settings(self):
        messagebox.showinfo("Aether", "Configurações salvas com sucesso!")

    def check_version_installed(self, version):
        jar_path = os.path.join(self.versions_dir, version, f"{version}.jar")
        return os.path.exists(jar_path)

    def check_version_status(self):
        if hasattr(self, 'version_status'):
            installed = self.check_version_installed(self.selected_version)
            if installed:
                self.version_status.config(text="✓ Versão instalada e pronta", 
                                          fg=self.colors["success"])
            else:
                self.version_status.config(text="⚠ Versão não instalada - clique em BAIXAR", 
                                          fg=self.colors["warning"])

    def on_version_change(self):
        self.selected_version = self.version_var.get()
        self.check_version_status()

    def download_version(self, version):
        if self.downloading:
            messagebox.showwarning("Aether", "Um download já está em andamento!")
            return
        
        self.downloading = True
        thread = threading.Thread(target=self._download_version_thread, args=(version,), daemon=True)
        thread.start()

    def _download_version_thread(self, version):
        try:
            version_dir = os.path.join(self.versions_dir, version)
            os.makedirs(version_dir, exist_ok=True)
            
            jar_path = os.path.join(version_dir, f"{version}.jar")
            url = self.available_versions[version]
            
            self.root.after(0, lambda: self.update_progress(f"Baixando Minecraft {version}...", 0))
            
            # Download com progresso
            self.download_file(url, jar_path)
            
            self.root.after(0, lambda: self.update_progress(f"✓ Minecraft {version} instalado!", 100))
            self.root.after(0, lambda: messagebox.showinfo("Aether", f"Minecraft {version} instalado com sucesso!"))
            self.root.after(0, self.show_versions_page)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Falha ao baixar: {str(e)}"))
        finally:
            self.downloading = False
            self.root.after(0, lambda: self.hide_progress())

    def download_file(self, url, dest):
        context = ssl._create_unverified_context()
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, context=context) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            block_size = 8192
            downloaded = 0
            
            with open(dest, 'wb') as f:
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    f.write(buffer)
                    downloaded += len(buffer)
                    
                    if total_size > 0:
                        progress = int((downloaded / total_size) * 100)
                        self.root.after(0, lambda p=progress: self.update_progress_bar(p))

    def delete_version(self, version):
        if messagebox.askyesno("Confirmar", f"Deseja deletar Minecraft {version}?"):
            version_dir = os.path.join(self.versions_dir, version)
            if os.path.exists(version_dir):
                shutil.rmtree(version_dir)
                messagebox.showinfo("Aether", f"Minecraft {version} deletado!")
                self.show_versions_page()

    def update_progress(self, text, value):
        if hasattr(self, 'progress_label'):
            self.progress_label.config(text=text)
            self.progress_frame.pack(fill="x", pady=(20, 0))
            self.progress_bar.pack(fill="x")
            self.progress_bar['value'] = value

    def update_progress_bar(self, value):
        if hasattr(self, 'progress_bar'):
            self.progress_bar['value'] = value

    def hide_progress(self):
        if hasattr(self, 'progress_frame'):
            self.progress_frame.pack_forget()

    def launch_game(self):
        self.save_profiles()
        
        if not self.check_version_installed(self.selected_version):
            response = messagebox.askyesno("Aether", 
                f"Minecraft {self.selected_version} não está instalado.\n\nDeseja baixá-lo agora?")
            if response:
                self.download_version(self.selected_version)
            return
        
        username = self.user_entry.get() or "Player"
        version = self.selected_version
        
        # Lançar Minecraft
        threading.Thread(target=self._launch_minecraft_thread, 
                        args=(username, version), daemon=True).start()

    def _launch_minecraft_thread(self, username, version):
        try:
            jar_path = os.path.join(self.versions_dir, version, f"{version}.jar")
            
            # Verificar Java
            java_cmd = self.find_java()
            if not java_cmd:
                self.root.after(0, lambda: messagebox.showerror("Erro", 
                    "Java não encontrado!\n\nInstale com: sudo pacman -S jre-openjdk"))
                return
            
            # Comando de lançamento
            cmd = [
                java_cmd,
                "-Xmx2G",
                "-Xms1G",
                f"-Djava.library.path={self.natives_dir}",
                "-cp", jar_path,
                "net.minecraft.client.main.Main",
                "--username", username,
                "--version", version,
                "--gameDir", self.minecraft_dir,
                "--assetsDir", self.assets_dir
            ]
            
            self.root.after(0, lambda: messagebox.showinfo("Aether", 
                f"Iniciando Minecraft {version}...\n\nUsuário: {username}"))
            
            process = subprocess.Popen(cmd, cwd=self.minecraft_dir,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Aguardar o processo
            process.wait()
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", 
                f"Falha ao iniciar Minecraft:\n{str(e)}"))

    def find_java(self):
        """Encontra o executável Java no sistema"""
        java_paths = [
            "/usr/bin/java",
            "/usr/lib/jvm/default/bin/java",
            "/usr/lib/jvm/java-17-openjdk/bin/java",
            "/usr/lib/jvm/java-11-openjdk/bin/java",
            "/usr/lib/jvm/java-8-openjdk/bin/java"
        ]
        
        for path in java_paths:
            if os.path.exists(path):
                return path
        
        # Tentar via PATH
        try:
            result = subprocess.run(['which', 'java'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return None

    def get_remote_version(self):
        try:
            url = "https://raw.githubusercontent.com/DragonSCPOFICIAL/Arch-Linux/main/AetherLauncher/version.json"
            headers = {'User-Agent': 'Mozilla/5.0'}
            context = ssl._create_unverified_context()
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10, context=context) as response:
                return json.load(response)
        except:
            return None

    def silent_update_check(self):
        remote = self.get_remote_version()
        if remote and remote.get('build', 0) > 2:  # Build 2 é a v2.0.0
            self.root.after(0, lambda: self.version_lbl.config(
                text="Nova versão disponível!", fg=self.colors["accent"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = AetherLauncherUI(root)
    root.mainloop()
