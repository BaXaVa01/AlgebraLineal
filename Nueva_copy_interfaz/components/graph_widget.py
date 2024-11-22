# components/graph_widget.py
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox

class GraphWidget(ctk.CTkFrame):
    def __init__(self, master, width=500, height=400, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.pack_propagate(False)
        self.previous_points = []  # Almacena referencias a puntos previos


        # Inicializar la figura de Matplotlib
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Añadir toolbar interactiva para zoom y desplazamiento
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        toolbar.pack(side="bottom", fill="x")

        # Variable para almacenar la función a graficar
        self.func = None

    def plot_function(self, func, x_range=(-10, 10)):
        """Dibuja la función `func` en un rango amplio de -100 a 100, pero establece el rango visible en `x_range`."""
        self.func = func
        self._initial_x_range = x_range

        # Plotea en un rango extendido y ajusta la vista a `x_range`
        self.update_plot_function(-100, 100)
        self.ax.set_xlim(*x_range)
        
        # Ajustar el eje y a la misma escala que x
        y_min, y_max = self.ax.get_ylim()
        x_min, x_max = x_range
        range_span = max(abs(x_min), abs(x_max))  # Usar el mismo rango en ambos ejes
        self.ax.set_ylim(-range_span, range_span)

        self.canvas.draw()

    def update_plot_function(self, x_min, x_max):
        """Actualiza el gráfico de la función en un rango extendido."""
        if self.func is None:
            return

        # Genera un rango extendido para visualizar en desplazamientos
        x_values = np.linspace(x_min, x_max, 1000)

        try:
            y_values = self.func(x_values)
        except Exception as e:
            messagebox.showerror("Error", f"Error al evaluar la función: {e}")
            return

        # Limpiar gráficos previos y dibujar nuevo
        self.ax.clear()
        self.ax.plot(x_values, y_values, label="f(x)", color="blue")
        self.ax.axhline(0, color="black", linewidth=1)  # Eje x
        self.ax.axvline(0, color="black", linewidth=1)  # Eje y
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.set_title("Gráfica de la función")
        self.ax.legend()

        # Actualizar el canvas
        self.canvas.draw()
    def plot_points(self, points):
        """
        Grafica puntos individuales en el eje actual.
        Args:
            points (list): Lista de diccionarios con las claves:
                        - 'x': Coordenada x del punto.
                        - 'y': Coordenada y del punto.
                        - 'color': Color del punto.
                        - 'label': Etiqueta del punto (opcional).
        """
        # Limpiar puntos previos si existen
        if hasattr(self, "previous_points") and self.previous_points:
            for artist in self.previous_points:
                artist.remove()
            self.previous_points.clear()

        # Almacenar puntos actuales
        self.previous_points = []

        for point in points:
            scatter = self.ax.scatter(point["x"], point["y"], color=point["color"], label=point.get("label", ""))
            self.previous_points.append(scatter)

        # Actualizar la leyenda para incluir nuevos puntos
        self.ax.legend()
        self.canvas.draw()


    def clear_plot(self):
        """Limpia el gráfico."""
        self.ax.clear()
        self.canvas.draw()

