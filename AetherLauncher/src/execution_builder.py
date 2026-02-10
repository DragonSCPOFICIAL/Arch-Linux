import os
import json
import subprocess
import minecraft_launcher_lib

class ExecutionBuilder:
    """
    Classe isolada para construir o comando de execução do Minecraft,
    garantindo compatibilidade entre Vanilla e Forge.
    """
    
    @staticmethod
    def build_command(version_id, minecraft_dir, options):
        """
        Constrói o comando de execução. 
        Se for Forge, aplica a lógica de correção de Classpath e MainClass.
        """
        print(f"[ExecutionBuilder] Construindo comando para: {version_id}")
        
        # 1. Garantir que a pasta natives exista para a instância
        game_dir = options.get("gameDirectory")
        if game_dir:
            natives_dir = os.path.join(game_dir, "natives")
            os.makedirs(natives_dir, exist_ok=True)
            options["nativePath"] = natives_dir

        # 2. Tentar obter o comando padrão via biblioteca
        try:
            command = minecraft_launcher_lib.command.get_minecraft_command(version_id, minecraft_dir, options)
        except Exception as e:
            print(f"[ExecutionBuilder] Erro ao gerar comando base: {e}")
            return None

        # 2. Verificar se é uma versão Forge para aplicar correções
        version_json_path = os.path.join(minecraft_dir, "versions", version_id, f"{version_id}.json")
        
        if os.path.exists(version_json_path):
            try:
                with open(version_json_path, 'r') as f:
                    data = json.load(f)
                
                # Se houver herança ou for explicitamente Forge
                is_forge = "forge" in version_id.lower() or "inheritsFrom" in data
                
                if is_forge:
                    print("[ExecutionBuilder] Aplicando correções específicas para Forge...")
                    return ExecutionBuilder._fix_forge_command(command, data, minecraft_dir, version_id)
            except Exception as e:
                print(f"[ExecutionBuilder] Erro ao analisar JSON da versão: {e}")
        
        return command

    @staticmethod
    def _fix_forge_command(command, version_data, minecraft_dir, version_id):
        """
        Corrige o comando do Forge:
        - Garante que a MainClass seja a do Forge.
        - Garante que o Classpath inclua todas as bibliotecas necessárias.
        """
        # Extrair a MainClass correta do JSON
        forge_main_class = version_data.get("mainClass")
        if not forge_main_class:
            return command # Se não tiver, mantém o original
            
        # Localizar a MainClass no comando original (geralmente o último argumento ou próximo ao fim)
        # O comando gerado pela lib costuma terminar com os argumentos do jogo.
        # A MainClass fica logo após os argumentos da JVM e antes dos argumentos do jogo.
        
        new_command = list(command)
        
        # Tentar substituir a MainClass vanilla pela do Forge
        # A biblioteca às vezes coloca a mainClass errada se não processar corretamente a herança
        vanilla_main = "net.minecraft.client.main.Main"
        if vanilla_main in new_command:
            idx = new_command.index(vanilla_main)
            new_command[idx] = forge_main_class
            print(f"[ExecutionBuilder] ✓ MainClass corrigida: {vanilla_main} -> {forge_main_class}")
        
        # Correção de Classpath (-cp)
        # O Forge moderno exige que o classpath seja montado com cuidado.
        # Vamos garantir que o arquivo JAR da versão Forge esteja no CP.
        try:
            cp_idx = -1
            if "-cp" in new_command:
                cp_idx = new_command.index("-cp") + 1
            elif "-classpath" in new_command:
                cp_idx = new_command.index("-classpath") + 1
                
            if cp_idx > 0:
                current_cp = new_command[cp_idx]
                forge_jar = os.path.join(minecraft_dir, "versions", version_id, f"{version_id}.jar")
                
                if os.path.exists(forge_jar) and forge_jar not in current_cp:
                    # No Linux o separador é :
                    new_command[cp_idx] = f"{forge_jar}:{current_cp}"
                    print("[ExecutionBuilder] ✓ JAR do Forge adicionado ao Classpath")
        except Exception as e:
            print(f"[ExecutionBuilder] Erro ao ajustar Classpath: {e}")

        return new_command
