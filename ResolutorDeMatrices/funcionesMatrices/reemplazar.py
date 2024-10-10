def reemplazarFila(matrix:list , fila_por_reemplazar:list , fila:int):
    matrix[fila] = fila_por_reemplazar

    return matrix

def alternarFilas(matrix:list, fila1:int, fila2:int):
    print(f"\n F {fila1} <==> F{fila2} \n ")
    matrix[fila1], matrix[fila2] = matrix[fila2] , matrix[fila1]   

def rotar_matriz_90(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])

    rotada = [[0] * filas for _ in range(columnas)]

    for i in range(filas):
        for j in range(columnas):
            rotada[j][i] = matriz[i][j]

    return rotada