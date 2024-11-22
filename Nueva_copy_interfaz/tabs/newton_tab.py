import customtkinter as ctk
from utils.json_utils import guardar_input_operacion, obtener_ultimo_indice
from utils.git_utils import generar_gif_desde_json
from logic.newton_raphson_logic import newton_raphson
from components.graph_widget import GraphWidget
from components.sidebar import FloatingSidebar
from components.CustomTab import CustomTab  # El nuevo módulo creado
from sympy import symbols, sympify, lambdify, diff
from tkinter import messagebox
import os
import numpy as np

# Definir rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "files", "operaciones.json")

class NewtonRaphsonTab:
    def __init__(self, tabview):
        # Crear el graficador y la barra lateral

        # Crear la pestaña personalizada con el módulo CustomTab
        self.custom_tab = CustomTab(
            tabview=tabview,
            tab_name="Newton",
            input_fields=["Función f(x)", "Valor inicial x0", "Tolerancia", "Máx. Iteraciones"],
            table_columns=["Iteración", "x", "f(x)", "f'(x)", "Error"],
            execute_callback=self.ejecutar_newton_raphson,
            plot_step_callback=self.plot_step
        )
        
        # Crear la barra lateral asociada a la pestaña
        self.sidebar = FloatingSidebar(
            self.custom_tab.tab,  # Usar la pestaña creada por CustomTab
            title="Gifs Newton-Raphson",
            from_right=True,
            width=250,
            height=500
        )

        # Inicializar variables específicas para Newton-Raphson
        self.resultado = None
        self.funcion_simb = None
        self.derivada_simb = None
        self.current_step = 0
        self.previous_artists = []
        self.x_sym = symbols("x")

    def ejecutar_newton_raphson(self, inputs, tab):
        """Callback para ejecutar el método de Newton-Raphson."""
        try:
            # Mostrar la barra lateral
            self.sidebar.toggle_sidebar()

            # Obtener valores de entrada
            funcion = inputs["Función f(x)"]
            x0 = float(inputs["Valor inicial x0"])
            tol = float(inputs["Tolerancia"])
            max_iter = int(inputs["Máx. Iteraciones"])

            # Crear función evaluable utilizando sympy y numpy
            expr = sympify(funcion)
            f = lambdify(self.x_sym, expr, "numpy")
            f_prime = lambdify(self.x_sym, expr.diff(self.x_sym), "numpy")

            # Almacenar las funciones simbólicas
            self.funcion_simb = expr
            self.derivada_simb = expr.diff(self.x_sym)

            # Llamar al método de Newton-Raphson
            self.resultado = newton_raphson(funcion, x0, tol, max_iter)

            # Verificar estructura del resultado
            if not isinstance(self.resultado, dict) or "raiz" not in self.resultado or "iteraciones" not in self.resultado:
                raise ValueError("La función 'newton_raphson' no devolvió el formato esperado.")

            raiz = self.resultado["raiz"]
            pasos = self.resultado["iteraciones"]

            # Mostrar resultados en la tabla
            data = []
            for paso in pasos:
                iteracion = paso.get("iteracion", "N/A")
                xi = paso.get("x", "N/A")
                fi = paso.get("f(x)", "N/A")
                f_prime_i = diff(expr, self.x_sym).subs(self.x_sym, xi).evalf()
                error = paso.get("error", "N/A")
                data.append([iteracion, xi, fi, f_prime_i, error])

            tab.table.insert_data(data)

            # Graficar la función
            tab.graph_widget.plot_function(f, x_range=(x0 - 5, x0 + 5))

            # Guardar operación en JSON
            variables = {"x0": x0, "tol": tol, "max_iter": max_iter}
            guardar_input_operacion("newton_raphson", funcion, variables, raiz, str(f_prime))

            # Generar GIF
            indice = obtener_ultimo_indice(JSON_PATH, "newton_raphson")

            def mostrar_gif_en_sidebar(gif_path):
                if gif_path:
                    self.sidebar.show_single_gif(gif_path)
                else:
                    messagebox.showerror("Error", "No se pudo generar el GIF.")

            generar_gif_desde_json(
                "newton_raphson", 
                indice, 
                gif_frame=self.sidebar.scrollable_gif_frame, 
                callback=mostrar_gif_en_sidebar
            )

        except ValueError as ve:
            tab.table.clear_data()
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            tab.table.clear_data()
            messagebox.showerror("Error", str(e))

    def plot_step(self, step_index, tab):
        """Callback para graficar un paso específico."""
        try:
            if not self.resultado:
                raise ValueError("No hay resultados para graficar.")

            # Eliminar artistas previos
            for artist in self.previous_artists:
                artist.remove()
            self.previous_artists.clear()

            # Obtener valores del paso
            x_i = self.resultado["iteraciones"][step_index]["x"]
            f_x = self.funcion_simb.subs(self.x_sym, x_i).evalf()
            f_prime_x = self.derivada_simb.subs(self.x_sym, x_i).evalf()

            # Graficar el punto actual
            point_artist = tab.graph_widget.ax.scatter([x_i], [f_x], color="red", label=f"Iteración {step_index}")

            # Graficar la tangente
            x_range = np.linspace(x_i - 2, x_i + 2, 100)
            tangente = f_prime_x * (x_range - x_i) + f_x
            tangent_line, = tab.graph_widget.ax.plot(x_range, tangente, color="green", linestyle="--", label=f"Tangente {step_index}")

            # Añadir artistas a la lista
            self.previous_artists.extend([point_artist, tangent_line])

            # Actualizar el gráfico
            tab.graph_widget.ax.relim()
            tab.graph_widget.ax.autoscale_view()
            tab.graph_widget.ax.legend()
            tab.graph_widget.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))