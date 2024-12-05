import sympy as sp

def validar_entrada(funcion_str, a, b, tol, max_iter):
    """Valida los parámetros de entrada para el método de Falsa Posición."""
    x = sp.symbols('x')

    # Validar que la función sea válida
    try:
        funcion = sp.sympify(funcion_str)
    except (sp.SympifyError, Exception):
        raise ValueError("La función ingresada no es válida.")

    # Validar que a y b sean números reales
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Los extremos a y b deben ser números reales.")

    if not sp.S(a).is_real or not sp.S(b).is_real:
        raise ValueError("Los extremos a y b deben ser números reales.")

    # Validar que el intervalo no sea vacío
    if a == b:
        raise ValueError("Los extremos del intervalo no pueden ser iguales.")

    # Validar que a y b estén dentro del dominio de la función
    dominio = sp.calculus.util.continuous_domain(funcion, x, sp.S.Reals)
    if not dominio.contains(a) or not dominio.contains(b):
        raise ValueError("Los extremos a y b no están en el dominio de la función.")

    # Validar que el intervalo contenga una raíz
    f = sp.lambdify(x, funcion)
    if f(a) * f(b) >= 0:
        raise ValueError("El intervalo no contiene una raíz o la raíz no es única.")

    # Validar que la tolerancia sea positiva
    if not isinstance(tol, (int, float)) or tol <= 0:
        raise ValueError("La tolerancia debe ser un número positivo.")

    # Validar que max_iter sea un entero positivo
    if not isinstance(max_iter, int) or max_iter <= 0:
        raise ValueError("El número máximo de iteraciones debe ser un entero positivo.")

    return funcion, f

def falsa_posicion(funcion_str, a, b, tol=1e-6, max_iter=1000):
    """
    Implementa el método de Falsa Posición.
    """
    # Validar la entrada
    funcion, f = validar_entrada(funcion_str, a, b, tol, max_iter)

    iteraciones = []
    c = None

    for i in range(1, max_iter + 1):
        fa, fb = f(a), f(b)
        if fb - fa == 0:
            raise ValueError(f"División por cero en la iteración {i}.")

        # Calcular c
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)

        # Almacenar resultados de la iteración
        iteraciones.append({"iteracion": i, "a": a, "b": b, "c": c, "f(c)": fc, "error_relativo": abs(b-c)})

        # Verificar convergencia
        if abs(fc) < tol or abs(b - a) < tol:
            return {"convergencia": True, "raiz": c, "iteraciones": iteraciones}

        # Actualizar el intervalo
        if fa * fc < 0:
            b = c
        else:
            a = c

    # Si no converge
    return {"convergencia": False, "raiz": c, "iteraciones": iteraciones}
