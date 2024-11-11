import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

def detectar_desplazamientos(expr):
    """
    Detecta desplazamientos en los ejes x e y de una expresión.
    """
    x = sp.symbols('x')
    
    # Inicializar desplazamientos
    desplazamiento_x = 0
    desplazamiento_y = 0

    # Detectar desplazamiento en y (parte constante en la expresión)
    expr_sin_constante, constante_y = expr.as_independent(x, as_Add=True)
    desplazamiento_y = constante_y.evalf() if constante_y else 0

    # Detectar desplazamiento en x: buscar términos (x - h)
    if expr.has(x):
        for arg in expr.args:
            if arg.has(x):
                if arg.is_Add or arg.is_Mul:
                    desplazamiento_x = -arg.as_independent(x, as_Add=True)[1]

    # Asegurarse de que ambos desplazamientos sean numéricos
    return float(N(desplazamiento_x)), float(N(desplazamiento_y))

from sympy import N  # N convierte expresiones a numéricos cuando es posible

def definir_intervalo_auto(funcion_str):
    x = sp.symbols('x')
    expr = parse_expr(funcion_str)
    
    # Detectar desplazamientos
    desplazamiento_x, desplazamiento_y = detectar_desplazamientos(expr)
    
    # Seleccionar un intervalo basado en el tipo de función y convertir desplazamientos a float cuando sea posible
    if expr.has(sp.sin, sp.cos, sp.tan):
        intervalo = (float(N(-2 * sp.pi + desplazamiento_x)), float(N(2 * sp.pi + desplazamiento_x)))
    elif expr.has(sp.log):
        intervalo = (float(N(0.1 + desplazamiento_x)), float(N(10 + desplazamiento_x)))
    elif expr.has(sp.exp):
        intervalo = (float(N(-5 + desplazamiento_x)), float(N(5 + desplazamiento_x)))
    elif expr.is_polynomial():
        intervalo = (float(N(-10 + desplazamiento_y)), float(N(10 + desplazamiento_y)))
    else:
        intervalo = (-10, 10)
    
    # Buscar un intervalo con cambio de signo
    f = sp.lambdify(x, expr, 'math')
    a, b = intervalo
    for _ in range(5):
        if f(a) * f(b) < 0:
            return a, b
        a -= 1
        b += 1

    raise ValueError("No se encontró un intervalo inicial con cambio de signo.")
