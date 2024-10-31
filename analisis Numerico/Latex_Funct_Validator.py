import sympy as sp

def crear_funcion(latex_expr):
    """
    Convierte una expresión LaTeX en una función evaluable en Python.
    """
    # Parsear la expresión LaTeX a una expresión simbólica de sympy
    expr = sp.sympify(sp.parsing.latex.parse_latex(latex_expr))
    x = sp.symbols('x')

    # Convertir la expresión en una función lambda para evaluación rápida
    funcion = sp.lambdify(x, expr, 'math')
    return funcion

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
