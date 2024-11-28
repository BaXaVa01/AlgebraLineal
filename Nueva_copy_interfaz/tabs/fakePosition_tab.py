import customtkinter as ctk
from utils.json_utils import guardar_input_operacion, obtener_ultimo_indice
from logic.fakePosition_logic import falsa_posicion
from components.graph_widget import GraphWidget
from components.sidebar import FloatingSidebar
from components.CustomTab import CustomTab
from sympy import symbols, sympify, lambdify
from tkinter import messagebox

class FakePositionTab:
    def __init__(self, parent):
        # Crear la pestaña personalizada con el módulo CustomTab
        self.custom_tab = CustomTab(
            tabview=parent,
            tab_name="Falsa Posición",
            input_fields=["Función f(x)", "Extremo a", "Extremo b", "Tolerancia", "Máx. Iteraciones"],
            table_columns=["Iteración", "a", "b", "c", "f(c)", "Error absoluto"],
            execute_callback=self.ejecutar_falsa_posicion,
            plot_step_callback=self.plot_step
        )

        # Crear la barra lateral asociada a la pestaña
        self.sidebar = FloatingSidebar(
            self.custom_tab.tab,  # Usar la pestaña creada por CustomTab
            title="Gifs Falsa Posición",
            from_right=True,
            width=250,
            height=500
        )

        # Inicializar variables específicas para Falsa Posición
        self.resultado = None
        self.funcion_simb = None
        self.x_sym = symbols("x")
        self.previous_artists = []  # Lista para almacenar los elementos gráficos previos

    def ejecutar_falsa_posicion(self, inputs, tab):
        """Callback para ejecutar el método de Falsa Posición."""
        try:
            # Mostrar la barra lateral
            self.sidebar.toggle_sidebar()

            # Obtener valores de entrada
            funcion = inputs["Función f(x)"]
            a = float(inputs["Extremo a"])
            b = float(inputs["Extremo b"])
            tol = float(inputs["Tolerancia"])
            max_iter = int(inputs["Máx. Iteraciones"])

            # Crear función evaluable utilizando sympy
            expr = sympify(funcion)
            f = lambdify(self.x_sym, expr)

            # Almacenar la función simbólica
            self.funcion_simb = expr

            # Llamar al método de Falsa Posición
            self.resultado = falsa_posicion(funcion, a, b, tol, max_iter)

            # Verificar estructura del resultado
            if not isinstance(self.resultado, dict) or "raiz" not in self.resultado or "iteraciones" not in self.resultado:
                raise ValueError("La función 'falsa_posicion' no devolvió el formato esperado.")

            raiz = self.resultado["raiz"]
            pasos = self.resultado["iteraciones"]

            # Mostrar resultados en la tabla
            data = []
            for paso in pasos:
                iteracion = paso["iteracion"]
                a_i = paso["a"]
                b_i = paso["b"]
                c_i = paso["c"]
                fc_i = paso["f(c)"]
                error_relativo = paso["error_relativo"]
                data.append([iteracion, a_i, b_i, c_i, fc_i, error_relativo])

            tab.table.insert_data(data)

            # Graficar la función
            tab.graph_widget.plot_function(f, x_range=(min(a, b) - 2, max(a, b) + 2))

            # Guardar operación en JSON
            variables = {"a": a, "b": b, "tol": tol, "max_iter": max_iter}
            guardar_input_operacion("falsa_posicion", funcion, variables, raiz)

        except ValueError as ve:
            tab.table.clear_data()
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            tab.table.clear_data()
            messagebox.showerror("Error", str(e))

    def plot_step(self, step_index, tab):
        """Callback para graficar un paso específico del método."""
        try:
            if not self.resultado:
                raise ValueError("No hay resultados para graficar.")

            # Limpiar elementos gráficos previos
            for artist in self.previous_artists:
                artist.remove()
            self.previous_artists.clear()

            # Obtener valores del paso actual
            iteracion_actual = self.resultado["iteraciones"][step_index]
            a_i = iteracion_actual["a"]
            b_i = iteracion_actual["b"]
            c_i = iteracion_actual["c"]
            f_a_i = self.funcion_simb.subs(self.x_sym, a_i).evalf()
            f_b_i = self.funcion_simb.subs(self.x_sym, b_i).evalf()
            f_c_i = self.funcion_simb.subs(self.x_sym, c_i).evalf()

            # Graficar el intervalo actual
            intervalo, = tab.graph_widget.ax.plot(
                [a_i, b_i],
                [f_a_i, f_b_i],
                color="blue",
                linestyle="--",
                linewidth=2,
                label=f"Intervalo [{a_i:.3f}, {b_i:.3f}]"
            )
            self.previous_artists.append(intervalo)

            # Graficar el punto c_i
            punto_c = tab.graph_widget.ax.scatter(
                [c_i],
                [f_c_i],
                color="red",
                s=80,  # Tamaño del marcador
                label=f"Punto c: ({c_i:.3f}, {f_c_i:.3f})"
            )
            self.previous_artists.append(punto_c)

            # Agregar líneas verticales para a, b y c
            linea_a = tab.graph_widget.ax.axvline(
                x=a_i, color="purple", linestyle=":", alpha=0.8, label=f"a = {a_i:.3f}"
            )
            linea_b = tab.graph_widget.ax.axvline(
                x=b_i, color="orange", linestyle=":", alpha=0.8, label=f"b = {b_i:.3f}"
            )
            linea_c = tab.graph_widget.ax.axvline(
                x=c_i, color="red", linestyle="-.", alpha=0.8, label=f"c = {c_i:.3f}"
            )
            self.previous_artists.extend([linea_a, linea_b, linea_c])

            # Actualizar el gráfico
            tab.graph_widget.ax.relim()
            tab.graph_widget.ax.autoscale_view()
            tab.graph_widget.ax.legend(loc="upper right", fontsize=8)  # Colocar leyenda en la esquina superior derecha
            tab.graph_widget.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))

