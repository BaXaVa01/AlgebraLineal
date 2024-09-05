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
        
        rowFrom[index] = rowFrom[index] + auxRow[index]

    
    return rowFrom

def validar_matriz(matriz):
    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):
            if not isinstance(valor, (int, float)):
                print(f"Error: El valor en la posición ({i+1}, {j+1}) no es un número. Es un {type(valor).__name__}.")
                return False
    return True

