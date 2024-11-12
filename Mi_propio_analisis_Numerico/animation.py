# animation.py
from manim import *
import biseccion_logic
import newton_raphson_logic
import math
import sys
from sympy import sympify, lambdify
import sympy as sp
# Variable global para almacenar la función
# Función para cargar la función desde el archivo temporal
def cargar_funcion_desde_archivo():
    temp_file = sys.argv[-1]  # Obtiene el último argumento, que es el archivo temporal
    with open(temp_file, "r") as file:
        return file.read().strip()

class BiseccionAnimation(Scene):
    def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.funcion_str = cargar_funcion_desde_archivo()  # Cargar la función desde el archivo

    def construct(self):
        funcion_str = self.funcion_str

        # Parámetros de entrada
        a, b, tol, max_iter = -2, 2, 0.01, 20

        # Procesar y preparar la función
        funcion = biseccion_logic.procesar_funcion(funcion_str)
        f = lambda x: eval(funcion, {"x": x, "math": math})

        # Ejecutar el método de Bisección y obtener los pasos
        raiz, error, pasos, iteraciones = biseccion_logic.biseccion(f, a, b, tol, max_iter)

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


class NewtonRaphsonAnimation(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.funcion_str = cargar_funcion_desde_archivo()  # Cargar la función desde el archivo

    def construct(self):
        # Parámetros de entrada
        x0, tol = 1.5, 0.01

        # Convertir la cadena de la función a una expresión simbólica
        x = sp.symbols('x')
        funcion_sympy = sympify(self.funcion_str)  # Crear la función simbólica
        f = lambdify(x, funcion_sympy, modules=["math"])  # Convertir la función a una función evaluable

        # Ejecutar el método de Newton-Raphson y obtener los resultados
        resultado = newton_raphson_logic.newton_raphson(self.funcion_str, x0)

        # Crear ejes y gráfica de la función
        axes = Axes(x_range=[-3, 3, 1], y_range=[-10, 10, 5], axis_config={"color": BLUE})
        graph = axes.plot(lambda x_val: f(x_val), color=YELLOW)
        self.add(axes, graph)

        # Iterar sobre las iteraciones para mostrar los puntos de cada paso
        for iteracion in resultado["iteraciones"]:
            x_val = iteracion['x']
            y_val = f(x_val)

            # Calcular pendiente en el punto x usando derivada simbólica
            derivada = sp.diff(funcion_sympy, x)  # Derivada simbólica
            f_prime = lambdify(x, derivada, modules=["math"])  # Función evaluable de la derivada
            slope = f_prime(x_val)
            y_intercept = y_val - slope * x_val  # Intersección con el eje y

            # Crear la línea tangente manualmente
            x_min, x_max = -3, 3  # Define el rango de la tangente en x
            tangent_start = axes.coords_to_point(x_min, slope * x_min + y_intercept)
            tangent_end = axes.coords_to_point(x_max, slope * x_max + y_intercept)
            tangent_line = Line(tangent_start, tangent_end, color=BLUE)

            # Crear un punto en la gráfica para la posición actual
            point = Dot(axes.coords_to_point(x_val, y_val), color=RED)

            # Animar el punto y la línea tangente y luego eliminarlos
            self.play(FadeIn(point), Create(tangent_line), run_time=0.5)
            self.wait(0.2)
            self.play(FadeOut(tangent_line), FadeOut(point))

        # Mostrar el resultado final
        if resultado["convergencia"]:
            result_text = Text(f"Raíz aproximada: {resultado['raiz']:.5f}").next_to(axes, DOWN)
        else:
            result_text = Text("No se encontró convergencia.").next_to(axes, DOWN)

        self.play(Write(result_text))
        self.wait(1)