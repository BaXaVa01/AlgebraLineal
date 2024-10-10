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

        

            