# main.py
import customtkinter as ctk
from tabs.algebra.inversaDeMatriz_Tab import InversaDeMatriz_Tab
from tabs.matrices_Tab import MatricesTab
from tabs.graph_tab import GraphTab
from tabs.ResolutorMatrix import EquationSolver
from tabs.Gaus_tab import GaussJordanSolver
# from tabs.algebra.cramer_Tab import CramerTab
# from tabs.algebra.gauss_Tab import GaussTab
# from tabs.algebra.gauss_jordan_Tab import GaussJordanTab



from tabs.settings_tab import SettingsTab, initialize_fonts
from tabs.reportes_tab import ReportesTab  # Importar la nueva pestaña de Reportes
from components.sidebar import FloatingSidebar

class AlgebraLin(ctk.CTk):
    def __init__(self, parent_menu):
        super().__init__()

        # Guardar referencia al menú principal
        self.parent_menu = parent_menu

        # Configuración de la ventana principal
        self.title("Aplicación de metodos matriciales")
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
        self.inversaDeMatriz_tab = InversaDeMatriz_Tab(self.tabview)
        self.matrix_tab = MatricesTab(self.tabview)
        self.graficador_tab = GraphTab(self.tabview)
        self.resolutorLU = EquationSolver(self.tabview)
        self.gauss = GaussJordanSolver(self.tabview)

        # Vincular el evento de cerrar ventana
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def set_appearance(self):
        """Configura el modo de apariencia y el tema de color."""
        ctk.set_appearance_mode("System")  # Cambia entre 'System', 'Dark' y 'Light'
        ctk.set_default_color_theme("blue")  # Cambia el color de tema si es necesario

    def on_close(self):
        """Regresa al menú principal al cerrar AlgebraLin."""
        self.destroy()
        self.parent_menu.deiconify()
        
if __name__ == "__main__":
    app = AlgebraLin()
    app.mainloop()

