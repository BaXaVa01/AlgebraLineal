# main.py
import customtkinter as ctk
from tabs.intro_tab import IntroTab
from tabs.calculator_tab import CalculatorTab
from tabs.graph_tab import GraphTab
from tabs.bisection_tab import BisectionTab
from tabs.newton_tab import NewtonRaphsonTab
from tabs.settings_tab import SettingsTab, initialize_fonts
from tabs.reportes_tab import ReportesTab  # Importar la nueva pestaña de Reportes
from tabs.secante_tab import SecanteTab
from tabs.fakePosition_tab import FakePositionTab
from tabs.Aprox_tab import AproxTab  # Importar la nueva pestaña Aproximar

class AnalisisNum(ctk.CTk):
    def __init__(self, parent_menu):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Aplicación de Métodos Numéricos")
        window_width = 1000
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(800, 500)

        # Inicializar las fuentes
        initialize_fonts()

        # Configurar layout adaptable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Crear TabView principal
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Crear e inicializar pestañas
        self.intro_tab = IntroTab(self.tabview)
        self.calculator_tab = CalculatorTab(self.tabview)
        self.graph_tab = GraphTab(self.tabview)
        self.aprox_tab = AproxTab(self.tabview)  # Agregar la nueva pestaña "Aproximar"
        self.settings_tab = SettingsTab(self.tabview)
        self.reportes_tab = ReportesTab(self.tabview)

        # Vincular evento de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Regresa al menú principal al cerrar AnalisisNum."""
        self.destroy()
        self.parent_menu.deiconify()
