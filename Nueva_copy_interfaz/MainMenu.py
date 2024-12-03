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
        """Abre la interfaz de Calculadora de Matrices."""
        self.background.pack_forget()
        self.calc_button.place_forget()
        self.analysis_button.place_forget()
        self.footer_label.place_forget()
        # Inicializar vista de análisis numérico si no existe
        if not self.tabview:
            self.initialize_matrix_interface()
    def open_numerical_analysis(self):
        """Abre la interfaz de Análisis Numérico."""
        # Ocultar elementos del menú principal
        self.background.pack_forget()
        self.calc_button.place_forget()
        self.analysis_button.place_forget()
        self.footer_label.place_forget()

        # Inicializar vista de análisis numérico si no existe
        if not self.tabview:
            self.initialize_numerical_analysis()


    def initialize_numerical_analysis(self):
        """Crea la vista de análisis numérico dentro del menú principal."""
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
        self.aprox_tab = AproxTab(self.tabview)
        self.settings_tab = SettingsTab(self.tabview)
        self.reportes_tab = ReportesTab(self.tabview)

        self.back_button = ctk.CTkButton(
                self,
                text="  Regresar al Menú Principal",  # Espaciado para separar el texto del borde
                font=ctk.CTkFont(size=14),  # Tamaño de texto más pequeño
                fg_color="#2E2E2E",  # Color de fondo
                text_color="#FFFFFF",  # Color del texto
                width=200,  # Ancho del botón
                height=30,  # Altura del botón
                anchor="w",  # Alinear texto a la izquierda
                command=self.return_to_main_menu  # Nuevo método
            )
        self.back_button.place(relx=0, rely=0, x=10, y=10, anchor="nw")  # Posiciona en la esquina superior izquierda

    def initialize_matrix_interface(self):
        """Abre AlgebraLin y oculta el menú principal."""
        self.withdraw()  # Oculta el menú principal
        algebra_app = AlgebraLin(self)  # Pasa referencia al menú principal
        algebra_app.mainloop()
    


    def return_to_main_menu(self):
        """Regresa al menú principal."""
        if self.tabview:  # Asegura que las pestañas existan
            self.tabview.destroy()
            self.tabview = None  # Restablece el TabView
        if hasattr(self, "back_button"):
            self.back_button.destroy()

        # Restaurar elementos iniciales del menú principal
        self.background.pack(fill="both", expand=True)
        self.calc_button.place(relx=0.5, rely=0.4, anchor="center")
        self.analysis_button.place(relx=0.5, rely=0.6, anchor="center")
        self.footer_label.place(relx=0.5, rely=0.95, anchor="center")



# Ejecutar la aplicación
if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()

