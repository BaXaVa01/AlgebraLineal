def reemplazarFila(matrix:list , fila_por_reemplazar:list , fila:int):
    matrix[fila] = fila_por_reemplazar

    return matrix

def alternarFilas(matrix:list, fila1:int, fila2:int):
    print(f"\n F {fila1} <==> F{fila2} \n ")
    matrix[fila1], matrix[fila2] = matrix[fila2] , matrix[fila1]   