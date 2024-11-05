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
    
    return float(desplazamiento_x), float(desplazamiento_y)

def definir_intervalo_auto(funcion_str):
    """
    Define un intervalo automático basado en el tipo de función y los desplazamientos.
    """
    x = sp.symbols('x')
    expr = parse_expr(funcion_str)
    
    # Detectar desplazamientos
    desplazamiento_x, desplazamiento_y = detectar_desplazamientos(expr)
    
    # Seleccionar un intervalo basado en el tipo de función
    if expr.has(sp.sin, sp.cos, sp.tan):
        intervalo = (-2 * sp.pi + desplazamiento_x, 2 * sp.pi + desplazamiento_x)
    elif expr.has(sp.log):
        intervalo = (0.1 + desplazamiento_x, 10 + desplazamiento_x)
    elif expr.has(sp.exp):
        intervalo = (-5 + desplazamiento_x, 5 + desplazamiento_x)
    elif expr.is_polynomial():
        intervalo = (-10 + desplazamiento_y, 10 + desplazamiento_y)
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
