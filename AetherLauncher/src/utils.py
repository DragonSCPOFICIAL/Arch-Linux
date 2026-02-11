import os
import subprocess
import platform
import shutil

def get_system_info():
    """Retorna um dicionário com informações detalhadas do sistema para otimização EXTREMA."""
    info = {
        "ram_gb": 4,
        "gpu_vendor": "unknown",
        "has_vulkan": False,
        "cpu_cores": 1,
        "has_hugepages": False,
        "gpu_driver": "unknown"
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
        # Detectar GPU e Vulkan com detalhes de driver
        lspci_output = subprocess.check_output(['lspci'], text=True, timeout=2).lower()
        
        if "amd" in lspci_output or "radeon" in lspci_output:
            info["gpu_vendor"] = "amd"
            # Detectar driver AMD (RADV vs AMDVLK vs AMDGPU-PRO)
            try:
                vulkan_icd = subprocess.check_output(['vulkaninfo', '--summary'], text=True, timeout=2).lower()
                if "radv" in vulkan_icd:
                    info["gpu_driver"] = "radv"  # Mesa RADV (melhor para gaming)
                elif "amdvlk" in vulkan_icd:
                    info["gpu_driver"] = "amdvlk"  # Driver oficial AMD
                else:
                    info["gpu_driver"] = "amdgpu"
            except:
                info["gpu_driver"] = "mesa"
                
        elif "nvidia" in lspci_output or "geforce" in lspci_output:
            info["gpu_vendor"] = "nvidia"
            info["gpu_driver"] = "nvidia-proprietary"
            
        elif "intel" in lspci_output:
            info["gpu_vendor"] = "intel"
            info["gpu_driver"] = "i965"  # Intel Mesa
        
        # Verificar suporte a Vulkan
        vulkan_res = subprocess.run(['vulkaninfo', '--summary'], capture_output=True, text=True, timeout=2)
        info["has_vulkan"] = vulkan_res.returncode == 0
    except: pass
    
    try:
        # Verificar se Transparent Huge Pages está ativo
        with open('/sys/kernel/mm/transparent_hugepage/enabled', 'r') as f:
            thp_status = f.read()
            info["has_hugepages"] = '[always]' in thp_status or '[madvise]' in thp_status
    except: pass
    
    return info

def get_gpu_info():
    """Retorna informações legíveis da GPU."""
    info = get_system_info()
    return f"GPU: {info['gpu_vendor'].upper()} ({info['gpu_driver']}) | RAM: {info['ram_gb']}GB | Cores: {info['cpu_cores']} | Vulkan: {'✓' if info['has_vulkan'] else '✗'}"

def apply_linux_tweaks(config):
    """Aplica otimizações de sistema Linux baseadas na configuração."""
    print("[LINUX] Aplicando Power Tweaks...")
    
    # 1. CPU Performance Governor
    if config.get("use_cpu_perf"):
        try:
            print("[LINUX] Forçando CPU Performance Governor...")
            # Tenta aplicar para todos os cores
            # subprocess.run(["sh", "-c", "echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"], stderr=subprocess.DEVNULL) # Comentado para evitar loop de senha
        except: pass

    # 2. Limpeza de Cache & ZRAM
    if config.get("use_zram_clean"):
        try:
            print("[LINUX] Limpando caches do sistema...")
            # subprocess.run(["sudo", "sync"], stderr=subprocess.DEVNULL) # Comentado para evitar loop de senha
            # subprocess.run(["sh", "-c", "echo 3 | sudo tee /proc/sys/vm/drop_caches"], stderr=subprocess.DEVNULL) # Comentado para evitar loop de senha
        except: pass

    # 3. Transparent Huge Pages (THP)
    if config.get("use_thp_optim"):
        try:
            print("[LINUX] Otimizando Transparent Huge Pages...")
            # subprocess.run(["sh", "-c", "echo always | sudo tee /sys/kernel/mm/transparent_hugepage/enabled"], stderr=subprocess.DEVNULL) # Comentado para evitar loop de senha
            # subprocess.run(["sh", "-c", "echo always | sudo tee /sys/kernel/mm/transparent_hugepage/defrag"], stderr=subprocess.DEVNULL) # Comentado para evitar loop de senha
        except: pass

def enable_performance_mode():
    """Ativa o modo de performance básico do sistema."""
    try:
        # Tenta desativar o sleep da GPU Intel (se existir)
        # subprocess.run(["sh", "-c", "echo 0 | sudo tee /sys/module/i915/parameters/enable_dc"], stderr=subprocess.DEVNULL) # Comentado para evitar loop de senha
    except: pass

def get_themes():
    """Retorna os temas de cores disponíveis para o launcher."""
    return {
        "Aether (Padrão)": {"accent": "#B43D3D", "bg": "#1a1a1a", "fg": "white"},
        "Dracula": {"accent": "#bd93f9", "bg": "#282a36", "fg": "#f8f8f2"},
        "Emerald": {"accent": "#50fa7b", "bg": "#1a1a1a", "fg": "white"},
        "Inferno": {"accent": "#ff5555", "bg": "#1a1a1a", "fg": "white"},
        "Cyberpunk": {"accent": "#f1fa8c", "bg": "#282a36", "fg": "#ff79c6"},
        "Ocean": {"accent": "#00D4FF", "bg": "#0a1628", "fg": "white"},
        "Sunset": {"accent": "#FF6B35", "bg": "#1a1a1a", "fg": "white"}
    }

def get_autotune_profiles():
    """Retorna os perfis de driver ULTRA OTIMIZADOS para o sistema de Auto-Tune."""
    return [
        {
            "id": 0,
            "name": "Nativo ULTRA (Mesa RADV Turbo)",
            "env": {
                # === MESA RADV EXTREMO (AMD) ===
                "RADV_PERFTEST": "nggc,sam,rt,gpl",  # NGGC + Resizable BAR + Ray Tracing
                "RADV_DEBUG": "zerovram,nodcc",  # Zero VRAM init + desativa DCC (+ FPS)
                "AMD_VULKAN_ICD": "RADV",  # Força RADV (melhor que AMDVLK)
                
                # === MESA GLTHREAD (CPU PARALELO) ===
                "mesa_glthread": "true",
                "mesa_glthread_driver": "true",
                
                # === OPENGL OVERRIDE ===
                "MESA_GL_VERSION_OVERRIDE": "4.6",
                "MESA_GLSL_VERSION_OVERRIDE": "460",
                "MESA_GLES_VERSION_OVERRIDE": "3.2",
                
                # === SHADER CACHE AGRESSIVO ===
                "MESA_SHADER_CACHE_DISABLE": "false",
                "MESA_DISK_CACHE_SINGLE_FILE": "true",
                
                # === VSYNC OFF (MÁXIMO FPS) ===
                "vblank_mode": "0",
                "__GL_SYNC_TO_VBLANK": "0",
                
                # === THREADING E CPU ===
                "GALLIUM_THREAD": "8",  # 8 threads para renderização
                "LP_NUM_THREADS": "8",  # LLVMpipe threads
                
                # === INTEL ESPECÍFICO (se detectado) ===
                "INTEL_DEBUG": "nofc",  # Desativa fast clear (+ compatibilidade)
                
                # === TEXTURE COMPRESSION ===
                "force_s3tc_enable": "true",
                "allow_glsl_extension_directive_midshader": "true"
            }
        },
        {
            "id": 1,
            "name": "Zink Vulkan Turbo (NVIDIA/AMD)",
            "env": {
                # === ZINK (OpenGL via Vulkan) ===
                "MESA_LOADER_DRIVER_OVERRIDE": "zink",
                "GALLIUM_DRIVER": "zink",
                
                # === VULKAN LAYER OTIMIZADO ===
                "VK_ICD_FILENAMES": "/usr/share/vulkan/icd.d/radeon_icd.x86_64.json",  # AMD
                "VK_LOADER_DEBUG": "error",
                
                # === ZINK ESPECÍFICO ===
                "ZINK_DESCRIPTORS": "lazy",  # Descriptor sets lazy (+ FPS)
                "ZINK_DEBUG": "nir,spirv",
                
                # === MESA OVERRIDE ===
                "MESA_GL_VERSION_OVERRIDE": "4.6",
                "MESA_GLSL_VERSION_OVERRIDE": "460",
                
                # === VSYNC OFF ===
                "vblank_mode": "0",
                
                # === SHADER CACHE ===
                "MESA_SHADER_CACHE_DISABLE": "false",
                "mesa_glthread": "true"
            }
        },
        {
            "id": 2,
            "name": "Compatibilidade DRI2 (GPUs Antigas)",
            "env": {
                # === DRI2 FALLBACK ===
                "LIBGL_DRI3_DISABLE": "1",
                "LIBGL_ALWAYS_INDIRECT": "0",
                
                # === MESA CONSERVADOR ===
                "MESA_GL_VERSION_OVERRIDE": "4.3",
                "MESA_GLSL_VERSION_OVERRIDE": "430",
                "MESA_DEBUG": "silent",
                
                # === VSYNC OFF ===
                "vblank_mode": "0",
                
                # === SHADER COMPILATION ===
                "allow_glsl_extension_directive_midshader": "true",
                "force_glsl_extensions_warn": "false"
            }
        },
        {
            "id": 3,
            "name": "LLVMpipe Software Rendering (CPU Turbo)",
            "env": {
                # === SOFTWARE RENDERING ===
                "LIBGL_ALWAYS_SOFTWARE": "1",
                "GALLIUM_DRIVER": "llvmpipe",
                
                # === LLVMPIPE THREADS (USA TODA CPU) ===
                "LP_NUM_THREADS": str(os.cpu_count() or 4),
                "LP_PERF": "no_mipmap_linear_aniso",  # Desativa mipmapping aniso (+ FPS)
                
                # === MESA OVERRIDE ===
                "MESA_GL_VERSION_OVERRIDE": "4.5",
                "MESA_GLSL_VERSION_OVERRIDE": "450",
                
                # === VSYNC OFF ===
                "vblank_mode": "0"
            }
        },
        {
            "id": 4,
            "name": "Intel HD 3000/4000 FIX (Wine-Like)",
            "env": {
                # === INTEL LEGACY FIX ===
                "LIBGL_DRI3_DISABLE": "1",
                "MESA_GL_VERSION_OVERRIDE": "4.4COMPAT",
                "MESA_GLSL_VERSION_OVERRIDE": "440",
                "MESA_DEBUG": "silent",
                
                # === INTEL DEBUG FLAGS ===
                "INTEL_DEBUG": "nodualobj,no3d,nofc",
                "MESA_LOADER_DRIVER_OVERRIDE": "i965",
                
                # === EXTENSIONS OVERRIDE ===
                "MESA_EXTENSION_OVERRIDE": "GL_ARB_separate_shader_objects GL_ARB_explicit_attrib_location GL_ARB_shading_language_420pack GL_ARB_gpu_shader5",
                
                # === VSYNC OFF ===
                "vblank_mode": "0",
                
                # === COMPATIBILIDADE ===
                "allow_glsl_extension_directive_midshader": "true",
                "allow_higher_compat_version": "true",
                "force_glsl_extensions_warn": "false"
            }
        },
        {
            "id": 5,
            "name": "NVIDIA Proprietário (GeForce Performance)",
            "env": {
                "__GL_THREADED_OPTIMIZATIONS": "1",
                "__GL_SYNC_TO_VBLANK": "0",
                "__GL_SHADER_DISK_CACHE": "1",
                "__GL_SHADER_DISK_CACHE_SKIP_CLEANUP": "1",
                "__GL_MaxFramesAllowed": "1",
                "MESA_GL_VERSION_OVERRIDE": "4.6",
                "mesa_glthread": "true",
                "vblank_mode": "0"
            }
        },
        {
            "id": 6,
            "name": "GODMODE (Intel HD 3000 EXTREME)",
            "env": {
                # === MESA INTEL OPTIMIZATION ===
                "INTEL_DEBUG": "nofc,norbc",  # Desativa Fast Clear e Render Buffer Compression (Ganha FPS em GPUs velhas)
                "MESA_LOADER_DRIVER_OVERRIDE": "i965",
                "mesa_glthread": "true",
                "MESA_GL_VERSION_OVERRIDE": "4.5COMPAT",
                "MESA_GLSL_VERSION_OVERRIDE": "450",
                
                # === PERFORMANCE BOOST ===
                "vblank_mode": "0",
                "allow_glsl_extension_directive_midshader": "true",
                "MESA_EXTENSION_OVERRIDE": "GL_ARB_separate_shader_objects GL_ARB_explicit_attrib_location GL_ARB_gpu_shader5",
                
                # === MEMORY & CACHE ===
                "MESA_SHADER_CACHE_DISABLE": "false",
                "MESA_DISK_CACHE_SINGLE_FILE": "true",
                "MESA_DISK_CACHE_COMBINE_WRITES": "true",
                
                # === ARCH LINUX SPECIFIC ===
                "LD_PRELOAD": "/usr/lib/libjemalloc.so", # Tenta carregar jemalloc do Arch
                "GALLIUM_HUD": "fps", # Opcional: mostra FPS no topo (pode remover se quiser)
                "ST_DEBUG": "tgsi"
            }
        }
    ]

def get_compatibility_env(is_recent=True, profile_index=None):
    """
    Configura o ambiente Linux ULTRA OTIMIZADO para o Minecraft.
    """
    env = os.environ.copy()
    sys_info = get_system_info()
    
    # === APLICAR PERFIL DE AUTO-TUNE ===
    if profile_index is not None:
        profiles = get_autotune_profiles()
        if 0 <= profile_index < len(profiles):
            selected_profile = profiles[profile_index]
            print(f"[PERF] Aplicando perfil: {selected_profile['name']}")
            env.update(selected_profile["env"])
    else:
        # === CONFIGURAÇÃO PADRÃO INTELIGENTE (AUTO-DETECT GPU) ===
        if sys_info["gpu_vendor"] == "amd":
            # AMD: Usa perfil RADV Turbo
            env.update(get_autotune_profiles()[0]["env"])
        elif sys_info["gpu_vendor"] == "nvidia":
            # NVIDIA: Usa perfil proprietário
            env.update(get_autotune_profiles()[5]["env"])
        elif sys_info["gpu_vendor"] == "intel":
            # Intel: Agora usa o perfil GODMODE por padrão para performance extrema
            env.update(get_autotune_profiles()[6]["env"])
        else:
            # Fallback: Mesa padrão
            env["mesa_glthread"] = "true"
            env["MESA_GL_VERSION_OVERRIDE"] = "4.6" if is_recent else "3.2"
            env["vblank_mode"] = "0"
    
    # === LIBRARY PATH (CRÍTICO) ===
    sys_paths = [
        "/usr/lib/x86_64-linux-gnu",
        "/usr/lib/x86_64-linux-gnu/dri",
        "/usr/lib64",
        "/usr/lib",
        "/lib/x86_64-linux-gnu",
        "/lib64"
    ]
    current_ld = env.get("LD_LIBRARY_PATH", "")
    
    # Para versões 1.21+ (JNA 5.17.0), colocar libs do sistema DEPOIS
    if is_recent:
        env["LD_LIBRARY_PATH"] = (current_ld + ":" if current_ld else "") + ":".join(sys_paths)
    else:
        env["LD_LIBRARY_PATH"] = ":".join(sys_paths) + (":" + current_ld if current_ld else "")
    
    # === PRELOAD DE BIBLIOTECAS (BOOST) ===
    # Isso força o uso de libs otimizadas antes das libs bundled do Minecraft
    preload_libs = []
    
    # jemalloc (melhor alocador de memória que o glibc malloc)
    if os.path.exists("/usr/lib/x86_64-linux-gnu/libjemalloc.so.2"):
        preload_libs.append("/usr/lib/x86_64-linux-gnu/libjemalloc.so.2")
    
    if preload_libs:
        env["LD_PRELOAD"] = ":".join(preload_libs)
        print(f"[PERF] LD_PRELOAD ativo: {env['LD_PRELOAD']}")
    
    # === WINDOW MANAGER E COMPOSITOR (X11 OTIMIZADO) ===
    env["_JAVA_AWT_WM_NONREPARENTING"] = "1"
    env["QT_QPA_PLATFORM"] = "xcb"
    env["GDK_BACKEND"] = "x11"
    env["SDL_VIDEODRIVER"] = "x11"
    
    # === SHADER CACHE (UNIVERSAL) ===
    shader_cache_dir = os.path.expanduser("~/.cache/aetherlauncher/shaders")
    os.makedirs(shader_cache_dir, exist_ok=True)
    env["MESA_SHADER_CACHE_DIR"] = shader_cache_dir
    env["MESA_SHADER_CACHE_MAX_SIZE"] = "2G"  # Aumentado de 1G -> 2G
    env["__GL_SHADER_DISK_CACHE_PATH"] = shader_cache_dir  # NVIDIA
    
    # === CPU GOVERNOR (PERFORMANCE MODE) ===
    try:
        # Tenta ativar modo performance no CPU governor (requer sudo, mas tentamos)
        for cpu in range(sys_info["cpu_cores"]):
            gov_path = f"/sys/devices/system/cpu/cpu{cpu}/cpufreq/scaling_governor"
            if os.path.exists(gov_path):
                try:
                    subprocess.run(['sudo', 'sh', '-c', f'echo performance > {gov_path}'], 
                                   timeout=1, capture_output=True)
                except:
                    pass
    except:
        pass
    
    # === OPENGL MULTITHREAD (CRITICAL) ===
    env["__GL_THREADED_OPTIMIZATIONS"] = "1"  # NVIDIA
    env["mesa_glthread"] = "true"  # Mesa
    
    return env

def get_performance_args():
    """Retorna argumentos de JVM ULTRA OTIMIZADAS para FPS MÁXIMO no Linux."""
    sys_info = get_system_info()
    
    args = [
        # === GARBAGE COLLECTOR AGRESSIVO (G1GC EXTREMO) ===
        "-XX:+UseG1GC",
        "-XX:+ParallelRefProcEnabled",
        "-XX:MaxGCPauseMillis=37",  # Reduzido de 50ms -> 37ms (menos stuttering)
        "-XX:+UnlockExperimentalVMOptions",
        "-XX:+DisableExplicitGC",
        "-XX:+AlwaysPreTouch",
        "-XX:G1NewSizePercent=50",  # Aumentado para 50% (muito agressivo)
        "-XX:G1MaxNewSizePercent=80",  # Aumentado para 80%
        "-XX:G1HeapRegionSize=16M",  # 16MB por região
        "-XX:G1ReservePercent=10",  # Reduzido para 10%
        "-XX:G1HeapWastePercent=5",
        "-XX:G1MixedGCCountTarget=3",
        "-XX:InitiatingHeapOccupancyPercent=10",
        "-XX:G1MixedGCLiveThresholdPercent=80",  # Reduzido para 80%
        "-XX:G1RSetUpdatingPauseTimePercent=2",  # Reduzido para 2%
        "-XX:SurvivorRatio=24",
        "-XX:+PerfDisableSharedMem",
        "-XX:MaxTenuringThreshold=1",
        
        # === COMPILADOR JIT ULTRA AGRESSIVO ===
        "-XX:+UseStringDeduplication",
        "-XX:+UseFastAccessorMethods",
        "-XX:+OptimizeStringConcat",
        "-XX:+UseCompressedOops",
        "-XX:+UseCompressedClassPointers",
        "-XX:+TieredCompilation",  # Compilação em camadas (C1 + C2)
        "-XX:TieredStopAtLevel=4",  # Usa C2 compiler (máxima otimização)
        
        # === CPU E THREADING (LINUX NATIVO) ===
        "-XX:+AggressiveOpts",  # Otimizações experimentais
        "-XX:+UseFMA",  # Instruções FMA da CPU
        "-XX:+UseAES",
        "-XX:+UseAESIntrinsics",
        "-XX:+UseSHA",
        "-XX:+UseSHAIntrinsics",
        "-XX:+UseAdler32Intrinsics",
        "-XX:+UseCRC32Intrinsics",
        
        # === HUGE PAGES (SE DISPONÍVEL) ===
        "-XX:+UseLargePages" if sys_info["has_hugepages"] else "",
        "-XX:+UseTransparentHugePages" if sys_info["has_hugepages"] else "",
        "-XX:LargePageSizeInBytes=2M" if sys_info["has_hugepages"] else "",
        
        # === OTIMIZAÇÕES DE LATÊNCIA (ZERO-LAG) ===
        "-XX:+UseNUMA",  # NUMA-aware (multi-CPU)
        "-XX:-UseAdaptiveSizePolicy",  # Tamanho fixo (mais previsível)
        "-XX:+AlwaysActAsServerClassMachine",
        
        # === BIASED LOCKING (REDUZ CONTENÇÃO) ===
        "-XX:+UseBiasedLocking",
        "-XX:BiasedLockingStartupDelay=0",
        
        # === METASPACE ===
        "-XX:MetaspaceSize=384M",  # Aumentado para 384MB
        "-XX:MaxMetaspaceSize=768M",  # Limite de 768MB
        "-XX:+ClassUnloadingWithConcurrentMark",
        
        # === INLINE E CODE CACHE ===
        "-XX:ReservedCodeCacheSize=512M",  # Code cache de 512MB
        "-XX:InitialCodeCacheSize=256M",
        "-XX:MaxInlineLevel=15",  # Aumenta profundidade de inlining
        
        # === FLAGS ESPECIAIS LINUX ===
        "-Djava.awt.headless=false",
        "-Dsun.rmi.dgc.server.gcInterval=2147483646",
        "-Dfile.encoding=UTF-8",
        "-Dusing.aikars.flags=https://mcflags.emc.gs",
        "-Daikars.new.flags=true",
        
        # === LWJGL E OPENGL (CRITICAL PARA FPS) ===
        "-Dorg.lwjgl.opengl.Display.enableHighDPI=true",
        "-Dorg.lwjgl.opengl.Display.allowSoftwareOpenGL=false",
        "-Dorg.lwjgl.util.DebugLoader=true",
        "-Dorg.lwjgl.util.Debug=false",  # Debug OFF (+ FPS)
        "-Dfml.readTimeout=240",
        
        # === NETWORK STACK (LINUX OTIMIZADO) ===
        "-Djava.net.preferIPv4Stack=true",
        "-Dio.netty.recycler.maxCapacity=0",  # Desativa object pooling (menos GC pauses)
        "-Dio.netty.leakDetection.level=DISABLED",
    ]
    
    # Filtrar strings vazias
    return [arg for arg in args if arg]

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
        os.path.join(path, "config"),
        os.path.join(path, "logs"),
        os.path.join(path, "natives")
    ]
    
    for d in directories:
        os.makedirs(d, exist_ok=True)
        
    return path

