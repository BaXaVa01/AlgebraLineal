import sympy as sp

def newton_raphson(funcion_str, x0, tol=1e-6, max_iter=1000):
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
            # Depuración: Verificar valores de f y f_prime en x0
            fx = f(x0)
            fpx = f_prime(x0)
            print(f"Iteración {i+1}: x0 = {x0}, f(x0) = {fx}, f'(x0) = {fpx}")

            # Verificar si la derivada es cero
            if fpx == 0:
                raise ValueError(f"La derivada es cero en la iteración {i + 1}. No se puede continuar.")
            
            # Calcular el siguiente valor de x
            x1 = x0 - fx / fpx
            
            # Añadir el resultado de la iteración
            iteraciones.append({"iteracion": i + 1, "x": float(x1), "f(x)": float(fx)})
            
            # Verificar la convergencia
            if abs(x1 - x0) < tol:
                return {"convergencia": True, "raiz": float(x1), "iteraciones": iteraciones}
            
            # Actualizar x0 para la siguiente iteración
            x0 = x1

        # Si no se encontró convergencia
        return {"convergencia": False, "iteraciones": iteraciones}

    except Exception as e:
        raise ValueError(f"Error en los cálculos: {e}")