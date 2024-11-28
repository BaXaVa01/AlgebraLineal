from sympy import symbols, sympify, lambdify
from utils.calc_utils import dominio_funcion, calcular_rango_valido

def secante(funcion_str, x0, x1, tol=1e-6, max_iter=1000):
    """
    Implementa el método de la secante para encontrar raíces de una función,
    manejando automáticamente excepciones comunes y ajustando valores iniciales.

    Args:
        funcion_str (str): La función como cadena.
        x0 (float): Primer valor inicial.
        x1 (float): Segundo valor inicial.
        tol (float): Tolerancia para la convergencia.
        max_iter (int): Número máximo de iteraciones.

    Returns:
        dict: Información sobre la convergencia, raíz y (opcionalmente) iteraciones.
    """
    x = symbols("x")

    if not funcion_str:
        raise ValueError("La función no puede estar vacía.")

    try:
        # Convertir la función en un formato evaluable
        funcion = sympify(funcion_str)
        f = lambdify(x, funcion)

        # Validar dominio de la función
        dominio = dominio_funcion(funcion_str)
        rango_valido = calcular_rango_valido(funcion_str)

        # Ajustar x0 y x1 si están fuera del dominio
        if not (dominio.contains(x0) and dominio.contains(x1)):
            raise ValueError(
                f"Valores iniciales fuera del dominio. Ajuste los valores a dentro de {rango_valido}."
            )

        # Inicializar variables
        iteraciones = []
        error_relativo = None

        for i in range(max_iter):
            try:
                # Evaluar la función en los puntos iniciales
                fx0 = f(x0)
                fx1 = f(x1)

                # Manejar división por cero ajustando valores iniciales
                if fx0 == fx1:
                    ajuste = (rango_valido[1] - rango_valido[0]) * 0.01  # Pequeño ajuste
                    x0 += ajuste
                    x1 -= ajuste
                    fx0 = f(x0)
                    fx1 = f(x1)
                    if fx0 == fx1:
                        raise ValueError(
                            "No se puede continuar: f(x0) = f(x1) incluso después de ajustar los valores iniciales."
                        )

                # Calcular el nuevo valor x2
                x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)

                # Calcular error relativo
                if i > 0:
                    error_relativo = abs((x2 - x1) / x2)

                # Almacenar la iteración
                iteraciones.append({
                    "iteracion": i + 1,
                    "x": float(x2),
                    "f(x)": float(fx1),
                    "error_relativo": float(error_relativo) if error_relativo is not None else None
                })

                # Verificar convergencia
                if abs(x2 - x1) < tol:
                    return {
                        "convergencia": True,
                        "raiz": float(x2),
                        "iteraciones": iteraciones
                    }

                # Actualizar valores para la siguiente iteración
                x0, x1 = x1, x2

            except ZeroDivisionError:
                raise ValueError("División por cero detectada. Intente ajustar los valores iniciales.")
            except Exception as e:
                raise ValueError(f"Error inesperado en la iteración {i + 1}: {e}")

        # Si no converge dentro del número máximo de iteraciones
        return {
            "convergencia": False,
            "mensaje": "No se alcanzó la convergencia en el número máximo de iteraciones.",
            "iteraciones": iteraciones
        }

    except Exception as e:
        raise ValueError(f"Error general en los cálculos: {e}")