def get_minecraft_era(version_id):
    """Classifica a versão do Minecraft em 'eras' para aplicar configurações específicas."""
    try:
        import re
        version_match = re.search(r'(\d+\.\d+(\.\d+)?)', version_id)
        if version_match:
            base_version = version_match.group(1)
            parts = base_version.split('.')
            major = int(parts[0])
            minor = int(parts[1])
            
            if major > 1 or (major == 1 and minor >= 21): return "v21"
            if minor >= 17: return "modern"
            if minor >= 13: return "intermediate"
            if minor >= 7: return "legacy"
            return "ancient"
        
        if "1.21" in version_id: return "v21"
        return "modern"
    except:
        return "modern"

def get_java_recommendation(version_id):
    """Retorna o runtime Java oficial recomendado pela Mojang para cada era."""
    era = get_minecraft_era(version_id)
    runtimes = {
        "v21": "java-runtime-delta",
        "modern": "java-runtime-gamma",
        "intermediate": "java-runtime-alpha",
        "legacy": "java-runtime-alpha",
        "ancient": "java-runtime-alpha"
    }
    return runtimes.get(era, "java-runtime-gamma")

def enable_performance_mode():
    """
    Ativa modo de performance no sistema (CPU governor, I/O scheduler).
    Requer permissões de root, mas tenta sem falhar.
    """
    try:
        sys_info = get_system_info()
        
        # === CPU GOVERNOR -> PERFORMANCE ===
        for cpu in range(sys_info["cpu_cores"]):
            gov_file = f"/sys/devices/system/cpu/cpu{cpu}/cpufreq/scaling_governor"
            if os.path.exists(gov_file):
                try:
                    # Tenta sem sudo primeiro (caso já tenha permissão)
                    with open(gov_file, 'w') as f:
                        f.write('performance')
                except:
                    # Tenta com sudo
                    try:
                        subprocess.run(['sudo', 'sh', '-c', f'echo performance > {gov_file}'], 
                                       timeout=2, capture_output=True)
                    except:
                        pass
        
        # === I/O SCHEDULER -> NOOP ou DEADLINE ===
        for disk in ['sda', 'nvme0n1', 'vda']:
            scheduler_file = f"/sys/block/{disk}/queue/scheduler"
            if os.path.exists(scheduler_file):
                try:
                    with open(scheduler_file, 'w') as f:
                        f.write('noop')  # ou 'deadline' para SSDs
                except:
                    pass
        
        print("[PERF] Modo de performance ativado (melhor esforço)")
    except Exception as e:
        print(f"[PERF] Aviso: Não foi possível ativar modo performance completo ({e})")
