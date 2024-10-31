import re
import math

# Diccionario para mapear funciones y operadores LaTeX a Python
latex_a_python = {
    r'\\frac': '/',
    r'\\cdot': '*',
    r'\\left': '',
    r'\\right': '',
    r'\\sin': 'sin',
    r'\\cos': 'cos',
    r'\\tan': 'tan',
    r'\\log': 'log',
    r'\\sqrt': '**(1/2)',  # Raíz cuadrada como potencia
}

def parse_latex_to_python(latex_expr):
    """Convierte una expresión LaTeX en una función evaluable en Python."""
    for latex, python_op in latex_a_python.items():
        latex_expr = re.sub(latex, python_op, latex_expr)
    latex_expr = re.sub(r'(\^)([0-9]+)', r'**\2', latex_expr)
    return latex_expr

def crear_funcion(latex_expr):
    """Convierte la expresión LaTeX y devuelve una función que acepta un valor de x."""
    python_expr = parse_latex_to_python(latex_expr)

    def funcion(x):
        return eval(python_expr, {"x": x, "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log})
    
    return funcion

def identificar_tipo_funcion(latex_expr):
    """Identifica el tipo de función en base a palabras clave en la expresión LaTeX."""
    if re.search(r'\\log', latex_expr):
        return "Logarítmica"
    elif re.search(r'\\exp', latex_expr) or re.search(r'e\^', latex_expr):
        return "Exponencial"
    elif re.search(r'\\sin|\\cos|\\tan', latex_expr):
        return "Trigonométrica"
    elif re.search(r'\\sqrt', latex_expr):
        return "Radical"
    elif re.search(r'x\^\d', latex_expr):
        return "Polinómica"
    else:
        return "Otro tipo o función no clasificada"