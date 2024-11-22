import sympy as sp
from logic.intsteps import integral_steps_to_latex_general  # Importa la función mejorada


# Función para encontrar las intersecciones en x de f(x) y g(x)
def intervx(f, g):
    """
    Encuentra las intersecciones simbólicas entre f(x) y g(x).

    Args:
        f (sympy.Expr): Primera función simbólica.
        g (sympy.Expr): Segunda función simbólica.

    Returns:
        list: Lista de intersecciones reales evaluadas numéricamente.
    """
    x = sp.symbols('x')
    intersections = sp.solve(f - g, x)
    real_intersections = [sol.evalf() for sol in intersections if sol.is_real]
    return real_intersections


# Ajustar el intervalo de integración automáticamente
def ajustar_intervalo(f, g, a=None, b=None):
    """
    Ajusta el intervalo de integración basado en las intersecciones de f(x) y g(x).

    Args:
        f (sympy.Expr): Primera función simbólica.
        g (sympy.Expr): Segunda función simbólica.
        a (float, optional): Límite inferior del intervalo. Si no se proporciona, se calcula automáticamente.
        b (float, optional): Límite superior del intervalo. Si no se proporciona, se calcula automáticamente.

    Returns:
        tuple: Intervalo ajustado (a, b).
    """
    x = sp.symbols('x')
    intersections = intervx(f, g)
    if len(intersections) >= 2:
        a, b = intersections[0], intersections[1]
    elif len(intersections) == 1:
        a = intersections[0]
        b = a + 1  # Ajuste básico si solo hay una raíz
    else:
        raise ValueError("No se encontraron intersecciones en el rango especificado.")

    return float(a), float(b)


# Función para integrar y calcular el volumen, mostrando pasos de integración
def integrate_volume_con_pasos(f, g, a, b):
    """
    Calcula el volumen entre dos funciones rotadas alrededor del eje X, mostrando pasos de integración.

    Args:
        f (sympy.Expr): Primera función simbólica.
        g (sympy.Expr): Segunda función simbólica.
        a (float): Límite inferior del intervalo.
        b (float): Límite superior del intervalo.

    Returns:
        dict: Contiene el resultado de la integral y los pasos en LaTeX.
    """
    x = sp.symbols('x')
    
    # Calcular el integrando de la fórmula de casquillos cilíndricos
    integrand = 2 * sp.pi * x * (f - g)

    # Usar la función mejorada para manejar la integración simbólica y numérica
    result = integral_steps_to_latex_general(integrand, x, a, b)

    return result


# Función para aproximar un valor a una fracción de pi
def aproximar_a_fraccion_pi(valor, precision=1e-3):
    """
    Aproxima un valor numérico a una fracción de pi.

    Args:
        valor (float): Valor numérico.
        precision (float): Precisión de la aproximación.

    Returns:
        sympy.Basic: Aproximación simbólica en términos de pi.
    """
    return sp.nsimplify(valor, tolerance=precision, rational=True)


# Función para formatear el texto del volumen simbólico
def format_volume(volume_symbolic):
    """
    Simplifica y formatea una expresión simbólica del volumen en formato LaTeX.

    Args:
        volume_symbolic (sympy.Expr): Expresión simbólica del volumen.

    Returns:
        str: Representación simplificada en LaTeX.
    """
    return sp.latex(sp.simplify(volume_symbolic))


# Función para formatear el intervalo
def format_interval(a, b):
    """
    Devuelve el intervalo en formato legible.

    Args:
        a (float): Límite inferior.
        b (float): Límite superior.

    Returns:
        str: Representación del intervalo.
    """
    return f"[{a}, {b}]"