# main.py
import customtkinter as ctk

from tabs.ComprobanteMatrix_tab import ComprobanteResultados
from tabs.algebra.inversaDeMatriz_Tab import InversaDeMatriz_Tab
from tabs.matrices_Tab import MatricesTab
from tabs.graph_tab import GraphTab
from tabs.ResolutorMatrix import EquationSolver
from tabs.Gaus_tab import GaussJordanSolver
from tabs.Cramer_tab import MetodoCramer
# from tabs.algebra.cramer_Tab import CramerTab
# from tabs.algebra.gauss_Tab import GaussTab
# from tabs.algebra.gauss_jordan_Tab import GaussJordanTab



from tabs.settings_tab import SettingsTab, initialize_fonts
from tabs.reportes_tab import ReportesTab  # Importar la nueva pestaña de Reportes
from components.sidebar import FloatingSidebar

class AlgebraLin(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Configuración del contenedor
        self.master = master
        self.pack(fill="both", expand=True)

        # Configurar el layout adaptable
        self.grid_rowconfigure(0, weight=1)  # Hacer que el Tabview se expanda verticalmente
        self.grid_columnconfigure(0, weight=1)  # Hacer que el Tabview se expanda horizontalmente

        # Inicializar las fuentes después de crear la raíz
        initialize_fonts()

        # Crear y empaquetar el Tabview principal
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Inicializar las pestañas

        self.graficador_tab = GraphTab(self.tabview)
        self.matrix_tab = MatricesTab(self.tabview)
        self.resolutorLU = EquationSolver(self.tabview)
        self.gauss = GaussJordanSolver(self.tabview)
        self.cramer = MetodoCramer(self.tabview)
        self.comprobante = ComprobanteResultados(self.tabview)

        
    def set_appearance(self):
        """Configura el modo de apariencia y el tema de color."""
        ctk.set_appearance_mode("System")  # Cambia entre 'System', 'Dark' y 'Light'
        ctk.set_default_color_theme("blue")  # Cambia el color de tema si es necesario

    def on_close(self):
        """Regresa al menú principal al cerrar AlgebraLin."""
        self.destroy()
        self.parent_menu.deiconify()  # Muestra el menú principal

        
if __name__ == "__main__":
    app = AlgebraLin()
    app.mainloop()

