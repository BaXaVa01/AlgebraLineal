import tkinter as tk
from tkinter import font

def crear_campos():
    try:
        # Obtener dimensiones de la matriz
        filas = int(entry_filas.get())
        columnas = int(entry_columnas.get())

        # Limpiar los frames antes de agregar nuevos widgets
        for widget in frame_matriz.winfo_children():
            widget.destroy()
        for widget in frame_uv.winfo_children():
            widget.destroy()

        # Crear campos para la matriz A
        global entries_A
        entries_A = [[tk.Entry(frame_matriz, width=10, font=font_style, relief="solid") for _ in range(columnas)] for _ in range(filas)]
        for i in range(filas):
            for j in range(columnas):
                entries_A[i][j].grid(row=i, column=j, padx=5, pady=5)

        # Crear campos para el vector u
        tk.Label(frame_uv, text="Vector u:", font=font_style, bg='#f0f0f0').grid(row=0, column=0, pady=10, sticky="w")
        global entry_u
        entry_u = [tk.Entry(frame_uv, width=10, font=font_style, relief="solid") for _ in range(columnas)]
        for i in range(columnas):
            entry_u[i].grid(row=0, column=i+1, padx=5, pady=5)

        # Crear campos para el vector v
        tk.Label(frame_uv, text="Vector v:", font=font_style, bg='#f0f0f0').grid(row=1, column=0, pady=10, sticky="w")
        global entry_v
        entry_v = [tk.Entry(frame_uv, width=10, font=font_style, relief="solid") for _ in range(columnas)]
        for i in range(columnas):
            entry_v[i].grid(row=1, column=i+1, padx=5, pady=5)

        # Botón para calcular con estilo redondeado
        calc_button = tk.Button(window, text="Calcular", font=font_style, command=calcular, bg='#007acc', fg='white', relief="raised")
        calc_button.grid(row=5, column=0, columnspan=2, pady=20)
        calc_button.config(highlightbackground='#007acc', borderwidth=3, relief="groove")

        # Etiqueta para mostrar los resultados
        global result_label
        result_label = tk.Label(window, text="", font=("Helvetica", 12), bg='#f0f0f0', justify="left")
        result_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    except ValueError:
        pass

# Función para realizar el cálculo
def calcular():
    try:
        filas = int(entry_filas.get())
        columnas = int(entry_columnas.get())
        A = [[float(entries_A[i][j].get()) for j in range(columnas)] for i in range(filas)]
        u = [float(entry_u[i].get()) for i in range(columnas)]
        v = [float(entry_v[i].get()) for i in range(columnas)]

        # Ejemplo de cálculo: suma de todos los elementos de A, u y v
        suma_A = sum(sum(row) for row in A)
        suma_u = sum(u)
        suma_v = sum(v)

        resultado = f"Suma de A: {suma_A}\nSuma de u: {suma_u}\nSuma de v: {suma_v}"
        result_label.config(text=resultado)
    except ValueError:
        result_label.config(text="Error en los valores ingresados.")

# Configuración de la ventana principal
window = tk.Tk()
window.title("Calculadora de Matrices")
window.configure(bg='#f0f0f0')
font_style = font.Font(family="Helvetica", size=12)

# Configurar la ventana para que sea fullscreen
window.attributes('-fullscreen', True)

# Deshabilitar la capacidad de salir del modo fullscreen
window.bind("<Escape>", lambda e: None)

# Configurar el grid layout para centrar los elementos
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(3, weight=1)
window.grid_rowconfigure(4, weight=1)
window.grid_rowconfigure(5, weight=1)
window.grid_rowconfigure(6, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

# Entrada para las dimensiones de la matriz
tk.Label(window, text="Filas de la matriz:", font=font_style, bg='#f0f0f0').grid(row=0, column=0, pady=10, sticky="e")
entry_filas = tk.Entry(window, width=5, font=font_style, relief="solid")
entry_filas.grid(row=0, column=1, padx=5, pady=10, sticky="w")

tk.Label(window, text="Columnas de la matriz:", font=font_style, bg='#f0f0f0').grid(row=1, column=0, pady=10, sticky="e")
entry_columnas = tk.Entry(window, width=5, font=font_style, relief="solid")
entry_columnas.grid(row=1, column=1, padx=5, pady=10, sticky="w")

# Botón para crear los campos
create_button = tk.Button(window, text="Crear Campos", font=font_style, command=crear_campos, bg='#007acc', fg='white', relief="raised")
create_button.grid(row=2, column=0, columnspan=2, pady=10)
create_button.config(highlightbackground='#007acc', borderwidth=3, relief="groove")

# Frame para la matriz y los vectores
frame_matriz = tk.Frame(window, bg='#f0f0f0')
frame_matriz.grid(row=3, column=0, columnspan=2, pady=10)

frame_uv = tk.Frame(window, bg='#f0f0f0')
frame_uv.grid(row=4, column=0, columnspan=2, pady=10)

window.mainloop()