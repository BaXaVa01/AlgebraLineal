import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def inicializar_grafico(parent):
    # Crear la figura y el eje para el gráfico
    fig, ax = plt.subplots(figsize=(6, 4))
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return fig, ax, canvas

def actualizar_grafico(ax, canvas, funcion, x_min=-10, x_max=10):
    # Generar valores de x y y con la función proporcionada en el rango especificado
    x_values = [x * 0.1 for x in range(int(x_min * 10), int(x_max * 10) + 1)]
    y_values = [funcion(x) for x in x_values]

    # Limpiar el eje y graficar los nuevos datos
    ax.clear()
    ax.plot(x_values, y_values, color="blue", linewidth=2)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_title("Gráfico de la Función")
    ax.set_xlabel("Eje X")
    ax.set_ylabel("f(x)")
    canvas.draw()  # Redibujar el gráfico

