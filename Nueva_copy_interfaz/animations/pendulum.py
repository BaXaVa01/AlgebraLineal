import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

class SineWaveBackground(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Crear figura y ejes
        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_facecolor("black")
        self.ax.set_facecolor("black")
        self.ax.axis("off")  # Desactivar ejes
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(-2, 2)

        # Configurar la onda
        self.x = np.linspace(0, 10, 300)
        self.line, = self.ax.plot(self.x, np.sin(self.x), color="cyan", lw=1.5)

        self.text = self.ax.text(
            7, 1.5, "", color="white", fontsize=10, ha="center", va="center"
        )

        # Integrar canvas en el widget
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        self.start_time = 0

        # Animación
        self.anim = FuncAnimation(
            self.fig,
            self.update_wave,
            interval=10,  # Controla la rapidez
            blit=True
        )

    def update_wave(self, frame):
        self.start_time += 0.1
        y_data = np.sin(self.x + self.start_time)

        # Actualizar la onda
        self.line.set_ydata(y_data)

        # Actualizar el texto
        matrix_values = [
            [f"{y_data[100]:.2f}", f"{y_data[200]:.2f}"],
            [f"{y_data[150]:.2f}", f"{y_data[250]:.2f}"],
        ]

        matrix_text = (
            f"[{matrix_values[0][0]} {matrix_values[0][1]}]\n"
            f"[{matrix_values[1][0]} {matrix_values[1][1]}]"
        )
        self.text.set_text(matrix_text)
        return self.line, self.text

