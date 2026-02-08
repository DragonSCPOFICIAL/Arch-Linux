import os
import subprocess
import platform
import shutil

def get_system_info():
    """Retorna um dicionário com informações detalhadas do sistema para otimização."""
    info = {
        "ram_gb": 4,
        "gpu_vendor": "unknown",
        "has_vulkan": False,
        "cpu_cores": 1
    }
    
    try:
        # Detectar RAM total
        with open('/proc/meminfo', 'r') as f:
            mem = f.readline()
            info["ram_gb"] = int(mem.split()[1]) // 1024 // 1024
    except: pass

    try:
        # Detectar CPU cores
        info["cpu_cores"] = os.cpu_count() or 1
    except: pass

    try:
        # Detectar GPU e Vulkan
        gpu_res = subprocess.run(['glxinfo', '-B'], capture_output=True, text=True, timeout=2)
        if "Intel" in gpu_res.stdout: info["gpu_vendor"] = "intel"
        elif "AMD" in gpu_res.stdout: info["gpu_vendor"] = "amd"
        elif "NVIDIA" in gpu_res.stdout: info["gpu_vendor"] = "nvidia"
        
        vulkan_res = subprocess.run(['vulkaninfo', '--summary'], capture_output=True, text=True, timeout=2)
        info["has_vulkan"] = vulkan_res.returncode == 0
    except: pass
    
    return info

def get_gpu_info():
    """Retorna informações legíveis da GPU."""
    info = get_system_info()
    return f"GPU: {info['gpu_vendor'].upper()} | RAM: {info['ram_gb']}GB | Cores: {info['cpu_cores']}"

def get_compatibility_env(is_recent=True):
    """
    Configura o ambiente Linux para o conector do Minecraft.
    is_recent: True para 1.17+, False para versões antigas.
    """
    env = os.environ.copy()
    
    # Otimizações de driver Mesa (O "segredo" do Linux)
    # Zink é um driver que traduz OpenGL para Vulkan, excelente para GPUs que pararam no OpenGL 3.x/4.x
    env["MESA_GL_VERSION_OVERRIDE"] = "4.6" if is_recent else "3.2"
    env["MESA_GLSL_VERSION_OVERRIDE"] = "460" if is_recent else "150"
    
    # Tenta forçar o driver Zink para melhor compatibilidade em hardware antigo
    env["MESA_LOADER_DRIVER_OVERRIDE"] = "zink"
    env["GALLIUM_DRIVER"] = "zink"
    
    # Desabilita sincronização vertical para ganhar FPS e reduzir input lag
    env["vblank_mode"] = "0"
    env["__GL_SYNC_TO_VBLANK"] = "0"
    
    # Otimizações de Memória e Driver para GPUs Fracas
    env["MESA_DEBUG"] = "silent"
    env["allow_glsl_extension_directive_mid_shader"] = "true"
    env["pre_shader_compiler"] = "true"
    
    # Otimizações de Memória de Vídeo (VRAM)
    env["mesa_glthread"] = "true" # Multithreading no driver OpenGL (Ganho de FPS)
    env["MESA_EXTENSION_MAX_YEAR"] = "2024"
    env["MESA_GL_VERSION_OVERRIDE"] = "4.6"
    
    # Cache de Shaders (Evita stutters em GPUs fracas)
    shader_cache_dir = os.path.expanduser("~/.cache/aetherlauncher/shaders")
    os.makedirs(shader_cache_dir, exist_ok=True)
    env["MESA_SHADER_CACHE_DIR"] = shader_cache_dir
    env["MESA_SHADER_CACHE_MAX_SIZE"] = "1G"
    
    # Corrige problemas de interface em algumas distros
    env["_JAVA_AWT_WM_NONREPARENTING"] = "1"
    
    # No Linux, ExceptionInInitializerError muitas vezes é conflito entre bibliotecas nativas
    # Vamos deixar o launcher gerenciar os natives, mas garantir que os drivers de vídeo do sistema estejam acessíveis
    sys_libs = "/usr/lib/x86_64-linux-gnu:/usr/lib64:/usr/lib"
    if "LD_LIBRARY_PATH" in env:
        env["LD_LIBRARY_PATH"] = f"{env['LD_LIBRARY_PATH']}:{sys_libs}"
    else:
        env["LD_LIBRARY_PATH"] = sys_libs
    
    # Garantir que o Java não tente usar o Wayland se estiver dando erro (forçar X11)
    env["_JAVA_AWT_WM_NONREPARENTING"] = "1"
    env["QT_QPA_PLATFORM"] = "xcb"
    env["GDK_BACKEND"] = "x11"
    
    return env

