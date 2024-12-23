from ResolutorDeMatrices.funcionesMatrices.printing import printMatrix
def multiplyRow(row:list, multiply):
    
    """Esta funcion lo que hace es muiltiplicar una fila: {row}
      por el segundo parametro {multiply} que es un numero"""

    for index in range(len(row)):
        row[index] *= multiply

    return row

def OperateRows(rowFrom:list , rowAuxiliar:list, operation:bool) -> list:
    """
    \n operation:bool -> true: sumar , false: restar
    \nNOTE: AMBAS FILAS TIENEN QUE TENER EL MISMO TAMAÑO PARA PODER
    REALIZAR LA OPERACION
    """

    if len(rowFrom) != len(rowAuxiliar):
        print("No se pudo realizar la operacion debido a que ambas filas no son del mismo tamanio")
        return rowFrom
    
    auxRow:list = rowAuxiliar[:]

    if not operation:
        auxRow =  (multiplyRow(rowAuxiliar[:], -1))
        

    for index in range(len(rowFrom)):
        
        rowFrom[index] = round(rowFrom[index] + auxRow[index],7)

    
    return rowFrom

def validar_matriz(matriz):
    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):
            if not isinstance(valor, (int, float)):
                print(f"Error: El valor en la posición ({i+1}, {j+1}) no es un número. Es un {type(valor).__name__}.")
                return False
    return True

def Suma_de_Matrices(lista_matriz):
    
    n=len(lista_matriz)
    
    if lista_matriz == None:
        return 1
    
    TotalMatriz=lista_matriz[0]
    
    for i in range(n-1):
        tempSumaMatriz = lista_matriz[i+1]
        for j in range(len(tempSumaMatriz)):
            for k in range(len(tempSumaMatriz[0])):
                TotalMatriz[j][k]= TotalMatriz[j][k] + tempSumaMatriz[j][k]
                
    return TotalMatriz
        

def sumar_vectores(u, v):
    return [u[i] + v[i] for i in range(len(u))]

def multiplicar_matriz_vector(matriz, vector):
    resultado = []
    for fila in matriz:
        valor = sum(fila[i] * vector[i] for i in range(len(vector)))
        resultado.append(valor)
    return resultado

def son_vectores_iguales(u, v):
    return all([u[i] == v[i] for i in range(len(u))])

def mostrar_vector(vector):
    return f"[{', '.join(map(str, vector))}]"

def mostrar_matriz(matriz):
    return f"[{', '.join(mostrar_vector(fila) for fila in matriz)}]"


def calcular(matriz, u, v):
    # Suma de los vectores u y v
    u_plus_v = sumar_vectores(u, v)

    # Multiplicación de la matriz por u+v
    A_u_plus_v = multiplicar_matriz_vector(matriz, u_plus_v)

    # Multiplicación de la matriz por u y por v
    A_u = multiplicar_matriz_vector(matriz, u)
    A_v = multiplicar_matriz_vector(matriz, v)

    # Suma de los productos
    A_u_plus_A_v = sumar_vectores(A_u, A_v)

    # Texto explicativo paso a paso
    steps = []
    steps.append(f"1. Suma de los vectores u y v:")
    steps.append(f"   u = {mostrar_vector(u)}")
    steps.append(f"   v = {mostrar_vector(v)}")
    steps.append(f"   u + v = {mostrar_vector(u)} + {mostrar_vector(v)} = {mostrar_vector(u_plus_v)}")
    steps.append("\n2. Multiplicación de la matriz A por el vector (u + v):")
    steps.append(f"   A = {mostrar_matriz(matriz)}")
    steps.append(f"   A(u + v) = A * {mostrar_vector(u_plus_v)} = {mostrar_vector(A_u_plus_v)}")
    steps.append("\n3. Multiplicación de A por u y A por v por separado:")
    steps.append(f"   Au = A * {mostrar_vector(u)} = {mostrar_vector(A_u)}")
    steps.append(f"   Av = A * {mostrar_vector(v)} = {mostrar_vector(A_v)}")
    steps.append("\n4. Suma de Au y Av:")
    steps.append(f"   Au + Av = {mostrar_vector(A_u)} + {mostrar_vector(A_v)} = {mostrar_vector(A_u_plus_A_v)}")

    # Verificar si se cumple la propiedad distributiva
    if son_vectores_iguales(A_u_plus_v, A_u_plus_A_v):
        steps.append(f"\nPropiedad distributiva verificada: A(u + v) = Au + Av")
        steps.append("\n**Explicación:**")
        steps.append("   Se cumple la propiedad distributiva porque:")
        steps.append("   A(u + v) es igual a la suma de los productos A por u y A por v por separado.")
    else:
        steps.append(f"\nLa propiedad distributiva NO se cumple")

    steps_text = "\n".join(steps)
    return steps_text

