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

def get_themes():
    """Retorna os temas de cores disponíveis para o launcher."""
    return {
        "Aether (Padrão)": {"accent": "#00aaff", "bg": "#1a1a1a", "fg": "white"},
        "Dracula": {"accent": "#bd93f9", "bg": "#282a36", "fg": "#f8f8f2"},
        "Emerald": {"accent": "#50fa7b", "bg": "#1a1a1a", "fg": "white"},
        "Inferno": {"accent": "#ff5555", "bg": "#1a1a1a", "fg": "white"},
        "Cyberpunk": {"accent": "#f1fa8c", "bg": "#282a36", "fg": "#ff79c6"}
    }

def get_autotune_profiles():
    """Retorna os perfis de driver para o sistema de Auto-Tune."""
    return [
        {
            "id": 0,
            "name": "Nativo (Mesa Otimizado)",
            "env": {
                "vblank_mode": "0",
                "mesa_glthread": "true",
                "MESA_GL_VERSION_OVERRIDE": "4.6",
                "MESA_GLSL_VERSION_OVERRIDE": "460"
            }
        },
        {
            "id": 1,
            "name": "Zink (Vulkan Translation)",
            "env": {
                "MESA_LOADER_DRIVER_OVERRIDE": "zink",
                "GALLIUM_DRIVER": "zink",
                "vblank_mode": "0",
                "MESA_GL_VERSION_OVERRIDE": "4.6"
            }
        },
        {
            "id": 2,
            "name": "Compatibilidade Extrema (DRI2)",
            "env": {
                "LIBGL_DRI3_DISABLE": "1",
                "MESA_GL_VERSION_OVERRIDE": "4.3",
                "MESA_DEBUG": "silent",
                "vblank_mode": "0"
            }
        },
        {
            "id": 3,
            "name": "Software Rendering (CPU Boost)",
            "env": {
                "LIBGL_ALWAYS_SOFTWARE": "1",
                "GALLIUM_DRIVER": "llvmpipe",
                "vblank_mode": "0"
            }
        },
        {
            "id": 4,
            "name": "Aether Wine-Like (Intel HD 3000 Fix)",
            "env": {
                "LIBGL_DRI3_DISABLE": "1",
                "MESA_GL_VERSION_OVERRIDE": "4.4FC",
                "MESA_GLSL_VERSION_OVERRIDE": "440",
                "MESA_DEBUG": "silent",
                "vblank_mode": "0",
                "allow_glsl_extension_directive_midshader": "true",
                "allow_higher_compat_version": "true",
                "INTEL_DEBUG": "nocreatcontext,no_vbo",
                "MESA_LOADER_DRIVER_OVERRIDE": "i965",
                "MESA_EXTENSION_OVERRIDE": "GL_ARB_separate_shader_objects GL_ARB_explicit_attrib_location GL_ARB_shading_language_420pack"
            }
        }
    ]

def get_compatibility_env(is_recent=True, profile_index=None):
    """
    Configura o ambiente Linux para o conector do Minecraft.
    """
    env = os.environ.copy()
    
    # Se um perfil de Auto-Tune for especificado, usa ele
    if profile_index is not None:
        profiles = get_autotune_profiles()
        if 0 <= profile_index < len(profiles):
            env.update(profiles[profile_index]["env"])
    else:
        # Configuração padrão robusta
        env["vblank_mode"] = "0"
        env["mesa_glthread"] = "true"
        env["MESA_GL_VERSION_OVERRIDE"] = "4.6" if is_recent else "3.2"
        env["MESA_GLSL_VERSION_OVERRIDE"] = "460" if is_recent else "150"
    
    # Injeção Universal de Bibliotecas do Sistema (Ajustado para 1.21.11+)
    # Na 1.21.11+, a JNA 5.17.0 conflita se forçarmos o LD_LIBRARY_PATH do sistema antes das libs do jogo
    sys_paths = ["/usr/lib/x86_64-linux-gnu", "/usr/lib/x86_64-linux-gnu/dri", "/usr/lib64", "/usr/lib"]
    current_ld = env.get("LD_LIBRARY_PATH", "")
    
    # Se for uma versão muito recente (1.21.11+), colocamos as libs do sistema DEPOIS para não quebrar a JNA interna
    if is_recent:
        env["LD_LIBRARY_PATH"] = (current_ld + ":" if current_ld else "") + ":".join(sys_paths)
    else:
        env["LD_LIBRARY_PATH"] = ":".join(sys_paths) + (":" + current_ld if current_ld else "")
    
    # Fixes de Interface e Janela (X11)
    env["_JAVA_AWT_WM_NONREPARENTING"] = "1"
    env["QT_QPA_PLATFORM"] = "xcb"
    env["GDK_BACKEND"] = "x11"
    
    # Cache de Shaders
    shader_cache_dir = os.path.expanduser("~/.cache/aetherlauncher/shaders")
    os.makedirs(shader_cache_dir, exist_ok=True)
    env["MESA_SHADER_CACHE_DIR"] = shader_cache_dir
    env["MESA_SHADER_CACHE_MAX_SIZE"] = "1G"
    
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
    safe_name = "".join([c for c in profile_name if c.isalnum() or c in (' ', '_', '-')]).strip().replace(" ", "_")
    path = os.path.join(base_dir, "instances", safe_name)
    
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
        # Tentar extrair a versão base se for um ID complexo (ex: forge-1.21.1-...)
        import re
        version_match = re.search(r'(\d+\.\d+(\.\d+)?)', version_id)
        if version_match:
            base_version = version_match.group(1)
            parts = base_version.split('.')
            major = int(parts[0])
            minor = int(parts[1])
            
            if major > 1 or (major == 1 and minor >= 21): return "v21"      # 1.21+ (Java 21)
            if minor >= 17: return "modern"                # 1.17 - 1.20 (Java 17)
            if minor >= 13: return "intermediate"          # 1.13 - 1.16 (Java 8/11/16)
            if minor >= 7: return "legacy"                 # 1.7 - 1.12 (Java 8)
            return "ancient"                               # < 1.7 (Java 8 + fixes)
        
        # Fallback para IDs que não seguem o padrão
        if "1.21" in version_id: return "v21"
        return "modern"
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