def get_performance_args():
    """Retorna argumentos de JVM de alta performance (Aikar's Flags otimizadas para cliente)."""
    return [
        "-XX:+UseG1GC",
        "-XX:+ParallelRefProcEnabled",
        "-XX:MaxGCPauseMillis=200",
        "-XX:+UnlockExperimentalVMOptions",
        "-XX:+DisableExplicitGC",
        "-XX:+AlwaysPreTouch",
        "-XX:G1NewSizePercent=30",
        "-XX:G1MaxNewSizePercent=40",
        "-XX:G1HeapRegionSize=8M",
        "-XX:G1ReservePercent=20",
        "-XX:G1HeapWastePercent=5",
        "-XX:G1MixedGCCountTarget=4",
        "-XX:InitiatingHeapOccupancyPercent=15",
        "-XX:G1MixedGCLiveThresholdPercent=90",
        "-XX:G1RSetUpdatingPauseTimePercent=5",
        "-XX:SurvivorRatio=32",
        "-XX:+PerfDisableSharedMem",
        "-XX:MaxTenuringThreshold=1",
        "-Dusing.aikars.flags=https://mcflags.emc.gs",
        "-Daikars.new.flags=true"
    ]

def get_instance_path(base_dir, profile_name):
    """Cria e retorna o caminho isolado para uma instância, garantindo estrutura completa."""
    # Sanitizar nome da pasta
    safe_name = "".join([c for c in profile_name if c.isalnum() or c in (' ', '_', '-')]).strip().replace(" ", "_")
    path = os.path.join(base_dir, "instances", safe_name)
    
    # Criar estrutura de pastas essencial para o Minecraft
    directories = [
        path,
        os.path.join(path, "mods"),
        os.path.join(path, "resourcepacks"),
        os.path.join(path, "shaderpacks"),
        os.path.join(path, "screenshots"),
        os.path.join(path, "saves"),
        os.path.join(path, "config")
    ]
    
    for d in directories:
        os.makedirs(d, exist_ok=True)
        
    return path

def get_minecraft_era(version_id):
    """Classifica a versão do Minecraft em 'eras' para aplicar configurações específicas."""
    try:
        parts = version_id.split('.')
        major = int(parts[0]) if len(parts) > 0 else 1
        minor = int(parts[1]) if len(parts) > 1 else 0
        
        if major > 1 or minor >= 21: return "v21"      # 1.21+ (Java 21)
        if minor >= 17: return "modern"                # 1.17 - 1.20 (Java 17)
        if minor >= 13: return "intermediate"          # 1.13 - 1.16 (Java 8/11/16)
        if minor >= 7: return "legacy"                 # 1.7 - 1.12 (Java 8)
        return "ancient"                               # < 1.7 (Java 8 + fixes)
    except:
        return "modern"

def get_java_recommendation(version_id):
    """Retorna o runtime Java oficial recomendado pela Mojang para cada era."""
    era = get_minecraft_era(version_id)
    runtimes = {
        "v21": "java-runtime-delta",    # Java 21
        "modern": "java-runtime-gamma",  # Java 17
        "intermediate": "java-runtime-alpha", # Java 16/8
        "legacy": "java-runtime-alpha", # Java 8
        "ancient": "java-runtime-alpha" # Java 8
    }
    return runtimes.get(era, "java-runtime-gamma")
