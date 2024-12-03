import customtkinter as ctk
from components.graph_widget import GraphWidget
from components.upgrade.desmosui import FunctionManager
from tkinter import messagebox
from sympy import symbols, sympify, lambdify


class GraphTab:
    def __init__(self, tabview):
        # Crear la pestaña de graficador
        self.tab = tabview.add("Graficador")

        # Contenedor principal
        self.main_frame = ctk.CTkFrame(self.tab)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame superior para el gestor de funciones
        self.function_manager_frame = ctk.CTkFrame(self.main_frame)
        self.function_manager_frame.pack(fill="x", pady=5)

        # Instancia del graficador
        self.graph_frame = ctk.CTkFrame(self.main_frame)
        self.graph_frame.pack(fill="both", expand=True, pady=10)

        self.graph = GraphWidget(self.graph_frame)
        self.graph.pack(fill="both", expand=True, padx=10, pady=10)

        # Instancia del gestor de funciones
        self.function_manager = FunctionManager(self.function_manager_frame, self.graph)
        self.function_manager.pack(fill="x", expand=True)

        # Botón para limpiar el gráfico
        self.clear_button = ctk.CTkButton(
            self.main_frame,
            text="Limpiar Todo",
            fg_color="#F44336",
            hover_color="#E53935",
            command=self.clear_all
        )
        self.clear_button.pack(fill="x", pady=5)

    def clear_all(self):
        """Limpia el gráfico y el gestor de funciones, dejando solo una fila vacía."""
        # Limpia el gráfico
        self.graph.clear_plot()

        # Limpia la tabla de funciones y asegura una fila vacía
        self.function_manager.clear_data()
        self.function_manager.ensure_empty_row()  # Garantiza que haya una fila vacía

