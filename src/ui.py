"""
BRX AI - Interface Gráfica (UI/UX)
Interface moderna inspirada no Manus com design "Modo Prime"
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import threading
import sys
import os
from datetime import datetime

# Importar configurações e utilidades
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *
from utils import logger, format_timestamp, get_system_info, check_system_health

# ============================================================================
# CLASSE PRINCIPAL DA INTERFACE
# ============================================================================
class BRXAIInterface:
    def __init__(self, root, ai_engine=None):
        """Inicializa a interface do BRX AI"""
        self.root = root
        self.ai_engine = ai_engine
        self.is_processing = False
        self.current_page = "chat"
        
        # Configurar janela
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.root.configure(bg=COLORS["bg_primary"])
        
        # Configurar estilo
        self.setup_styles()
        
        # Construir interface
        self.build_ui()
        
        logger.info("Interface BRX AI inicializada com sucesso")
    
    def setup_styles(self):
        """Configura estilos da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores do tema
        style.configure('TFrame', background=COLORS["bg_primary"])
        style.configure('TLabel', background=COLORS["bg_primary"], foreground=COLORS["text_primary"])
        style.configure('TButton', background=COLORS["accent_primary"], foreground=COLORS["text_primary"])
    
    def build_ui(self):
        """Constrói a interface principal"""
        # Container principal
        main_container = tk.Frame(self.root, bg=COLORS["bg_primary"])
        main_container.pack(fill="both", expand=True)
        
        # Sidebar
        self.build_sidebar(main_container)
        
        # Área principal
        self.main_area = tk.Frame(main_container, bg=COLORS["bg_primary"])
        self.main_area.pack(side="right", fill="both", expand=True)
        
        # Mostrar página inicial
        self.show_chat_page()
    
    def build_sidebar(self, parent):
        """Constrói a barra lateral"""
        sidebar = tk.Frame(parent, bg=COLORS["bg_secondary"], width=SIDEBAR_WIDTH)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Logo
        logo_frame = tk.Frame(sidebar, bg=COLORS["bg_secondary"], pady=30)
        logo_frame.pack(fill="x")
        
        logo_label = tk.Label(
            logo_frame,
            text="BRX AI",
            font=FONTS["title_large"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["accent_primary"]
        )
        logo_label.pack()
        
        version_label = tk.Label(
            logo_frame,
            text=f"v{APP_VERSION}",
            font=FONTS["label"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_secondary"]
        )
        version_label.pack()
        
        # Divisor
        divider = tk.Frame(sidebar, bg=COLORS["border"], height=1)
        divider.pack(fill="x", padx=20, pady=10)
        
        # Menu de navegação
        nav_frame = tk.Frame(sidebar, bg=COLORS["bg_secondary"])
        nav_frame.pack(fill="both", expand=True, padx=10, pady=20)
        
        self.nav_buttons = {}
        
        nav_items = [
            ("💬 Chat", "chat", self.show_chat_page),
            ("👁️ Visão", "vision", self.show_vision_page),
            ("🛠️ Automação", "automation", self.show_automation_page),
            ("⚙️ Configurações", "settings", self.show_settings_page),
        ]
        
        for label, page_id, command in nav_items:
            btn = self.create_nav_button(nav_frame, label, page_id, command)
            self.nav_buttons[page_id] = btn
        
        # Divisor inferior
        divider2 = tk.Frame(sidebar, bg=COLORS["border"], height=1)
        divider2.pack(fill="x", padx=20, pady=10, side="bottom")
        
        # Status do sistema
        footer = tk.Frame(sidebar, bg=COLORS["bg_secondary"], pady=15)
        footer.pack(side="bottom", fill="x", padx=10)
        
        status_label = tk.Label(
            footer,
            text="● AGENTE ATIVO",
            font=FONTS["label"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["success"]
        )
        status_label.pack(anchor="w")
        
        self.system_label = tk.Label(
            footer,
            text="CPU: 0% | MEM: 0%",
            font=FONTS["body_small"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_secondary"]
        )
        self.system_label.pack(anchor="w", pady=(5, 0))
        
        # Atualizar status do sistema periodicamente
        self.update_system_status()
    
    def create_nav_button(self, parent, label, page_id, command):
        """Cria um botão de navegação"""
        btn = tk.Button(
            parent,
            text=label,
            font=FONTS["button"],
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            activebackground=COLORS["bg_tertiary"],
            activeforeground=COLORS["accent_primary"],
            bd=0,
            padx=15,
            pady=12,
            anchor="w",
            cursor="hand2",
            command=lambda: self.switch_page(page_id, command)
        )
        btn.pack(fill="x", pady=5)
        return btn
    
    def switch_page(self, page_id, command):
        """Muda de página"""
        self.current_page = page_id
        command()
    
    def clear_main_area(self):
        """Limpa a área principal"""
        for widget in self.main_area.winfo_children():
            widget.destroy()
    
    def show_chat_page(self):
        """Mostra a página de chat"""
        self.clear_main_area()
        
        # Header
        header = tk.Frame(self.main_area, bg=COLORS["bg_primary"], height=HEADER_HEIGHT)
        header.pack(fill="x", padx=20, pady=15)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="Central de Comando",
            font=FONTS["title_medium"],
            bg=COLORS["bg_primary"],
            fg=COLORS["text_primary"]
        )
        title.pack(side="left", anchor="w")
        
        # Chat container
        chat_container = tk.Frame(self.main_area, bg=COLORS["bg_primary"])
        chat_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            bg=COLORS["bg_tertiary"],
            fg=COLORS["text_primary"],
            font=FONTS["body_medium"],
            bd=0,
            padx=15,
            pady=15,
            state="disabled",
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            wrap=tk.WORD
        )
        self.chat_display.pack(fill="both", expand=True)
        
        # Configurar tags de cor
        self.chat_display.tag_config("user", foreground=COLORS["accent_primary"], font=FONTS["body_large"])
        self.chat_display.tag_config("ai", foreground=COLORS["success"], font=FONTS["body_large"])
        self.chat_display.tag_config("system", foreground=COLORS["warning"], font=FONTS["body_large"])
        self.chat_display.tag_config("timestamp", foreground=COLORS["text_secondary"], font=FONTS["body_small"])
        
        # Input frame
        input_frame = tk.Frame(self.main_area, bg=COLORS["bg_primary"])
        input_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Input background
        input_bg = tk.Frame(
            input_frame,
            bg=COLORS["bg_tertiary"],
            highlightthickness=1,
            highlightbackground=COLORS["border"]
        )
        input_bg.pack(fill="x")
        
        # Input field
        self.msg_entry = tk.Entry(
            input_bg,
            bg=COLORS["bg_tertiary"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["accent_primary"],
            bd=0,
            font=FONTS["body_medium"],
            padx=15,
            pady=12
        )
        self.msg_entry.pack(side="left", fill="both", expand=True)
        self.msg_entry.bind("<Return>", lambda e: self.send_message())
        self.msg_entry.bind("<Shift-Return>", lambda e: self.add_newline(e))
        
        # Send button
        send_btn = tk.Button(
            input_bg,
            text="ENVIAR",
            font=FONTS["button"],
            bg=COLORS["accent_primary"],
            fg="#FFFFFF",
            activebackground=COLORS["accent_secondary"],
            activeforeground="#FFFFFF",
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2",
            command=self.send_message
        )
        send_btn.pack(side="right", padx=5, pady=5)
        
        # Mensagem de boas-vindas
        self.append_message("BRX AI", "Bem-vindo! Sou seu agente autônomo para Linux. Como posso ajudá-lo?", "ai")
        
        # Focus no input
        self.msg_entry.focus()
    
    def send_message(self):
        """Envia uma mensagem"""
        message = self.msg_entry.get().strip()
        if not message:
            return
        
        self.append_message("Você", message, "user")
        self.msg_entry.delete(0, tk.END)
        
        # Processar em thread separada
        if self.ai_engine:
            thread = threading.Thread(target=self.process_message, args=(message,))
            thread.daemon = True
            thread.start()
        else:
            self.append_message("BRX AI", "Processando sua solicitação...", "ai")
    
    def process_message(self, message):
        """Processa a mensagem (chamará o engine de IA)"""
        try:
            self.is_processing = True
            
            # Aqui você chamaria o engine de IA real
            # response = self.ai_engine.process(message)
            
            # Por enquanto, simulação
            response = f"Entendi sua solicitação: '{message}'. Estou processando..."
            self.append_message("BRX AI", response, "ai")
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            self.append_message("SISTEMA", f"Erro: {str(e)}", "system")
        finally:
            self.is_processing = False
    
    def append_message(self, sender, message, tag="system"):
        """Adiciona uma mensagem ao chat"""
        self.chat_display.config(state="normal")
        
        timestamp = format_timestamp()
        
        # Adicionar timestamp
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Adicionar remetente
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        
        # Adicionar mensagem
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)
    
    def add_newline(self, event):
        """Adiciona uma nova linha no input"""
        self.msg_entry.insert(tk.END, "\n")
        return "break"
    
    def show_vision_page(self):
        """Mostra a página de visão do sistema"""
        self.clear_main_area()
        
        container = tk.Frame(self.main_area, bg=COLORS["bg_primary"], padx=20, pady=20)
        container.pack(fill="both", expand=True)
        
        title = tk.Label(
            container,
            text="Visão do Agente",
            font=FONTS["title_medium"],
            bg=COLORS["bg_primary"],
            fg=COLORS["text_primary"]
        )
        title.pack(anchor="w", pady=(0, 20))
        
        # Placeholder para visão
        vision_card = tk.Frame(
            container,
            bg=COLORS["bg_tertiary"],
            height=400,
            highlightthickness=1,
            highlightbackground=COLORS["border"]
        )
        vision_card.pack(fill="both", expand=True)
        vision_card.pack_propagate(False)
        
        placeholder = tk.Label(
            vision_card,
            text="[ FEED DE TELA EM TEMPO REAL ]",
            font=FONTS["title_small"],
            bg=COLORS["bg_tertiary"],
            fg=COLORS["text_secondary"]
        )
        placeholder.place(relx=0.5, rely=0.5, anchor="center")
    
    def show_automation_page(self):
        """Mostra a página de automação"""
        self.clear_main_area()
        
        container = tk.Frame(self.main_area, bg=COLORS["bg_primary"], padx=20, pady=20)
        container.pack(fill="both", expand=True)
        
        title = tk.Label(
            container,
            text="Painel de Automação",
            font=FONTS["title_medium"],
            bg=COLORS["bg_primary"],
            fg=COLORS["text_primary"]
        )
        title.pack(anchor="w", pady=(0, 20))
        
        # Scroll frame
        canvas = tk.Canvas(container, bg=COLORS["bg_primary"], bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["bg_primary"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Tools
        tools = [
            ("📸 Captura de Tela", "Permite que a IA veja o que está acontecendo na tela."),
            ("🖱️ Controle de Mouse", "Permite que a IA clique e mova o cursor."),
            ("⌨️ Injeção de Teclado", "Permite que a IA digite comandos e textos."),
            ("🔧 Terminal Root", "Acesso direto ao shell para tarefas complexas."),
            ("📊 Monitoramento", "Monitora recursos do sistema em tempo real."),
            ("🔐 Segurança", "Controles de segurança e permissões."),
        ]
        
        for title_tool, desc in tools:
            card = tk.Frame(
                scrollable_frame,
                bg=COLORS["bg_tertiary"],
                padx=15,
                pady=12,
                highlightthickness=1,
                highlightbackground=COLORS["border"]
            )
            card.pack(fill="x", pady=8)
            
            title_label = tk.Label(
                card,
                text=title_tool,
                font=FONTS["title_small"],
                bg=COLORS["bg_tertiary"],
                fg=COLORS["accent_primary"]
            )
            title_label.pack(anchor="w")
            
            desc_label = tk.Label(
                card,
                text=desc,
                font=FONTS["body_small"],
                bg=COLORS["bg_tertiary"],
                fg=COLORS["text_secondary"],
                wraplength=400,
                justify="left"
            )
            desc_label.pack(anchor="w", pady=(5, 0))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_settings_page(self):
        """Mostra a página de configurações"""
        self.clear_main_area()
        
        container = tk.Frame(self.main_area, bg=COLORS["bg_primary"], padx=20, pady=20)
        container.pack(fill="both", expand=True)
        
        title = tk.Label(
            container,
            text="Configurações do Núcleo",
            font=FONTS["title_medium"],
            bg=COLORS["bg_primary"],
            fg=COLORS["text_primary"]
        )
        title.pack(anchor="w", pady=(0, 20))
        
        # Settings card
        settings_card = tk.Frame(
            container,
            bg=COLORS["bg_tertiary"],
            padx=20,
            pady=20,
            highlightthickness=1,
            highlightbackground=COLORS["border"]
        )
        settings_card.pack(fill="x")
        
        # Checkbuttons
        settings = [
            "Permitir Controle Total do Mouse/Teclado",
            "Modo de Resposta Ultra-Rápida (Prime)",
            "Registrar Todas as Ações",
            "Notificações de Sistema",
        ]
        
        for setting in settings:
            var = tk.BooleanVar()
            check = tk.Checkbutton(
                settings_card,
                text=setting,
                font=FONTS["body_medium"],
                bg=COLORS["bg_tertiary"],
                fg=COLORS["text_primary"],
                activebackground=COLORS["bg_tertiary"],
                activeforeground=COLORS["accent_primary"],
                selectcolor=COLORS["bg_secondary"],
                variable=var
            )
            check.pack(anchor="w", pady=8)
    
    def update_system_status(self):
        """Atualiza o status do sistema na sidebar"""
        try:
            health = check_system_health()
            status_text = f"CPU: {health['cpu']:.0f}% | MEM: {health['memory']:.0f}%"
            self.system_label.config(text=status_text)
        except Exception as e:
            logger.error(f"Erro ao atualizar status do sistema: {e}")
        
        # Atualizar a cada 2 segundos
        self.root.after(2000, self.update_system_status)

# ============================================================================
# FUNÇÃO PARA INICIAR A INTERFACE
# ============================================================================
def create_interface(root, ai_engine=None):
    """Cria e retorna a interface do BRX AI"""
    return BRXAIInterface(root, ai_engine)
