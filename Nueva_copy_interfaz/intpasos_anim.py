from manim import *
import sympy as sp
from sympy.integrals.manualintegrate import integral_steps
from logic.intsteps import integral_steps_to_latex_wrapper
from sympy import latex
class MostrarPasosIntegracion(Scene):
    def construct(self):
        # Definir la integral simbólica
        x = sp.symbols('x')
        integrand = 1/sp.sqrt(x-2) # Cambia esta función para otros ejemplos

        # Generar los pasos de la integral simbólica
        steps = integral_steps(integrand, x)
        latex_steps = integral_steps_to_latex_wrapper(steps)

        # Mostrar título
        title = Text("Pasos de Integración").scale(0.8).to_edge(UP)
        self.play(Write(title))

        # Mostrar el primer paso
        current_step = MathTex(latex_steps[0]).scale(0.7).next_to(title, DOWN)
        self.play(Write(current_step))
        self.wait(2)

        # Mostrar pasos siguientes
        for step in latex_steps[1:]:
            next_step = MathTex(step).scale(0.7).next_to(title, DOWN)
            self.play(TransformMatchingTex(current_step, next_step, path_arc=90))
            self.wait(2)
            current_step = next_step

        # Resultado final
        final_result = sp.integrate(integrand, x)
        final_text = Text("Resultado Final:").scale(0.8).next_to(current_step, DOWN)
        result_tex = MathTex(latex(final_result)).scale(0.7).next_to(final_text, RIGHT)
        self.play(Write(final_text), Write(result_tex))
        self.wait(3)


if __name__ == "__main__":
    config.media_width = "75%"  # Configuración opcional para ajustar el tamaño del video en la salida.
    command = "manim -pql intpasos_anim.py MostrarPasosIntegracion"
    import os
    os.system(command)