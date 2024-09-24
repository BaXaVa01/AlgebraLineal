def multiplyMatrix(matrixA:list , matrixB: list) -> list:
    if len(matrixA[0]) != len(matrixB):
        return 0
    lista = []
    for index in len(matrixA):

        for indexColumn in len(matrixB):
            num  = matrixA[index]
    