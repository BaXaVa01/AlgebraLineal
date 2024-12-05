import customtkinter as ctk
from animations.pendulum import SineWaveBackground
from tabs.intro_tab import IntroTab
from tabs.calculator_tab import CalculatorTab
from tabs.graph_tab import GraphTab
from tabs.bisection_tab import BisectionTab
from tabs.newton_tab import NewtonRaphsonTab
from tabs.settings_tab import SettingsTab, initialize_fonts
from tabs.reportes_tab import ReportesTab
from tabs.secante_tab import SecanteTab
from tabs.fakePosition_tab import FakePositionTab
from tabs.Aprox_tab import AproxTab
from AlgebraLin import AlgebraLin
class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Menú Principal - Métodos Numéricos")
        window_width = 800
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(700, 400)

        # Fondo animado
        self.background = SineWaveBackground(self)
        self.background.pack(fill="both", expand=True)

        # Botones superpuestos
        self.calc_button = ctk.CTkButton(
            self,
            text="Calculadora de Matrices",
            font=ctk.CTkFont(size=18),
            command=self.open_matrix_calculator
        )
        self.calc_button.place(relx=0.5, rely=0.4, anchor="center")

        self.analysis_button = ctk.CTkButton(
            self,
            text="Análisis Numérico",
            font=ctk.CTkFont(size=18),
            command=self.open_numerical_analysis
        )
        self.analysis_button.place(relx=0.5, rely=0.6, anchor="center")

        # Crear footer
        self.footer_label = ctk.CTkLabel(
            self,
            text="Creado por BaxavaTeam - 2024",
            font=ctk.CTkFont(size=12),
            text_color="#88C0D0"
        )
        self.footer_label.place(relx=0.5, rely=0.95, anchor="center")

        # Inicializar pestañas
        self.tabview = None

    def open_matrix_calculator(self):
        """Abre una ventana independiente para la Calculadora de Matrices."""
        # Ocultar el menú principal
        self.withdraw()

        # Crear una nueva ventana para la calculadora de matrices
        calculator_window = ctk.CTkToplevel(self)
        calculator_window.title("Calculadora de Matrices")
        calculator_window.geometry("800x600")

        # Instanciar la interfaz de AlgebraLin dentro de la nueva ventana
        algebra_app = AlgebraLin(calculator_window)
        algebra_app.pack(fill="both", expand=True)

        # Manejar cierre de la ventana secundaria y restaurar el menú principal
        calculator_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close_secondary(calculator_window))

    def open_numerical_analysis(self):
        """Abre una ventana independiente para el Análisis Numérico."""
        # Ocultar el menú principal
        self.withdraw()

        # Crear una nueva ventana para el análisis numérico
        analysis_window = ctk.CTkToplevel(self)
        analysis_window.title("Análisis Numérico")
        analysis_window.geometry("800x600")

        # Inicializar TabView dentro de la nueva ventana
        self.initialize_numerical_analysis_in(analysis_window)

        # Manejar cierre de la ventana secundaria y restaurar el menú principal
        analysis_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close_secondary(analysis_window))

    def on_close_secondary(self, window):
        """Maneja el cierre de ventanas secundarias y restaura el menú principal."""
        window.destroy()
        self.deiconify()  # Restaurar el menú principal

    def initialize_numerical_analysis_in(self, parent):
        """Crea la vista de análisis numérico en un contenedor específico."""
        initialize_fonts()

        # Configurar layout adaptable
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Crear TabView principal dentro del contenedor
        tabview = ctk.CTkTabview(parent)
        tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Crear e inicializar pestañas
        IntroTab(tabview)
        CalculatorTab(tabview)
        GraphTab(tabview)
        AproxTab(tabview)
        SettingsTab(tabview)
        ReportesTab(tabview)

        # Botón para cerrar la ventana
        back_button = ctk.CTkButton(
            parent,
            text="Regresar al Menú Principal",
            font=ctk.CTkFont(size=14),
            fg_color="#2E2E2E",
            text_color="#FFFFFF",
            command=lambda: self.on_close_secondary(parent)
        )
        back_button.place(relx=0.05, rely=0.05)




# Ejecutar la aplicación
if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()

