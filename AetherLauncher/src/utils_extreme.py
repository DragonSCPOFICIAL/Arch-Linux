import os
import subprocess
import platform
import shutil
import json

def get_system_info():
    """Retorna um dicionário com informações EXTREMAMENTE detalhadas do sistema para otimização ABSURDA."""
    info = {
        "ram_gb": 4,
        "gpu_vendor": "unknown",
        "has_vulkan": False,
        "cpu_cores": 1,
        "has_hugepages": False,
        "gpu_driver": "unknown",
        "cpu_model": "unknown",
        "cpu_freq_ghz": 0.0,
        "kernel_version": "unknown",
        "mesa_version": "unknown",
        "vulkan_version": "unknown",
        "has_numa": False,
        "has_avx2": False,
        "has_fma": False,
        "has_aes": False,
        "io_scheduler": "unknown",
        "swap_available": 0,
        "cache_l3_mb": 0,
        "is_legacy_intel": False
    }
    
    try:
        # Detectar RAM total
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('MemTotal'):
                    info["ram_gb"] = int(line.split()[1]) // 1024 // 1024
                elif line.startswith('SwapTotal'):
                    info["swap_available"] = int(line.split()[1]) // 1024 // 1024
    except: pass

    try:
        # Detectar CPU cores e modelo
        info["cpu_cores"] = os.cpu_count() or 1
        with open('/proc/cpuinfo', 'r') as f:
            content = f.read()
            # Extrair modelo
            for line in content.split(                if line.startswith(\'model name\'):
                    info["cpu_model"] = line.split(\':\', 1)[1].strip()
                    # Detectar arquitetura da CPU
                    if "sandy bridge" in info["cpu_model"].lower():
                        info["is_legacy_intel"] = True
                    break
            # Detectar flags de CPU
            if \'avx2\' in content:
                info["has_avx2"] = True
            if \'fma\' in content:
                info["has_fma"] = True
            if \'aes\' in content:
                info["has_aes"] = True  except: pass

    try:
        # Detectar versão do kernel
        with open('/proc/version', 'r') as f:
            version_line = f.read()
            parts = version_line.split()
            if len(parts) > 2:
                info["kernel_version"] = parts[2]
    except: pass

    try:
        # Detectar GPU e Vulkan com detalhes de driver
        lspci_output = subprocess.check_output(['lspci'], text=True, timeout=2).lower()
        
        if "amd" in lspci_output or "radeon" in lspci_output:
            info["gpu_vendor"] = "amd"
            try:
                vulkan_icd = subprocess.check_output(['vulkaninfo', '--summary'], text=True, timeout=2).lower()
                if "radv" in vulkan_icd:
                    info["gpu_driver"] = "radv"
                elif "amdvlk" in vulkan_icd:
                    info["gpu_driver"] = "amdvlk"
                else:
                    info["gpu_driver"] = "amdgpu"
            except:
                info["gpu_driver"] = "mesa"
                
        elif "nvidia" in lspci_output or "geforce" in lspci_output:
            info["gpu_vendor"] = "nvidia"
            info["gpu_driver"] = "nvidia-proprietary"
            
        elif "intel" in lspci_output:
            info["gpu_vendor"] = "intel"
            # Detectar geração da GPU Intel para escolher driver
            if "sandybridge" in lspci_output or "ivybridge" in lspci_output:
                info["gpu_driver"] = "crocus" # Gen6/7
                info["is_legacy_intel"] = True
            elif "haswell" in lspci_output or "broadwell" in lspci_output:
                info["gpu_driver"] = "iris" # Gen7.5/8
            else:
                info["gpu_driver"] = "i965" # Fallback ou Gen9+
        
        # Verificar suporte a Vulkan e versão
        try:
            vulkan_res = subprocess.run([\'vulkaninfo\', \'--summary\'], capture_output=True, text=True, timeout=2)
            info["has_vulkan"] = vulkan_res.returncode == 0
            if info["has_vulkan"] and "Vulkan" in vulkan_res.stdout:
                for line in vulkan_res.stdout.split(\'\\n\'):
                    if \'Vulkan\' in line and \'Version\' in line:
                        info["vulkan_version"] = line.split(\'Version\')[1].strip()[:10]
        except: pass
        
        # Detectar versão do Mesa
        try:
            glxinfo = subprocess.check_output([\'glxinfo\'], capture_output=True, text=True, timeout=2)
            for line in glxinfo.split(\'\\n\'):
                if \'OpenGL version\' in line or \'Mesa\' in line:
                    info["mesa_version"] = line.strip()[:50]
        except: pass
    except: pass
    
    try:
        # Verificar se Transparent Huge Pages está ativo
        with open('/sys/kernel/mm/transparent_hugepage/enabled', 'r') as f:
            thp_status = f.read()
            info["has_hugepages"] = '[always]' in thp_status or '[madvise]' in thp_status
    except: pass
    
    try:
        # Detectar suporte a NUMA
        numa_nodes = subprocess.check_output(['numactl', '--hardware'], text=True, timeout=2)
        info["has_numa"] = 'available' in numa_nodes.lower()
    except: pass
    
    try:
        # Detectar I/O scheduler
        for disk in ['sda', 'nvme0n1', 'vda']:
            scheduler_file = f"/sys/block/{disk}/queue/scheduler"
            if os.path.exists(scheduler_file):
                with open(scheduler_file, 'r') as f:
                    schedulers = f.read().strip()
                    active = [s.strip('[]') for s in schedulers.split() if '[' in s]
                    if active:
                        info["io_scheduler"] = active[0]
                        break
    except: pass
    
    try:
        # Detectar cache L3
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'cache size' in line:
                    size_str = line.split(':', 1)[1].strip()
                    if 'KB' in size_str:
                        info["cache_l3_mb"] = int(size_str.split()[0]) // 1024
                    break
    except: pass
    
    return info

def get_gpu_info():
    """Retorna informações legíveis e detalhadas da GPU."""
    info = get_system_info()
    return f"GPU: {info['gpu_vendor'].upper()} ({info['gpu_driver']}) | RAM: {info['ram_gb']}GB | Cores: {info['cpu_cores']} | Vulkan: {'✓' if info['has_vulkan'] else '✗'} | Kernel: {info['kernel_version']}"

def apply_linux_tweaks(config):
    """Aplica otimizações EXTREMAS de sistema Linux baseadas na configuração."""
    print("[LINUX] Aplicando EXTREME Power Tweaks...")
    
    sys_info = get_system_info()
    
    # 1. CPU Performance Governor
    if config.get("use_cpu_perf"):
        try:
            print("[LINUX] Forçando CPU Performance Governor...")
            subprocess.run(["sh", "-c", "echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"], stderr=subprocess.DEVNULL)
        except: pass

    # 2. Limpeza de Cache & ZRAM
    if config.get("use_zram_clean"):
        try:
            print("[LINUX] Limpando caches do sistema...")
            subprocess.run(["sudo", "sync"], stderr=subprocess.DEVNULL)
            subprocess.run(["sh", "-c", "echo 3 | sudo tee /proc/sys/vm/drop_caches"], stderr=subprocess.DEVNULL)
        except: pass

    # 3. Transparent Huge Pages (THP)
    if config.get("use_thp_optim"):
        try:
            print("[LINUX] Otimizando Transparent Huge Pages...")
            subprocess.run(["sh", "-c", "echo always | sudo tee /sys/kernel/mm/transparent_hugepage/enabled"], stderr=subprocess.DEVNULL)
            subprocess.run(["sh", "-c", "echo always | sudo tee /sys/kernel/mm/transparent_hugepage/defrag"], stderr=subprocess.DEVNULL)
        except: pass
    
    # 4. I/O Scheduler Otimizado (para NVMe)
    if config.get("use_io_scheduler"):
        try:
            print("[LINUX] Otimizando I/O Scheduler...")
            for disk in ['nvme0n1', 'sda', 'vda']:
                scheduler_file = f"/sys/block/{disk}/queue/scheduler"
                if os.path.exists(scheduler_file):
                    try:
                        subprocess.run(["sh", "-c", f"echo mq-deadline | sudo tee {scheduler_file}"], stderr=subprocess.DEVNULL)
                    except: pass
        except: pass
    
    # 5. Sysctl Otimizações (Rede + VM)
    if config.get("use_sysctl_tweaks"):
        try:
            print("[LINUX] Aplicando otimizações de sysctl...")
            sysctl_tweaks = {
                "net.core.rmem_max": "16777216",
                "net.core.wmem_max": "16777216",
                "net.ipv4.tcp_rmem": "4096 87380 16777216",
                "net.ipv4.tcp_wmem": "4096 65536 16777216",
                "net.ipv4.tcp_fastopen": "3",
                "vm.swappiness": "10",
                "kernel.sched_latency_ns": "1000000",
                "kernel.sched_min_granularity_ns": "1000000"
            }
            for key, value in sysctl_tweaks.items():
                try:
                    subprocess.run(["sh", "-c", f"echo {key}={value} | sudo tee -a /etc/sysctl.d/99-minecraft-gaming.conf"], stderr=subprocess.DEVNULL)
                except: pass
        except: pass

def enable_performance_mode():
    """Ativa o modo de performance EXTREMO do sistema."""
    try:
        subprocess.run(["sh", "-c", "echo 0 | sudo tee /sys/module/i915/parameters/enable_dc"], stderr=subprocess.DEVNULL)
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
    """Retorna os perfis de driver ULTRA OTIMIZADOS para o sistema de Auto-Tune (versão EXTREMA)."""
    return [
        {
            "id": 0,
            "name": "Nativo ULTRA (Mesa RADV Turbo 26.0+)",
            "env": {
                # === MESA RADV EXTREMO (AMD) - Mesa 26.0+ ===
                "RADV_PERFTEST": "aco,ngg,nosam,no_vrs,no_dcc,no_hiz",
                "RADV_DEBUG": "invariant_geom,zerovram,nodcc",
                "RADV_TEX_ANISO": "16",
                "RADV_FORCE_VRS_TIER": "0",
                "RADV_QUEUE_PRIORITY": "high",
                "AMD_VULKAN_ICD": "RADV",
                
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
                "GALLIUM_THREAD": str(os.cpu_count() or 8),
                "LP_NUM_THREADS": str(os.cpu_count() or 8),
                
                # === TEXTURE COMPRESSION ===
                "force_s3tc_enable": "true",
                "allow_glsl_extension_directive_midshader": "true",
                
                # === VULKAN PRESENTATION ===
                "MESA_VK_WSI_PRESENT_MODE": "IMMEDIATE"
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
                "VK_ICD_FILENAMES": "/usr/share/vulkan/icd.d/radeon_icd.x86_64.json",
                "VK_LOADER_DEBUG": "error",
                
                # === ZINK ESPECÍFICO ===
                "ZINK_DESCRIPTORS": "lazy",
                "ZINK_DEBUG": "nir,spirv",
                
                # === MESA OVERRIDE ===
                "MESA_GL_VERSION_OVERRIDE": "4.6",
                "MESA_GLSL_VERSION_OVERRIDE": "460",
                
                # === VSYNC OFF ===
                "vblank_mode": "0",
                
                # === SHADER CACHE ===
                "MESA_SHADER_CACHE_DISABLE": "false",
                "mesa_glthread": "true",
                
                # === VULKAN PRESENTATION ===
                "MESA_VK_WSI_PRESENT_MODE": "IMMEDIATE"
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
                "LP_PERF": "no_mipmap_linear_aniso",
                
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
            "name": "NVIDIA Proprietário 2026+ (GeForce EXTREME)",
            "env": {
                "__GL_THREADED_OPTIMIZATIONS": "1",
                "__GL_SYNC_TO_VBLANK": "0",
                "__GL_SHADER_DISK_CACHE": "1",
                "__GL_SHADER_DISK_CACHE_SKIP_CLEANUP": "1",
                "__GL_MaxFramesAllowed": "1",
                "__GL_VRR_ENABLE": "1",
                "__GL_MAX_FRAME_LATENCY": "1",
                "__GL_PREFER_GRAPHICS_OVER_COMPUTE": "1",
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
                "INTEL_DEBUG": "nofc,norbc",
                "MESA_LOADER_DRIVER_OVERRIDE": "crocus", # Driver moderno para Gen6/7
                "mesa_glthread": "true",
                "MESA_GL_VERSION_OVERRIDE": "4.5",
                "MESA_GLSL_VERSION_OVERRIDE": "450",
                
                # === PERFORMANCE BOOST ===
                "vblank_mode": "0",
                "MESA_NO_ERROR": "1", # Performance pura
                "allow_glsl_extension_directive_midshader": "true",
                "MESA_EXTENSION_OVERRIDE": "GL_ARB_separate_shader_objects GL_ARB_explicit_attrib_location GL_ARB_gpu_shader5",
                
                # === MEMORY & CACHE ===
                "MESA_SHADER_CACHE_DISABLE": "false",
                "MESA_DISK_CACHE_SINGLE_FILE": "true",
                "MESA_DISK_CACHE_COMBINE_WRITES": "true",
                
                # === ARCH LINUX SPECIFIC ===
                "LD_PRELOAD": "/usr/lib/libjemalloc.so",
                "ST_DEBUG": "tgsi"
            }
        },
        {
            "id": 7,
            "name": "Legacy Boost Mode (Sandy Bridge i7-2760QM)",
            "env": {
                "MESA_LOADER_DRIVER_OVERRIDE": "crocus",
                "MESA_GL_VERSION_OVERRIDE": "4.4",
                "MESA_GLSL_VERSION_OVERRIDE": "440",
                "MESA_NO_ERROR": "1",
                "vblank_mode": "0",
                "mesa_glthread": "true",
                "INTEL_DEBUG": "nofc,norbc,no3d",
                "MESA_SHADER_CACHE_MAX_SIZE": "512M", # Cache menor para RAM limitada
                "LD_PRELOAD": "/usr/lib/libjemalloc.so.2",
                "SDL_VIDEO_MIN_VBLANKS": "0"
            }
        }
    ]

def get_compatibility_env(is_recent=True, profile_index=None):
    """
    Configura o ambiente Linux ULTRA OTIMIZADO para o Minecraft (versão EXTREMA).
    Implementa detecção automática de hardware e injeção dinâmica de drivers.
    """
    env = os.environ.copy()
    sys_info = get_system_info()
    profiles = get_autotune_profiles()

    # Prioridade para perfil manual se especificado
    if profile_index is not None:
        if 0 <= profile_index < len(profiles):
            selected_profile = profiles[profile_index]
            print(f"[PERF] Aplicando perfil manual: {selected_profile[\"name\"]}")
            env.update(selected_profile["env"])
            return env
        else:
            print(f"[WARN] Índice de perfil {profile_index} inválido. Tentando auto-detecção.")

    # === AUTO-TUNE AVANÇADO: Detectar melhor perfil com base no hardware ===
    selected_profile_env = {}
    if sys_info["gpu_vendor"] == "amd":
        if "radv" in sys_info["gpu_driver"]:
            print("[PERF] Auto-Tune: Nativo ULTRA (Mesa RADV Turbo 26.0+)")
            selected_profile_env = profiles[0]["env"]
        else:
            print("[PERF] Auto-Tune: AMD Universal (AMDGPU)")
            selected_profile_env = profiles[4]["env"]
    elif sys_info["gpu_vendor"] == "nvidia":
        print("[PERF] Auto-Tune: NVIDIA Proprietário 2026+")
        selected_profile_env = profiles[5]["env"]
    elif sys_info["gpu_vendor"] == "intel":
        if sys_info["is_legacy_intel"]:
            print("[PERF] Auto-Tune: Legacy Boost Mode (Sandy Bridge i7-2760QM)")
            selected_profile_env = profiles[7]["env"]
        elif sys_info["gpu_driver"] == "iris":
            print("[PERF] Auto-Tune: Intel Iris/UHD (Modern)")
            selected_profile_env = profiles[2]["env"]
        elif sys_info["gpu_driver"] == "crocus":
            print("[PERF] Auto-Tune: Intel HD 3000 EXTREME (Crocus)")
            selected_profile_env = profiles[6]["env"]
        else:
            print("[PERF] Auto-Tune: Intel Gen9+ (i965/Iris Fallback)")
            selected_profile_env = profiles[2]["env"] # Fallback para Iris/Modern
    else:
        print("[PERF] Auto-Tune: Padrão (Compatibilidade Universal)")
        selected_profile_env = profiles[3]["env"] # Perfil de compatibilidade geral

    env.update(selected_profile_env)

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
    
    if is_recent:
        env["LD_LIBRARY_PATH"] = (current_ld + ":" if current_ld else "") + ":".join(sys_paths)
    else:
        env["LD_LIBRARY_PATH"] = ":".join(sys_paths) + (":" + current_ld if current_ld else "")
    
    # === PRELOAD DE BIBLIOTECAS (BOOST) ===
    preload_libs = []
    
    if os.path.exists("/usr/lib/x86_64-linux-gnu/libjemalloc.so.2"):
        preload_libs.append("/usr/lib/x86_64-linux-gnu/libjemalloc.so.2")
    
    if preload_libs:
        env["LD_PRELOAD"] = ":".join(preload_libs)
        print(f"[PERF] LD_PRELOAD ativo: {env[\"LD_PRELOAD\"]}")
    
    # === WINDOW MANAGER E COMPOSITOR (X11 OTIMIZADO) ===
    env["_JAVA_AWT_WM_NONREPARENTING"] = "1"
    env["QT_QPA_PLATFORM"] = "xcb"
    env["GDK_BACKEND"] = "x11"
    env["SDL_VIDEODRIVER"] = "x11"
    env["SDL_VIDEO_MIN_VBLANKS"] = "0"
    
    # === SHADER CACHE (UNIVERSAL) ===
    shader_cache_dir = os.path.expanduser("~/.cache/aetherlauncher/shaders")
    os.makedirs(shader_cache_dir, exist_ok=True)
    env["MESA_SHADER_CACHE_DIR"] = shader_cache_dir
    env["MESA_SHADER_CACHE_MAX_SIZE"] = "4G"
    env["__GL_SHADER_DISK_CACHE_PATH"] = shader_cache_dir
    
    # === CPU GOVERNOR (PERFORMANCE MODE) ===
    try:
        for cpu in range(sys_info["cpu_cores"]):
            gov_path = f"/sys/devices/system/cpu/cpu{cpu}/cpufreq/scaling_governor"
            if os.path.exists(gov_path):
                try:
                    subprocess.run([\"sudo\", \"sh\", \"-c\", f\"echo performance > {gov_path}\"], 
                                   timeout=1, capture_output=True)
                except:
                    pass
    except:
        pass
    
    # === OPENGL MULTITHREAD (CRITICAL) ===
    env["__GL_THREADED_OPTIMIZATIONS"] = "1"
    env["mesa_glthread"] = "true"
    
    # === JAVA SPECIFIC ===
    # As flags JVM agora são injetadas pelo ExecutionBuilderExtreme, não aqui.
    # No entanto, podemos adicionar flags genéricas que não dependem de AVX2 aqui se necessário.
    # Por exemplo, para CPUs Sandy Bridge, podemos evitar flags que exigem AVX2.
    if not sys_info["has_avx2"]:
        print("[PERF] Detectado CPU sem AVX2. Ajustando JAVA_TOOL_OPTIONS para compatibilidade.")
        # Exemplo de flags JVM seguras para CPUs mais antigas
        env["JAVA_TOOL_OPTIONS"] = "-XX:+UseG1GC -XX:MaxGCPauseMillis=50 -XX:+UnlockExperimentalVMOptions -XX:+UseJVMCICompiler -XX:+EnableJVMCI -XX:JVMCICompiler=graal"
    else:
        env["JAVA_TOOL_OPTIONS"] = "-XX:+UseZGC -XX:+ZGenerational"

    return env

def get_performance_args():
    """Retorna argumentos de JVM ULTRA OTIMIZADAS para FPS MÁXIMO no Linux (versão EXTREMA)."""
    sys_info = get_system_info()
    
    args = [
        # === GENERATIONAL ZGC (Java 21+) ===
        "-XX:+UseZGC",
        "-XX:+ZGenerational",
        "-XX:ZCollectionInterval=250",
        "-XX:ZUncommitDelay=60",
        "-XX:ZUncommitInterval=5000",
        "-XX:ZAllocationSpikeTolerance=2.0",
        "-XX:ZUncommitClassPaths",
        "-XX:ZUncommitThreads",
        "-XX:ZUncommitHotSpots",
        
        # === COMPILADOR JIT GRAAL (EXPERIMENTAL) ===
        "-XX:+UnlockExperimentalVMOptions",
        "-XX:+UseJVMCICompiler",
        "-XX:+EnableJVMCI",
        "-XX:JVMCICompiler=graal",
        
        # === MEMORY MANAGEMENT ===
        "-XX:+AlwaysPreTouch",
        "-XX:+UseLargePages" if sys_info["has_hugepages"] else "",
        "-XX:+UseTransparentHugePages" if sys_info["has_hugepages"] else "",
        "-XX:LargePageSizeInBytes=2M" if sys_info["has_hugepages"] else "",
        "-XX:+DisableExplicitGC",
        "-XX:+PerfDisableSharedMem",
        
        # === GARBAGE COLLECTOR ===
        "-XX:+ParallelRefProcEnabled",
        "-XX:+UseStringDeduplication",
        "-XX:+UseCompressedOops",
        "-XX:+UseCompressedClassPointers",
        "-XX:MaxGCPauseMillis=50",
        "-XX:GCPauseIntervalMillis=100",
        "-XX:GCTimeRatio=99",
        
        # === COMPILADOR JIT ===
        "-XX:+TieredCompilation",
        "-XX:TieredStopAtLevel=4",
        "-XX:NmethodSweepInterval=10",
        "-XX:NmethodSweepLimit=100",
        "-XX:CompileThreshold=100",
        "-XX:OnStackReplacePercentage=120",
        "-XX:MaxInlineSize=1000",
        "-XX:FreqInlineSize=1000",
        
        # === CPU OPTIMIZATION ===
        "-XX:+AggressiveOpts",
        "-XX:+UseFMA" if sys_info["has_fma"] else "",
        "-XX:+UseAES" if sys_info["has_aes"] else "",
        "-XX:+UseAESIntrinsics" if sys_info["has_aes"] else "",
        "-XX:+UseSHA",
        "-XX:+UseSHAIntrinsics",
        "-XX:+UseAdler32Intrinsics",
        "-XX:+UseCRC32Intrinsics",
        
        # === NUMA & THREADING ===
        "-XX:+UseNUMA" if sys_info["has_numa"] else "",
        "-XX:+UseTransparentHugePages",
        "-XX:-UseAdaptiveSizePolicy",
        "-XX:+AlwaysActAsServerClassMachine",
        
        # === BIASED LOCKING ===
        "-XX:+UseBiasedLocking",
        "-XX:BiasedLockingStartupDelay=0",
        
        # === METASPACE ===
        "-XX:MetaspaceSize=512M",
        "-XX:MaxMetaspaceSize=1024M",
        "-XX:+ClassUnloadingWithConcurrentMark",
        
        # === CODE CACHE ===
        "-XX:ReservedCodeCacheSize=768M",
        "-XX:InitialCodeCacheSize=384M",
        "-XX:MaxInlineLevel=15",
        
        # === JAVA FLAGS ===
        "-Djava.awt.headless=false",
        "-Dsun.rmi.dgc.server.gcInterval=2147483646",
        "-Dfile.encoding=UTF-8",
        "-Dusing.aikars.flags=https://mcflags.emc.gs",
        "-Daikars.new.flags=true",
        
        # === LWJGL E OPENGL ===
        "-Dorg.lwjgl.opengl.Display.enableHighDPI=true",
        "-Dorg.lwjgl.opengl.Display.allowSoftwareOpenGL=false",
        "-Dorg.lwjgl.util.DebugLoader=true",
        "-Dorg.lwjgl.util.Debug=false",
        "-Dfml.readTimeout=240",
        
        # === NETWORK STACK ===
        "-Djava.net.preferIPv4Stack=true",
        "-Dio.netty.recycler.maxCapacity=0",
        "-Dio.netty.leakDetection.level=DISABLED",
    ]
    
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
    Ativa modo de performance EXTREMO no sistema (CPU governor, I/O scheduler, sysctl).
    Requer permissões de root, mas tenta sem falhar.
    """
    try:
        sys_info = get_system_info()
        
        # === CPU GOVERNOR -> PERFORMANCE ===
        for cpu in range(sys_info["cpu_cores"]):
            gov_file = f"/sys/devices/system/cpu/cpu{cpu}/cpufreq/scaling_governor"
            if os.path.exists(gov_file):
                try:
                    with open(gov_file, 'w') as f:
                        f.write('performance')
                except:
                    try:
                        subprocess.run(['sudo', 'sh', '-c', f'echo performance > {gov_file}'], 
                                       timeout=2, capture_output=True)
                    except:
                        pass
        
        # === I/O SCHEDULER -> MQ-DEADLINE (para NVMe) ===
        for disk in ['nvme0n1', 'sda', 'vda']:
            scheduler_file = f"/sys/block/{disk}/queue/scheduler"
            if os.path.exists(scheduler_file):
                try:
                    with open(scheduler_file, 'w') as f:
                        f.write('mq-deadline')
                except:
                    pass
        
        # === SYSCTL TWEAKS ===
        sysctl_tweaks = {
            "net.core.rmem_max": "16777216",
            "net.core.wmem_max": "16777216",
            "net.ipv4.tcp_rmem": "4096 87380 16777216",
            "net.ipv4.tcp_wmem": "4096 65536 16777216",
            "net.ipv4.tcp_fastopen": "3",
            "net.ipv4.tcp_tw_reuse": "1",
            "vm.swappiness": "10",
            "kernel.sched_latency_ns": "1000000",
            "kernel.sched_min_granularity_ns": "1000000"
        }
        
        for key, value in sysctl_tweaks.items():
            try:
                subprocess.run(['sudo', 'sysctl', '-w', f'{key}={value}'], 
                               timeout=2, capture_output=True)
            except:
                pass
        
        print("[PERF] Modo de performance EXTREMO ativado!")
    except Exception as e:
        print(f"[PERF] Aviso: Não foi possível ativar modo performance completo ({e})")
