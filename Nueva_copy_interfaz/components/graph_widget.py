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

    def plot_function(self, func, x_view=(-10, 10), x_range=(-100, 100)):
        """Dibuja la función `func` ajustando dinámicamente el rango del eje `y` y limitando la vista inicial."""
        self.func = func

        # Generar valores de x en el rango extendido
        x_values = np.linspace(x_range[0], x_range[1], 10000)
        try:
            y_values = func(x_values)
        except Exception as e:
            messagebox.showerror("Error", f"Error al evaluar la función: {e}")
            return

        # Limpiar y plotear
        self.ax.clear()
        self.ax.plot(x_values, y_values, label="f(x)", color="blue")

        # Configurar la vista inicial
        x_min, x_max = x_view
        x_range = x_max - x_min

        # Ajustar el rango `y` para que sea proporcional a `x`
        y_center = 0  # Puedes calcular el centro dinámicamente si lo prefieres
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_center - x_range / 2, y_center + x_range / 2)

        # Configurar la relación igualada entre ejes
        self.ax.set_aspect("equal", adjustable="datalim")

        # Configurar leyenda y ejes
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.set_title("Gráfica de la función")
        self.ax.legend()

        # Dibujar en el canvas
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
        """Restablece la vista inicial a -10 a 10."""
        if self._initial_x_range and self._initial_y_range:
            self.ax.set_xlim(self._initial_x_range)
            self.ax.set_ylim(self._initial_y_range)
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
        """Grafica múltiples funciones con una escala igual en los ejes."""
        self.ax.clear()
        x_range = (-100, 100)
        x_view = (-10, 10)

        # Determinar límites iniciales para y
        x_min, x_max = x_view
        x_range_width = x_max - x_min
        y_center = 0  # Ajusta según tus necesidades

        # Graficar cada función
        for item in functions:
            func = item.get("func")
            label = item.get("label", "f(x)")
            color = item.get("color", None)

            if func is None:
                continue

            try:
                x_values = np.linspace(x_range[0], x_range[1], 1000)
                y_values = func(x_values)
                self.ax.plot(x_values, y_values, label=label, color=color)
            except Exception as e:
                messagebox.showerror("Error", f"Error al evaluar una de las funciones: {e}")

        # Configurar la vista inicial
        self.ax.set_xlim(*x_view)
        self.ax.set_ylim(y_center - x_range_width / 2, y_center + x_range_width / 2)

        # Configurar la relación igualada entre ejes
        self.ax.set_aspect("equal", adjustable="datalim")

        # Configurar leyenda y ejes
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.set_title("Gráfica de múltiples funciones")
        self.ax.legend()

        self.canvas.draw()



