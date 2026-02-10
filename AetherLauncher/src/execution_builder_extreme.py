import os
import json
import subprocess
import minecraft_launcher_lib
from utils_extreme import get_system_info, get_performance_args, get_compatibility_env

class ExecutionBuilderExtreme:
    """
    Classe avançada para construir o comando de execução do Minecraft com otimizações EXTREMAS.
    Suporta Vanilla, Forge, Fabric, Quilt e NeoForge com injeção de flags JVM otimizadas.
    """
    
    @staticmethod
    def build_command(version_id, minecraft_dir, options, profile_index=None):
        """
        Constrói o comando de execução com otimizações EXTREMAS.
        Injeta flags de performance, gerenciamento de memória e variáveis de ambiente.
        """
        print(f"[ExecutionBuilderExtreme] Construindo comando EXTREMO para: {version_id}")
        
        sys_info = get_system_info()
        
        # 1. Garantir que a pasta natives exista para a instância
        game_dir = options.get("gameDirectory")
        if game_dir:
            natives_dir = os.path.join(game_dir, "natives")
            os.makedirs(natives_dir, exist_ok=True)
            options["nativePath"] = natives_dir

        # 2. Obter o comando padrão via biblioteca
        try:
            command = minecraft_launcher_lib.command.get_minecraft_command(version_id, minecraft_dir, options)
        except Exception as e:
            print(f"[ExecutionBuilderExtreme] Erro ao gerar comando base: {e}")
            return None

        # 3. Injetar flags JVM de performance EXTREMA
        command = ExecutionBuilderExtreme._inject_performance_flags(command, version_id, sys_info)
        
        # 4. Aplicar correções específicas para modloaders
        version_json_path = os.path.join(minecraft_dir, "versions", version_id, f"{version_id}.json")
        
        if os.path.exists(version_json_path):
            try:
                with open(version_json_path, 'r') as f:
                    data = json.load(f)
                
                is_modloader = any(x in version_id.lower() for x in ["forge", "neoforge", "fabric", "quilt"]) or "inheritsFrom" in data
                
                if is_modloader:
                    print(f"[ExecutionBuilderExtreme] Detectado modloader em {version_id}...")
                    command = ExecutionBuilderExtreme._fix_modloader_command(command, data, minecraft_dir, version_id)
            except Exception as e:
                print(f"[ExecutionBuilderExtreme] Erro ao analisar JSON: {e}")
        
        return command

    @staticmethod
    def _inject_performance_flags(command, version_id, sys_info):
        """
        Injeta flags JVM de performance EXTREMA no comando.
        """
        perf_args = get_performance_args()
        
        # Encontrar o índice do -cp ou -classpath para inserir as flags ANTES
        new_command = list(command)
        
        cp_idx = -1
        if "-cp" in new_command:
            cp_idx = new_command.index("-cp")
        elif "-classpath" in new_command:
            cp_idx = new_command.index("-classpath")
        
        # Inserir as flags de performance ANTES do classpath
        if cp_idx > 0:
            # Inserir todas as flags antes do -cp
            for i, flag in enumerate(perf_args):
                new_command.insert(cp_idx + i, flag)
            print(f"[ExecutionBuilderExtreme] ✓ {len(perf_args)} flags de performance injetadas")
        else:
            # Se não encontrar -cp, tentar inserir após o java
            if len(new_command) > 0 and 'java' in new_command[0]:
                for i, flag in enumerate(perf_args):
                    new_command.insert(1 + i, flag)
                print(f"[ExecutionBuilderExtreme] ✓ {len(perf_args)} flags de performance injetadas (alternativo)")
        
        return new_command

    @staticmethod
    def _fix_modloader_command(command, version_data, minecraft_dir, version_id):
        """
        Corrige o comando para Forge, Fabric, Quilt e NeoForge.
        """
        new_command = list(command)
        
        # Extrair a MainClass correta do JSON
        forge_main_class = version_data.get("mainClass")
        if forge_main_class:
            vanilla_main = "net.minecraft.client.main.Main"
            if vanilla_main in new_command:
                idx = new_command.index(vanilla_main)
                new_command[idx] = forge_main_class
                print(f"[ExecutionBuilderExtreme] ✓ MainClass corrigida: {vanilla_main} -> {forge_main_class}")
        
        # Correção de Classpath
        try:
            cp_idx = -1
            if "-cp" in new_command:
                cp_idx = new_command.index("-cp") + 1
            elif "-classpath" in new_command:
                cp_idx = new_command.index("-classpath") + 1
                
            if cp_idx > 0:
                current_cp = new_command[cp_idx]
                modloader_jar = os.path.join(minecraft_dir, "versions", version_id, f"{version_id}.jar")
                
                if os.path.exists(modloader_jar) and modloader_jar not in current_cp:
                    new_command[cp_idx] = f"{modloader_jar}:{current_cp}"
                    print("[ExecutionBuilderExtreme] ✓ JAR do modloader adicionado ao Classpath")
        except Exception as e:
            print(f"[ExecutionBuilderExtreme] Erro ao ajustar Classpath: {e}")

        return new_command

    @staticmethod
    def get_environment_variables(profile_index=None):
        """
        Retorna as variáveis de ambiente otimizadas para o launcher.
        """
        return get_compatibility_env(is_recent=True, profile_index=profile_index)

    @staticmethod
    def validate_command(command):
        """
        Valida se o comando está bem formado.
        """
        if not command or len(command) < 2:
            print("[ExecutionBuilderExtreme] ✗ Comando inválido ou vazio")
            return False
        
        if 'java' not in command[0]:
            print("[ExecutionBuilderExtreme] ✗ Comando não começa com java")
            return False
        
        print(f"[ExecutionBuilderExtreme] ✓ Comando validado ({len(command)} argumentos)")
        return True

    @staticmethod
    def print_command_info(command):
        """
        Imprime informações sobre o comando para debug.
        """
        if not command:
            return
        
        print("\n" + "="*80)
        print("[COMMAND INFO]")
        print(f"Java: {command[0]}")
        
        jvm_flags = [arg for arg in command if arg.startswith("-X") or arg.startswith("-D") or arg.startswith("-XX")]
        print(f"JVM Flags: {len(jvm_flags)}")
        
        if "-cp" in command:
            cp_idx = command.index("-cp") + 1
            if cp_idx < len(command):
                cp_parts = command[cp_idx].split(":")
                print(f"Classpath entries: {len(cp_parts)}")
        
        print("="*80 + "\n")
