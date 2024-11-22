# animation.py
from manim import *
from logic.biseccion_logic import *
from logic.newton_raphson_logic import *
import math
import sys
from sympy import sympify, lambdify, symbols, Interval
import json
import sys
from utils.calc_utils import calcular_rango_valido

def cargar_datos_desde_json():
    archivo = sys.argv[-1]

    if archivo.endswith(".json"):
        metodo, indice = sys.argv[-3], int(sys.argv[-2])
        with open(archivo, "r") as file:
            datos = json.load(file)
            # Cargar función y variables desde JSON
            funcion = datos[metodo]["funciones"][indice]["funcion"]
            variables = datos[metodo]["funciones"][indice]["variables"]
            return funcion, variables
    else:
        # Cargar desde un archivo temporal
        with open(archivo, "r") as file:
            return file.read().strip(), {}


class BiseccionAnimation(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.funcion_str, self.variables = cargar_datos_desde_json()  # Cargar datos desde JSON

    def construct(self):
        funcion_str = self.funcion_str
        a, b, tol, max_iter = self.variables["a"], self.variables["b"], self.variables["tol"], self.variables["max_iter"]

        # Procesar y preparar la función
        funcion = procesar_funcion(funcion_str)
        f = lambda x: eval(funcion, {"x": x, "math": math})

        # Ejecutar el método de Bisección y obtener los pasos
        raiz, error, pasos, iteraciones = biseccion(f, a, b, tol, max_iter)

        # Crear ejes y gráfica de la función
        axes = Axes(x_range=[-3, 3, 1], y_range=[-10, 10, 5], axis_config={"color": BLUE})
        graph = axes.plot(lambda x: f(x), color=YELLOW)
        self.add(axes, graph)

        # Iterar sobre los pasos para mostrar los puntos de xi, xu y xr
        for paso in pasos:
            iteracion, xi, xu, xr, Ea, yi, yu, yr = paso.split(", ")
            xi, xu, xr = float(xi), float(xu), float(xr)

            # Crear puntos en la gráfica
            point_xi = Dot(axes.coords_to_point(xi, float(yi)), color=RED)
            point_xu = Dot(axes.coords_to_point(xu, float(yu)), color=GREEN)
            point_xr = Dot(axes.coords_to_point(xr, float(yr)), color=WHITE)

            # Animar los puntos
            self.play(FadeIn(point_xi), FadeIn(point_xu), FadeIn(point_xr), run_time=0.5)
            self.wait(0.5)

        # Mostrar el resultado final
        result_text = Text(f"Raíz aproximada: {raiz:.5f}, Error: {error:.5f}%").next_to(axes, DOWN)
        self.play(Write(result_text))
        self.wait(2)


class NewtonRaphsonAnimation(MovingCameraScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.funcion_str, self.variables = cargar_datos_desde_json()  # Cargar datos desde JSON

    def construct(self):
        time = 0.5
        x0, tol = self.variables["x0"], self.variables["tol"]
        x = symbols("x")
        funcion_sympy = sympify(self.funcion_str)
        f = lambdify(x, funcion_sympy, modules=["numpy"])
        x_range = calcular_rango_valido(self.funcion_str)

        # Ejecutar el método de Newton-Raphson
        resultado = newton_raphson(self.funcion_str, x0, tol)

        # Crear ejes y gráfica de la función
        axes = Axes(
            x_range=x_range,
            y_range=[-10, 10, 5],
            axis_config={"color": BLUE, "include_numbers": True}
        )
        graph = axes.plot(lambda x_val: f(x_val), color=YELLOW)
        self.add(axes, graph)

        zoom_count = 0  # Control del zoom
        previous_x, previous_y = None, None

        # Capturar el estado inicial de la cámara
        self.camera.frame.save_state()

        for iteracion in resultado["iteraciones"]:
            x_val = iteracion["x"]
            y_val = f(x_val)

            # Calcular la pendiente de la tangente en x_val
            derivada = funcion_sympy.diff(x)
            slope = derivada.subs(x, x_val).evalf()

            # Verificar si se necesita hacer zoom cuando los puntos están cerca
            if (
                previous_x is not None 
                and abs(x_val - previous_x) < 1
                and abs(y_val - previous_y) < 1 
                and zoom_count < 3
            ):
                potencia=4
                # Hacer zoom hacia el punto
                self.play(
                    self.camera.frame.animate.move_to(axes.coords_to_point(x_val, y_val)).set(width=potencia),
                    run_time=1
                )
                potencia+=2
                zoom_count += 1
            else:
                # Mover la cámara para seguir el punto sin hacer zoom
                self.play(
                    self.camera.frame.animate.move_to(axes.coords_to_point(x_val, y_val)),
                    run_time=0.5
                )

            # Crear la línea tangente
            x_min, x_max = x_val - 1, x_val + 1
            tangent_start = axes.coords_to_point(x_min, slope * (x_min - x_val) + y_val)
            tangent_end = axes.coords_to_point(x_max, slope * (x_max - x_val) + y_val)
            tangent_line = Line(tangent_start, tangent_end, color=RED)

            # Crear el punto y su etiqueta
            point = Dot(axes.coords_to_point(x_val, y_val), color=RED)
            label = Text(f"x = {x_val:.5f}", font_size=24).next_to(point, UP)

            # Animar la tangente y el punto
            self.play(Create(tangent_line), FadeIn(point), FadeIn(label), run_time=time)
            self.wait(time-0.2)
            self.play(FadeOut(tangent_line), FadeOut(point), FadeOut(label))

            # Actualizar los valores para la próxima iteración
            previous_x, previous_y = x_val, y_val
            x0 = x_val

        # Restaurar la cámara al estado inicial
        self.play(Restore(self.camera.frame))

        # Mostrar el resultado final
        x_final = resultado["iteraciones"][-1]["x"]
        result_text = Text(f"Raíz aproximada: {x_final:.5f}").next_to(axes, DOWN)
        self.play(Write(result_text))
        self.wait(2)




