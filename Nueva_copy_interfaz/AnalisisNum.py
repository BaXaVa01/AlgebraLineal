# main.py
import customtkinter as ctk
from tabs.intro_tab import IntroTab
from tabs.calculator_tab import CalculatorTab
from tabs.graph_tab import GraphTab
from tabs.bisection_tab import BisectionTab
from tabs.newton_tab import NewtonRaphsonTab
from tabs.settings_tab import SettingsTab, initialize_fonts
from tabs.reportes_tab import ReportesTab  # Importar la nueva pestaña de Reportes


class AnalisisNum(ctk.CTk):
    def __init__(self, parent_menu):
        super().__init__()

        # Guardar referencia al menú principal
        self.parent_menu = parent_menu

        # Configuración de la ventana principal
        self.title("Aplicación de Métodos Numéricos")
        window_width = 1000
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(800, 500)  # Tamaño mínimo para evitar problemas de visualización
        self.set_appearance()
        
        # Inicializar las fuentes después de crear la raíz
        initialize_fonts()

        # Configurar el layout adaptable
        self.grid_rowconfigure(0, weight=1)  # Hacer que el Tabview se expanda verticalmente
        self.grid_columnconfigure(0, weight=1)  # Hacer que el Tabview se expanda horizontalmente

        # Crear y empaquetar el Tabview principal
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # Usar grid para mayor flexibilidad

        # Inicializar las pestañas
        self.intro_tab = IntroTab(self.tabview)
        self.calculator_tab = CalculatorTab(self.tabview)
        self.graph_tab = GraphTab(self.tabview)
        self.bisection_tab = BisectionTab(self.tabview)
        self.newton_raphson_tab = NewtonRaphsonTab(self.tabview)
        self.settings_tab = SettingsTab(self.tabview)
        self.reportes_tab = ReportesTab(self.tabview)  # Agregar la pestaña de Reportes

        # Vincular el evento de cerrar ventana
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def set_appearance(self):
        """Configura el modo de apariencia y el tema de color."""
        ctk.set_appearance_mode("System")  # Cambia entre 'System', 'Dark' y 'Light'
        ctk.set_default_color_theme("blue")  # Cambia el color de tema si es necesario

    def on_close(self):
        """Regresa al menú principal al cerrar AnalisisNum."""
        self.destroy()
        self.parent_menu.deiconify()
        
if __name__ == "__main__":
    app = AnalisisNum()
    app.mainloop()