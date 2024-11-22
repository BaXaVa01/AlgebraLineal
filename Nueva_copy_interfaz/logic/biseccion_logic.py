# biseccion_logic.py
import math
import re

def procesar_funcion(funcion):
    """
    Convierte la expresión de entrada del usuario a una que `eval` pueda interpretar.
    - Reemplaza `^` por `**` para potencias.
    - Añade el prefijo `math.` a funciones trigonométricas y logarítmicas.
    - Corrige el formato de expresiones como `2sin(x)` a `2*sin(x)`.
    """
    funcion = funcion.replace("^", "**")
    funcion = re.sub(r"(\d+)(?=\b(?:sin|cos|tan|log|sqrt|exp|ln)\b)", r"\1*", funcion)
    
    funciones_permitidas = ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp']
    for fn in funciones_permitidas:
        funcion = funcion.replace(f"{fn}(", f"math.{fn}(")
    
    funcion = funcion.replace("ln(", "math.log(")
    
    return funcion

def biseccion(f, a, b, E=1e-5, max_iter=100):
    """
    Implementa el método de bisección para encontrar la raíz de una función `f`
    en el intervalo `[a, b]` con una tolerancia `E` y un número máximo de iteraciones.
    Retorna:
        - La raíz aproximada `c`.
        - El error relativo.
        - Los pasos de la iteración en formato lista de strings.
        - El número de iteraciones.
    """
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe tener signos opuestos en los extremos del intervalo [a, b].")
    
    iter_count = 0
    c = (a + b) / 2.0
    prev_c = c
    error_relativo = float('inf')
    pasos = []
    
    while (b - a) / 2.0 > E and iter_count < max_iter:
        c = (a + b) / 2.0
        yi = f(a)
        yu = f(b)
        yr = f(c)
        if iter_count > 0:
            error_relativo = abs((c - prev_c))
        pasos.append(f"{iter_count + 1}, {a}, {b}, {c}, {error_relativo}, {yi}, {yu}, {yr}")
        if f(c) == 0:
            return c, 0, pasos, iter_count + 1
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
        prev_c = c
        iter_count += 1
    
    return c, error_relativo, pasos, iter_count
