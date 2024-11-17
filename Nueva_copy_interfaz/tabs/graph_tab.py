import customtkinter as ctk
from components.graph_widget import GraphWidget
from tkinter import messagebox
from sympy import sympify, symbols, lambdify

class GraphTab:
    def __init__(self, tabview):
        # Crear la pestaña de graficador
        self.tab = tabview.add("Graficador")

        # Entrada para la función
        self.entry_function = ctk.CTkEntry(self.tab, width=200, font=("Arial", 14))
        self.entry_function.pack(pady=10)

        # Rango de valores de x
        self.entry_x_min = ctk.CTkEntry(self.tab, width=100, placeholder_text="-10")
        self.entry_x_min.pack(side="left", padx=5)
        self.entry_x_max = ctk.CTkEntry(self.tab, width=100, placeholder_text="10")
        self.entry_x_max.pack(side="left", padx=5)

        # Botón para graficar
        self.plot_button = ctk.CTkButton(self.tab, text="Graficar", command=self.plot_graph)
        self.plot_button.pack(pady=10)

        # Instancia del graficador
        self.graph = GraphWidget(self.tab)
        self.graph.pack(fill="both", expand=True, padx=10, pady=10)

    def plot_graph(self):
        """Obtiene la función y los límites de x, luego grafica."""
        # Obtener función y rango de x
        func_str = self.entry_function.get().strip()
        x_min = float(self.entry_x_min.get() or -10)
        x_max = float(self.entry_x_max.get() or 10)

        # Verificar si los valores de x_min y x_max son válidos
        try:
            x_min = int(x_min)  # Convertir a entero si es necesario
            x_max = int(x_max)  # Convertir a entero si es necesario
        except ValueError:
            messagebox.showerror("Error", "Los valores de los límites deben ser números válidos.")
            return

        # Función evaluable para el graficador
        try:
            func = self.safe_eval_function(func_str)
            # Generar la gráfica en el widget
            self.graph.plot_function(func, x_range=(x_min, x_max))
        except Exception as e:
            # Mostrar mensaje de error si la función no es válida
            messagebox.showerror("Error", f"Hubo un error al procesar la función: {e}")

    def safe_eval_function(self, func_str):
        """Convierte la entrada de texto en una función evaluable utilizando sympy y numpy."""
        x = symbols("x")  # Definir x como una variable simbólica

        try:
            # Convertir la cadena de texto en una expresión simbólica
            expr = sympify(func_str)  # Convierte 'sin(x) + cos(x)' en una expresión
            # Crear una función evaluable de numpy a partir de la expresión
            func = lambdify(x, expr, "numpy")
            return func
        except Exception as e:
            raise ValueError(f"Función no válida: {str(e)}")


