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

def multiplicar_vectores(vector_a, vector_b):
    if len(vector_a) != len(vector_b):
        raise ValueError("Los vectores deben tener la misma longitud.")
    
    # Multiplicación elemento a elemento
    return [a * b for a, b in zip(vector_a, vector_b)]

def procesar_operacion():
    try:
        if var_tipo_operacion.get() == "Matrices":
            # Obtener las matrices desde las entradas
            matriz_a = eval(entry_matriz_a.get())
            matriz_b = eval(entry_matriz_b.get())

            # Realizar la multiplicación de matrices
            resultado = multiplicar_matrices(matriz_a, matriz_b)

            # Mostrar el resultado en un cuadro de mensaje
            resultado_texto = "\n".join(["\t".join(map(str, fila)) for fila in resultado])
            messagebox.showinfo("Resultado", f"Matriz resultado:\n{resultado_texto}")

        elif var_tipo_operacion.get() == "Vectores":
            # Obtener los vectores desde las entradas
            vector_a = eval(entry_matriz_a.get())
            vector_b = eval(entry_matriz_b.get())

            # Realizar la multiplicación de vectores
            resultado = multiplicar_vectores(vector_a, vector_b)

            # Mostrar el resultado en un cuadro de mensaje
            resultado_texto = "Vector resultado: [" + ", ".join(map(str, resultado)) + "]"
            messagebox.showinfo("Resultado", resultado_texto)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Crear la ventana principal

ventana = tk.Tk()
ventana.title("Multiplicador de Matrices y Vectores")

# Estilo de fuente
font_size = ("Arial", 14)

# Etiqueta para seleccionar el tipo de operación
tk.Label(ventana, text="Seleccione el tipo de operación", font=font_size).pack(pady=10)

# Opción de operación (Matrices o Vectores)
var_tipo_operacion = tk.StringVar(value="Matrices")
tk.Radiobutton(ventana, text="Multiplicar Matrices", variable=var_tipo_operacion, value="Matrices", font=font_size).pack()
tk.Radiobutton(ventana, text="Multiplicar Vectores", variable=var_tipo_operacion, value="Vectores", font=font_size).pack()

# Etiquetas y cuadros de texto para las matrices o vectores
tk.Label(ventana, text="Ingrese la primera matriz o vector (ej. [[1, 2], [3, 4]] o [1, 2, 3])", font=font_size).pack(pady=10)
entry_matriz_a = tk.Entry(ventana, width=50, font=font_size)
entry_matriz_a.pack(pady=10)

tk.Label(ventana, text="Ingrese la segunda matriz o vector (ej. [[5, 6], [7, 8]] o [4, 5, 6])", font=font_size).pack(pady=10)
entry_matriz_b = tk.Entry(ventana, width=50, font=font_size)
entry_matriz_b.pack(pady=10)

# Botón para procesar la operación
boton_procesar = tk.Button(ventana, text="Procesar", command=procesar_operacion, font=font_size)
boton_procesar.pack(pady=20)

# Iniciar la aplicación
ventana.mainloop()
