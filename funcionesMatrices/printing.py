from tabulate import tabulate
from fractions import Fraction
# def printMatrix(matrix:list):
#     """
#     Esta funcion acepta solamente matrices como parametro

#     Busca imprimir la matriz de la mejor forma posible
#     """

#     print(tabulate(matrix, tablefmt="github"))
#     print("\n")

def printMatrix(matrix: list):
    """
    Esta función acepta solamente matrices como parámetro.
    
    Busca imprimir la matriz de la mejor forma posible. Si as_fraction es True,
    imprime los elementos de la matriz como fracciones.
    """
    matrix2 = matrix
    matrix2 = [[Fraction(element) for element in row] for row in matrix]

    print(tabulate(matrix2, tablefmt="github"))
    
    print("\n")   
    
def printResult(matrix: list):
    n = len(matrix)    # Número de filas
    m = len(matrix[0]) # Número de columnas
    free_vars = []  # Lista para almacenar variables libres
    equations = []  # Lista para almacenar ecuaciones formadas
    es_identidad = True  # Asumimos que es identidad hasta que se pruebe lo contrario
    inconsistente = False  # Para marcar si encontramos una inconsistencia
    infinitas_soluciones = False  # Para marcar si encontramos infinitas soluciones

    # Verificar si la matriz es identidad
    for i in range(n):
        for j in range(m - 1):
            if (i == j and matrix[i][j] != 1) or (i != j and matrix[i][j] != 0):
                es_identidad = False

    # Generar ecuaciones
    for i in range(n):
        row_has_nonzero = any(matrix[i][j] != 0 for j in range(m - 1))
        
        # Caso inconsistente
        if not row_has_nonzero and matrix[i][-1] != 0:
            inconsistente = True
            break
        
        # Caso de fila de ceros
        if all(matrix[i][j] == 0 for j in range(m - 1)) and matrix[i][-1] == 0:
            infinitas_soluciones = True
            continue
        
        equation = ""
        pivot_index = -1
        if any(matrix[i][j] != 0 for j in range(m - 1)):
            for j in range(m - 1):
                coef = matrix[i][j]
                if coef != 0:
                    if pivot_index == -1:
                        pivot_index = j
                        equation += f"x{j+1} = "
                    else:
                        sign = '+' if coef > 0 else '-'
                        equation += f" {sign} {abs(coef)}x{j+1}"
            
            if matrix[i][-1] != 0:
                sign = '+' if matrix[i][-1] > 0 else '-'
                equation += f" {sign} {abs(matrix[i][-1])}"
            
            equations.append((pivot_index, equation.strip()))
    
    # Identificar variables libres
    all_vars = set(range(m - 1))
    dependent_vars = {eq[0] for eq in equations}

    free_vars = list(all_vars - dependent_vars)
    
    # Incluir variables libres en su lugar
    for free_var in free_vars:
        equations.append((free_var, f"x{free_var + 1} es libre"))

    equations.sort()  # Asegurar que las ecuaciones estén en el orden correcto
    
    # Imprimir el resultado en el formato esperado
    if inconsistente:
        print("Sistema inconsistente.")
    elif infinitas_soluciones:
        print("Sistema tiene infinitas soluciones.")
        for i, eq in enumerate(equations):
            if i == 0:
                print("[ " + eq[1])
            else:
                print("| " + eq[1])
    else:
        for i, eq in enumerate(equations):
            if i == 0:
                print("[ " + eq[1])
            else:
                print("| " + eq[1])

    # Uso de la variable `es_identidad` para imprimir un mensaje adicional
    if es_identidad:
        print("La matriz es una matriz identidad.")

