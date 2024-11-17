import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sympy as sp

class MathRendererWidget(tk.Frame):
    def __init__(self, parent, width=600, height=300, **kwargs):
        """
        Widget para renderizar expresiones matemáticas usando matplotlib.
        :param parent: El contenedor padre del widget.
        :param width: Ancho del widget.
        :param height: Alto del widget.
        """
        super().__init__(parent, **kwargs)

        # Configuración inicial
        self.width = width
        self.height = height
        self.figure, self.ax = plt.subplots(figsize=(width / 100, height / 100))
        self.ax.axis("off")  # Ocultamos los ejes

        # Integración con tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def render_math_expression(self, math_expression):
        """
        Renderiza una expresión matemática en LaTeX usando matplotlib.
        :param math_expression: Cadena de texto en formato LaTeX.
        """
        # Limpiar el contenido anterior
        self.ax.clear()
        self.ax.axis("off")

        # Renderizar el texto en el centro
        self.ax.text(
            0.5, 0.5, f"${math_expression}$", fontsize=25, ha="center", va="center", transform=self.ax.transAxes
        )

        # Actualizar el canvas
        self.canvas.draw()

    def update_text(self, math_expression):
        """
        Actualiza el contenido del widget con una nueva expresión matemática.
        :param math_expression: Cadena de texto en formato LaTeX.
        """
        self.render_math_expression(math_expression)

def procesar_formula(funcion_str):
    """
    Convierte una función matemática en formato string a su equivalente en LaTeX.
    
    :param funcion_str: La función matemática en formato string (e.g., "sin(x)/2").
    :return: La representación de la función en LaTeX.
    """
    try:
        # Convertir el string en una expresión de SymPy
        x = sp.symbols('x')  # Definir el símbolo 'x' por defecto
        expresion = sp.sympify(funcion_str)
        
        # Convertir la expresión de SymPy a LaTeX
        funcion_latex = sp.latex(expresion)
        return funcion_latex
    except Exception as e:
        return f""





