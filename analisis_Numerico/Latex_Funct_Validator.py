import sympy as sp
from sympy import sympify,latex
def crear_funcion(expr_text):
    """
    Convierte una cadena de texto (como 'x-2') en una función evaluable en Python.
    """
    x = sp.symbols('x')
    expr = sp.sympify(expr_text)  # Convierte el texto en una expresión simbólica
    return sp.lambdify(x, expr, 'math')  # Devuelve una función evaluable en Python

def identificar_tipo_funcion(latex_expr):
    """
    Identifica el tipo de función en base a la estructura de la expresión.
    """
    expr = sp.sympify(sp.parsing.latex.parse_latex(latex_expr))

    # Clasificar el tipo de función basado en operadores presentes en expr
    if expr.has(sp.log):
        return "Logarítmica"
    elif expr.has(sp.exp) or expr.has(sp.E):
        return "Exponencial"
    elif expr.has(sp.sin) or expr.has(sp.cos) or expr.has(sp.tan):
        return "Trigonométrica"
    elif expr.has(sp.sqrt):
        return "Radical"
    elif expr.is_polynomial():
        return "Polinómica"
    else:
        return "Otro tipo o función no clasificada"


def convertir_a_latex_sympy(expresion):
    try:
        # Convierte la expresión de cadena en una expresión simbólica
        expr_simp = sympify(expresion)
        # Convierte la expresión simbólica a LaTeX
        return f"${latex(expr_simp)}$"
    except Exception as e:
        print(f"Error en la conversión a LaTeX: {e}")
        return None

