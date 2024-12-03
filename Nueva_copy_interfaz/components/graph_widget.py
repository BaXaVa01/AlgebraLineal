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
        self._initial_xlim = None
        self._initial_ylim = None

        # Inicializar la figura de Matplotlib
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Añadir toolbar interactiva para zoom y desplazamiento
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.toolbar.pack(side="bottom", fill="x")

        # Sobrescribir el comportamiento del botón "home"
        self.toolbar.home = self.reset_zoom

        # Variable para almacenar la función a graficar
        self.func = None

        # Conectar evento de zoom
        self.canvas.mpl_connect("scroll_event", self._zoom)

    def plot_function(self, func, x_range=(-10, 10)):
        """Dibuja la función `func` en un rango amplio de -100 a 100, pero establece el rango visible en `x_range`."""
        self.func = func
        self._initial_x_range = x_range

        # Plotea en un rango extendido y ajusta la vista a `x_range`
        self.update_plot_function(-100, 100)
        self.ax.set_xlim(*x_range)

        # Ajustar el eje y a la misma escala que x
        range_span = max(abs(x_range[0]), abs(x_range[1]))
        self.ax.set_ylim(-range_span, range_span)

        # Guardar los límites iniciales para restablecer zoom
        self._initial_xlim = self.ax.get_xlim()
        self._initial_ylim = self.ax.get_ylim()

        self.canvas.draw()

    def update_plot_function(self, x_min, x_max):
        """Actualiza el gráfico de la función en un rango extendido."""
        if self.func is None:
            return

        x_values = np.linspace(x_min, x_max, 10000)

        try:
            y_values = self.func(x_values)
        except Exception as e:
            messagebox.showerror("Error", f"Error al evaluar la función: {e}")
            return

        # Limpiar gráficos previos y dibujar nuevo
        self.ax.clear()
        self.ax.plot(x_values, y_values, label="f(x)", color="blue")
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.set_title("Gráfica de la función")
        self.ax.legend()

        self.canvas.draw()

    def _zoom(self, event):
        """Controla el zoom con la rueda del mouse."""
        base_scale = 1.2
        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()

        xdata = event.xdata
        ydata = event.ydata

        if xdata is None or ydata is None:
            return

        if event.button == "up":  # Zoom in
            scale_factor = 1 / base_scale
        elif event.button == "down":  # Zoom out
            scale_factor = base_scale
        else:
            return

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

        self.ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
        self.ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
        self.canvas.draw()

    def reset_zoom(self):
        """Restablece el zoom al estado inicial."""
        if self._initial_xlim and self._initial_ylim:
            self.ax.set_xlim(self._initial_xlim)
            self.ax.set_ylim(self._initial_ylim)
            self.canvas.draw()

    def plot_points(self, points):
        """Grafica puntos individuales en el eje actual."""
        if hasattr(self, "previous_points") and self.previous_points:
            for artist in self.previous_points:
                artist.remove()
            self.previous_points.clear()

        self.previous_points = []

        for point in points:
            scatter = self.ax.scatter(point["x"], point["y"], color=point["color"], label=point.get("label", ""))
            self.previous_points.append(scatter)

        self.ax.legend()
        self.canvas.draw()

    def clear_plot(self):
        """Limpia el gráfico."""
        self.ax.clear()
        self.canvas.draw()

    def plot_multiple_functions(self, functions):
        """
        Grafica múltiples funciones en el mismo gráfico utilizando `plot_function`.
        
        Input:
        - functions (list): Una lista de diccionarios. Cada diccionario debe tener los siguientes campos:
        
          - 'func' (callable, obligatorio): La función matemática que se desea graficar.
            Ejemplo: lambda x: x**2 o numpy.sin.
        
          - 'x_range' (tuple, opcional): Una tupla que define el rango visible del eje x (x_min, x_max).
            Si no se especifica, se utiliza el rango predeterminado (-10, 10).
            Ejemplo: (-20, 20)
        
          - 'label' (str, opcional): Una etiqueta para identificar la función en la leyenda.
            Si no se especifica, se utiliza "f(x)" como etiqueta predeterminada.
            Ejemplo: "sin(x)"
        
          - 'color' (str, opcional): El color de la línea del gráfico. Puede ser cualquier color válido en Matplotlib.
            Si no se especifica, Matplotlib asigna un color automáticamente.
            Ejemplo: "blue", "#FF5733", "r"
        
        Ejemplo de uso:
            functions_to_plot = [
                {"func": np.sin, "x_range": (-10, 10), "label": "sin(x)", "color": "blue"},
                {"func": np.cos, "label": "cos(x)", "color": "green"},
                {"func": lambda x: x**2 - 5, "x_range": (-5, 5), "label": "x^2 - 5", "color": "red"}
            ]
            graph_widget.plot_multiple_functions(functions_to_plot)
        """
        self.ax.clear()  # Limpia cualquier gráfico previo

        for item in functions:
            func = item.get("func")
            x_range = item.get("x_range", (-10, 10))  # Rango predeterminado si no se especifica
            label = item.get("label", "f(x)")
            color = item.get("color", None)

            if func is None:
                continue

            try:
                # Genera valores x e y para graficar la función
                x_values = np.linspace(-100, 100, 10000)  # Rango extendido
                y_values = func(x_values)
                
                # Dibuja la función
                self.ax.plot(x_values, y_values, label=label, color=color)
                
                # Ajusta los límites del gráfico para la función actual si se especifica un rango
                if x_range:
                    self.ax.set_xlim(*x_range)

            except Exception as e:
                messagebox.showerror("Error", f"Error al evaluar una de las funciones: {e}")

        # Dibujar ejes comunes
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)

        # Etiquetas y leyenda
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.set_title("Gráfica de múltiples funciones")
        self.ax.legend()

        # Redibuja el canvas
        self.canvas.draw()
