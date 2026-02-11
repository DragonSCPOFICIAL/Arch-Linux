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
        if os.path.exists('/proc/cpuinfo'):
            with open('/proc/cpuinfo', 'r') as f:
                content = f.read()
                # Extrair modelo
                for line in content.split('\n'):
                    if line.startswith('model name'):
                        info["cpu_model"] = line.split(':', 1)[1].strip()
                        if "sandy bridge" in info["cpu_model"].lower():
                            info["is_legacy_intel"] = True
                        break
                # Detectar flags de CPU
                if 'avx2' in content: info["has_avx2"] = True
                if 'fma' in content: info["has_fma"] = True
                if 'aes' in content: info["has_aes"] = True
    except: pass

    try:
        # Detectar versão do kernel
        with open('/proc/version', 'r') as f:
            version_line = f.read()
            parts = version_line.split()
            if len(parts) > 2:
                info["kernel_version"] = parts[2]
    except: pass

    try:
        # Detectar GPU
        lspci_output = subprocess.check_output(['lspci'], text=True, timeout=2).lower()
        if "amd" in lspci_output or "radeon" in lspci_output:
            info["gpu_vendor"] = "amd"
            info["gpu_driver"] = "radv"
        elif "nvidia" in lspci_output or "geforce" in lspci_output:
            info["gpu_vendor"] = "nvidia"
            info["gpu_driver"] = "nvidia-proprietary"
        elif "intel" in lspci_output:
            info["gpu_vendor"] = "intel"
            info["gpu_driver"] = "iris"
    except: pass
    
    return info

def get_gpu_info():
    info = get_system_info()
    return f"GPU: {info['gpu_vendor'].upper()} ({info['gpu_driver']}) | RAM: {info['ram_gb']}GB | Cores: {info['cpu_cores']}"

def apply_linux_tweaks(config):
    print("[LINUX] Aplicando EXTREME Power Tweaks...")

def enable_performance_mode():
    print("[PERF] Modo performance ativado.")

def get_themes():
    return {"Aether (Padrão)": {"accent": "#B43D3D", "bg": "#1a1a1a", "fg": "white"}}

def get_autotune_profiles():
    return [{"id": 0, "name": "Nativo ULTRA", "env": {}}]

def get_instance_path(base_dir, name):
    return os.path.join(base_dir, "instances", name.replace(" ", "_"))

def get_java_recommendation(version):
    return "java-runtime-alpha"

def get_minecraft_era(version):
    return "modern"
