import customtkinter as ctk
from utils.json_utils import guardar_input_operacion, obtener_ultimo_indice
from utils.git_utils import generar_gif_desde_json
from logic.secante_logic import secante  # Asegúrate de tener esta lógica implementada
from components.graph_widget import GraphWidget
from components.sidebar import FloatingSidebar
from components.CustomTab import CustomTab  # El nuevo módulo creado
from sympy import symbols, sympify, lambdify
from tkinter import messagebox
import os

# Definir rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "files", "operaciones.json")

class SecanteTab:
    def __init__(self, tabview):
        # Crear la pestaña personalizada con el módulo CustomTab
        self.custom_tab = CustomTab(
            tabview=tabview,
            tab_name="Secante",
            input_fields=["Función f(x)", "Valor inicial x0", "Valor inicial x1", "Tolerancia", "Máx. Iteraciones"],
            table_columns=["Iteración", "x", "f(x)", "Error relativo"],
            execute_callback=self.ejecutar_secante,
            plot_step_callback=self.plot_step
        )

        # Crear la barra lateral asociada a la pestaña
        self.sidebar = FloatingSidebar(
            self.custom_tab.tab,  # Usar la pestaña creada por CustomTab
            title="Gifs Secante",
            from_right=True,
            width=250,
            height=500
        )

        # Inicializar variables específicas para Secante
        self.resultado = None
        self.funcion_simb = None
        self.x_sym = symbols("x")
        self.previous_artists = []  # Lista para almacenar los elementos gráficos anteriores

    def ejecutar_secante(self, inputs, tab):
        """Callback para ejecutar el método de la Secante."""
        try:
            # Mostrar la barra lateral
            self.sidebar.toggle_sidebar()

            # Obtener valores de entrada
            funcion = inputs["Función f(x)"]
            x0 = float(inputs["Valor inicial x0"])
            x1 = float(inputs["Valor inicial x1"])
            tol = float(inputs["Tolerancia"])
            max_iter = int(inputs["Máx. Iteraciones"])

            # Crear función evaluable utilizando sympy
            expr = sympify(funcion)
            f = lambdify(self.x_sym, expr)

            # Almacenar la función simbólica
            self.funcion_simb = expr

            # Llamar al método Secante
            self.resultado = secante(funcion, x0, x1, tol, max_iter)

            # Verificar estructura del resultado
            if not isinstance(self.resultado, dict) or "raiz" not in self.resultado or "iteraciones" not in self.resultado:
                raise ValueError("La función 'secante' no devolvió el formato esperado.")

            raiz = self.resultado["raiz"]
            pasos = self.resultado["iteraciones"]

            # Mostrar resultados en la tabla
            data = []
            for paso in pasos:
                iteracion = paso.get("iteracion", "N/A")
                xi = paso.get("x", "N/A")
                fi = paso.get("f(x)", "N/A")
                error_relativo = paso.get("error_relativo", "N/A")
                data.append([iteracion, xi, fi, error_relativo])

            tab.table.insert_data(data)

            # Graficar la función
            tab.graph_widget.plot_function(f, x_range=(min(x0, x1) - 5, max(x0, x1) + 5))

            # Guardar operación en JSON
            variables = {"x0": x0, "x1": x1, "tol": tol, "max_iter": max_iter}
            guardar_input_operacion("secante", funcion, variables, raiz)

            # Generar GIF
            indice = obtener_ultimo_indice(JSON_PATH, "secante")

            def mostrar_gif_en_sidebar(gif_path):
                if gif_path:
                    self.sidebar.show_single_gif(gif_path)
                else:
                    messagebox.showerror("Error", "No se pudo generar el GIF.")

            generar_gif_desde_json(
                "secante", 
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

            # Obtener valores del paso actual
            iteracion_actual = self.resultado["iteraciones"][step_index]
            x0 = self.resultado["iteraciones"][step_index - 1]["x"] if step_index > 0 else None
            x1 = iteracion_actual["x"]

            # Calcular f(x) para los puntos actuales
            f_x1 = self.funcion_simb.subs(self.x_sym, x1).evalf()
            if x0 is not None:
                f_x0 = self.funcion_simb.subs(self.x_sym, x0).evalf()

                # Graficar la secante
                x_secante = [x0, x1]
                y_secante = [f_x0, f_x1]
                secante_line, = tab.graph_widget.ax.plot(
                    x_secante, y_secante, color="green", linestyle="--", linewidth=2, alpha=0.7, label=f"Secante {step_index}"
                )
                self.previous_artists.append(secante_line)

                # Graficar el punto x0
                point_x0 = tab.graph_widget.ax.scatter([x0], [f_x0], color="blue", label=f"Punto x0 ({step_index})")
                self.previous_artists.append(point_x0)

            # Graficar el punto x1
            point_x1 = tab.graph_widget.ax.scatter([x1], [f_x1], color="red", label=f"Punto x1 ({step_index})")
            self.previous_artists.append(point_x1)

            # Actualizar el gráfico
            tab.graph_widget.ax.relim()
            tab.graph_widget.ax.autoscale_view()
            tab.graph_widget.ax.legend()
            tab.graph_widget.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))
