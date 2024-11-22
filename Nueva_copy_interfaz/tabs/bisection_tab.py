from logic.biseccion_logic import biseccion
from utils.json_utils import guardar_input_operacion, obtener_ultimo_indice
from utils.git_utils import generar_gif_desde_json
from sympy import symbols, sympify, lambdify
from tkinter import messagebox
from components.CustomTab import CustomTab
from components.sidebar import FloatingSidebar
import os
# Definir rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "files", "operaciones.json")

class BisectionTab:
    def __init__(self, tabview):
        # Configurar campos de entrada y columnas de la tabla
        input_fieldsa = ["Función f(x)", "Límite inferior (a)", "Límite superior (b)", "Tolerancia", "Máximo de iteraciones"]
        table_columnsa = ["Iteración", "a", "b", "c", "Error", "f(a)", "f(b)", "f(c)"]

        # Crear una pestaña genérica usando CustomTab
        self.tab = CustomTab(
            tabview=tabview,
            tab_name="Bisección",
            input_fields=input_fieldsa,
            table_columns=table_columnsa,
            execute_callback=self.execute_bisection,
            plot_step_callback=self.plot_step
        )
                # Crear la barra lateral asociada a la pestaña
        self.sidebar = FloatingSidebar(
            self.tab.tab,  # Usar la pestaña creada por CustomTab
            title="Gifs Newton-Raphson",
            from_right=True,
            width=250,
            height=500
        )


    def execute_bisection(self, inputs, tab):
        """Ejecuta el método de Bisección."""
        try:
            # Obtener valores de entrada
            funcion = inputs["Función f(x)"]
            a = float(inputs["Límite inferior (a)"])
            b = float(inputs["Límite superior (b)"])
            tol = float(inputs["Tolerancia"])
            max_iter = int(inputs["Máximo de iteraciones"])

            # Crear función evaluable
            x = symbols("x")
            expr = sympify(funcion)
            f = lambdify(x, expr, "numpy")

            # Ejecutar el método de Bisección
            raiz, error, pasos, iteraciones = biseccion(f, a, b, tol, max_iter)

            # Graficar la función
            tab.graph_widget.plot_function(f, x_range=(a, b))

            # Insertar resultados en la tabla
            data = []
            for paso in pasos:
                iteracion, xi, xu, xr, Ea, yi, yu, yr = paso.split(", ")
                data.append([iteracion, xi, xu, xr, Ea, yi, yu, yr])
            tab.table.insert_data(data)

            # Guardar operación en JSON
            variables = {"a": a, "b": b, "tol": tol, "max_iter": max_iter}
            guardar_input_operacion("biseccion", funcion, variables, raiz)

            # Generar GIF
            indice = obtener_ultimo_indice(JSON_PATH, "biseccion")
            generar_gif_desde_json("biseccion", indice, gif_frame=self.sidebar.scrollable_gif_frame)

        except ValueError as ve:
            tab.table.clear_data()
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            tab.table.clear_data()
            messagebox.showerror("Error", str(e))

    def plot_step(self, step_index, tab):
        """Grafica un paso específico de la tabla."""
        # Obtener datos de la fila seleccionada
        row_data = tab.table.get_row(step_index)
        iteracion, a, b, c, Ea, f_a, f_b, f_c = map(float, row_data)

        # Graficar puntos en la gráfica
        tab.graph_widget.plot_points(
            points=[
                {"x": a, "y": f_a, "color": "blue", "label": f"a (Iter {iteracion})"},
                {"x": b, "y": f_b, "color": "red", "label": f"b (Iter {iteracion})"},
                {"x": c, "y": f_c, "color": "green", "label": f"c (Iter {iteracion})"}
            ]
        )