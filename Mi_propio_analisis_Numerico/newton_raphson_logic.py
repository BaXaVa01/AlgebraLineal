# newton_raphson_logic.py
import sympy as sp

def newton_raphson(funcion_str, x0, tol=1e-6, max_iter=1000):
    x = sp.symbols('x')
    if not funcion_str:
        raise ValueError("La función no puede estar vacía.")

    try:
        # Convertir la función y calcular la derivada
        funcion = sp.sympify(funcion_str)
        derivada = sp.diff(funcion, x)
        f = sp.lambdify(x, funcion, "math")
        f_prime = sp.lambdify(x, derivada, "math")

        # Almacenar los resultados de cada iteración en una lista de diccionarios
        iteraciones = []

        for i in range(max_iter):
            fx = f(x0)
            fpx = f_prime(x0)
            if fpx == 0:
                raise ValueError("La derivada es cero. No se puede continuar.")

            # Calcular el siguiente valor de x
            x1 = x0 - fx / fpx

            # Añadir resultados de la iteración a la lista
            iteraciones.append({"iteracion": i + 1, "x": x1, "f(x)": fx})

            # Verificar convergencia
            if abs(x1 - x0) < tol:
                return {"convergencia": True, "raiz": x1, "iteraciones": iteraciones}

            x0 = x1

        # Si no converge en el número máximo de iteraciones
        return {"convergencia": False, "iteraciones": iteraciones}

    except Exception as e:
        raise ValueError(f"Error en los cálculos: {e}")
