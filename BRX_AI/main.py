import os
import subprocess
import requests
import datetime
import glob
import time
import shutil
from pathlib import Path

# =========================
# CONFIG FIXA
# =========================
ALLOWED_REPO_URL = "https://github.com/DragonSCPOFICIAL/ULX"
ALLOWED_REPO_NAME = "ULX"
WORKDIR = "./ULX_WORKDIR"

CONFIG_DIR = Path.home() / ".config" / "brx_ai"
TOKEN_FILE = CONFIG_DIR / "github_token.secure"

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    HEADER = '\033[95m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

class BRXAgent:
    def __init__(self):
        self.name = "BRX AI - ULX AUTONOMOUS CORE"
        self.version = "5.1.0-SECURE"
        self.model = "deepseek-coder:1.3b"
        self.api_url = "http://localhost:11434/api/generate"
        self.github_token = None

    # =========================
    # LOG
    # =========================
    def log(self, msg, t="INFO"):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        color = {
            "INFO": Colors.BLUE,
            "AI": Colors.HEADER,
            "GIT": Colors.GREEN,
            "ERROR": Colors.FAIL,
            "WARN": Colors.WARNING
        }.get(t, Colors.BLUE)

        print(f"{Colors.BOLD}[{now}] {color}[{t}]{Colors.ENDC} {msg}")

    # =========================
    # TOKEN SEGURO
    # =========================
    def load_or_request_token(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        if TOKEN_FILE.exists():
            self.github_token = TOKEN_FILE.read_text().strip()
            return

        token = input("🔑 GitHub TOKEN (repo): ").strip()
        if len(token) < 20:
            raise Exception("Token inválido")

        TOKEN_FILE.write_text(token)
        os.chmod(TOKEN_FILE, 0o600)
        self.github_token = token

    def configure_git_auth(self):
        token = self.github_token
        self.execute("git config --global credential.helper store")
        self.execute("git config --global user.name \"BRX AI\"")
        self.execute("git config --global user.email \"brx-ai@ulx.local\"")
        self.execute(
            f"git config --global url.\"https://{token}:x-oauth-basic@github.com/\".insteadOf https://github.com/"
        )

    # =========================
    # GIT
    # =========================
    def prepare_repo(self):
        if os.path.exists(WORKDIR):
            shutil.rmtree(WORKDIR)

        self.execute(f"git clone {ALLOWED_REPO_URL} {WORKDIR}")
        os.chdir(WORKDIR)

    def git_commit(self, msg):
        self.execute("git add .")
        self.execute(f"git commit -m \"{msg}\"")
        self.execute("git push")

    # =========================
    # FS
    # =========================
    def repo_snapshot(self):
        files = {}
        for f in glob.glob("**", recursive=True):
            if os.path.isfile(f) and ".git" not in f:
                try:
                    files[f] = open(f).read()
                except:
                    pass
        return files

    # =========================
    # AI
    # =========================
    def ask_ai(self, system_prompt):
        self.log("Raciocinando...", "AI")
        r = requests.post(self.api_url, json={
            "model": self.model,
            "prompt": system_prompt,
            "stream": False
        }, timeout=120)

        return r.json().get("response", "")

    # =========================
    # AUTONOMOUS CORE
    # =========================
    def autonomous_cycle(self):
        snapshot = self.repo_snapshot()

        system_prompt = f"""
Você é um agente autônomo de engenharia de linguagens.
Seu ÚNICO objetivo é evoluir ULX.

REGRAS ABSOLUTAS:
- Trabalhe somente neste repositório
- Não peça ajuda humana
- Uma melhoria real por ciclo
- Código completo e funcional

REPOSITÓRIO:
{snapshot}

RESPONDA EXATAMENTE NO FORMATO:
AÇÃO:
ARQUIVO:
CÓDIGO:
"""

        response = self.ask_ai(system_prompt)

        if "ARQUIVO:" not in response or "CÓDIGO:" not in response:
            self.log("Resposta inválida da IA", "WARN")
            return

        try:
            _, rest = response.split("ARQUIVO:")
            path, code = rest.split("CÓDIGO:")
            path = path.strip()

            os.makedirs(os.path.dirname(path), exist_ok=True)

            with open(path, "w") as f:
                f.write(code.strip())

            self.git_commit(f"ULX AI: evolução automática em {path}")

        except Exception as e:
            self.log(str(e), "ERROR")

    # =========================
    # EXEC
    # =========================
    def execute(self, cmd):
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # =========================
    # RUN
    # =========================
    def run(self):
        print(f"\n{Colors.HEADER}{Colors.BOLD}{self.name} v{self.version}{Colors.ENDC}")

        self.load_or_request_token()
        self.configure_git_auth()
        self.prepare_repo()

        while True:
            self.autonomous_cycle()
            time.sleep(15)

if __name__ == "__main__":
    BRXAgent().run()
