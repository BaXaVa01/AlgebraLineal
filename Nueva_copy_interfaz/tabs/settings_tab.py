import customtkinter as ctk

# Definir las fuentes como None por ahora
GLOBAL_FONT = None
MINI = None

def initialize_fonts():
    """Inicializa las fuentes globales después de crear la ventana raíz."""
    global GLOBAL_FONT, MINI
    GLOBAL_FONT = ctk.CTkFont(family="Arial", size=14)  # Tamaño inicial
    MINI = ctk.CTkFont(family="Arial", size=12)  # Tamaño inicial

class SettingsTab:
    def __init__(self, tabview):
        # Crear la pestaña de Configuración
        self.tab = tabview.add("Configuración")

        # Sección para cambiar el modo de apariencia (claro u oscuro)
        self.appearance_label = ctk.CTkLabel(self.tab, text="Modo de Apariencia:", font=GLOBAL_FONT)
        self.appearance_label.pack(pady=10)
        
        # Deslizador para cambiar entre Modo Oscuro y Claro
        self.appearance_mode = ctk.CTkComboBox(self.tab, values=["System", "Dark", "Light"], command=self.change_appearance)
        self.appearance_mode.set("System")  # Valor predeterminado
        self.appearance_mode.pack(pady=10)
        
        # Deslizador de tamaño de fuente
        self.font_size_label = ctk.CTkLabel(self.tab, text="Tamaño de Fuente Global:", font=GLOBAL_FONT)
        self.font_size_label.pack(pady=10)
        
        self.font_size_slider = ctk.CTkSlider(self.tab, from_=10, to=30, command=self.adjust_font_size)
        self.font_size_slider.pack(pady=10)

        # Sección de información adicional
        self.info_label = ctk.CTkLabel(self.tab, text="Información del Sistema:", font=GLOBAL_FONT)
        self.info_label.pack(pady=10)
        
        self.system_info = ctk.CTkLabel(self.tab, text="Versión: 1.0\nDesarrollado por: Davide", font=MINI)
        self.system_info.pack(pady=10)

    def change_appearance(self, mode):
        """Cambiar el modo de apariencia."""
        ctk.set_appearance_mode(mode)

    def adjust_font_size(self, size):
        """Ajustar el tamaño de la fuente en la aplicación."""
        GLOBAL_FONT.configure(size=int(size))  # Cambiar el tamaño global
        MINI.configure(size=int(size - 2))
        print(f"Tamaño de fuente ajustado a: {int(size)}")
