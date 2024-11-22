from sympy import symbols, sympify, S, solveset, Interval, Union
from sympy.calculus.util import continuous_domain

def dominio_funcion(funcion_str):
    """
    Calcula el dominio de una función matemática.
    
    Args:
        funcion_str (str): Cadena que representa la función matemática.
        
    Returns:
        sympy.sets.Set: Un conjunto que representa el dominio válido de la función.
    """
    x = symbols("x")
    expr = sympify(funcion_str)

    # Encontrar el dominio continuo de la función
    dominio = continuous_domain(expr, x, S.Reals)

    return dominio

def calcular_rango_valido(funcion_str, x_range=(-10, 10), epsilon=1e-5):
    """
    Calcula el rango válido de la función basándose en su dominio, truncando valores infinitos
    y ajustando límites abiertos a valores cercanos válidos.
    
    Args:
        funcion_str (str): Cadena que representa la función matemática.
        x_range (tuple): Rango inicial por defecto, si no se encuentra un dominio más específico.
        epsilon (float): Ajuste para límites abiertos en el dominio.
    
    Returns:
        list: Un rango ajustado en forma de [mínimo, máximo] dentro del dominio de la función.
    """
    x = symbols("x")
    try:
        # Obtener el dominio de la función
        expr = sympify(funcion_str)
        dominio = continuous_domain(expr, x, S.Reals)

        if isinstance(dominio, Interval):
            # Reemplazar infinitos por los valores del rango predeterminado
            minimo = dominio.inf if dominio.inf != float('-inf') else x_range[0]
            maximo = dominio.sup if dominio.sup != float('inf') else x_range[1]

            # Ajustar límites abiertos
            if dominio.left_open and minimo != float('-inf'):
                minimo += epsilon
            if dominio.right_open and maximo != float('inf'):
                maximo -= epsilon

            return [float(minimo), float(maximo)]

        elif dominio.is_Union:
            # Obtener los extremos mínimo y máximo de los intervalos
            extremos = [subinterval for subinterval in dominio.args if isinstance(subinterval, Interval)]
            if extremos:
                minimo = extremos[0].inf if extremos[0].inf != float('-inf') else x_range[0]
                maximo = extremos[-1].sup if extremos[-1].sup != float('inf') else x_range[1]

                # Ajustar límites abiertos en los extremos
                if extremos[0].left_open and minimo != float('-inf'):
                    minimo += epsilon
                if extremos[-1].right_open and maximo != float('inf'):
                    maximo -= epsilon

                return [float(minimo), float(maximo)]

    except Exception as e:
        print(f"Error al calcular el dominio: {e}")
    
    # Si algo falla, devuelve el rango predeterminado
    return list(x_range)
