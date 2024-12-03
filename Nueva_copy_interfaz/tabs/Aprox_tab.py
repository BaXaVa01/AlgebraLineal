import customtkinter as ctk
from tabs.bisection_tab import BisectionTab
from tabs.newton_tab import NewtonRaphsonTab
from tabs.secante_tab import SecanteTab
from tabs.fakePosition_tab import FakePositionTab


class AproxTab:
    def __init__(self, tabview):
        """Inicializa la pestaña dinámica 'Aproximar'."""
        self.tab = tabview.add("Aproximar")
        self.methods_frame = None  # Frame dinámico para contenido

        # Configurar layout
        self.tab.grid_rowconfigure(1, weight=1)  # Para contenido principal
        self.tab.grid_columnconfigure(0, weight=1)

        # Crear frame superior para el selector de métodos
        self.select_frame = ctk.CTkFrame(self.tab, height=50, fg_color="gray25", corner_radius=8)
        self.select_frame.grid(row=0, column=0, sticky="n", pady=5)
        self.select_frame.grid_propagate(False)

        # Lista desplegable para seleccionar método
        self.method_selector = ctk.CTkOptionMenu(
            self.select_frame,
            values=["Biseccion", "Newton-Raphson", "Secante", "Falsa Posición"],
            command=self.load_method,
        )
        self.method_selector.pack(pady=10)

        # Frame para contenido dinámico
        self.methods_frame = ctk.CTkFrame(self.tab)
        self.methods_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.methods_frame.grid_columnconfigure(0, weight=1)
        self.methods_frame.grid_rowconfigure(0, weight=1)

    def load_method(self, method_name):
        """Carga el método seleccionado y configura su contenido."""
        for widget in self.methods_frame.winfo_children():
            widget.destroy()

        # Crear instancia del método seleccionado
        if method_name == "Biseccion":
            self.current_method = BisectionTab(self.methods_frame)
        elif method_name == "Newton-Raphson":
            self.current_method = NewtonRaphsonTab(self.methods_frame)
        elif method_name == "Secante":
            self.current_method = SecanteTab(self.methods_frame)
        elif method_name == "Falsa Posición":
            self.current_method = FakePositionTab(self.methods_frame)