def multiplyMatrix(matrixA:list , matrixB: list) -> list:
    if len(matrixA[0]) != len(matrixB):
        return 0
    lista = []
    for index in len(matrixA):

        for indexColumn in len(matrixB):
            num  = matrixA[index]
            

def determinante(matrix, level=0):
    steps = ""
    
    # Función para formatear la matriz en formato monoespaciado
    def format_matrix(matrix):
        formatted_matrix = ""
        for fila in matrix:
            formatted_matrix += " ".join(f"{elem:8.2f}" for elem in fila) + "\n"
        return formatted_matrix

    # Verificar que la matriz sea cuadrada
    if len(matrix) != len(matrix[0]):
        raise ValueError("La matriz debe ser cuadrada.")
    
    # Caso base: si la matriz es 1x1, el determinante es el único elemento
    if len(matrix) == 1:
        steps += f"{'  ' * level}Determinante 1x1: {matrix[0][0]}\n"
        steps += f"{'  ' * level}Matriz:\n{format_matrix(matrix)}"
        return matrix[0][0], steps
    
    # Caso base: si la matriz es 2x2, calcular el determinante directamente
    if len(matrix) == 2:
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        steps += f"{'  ' * level}Matriz 2x2:\n{format_matrix(matrix)}"
        steps += f"{'  ' * level}Determinante 2x2: {matrix[0][0]}*{matrix[1][1]} - {matrix[0][1]}*{matrix[1][0]} = {det}\n"
        return det, steps
    
    # Expansión de cofactores para matrices mayores de 2x2
    det = 0
    for c in range(len(matrix)):
        # Crear la submatriz eliminando la primera fila y la columna c
        sub_matrix = [row[:c] + row[c+1:] for row in matrix[1:]]
        cofactor_det, sub_steps = determinante(sub_matrix, level + 1)
        term = ((-1) ** c) * matrix[0][c] * cofactor_det
        det += term
        steps += f"{'  ' * level}Matriz actual:\n{format_matrix(matrix)}"
        steps += f"{'  ' * level}Cofactor {matrix[0][c]} * determinante de submatriz:\n{sub_steps}\n"
        steps += f"{'  ' * level}Termino: {term}\n"

    return det, steps


def generar_matriz(n, entradas):
    matriz = []
    for i in range(n):
        fila = []
        for j in range(n):
            valor = entradas[i][j].get()
            try:
                fila.append(float(valor))
            except ValueError:
                raise ValueError("Por favor, ingrese valores numéricos válidos.")
        matriz.append(fila)
    return matriz


def cramer(matriz, vector):
    n = len(matriz)
    det_matriz, pasos = determinante(matriz)  # Reutilizamos la función de determinante
    if det_matriz == 0:
        raise ValueError("El sistema no tiene solución por el método de cramer (determinante 0).")
    
    soluciones = []
    for i in range(n):
        # Crear una copia de la matriz original y reemplazar la columna i por el vector
        matriz_modificada = [fila[:] for fila in matriz]
        for j in range(n):
            matriz_modificada[j][i] = vector[j]
        
        # Calcular el determinante de la matriz modificada
        det_modificada, pasos_mod = determinante(matriz_modificada)
        soluciones.append(det_modificada / det_matriz)
        pasos += f"Determinante de la matriz con la columna {i+1} reemplazada:\n{pasos_mod}\n"
        pasos += f"Solución {i+1}: {det_modificada} / {det_matriz} = {soluciones[-1]}\n"
    
    return soluciones, pasos

def matriz_aumentada_con_identidad(matriz):
    n = len(matriz)
    
    identidad = [[float(i == j) for i in range(n)] for j in range(n)]
    
    matriz_aumentada = [fila + identidad[i] for i, fila in enumerate(matriz)]
    
    print("Matriz aumentada con identidad:")
    printMatrix(matriz_aumentada)
    
    return matriz_aumentada
        
def multiplicar_matrices(matrices):
    if len(matrices) < 2:
        raise ValueError("Debes proporcionar al menos dos matrices para multiplicar.")
    
    resultado = matrices[0]
    
    # Multiplicar secuencialmente todas las matrices
    for matriz in matrices[1:]:
        if len(resultado[0]) != len(matriz):
            raise ValueError("Las dimensiones de las matrices no son compatibles para multiplicar.")
        
        resultado = [[sum(round(a * b,3) for a, b in zip(filaA, columnaB)) for columnaB in zip(*matriz)] for filaA in resultado]

    return resultado
            