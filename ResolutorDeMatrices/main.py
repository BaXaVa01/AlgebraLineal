from funcionesMatrices.pivoteo import *
import tkinter as tk
from tkinter import simpledialog
import sys
import os

def main():
    salir=False
    while salir==False:
        matrix=obtener_matriz_desde_input()
        if validar_matriz(matrix):
            
            printMatrix(matrix)
            pivoteoMax(matrix)

            print("##############################")
            print("resultados:")

            printMatrix(matrix)
            printResult(matrix)
           
            
            print("Deseas resolver otra matriz?")
           #me molestaba que no hiciera cls
            input_text = input("Ingrese 's' para resolver otra matriz o cualquier otra tecla para salir: ")
            if input_text.lower() == 's':
                os.system('cls')
            else:
                salir = True
    
    

        
def obtener_matriz_desde_input():
    root = tk.Tk()
    root.withdraw()  # Esconder la ventana principal

    input_text = simpledialog.askstring("Entrada de Matriz", "Pega aquí la matriz copiada desde Excel:")
    if input_text:
        filas = input_text.strip().split("\n")
        matriz = [list(map(float, fila.split())) for fila in filas]
        return matriz
    else:
        print("Operación cancelada. Saliendo del programa.")
        sys.exit()  # Detiene la ejecución del programa

main()