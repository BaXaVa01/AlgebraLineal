import re
# Función para validar que una matriz no esté vacía y que todas las filas tengan el mismo número de columnas
def validar_matriz(matriz):
    if not matriz:
        return False
    if matriz == None:
        return False
    num_columnas = len(matriz[0])
    for fila in matriz:
        if len(fila) != num_columnas:
            return False
    return True
    

# Función para validar la entrada de texto, verificando si puede ser convertida a una matriz válida
from fractions import Fraction

def convertir_fraccion_a_decimal(texto):
    try:
        if '/' in texto:
            return float(Fraction(texto))  # Convierte la fracción a decimal
        else:
            return float(texto)  # Si no es fracción, lo convierte a float directamente
    except ValueError:
        return None  # Si no puede convertir, retorna None

def convertir_fraccion_a_decimal_Latex(fraccion_str):
    """
    Convierte todas las fracciones en formato LaTeX a números decimales dentro de una cadena.
    
    :param fraccion_str: Cadena que contiene una o más fracciones en formato LaTeX, por ejemplo, "\\frac{1}{2}".
    :return: Cadena con las fracciones convertidas a sus valores decimales.
    """
    # Buscar el formato de fracción \frac{a}{b} y reemplazarlo con su valor decimal
    patron_fraccion = r"\\frac\{(-?\d+)\}\{(-?\d+)\}"
    
    def reemplazar_por_decimal(match):
        numerador = int(match.group(1))
        denominador = int(match.group(2))
        return str(float(Fraction(numerador, denominador)))
    
    # Usar sub para reemplazar todas las fracciones encontradas en la cadena
    resultado = re.sub(patron_fraccion, reemplazar_por_decimal, fraccion_str)
    
    return resultado

def validar_entrada_matriz(input_text):
    try:
        filas = input_text.strip().split("\n")
        matriz = [list(map(convertir_fraccion_a_decimal, fila.split())) for fila in filas]
        if None in [elem for fila in matriz for elem in fila]:  # Verifica si alguna conversión falló
            return None
        if validar_matriz(matriz):
            return matriz
        else:
            return None
    except ValueError:
        return None


# Función para validar si dos o más matrices tienen las mismas dimensiones
def validar_dimensiones_matrices(matrices):
    if len(matrices) < 2:
        return False  # Se requieren al menos dos matrices para comparar

    filas_primera_matriz = len(matrices[0])
    columnas_primera_matriz = len(matrices[0][0])

    for matriz in matrices[1:]:
        if len(matriz) != filas_primera_matriz or len(matriz[0]) != columnas_primera_matriz:
            return False
    return True

def validar_matriz_vectores(matriz, u, v):
    # Validar que la matriz tenga la misma cantidad de columnas que la longitud de los vectores
    num_columnas = len(matriz[0])
    if any(len(fila) != num_columnas for fila in matriz):
        raise ValueError("Todas las filas de la matriz deben tener la misma cantidad de columnas.")
    
    if len(u) != len(v):
        raise ValueError("Los vectores u y v deben tener la misma longitud.")
    
    if num_columnas != len(u):
        raise ValueError("La cantidad de columnas de la matriz debe ser igual a la longitud de los vectores.")

    # Si pasa todas las validaciones
    return True

def obtener_segunda_mitad(matrix):
    # Obtenemos el número de columnas
    num_columnas = len(matrix[0])
    
    # Calculamos el punto medio de las columnas
    mitad = num_columnas // 2
    
    # Extraemos la segunda mitad de las columnas
    matrix2 = [fila[mitad:] for fila in matrix]
    return matrix2

def Validar_matriz_cuadrada(matriz):
    # Verificamos que la matriz no esté vacía
    if len(matriz) == 0:
        return False
    
    # Verificamos que el número de columnas en cada fila sea igual al número de filas
    num_filas = len(matriz)
    for fila in matriz:
        if len(fila) != num_filas:
            return False
    
    return True