import os
import json
import urllib.request
import ssl
import sys
import shutil

class AetherUpdater:
    def __init__(self):
        self.base_url = "https://raw.githubusercontent.com/DragonSCPOFICIAL/Arch-Linux/main/AetherLauncher/"
        self.install_dir = "/opt/aetherlauncher"
        if not os.path.exists(self.install_dir):
            self.install_dir = os.path.dirname(os.path.abspath(__file__))
            
        self.files_to_update = [
            "AetherLauncher.sh",
            "updater.py",
            "version.json",
            "uninstall.sh",
            "src/main.py",
            "src/core.py",
            "src/hardware.py"
        ]

    def get_remote_version(self):
        try:
            url = self.base_url + "version.json"
            headers = {'User-Agent': 'Mozilla/5.0'}
            context = ssl._create_unverified_context()
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10, context=context) as response:
                return json.load(response)
        except Exception as e:
            print(f"Erro ao buscar versão remota: {e}")
            return None

    def update(self):
        print("Iniciando Atualização do Aether Launcher")
        remote_info = self.get_remote_version()
        if not remote_info:
            print("Falha ao conectar ao GitHub.")
            return False

        for file_path in self.files_to_update:
            print(f"Atualizando: {file_path}...")
            try:
                url = self.base_url + file_path
                headers = {'User-Agent': 'Mozilla/5.0'}
                context = ssl._create_unverified_context()
                req = urllib.request.Request(url, headers=headers)
                
                target_path = os.path.join(self.install_dir, file_path)
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                with urllib.request.urlopen(req, timeout=15, context=context) as response:
                    with open(target_path, 'wb') as f:
                        f.write(response.read())
                
                if file_path.endswith(".sh") or file_path == "updater.py":
                    os.chmod(target_path, 0o755)
            except Exception as e:
                print(f"Erro ao atualizar {file_path}: {e}")
                return False

        print(f"Atualizado para v{remote_info["version"]} (Build {remote_info["build"]})")
        return True

if __name__ == "__main__":
    updater = AetherUpdater()
    if updater.update():
        print("Sucesso! Reinicie o launcher.")
    else:
        print("Falha na atualização.")
        sys.exit(1)
