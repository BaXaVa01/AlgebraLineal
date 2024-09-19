import tkinter as tk
from tkinter import messagebox
from ResolutorDeMatrices.resolutorMatrix import resolverMatriz
from MultiplicacionMatrices.multiplicacionMatrix import ventanaPrincipal
from ResolutorDeVectores.vectores import resolutorVectores

# Funciones que se ejecutarán al hacer clic en cada botón
def multiplicacion_matriz():
    # Aquí podrías agregar la lógica de multiplicación de matrices
    messagebox.showinfo("Multiplicación de Matrices")
    ventanaPrincipal()

def pivoteo():
    # Aquí podrías agregar la lógica de pivoteo
    messagebox.showinfo("Pivoteo")
    # resolverMatriz()

def resolutor_vectores():
    # Aquí podrías agregar la lógica para resolver vectores
    messagebox.showinfo("Resolutor de Vectores", "Aquí se ejecutará el resolutor de vectores.")
    resolutor_vectores()
# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Aplicación General")

# Estilo de fuente
font_size = ("Arial", 14)

# Botón 1: Multiplicación de Matriz
boton_multiplicacion = tk.Button(ventana, text="Multiplicación de matriz", font=font_size, command=multiplicacion_matriz)
boton_multiplicacion.pack(pady=20)

# Botón 2: Pivoteo
boton_pivoteo = tk.Button(ventana, text="Pivoteo", font=font_size, command=pivoteo)
boton_pivoteo.pack(pady=20)

# Botón 3: Resolutor de Vectores
boton_resolutor_vectores = tk.Button(ventana, text="Resolutor de vectores", font=font_size, command=resolutor_vectores)
boton_resolutor_vectores.pack(pady=20)

# Iniciar la aplicación
ventana.mainloop()
