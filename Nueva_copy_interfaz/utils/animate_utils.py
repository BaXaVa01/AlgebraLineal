from sympy import symbols, sympify, S

def analizar_restricciones(funcion_str):
    """
    Analiza una función y detecta restricciones de dominio basadas en las operaciones.
    Devuelve un rango sugerido para el dominio válido.
    """
    x = symbols("x")
    expr = sympify(funcion_str)
    restricciones = []

    # Detectar sqrt: x >= 0
    if expr.has(S.sqrt(x)):
        restricciones.append(x >= 0)
    
    # Detectar log: x > 0
    if expr.has(S.log(x)):
        restricciones.append(x > 0)

    # Detectar divisiones por x: x != 0
    for denominador in expr.as_numer_denom()[1].free_symbols:
        restricciones.append(x != 0)

    return restricciones
