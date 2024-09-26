from funcionesMatrices.printing import *
from funcionesMatrices.reemplazar import reemplazarFila, alternarFilas
from funcionesMatrices.matrixFunctions import *
from fractions import Fraction

def pivoteoMax(matrix):
    '''Se recorre la matriz iniciando desde 0,0, row y column
    siempre son el mismo valor, a menos que hayan más columnas que filas
    en ese caso dejan de aumentar.
    '''
    row:int = 0
    for column in range(len(matrix[0])- 1):
        
        if row > len(matrix) - 1:
            row = len(matrix) - 1
        
        #Se busca que cuando el numero de columnas sea mayor que el de filas, se detenga
        if column > len(matrix) - 1:
            break

        column=column + liberar_columna_pivote(matrix, row, column)
        
        for fila in range(row + 1, len(matrix)):
            
            if matrix[fila][column] == 0: continue
            
            operation = False
            operacionString = "-"
            if matrix[fila][column] < 0: operation = True

            if operation: operacionString = " + "
            print(f"F{fila + 1}=> F{fila + 1}{operacionString}{abs(matrix[fila][column])}*F{row + 1} \n") 

            matrix[fila] = OperateRows(matrix[fila], multiplyRow(matrix[row][:],abs(matrix[fila][column])), operation)

            
            
            printMatrix(matrix)
        
        for filaArriba in range(row, 0, -1):
            # if row == 0: break
            
            operation = False
            operacionString = "-"
            if matrix[filaArriba - 1][column] < 0: 
                operacionString="+"
                operation = True
            
            print(f"F{filaArriba - 1}=> F{filaArriba - 1}{operacionString}{abs(matrix[filaArriba][column])}*F{row + 1} \n")
            matrix[filaArriba -1] = OperateRows(matrix[filaArriba -1],multiplyRow(matrix[row][:], abs(matrix[filaArriba -1][column])), operation)
            
            printMatrix(matrix)
            

        row += 1

        
        
def hacer_uno_el_pivote(matrix, row, column):  
    '''
    Esta funcion lo que hace es hacer que el pivote sea 1, si el pivote es 0
    se busca una fila que tenga un pivote diferente de 0 y se intercambian las filas
    '''
    # COMPROBAR SI EL PIVOTE 1 ES 0:
    if matrix[row][column] == 0:
    
        for fila in range(row + 1, len(matrix)):
            if matrix[fila][column] != 0:
                alternarFilas(matrix, fila, row)
                printMatrix(matrix)
                return column
            
        if column + 1 < len(matrix[0]):
            return hacer_uno_el_pivote(matrix, row, column + 1)
        else:
            return column
    return column

                
                  

def liberar_columna_pivote(matrix,row,column):
    '''Después de obtener el pivote con la funcion anterior hace que los nums
    en la misma columna pero una fila debajo sean 0
    '''
    newColumn=hacer_uno_el_pivote(matrix,row,column)
    if matrix[row][newColumn] != 1 and matrix[row][newColumn] != 0:
            #Aqui lo unico qeu hace es imprimir la operacion que hace: en caso de la primera iteracion imprimiria:
            #F[0+1] => [1/matriz[0][0]] * F[0+1]
            print(f"F{row+1} => {1/matrix[row][newColumn]}*F{row+1}")
            print("###################################") 
            # Aqui solo multiplica la fila por una fraccion para que el pivote sea 1 siempre :D
            matrix[row] = multiplyRow(matrix[row],(1/matrix[row][newColumn])) 
            printMatrix(matrix) 
    return newColumn-column
            