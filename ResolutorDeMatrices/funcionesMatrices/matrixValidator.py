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
