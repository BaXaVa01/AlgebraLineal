import sympy as sp

def newton_raphson(funcion_str, x0, tol=1e-6, max_iter=1000):
    """
    Implementa el método de Newton-Raphson para encontrar raíces de una función.

    Args:
        funcion_str (str): La función como cadena.
        x0 (float): Valor inicial.
        tol (float): Tolerancia para la convergencia.
        max_iter (int): Número máximo de iteraciones.

    Returns:
        dict: Información sobre la convergencia y las iteraciones realizadas.

    Raises:
        ValueError: Si la función o derivada no es válida en algún punto.
    """
    # Definir la variable simbólica
    x = sp.symbols('x')
    if not funcion_str:
        raise ValueError("La función no puede estar vacía.")
    
    try:
        # Convertir la función a una expresión simbólica y calcular su derivada
        funcion = sp.sympify(funcion_str)
        derivada = sp.diff(funcion, x)
        
        # Convertir la función y su derivada en funciones evaluables
        f = sp.lambdify(x, funcion, "numpy")
        f_prime = sp.lambdify(x, derivada, "numpy")
        
        # Inicializar lista para almacenar los resultados de cada iteración
        iteraciones = []

        for i in range(max_iter):
            # Verificar si el valor actual está dentro del dominio válido
            if x0 <= 0 and 'log' in funcion_str:
                raise ValueError(f"x no válido en la iteración {i + 1}. Dominio restringido para logaritmos.")

            # Evaluar la función y su derivada
            try:
                fx = f(x0)
                fpx = f_prime(x0)
            except Exception as eval_error:
                raise ValueError(f"Error al evaluar f(x) o f'(x) en x = {x0}: {eval_error}")
            
            print(f"Iteración {i+1}: x0 = {x0}, f(x0) = {fx}, f'(x0) = {fpx}")

            # Verificar si la derivada es cero
            if fpx == 0:
                raise ValueError(f"La derivada es cero en la iteración {i + 1}. No se puede continuar.")
            
            # Calcular el siguiente valor de x
            x1 = x0 - fx / fpx

            # Calcular el error absoluto
            error_absoluto = abs(x1 - x0)
            
            # Añadir el resultado de la iteración
            iteraciones.append({
                "iteracion": i + 1,
                "x": float(x1),
                "f(x)": float(fx),
                "error_absoluto": error_absoluto
            })
            
            # Verificar la convergencia
            if error_absoluto < tol:
                return {
                    "convergencia": True,
                    "raiz": float(x1),
                    "error_absoluto": error_absoluto,
                    "iteraciones": iteraciones
                }
            
            # Actualizar x0 para la siguiente iteración
            x0 = x1

        # Si no se encontró convergencia
        return {"convergencia": False, "iteraciones": iteraciones}

    except Exception as e:
        raise ValueError(f"Error en los cálculos: {e}")
