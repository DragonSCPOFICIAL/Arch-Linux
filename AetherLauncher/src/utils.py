import os
import subprocess
import platform

def get_gpu_info():
    """Retorna informações básicas da GPU para decidir sobre overrides de compatibilidade."""
    try:
        res = subprocess.run(['glxinfo', '-B'], capture_output=True, text=True)
        if res.returncode == 0:
            return res.stdout
    except:
        pass
    return "Não foi possível detectar a GPU."

def get_compatibility_env():
    """Retorna um dicionário com variáveis de ambiente para melhorar a compatibilidade OpenGL no Linux."""
    env = os.environ.copy()
    # Força o uso do driver Mesa para hardware antigo se necessário
    # Estes overrides ajudam o Minecraft a rodar em placas que não suportam OpenGL 3.3+ nativamente
    env["MESA_GL_VERSION_OVERRIDE"] = "4.5"
    env["MESA_GLSL_VERSION_OVERRIDE"] = "450"
    # Melhora performance em drivers Intel/AMD antigos
    env["vblank_mode"] = "0"
    return env

def ensure_java_version(version_id):
    """Verifica e sugere a versão correta do Java baseada na versão do Minecraft."""
    try:
        v_num = float(version_id.split('.')[1])
        if v_num >= 17:
            return 17
        elif v_num >= 12:
            return 11
        else:
            return 8
    except:
        return 17 # Padrão para versões novas

def get_instance_path(base_dir, profile_name):
    """Cria e retorna o caminho isolado para uma instância."""
    path = os.path.join(base_dir, "instances", profile_name.replace(" ", "_"))
    os.makedirs(path, exist_ok=True)
    # Criar subpastas padrão para facilitar o usuário
    for sub in ["mods", "resourcepacks", "shaderpacks", "screenshots", "saves"]:
        os.makedirs(os.path.join(path, sub), exist_ok=True)
    return path
