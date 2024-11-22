import customtkinter as ctk
from AnalisisNum import AnalisisNum
from animations.pendulum import SineWaveBackground


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
            text="Creado por Davide - 2024",
            font=ctk.CTkFont(size=12),
            text_color="#88C0D0"
        )
        self.footer_label.place(relx=0.5, rely=0.95, anchor="center")

    def open_matrix_calculator(self):
        """Abre la interfaz de Calculadora de Matrices."""
        print("Calculadora de Matrices abierta")

    def open_numerical_analysis(self):
        """Abre la interfaz de Análisis Numérico."""
        self.withdraw()  # Ocultar el menú principal
        app = AnalisisNum(self)  # Pasar referencia al menú principal
        app.mainloop()


# Ejecutar la aplicación
if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
