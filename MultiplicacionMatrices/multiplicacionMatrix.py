import tkinter as tk
from tkinter import messagebox

def multiplicar_matrices(matriz_a, matriz_b):
    filas_a = len(matriz_a)
    columnas_a = len(matriz_a[0])
    filas_b = len(matriz_b)
    columnas_b = len(matriz_b[0])

    if columnas_a != filas_b:
        raise ValueError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz.")

    resultado = [[0 for _ in range(columnas_b)] for _ in range(filas_a)]

    for i in range(filas_a):
        for j in range(columnas_b):
            for k in range(columnas_a):
                resultado[i][j] += matriz_a[i][k] * matriz_b[k][j]

    return resultado

def procesar_matrices():
    try:
        # Obtener las matrices desde las entradas
        matriz_a = eval(entry_matriz_a.get())
        matriz_b = eval(entry_matriz_b.get())

        # Realizar la multiplicación
        resultado = multiplicar_matrices(matriz_a, matriz_b)

        # Mostrar el resultado en un cuadro de mensaje
        resultado_texto = "\n".join(["\t".join(map(str, fila)) for fila in resultado])
        messagebox.showinfo("Resultado", f"Matriz resultado:\n{resultado_texto}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Multiplicador de Matrices")

# Etiquetas y cuadros de texto para las matrices
tk.Label(ventana, text="Ingrese la primera matriz (ej. [[1, 2], [3, 4]])").pack()
entry_matriz_a = tk.Entry(ventana, width=50)
entry_matriz_a.pack()

tk.Label(ventana, text="Ingrese la segunda matriz (ej. [[5, 6], [7, 8]])").pack()
entry_matriz_b = tk.Entry(ventana, width=50)
entry_matriz_b.pack()

# Botón para procesar la multiplicación
boton_multiplicar = tk.Button(ventana, text="Multiplicar", command=procesar_matrices)
boton_multiplicar.pack()

# Iniciar la aplicación
ventana.mainloop()
