import customtkinter as ctk

# Función para generar los campos de entrada de la matriz
def generar_campos():
    try:
        # Limpiar el área de resultados y de entradas de la matriz anteriores
        for widget in matriz_frame.winfo_children():
            widget.destroy()
        
        # Obtener número de filas y columnas
        filas = int(filas_entry.get())
        columnas = int(columnas_entry.get())
        
        # Crear una lista para almacenar las entradas
        global entradas
        entradas = []
        
        # Crear campos de entrada para cada elemento de la matriz
        for i in range(filas):
            fila_entradas = []
            for j in range(columnas):
                entrada = ctk.CTkEntry(matriz_frame, width=50)
                entrada.grid(row=i, column=j, padx=5, pady=5)
                fila_entradas.append(entrada)
            entradas.append(fila_entradas)
        
    except Exception as e:
        resultado_texto.delete("1.0", ctk.END)
        resultado_texto.insert(ctk.END, "Error al generar los campos: Asegúrate de que los valores sean números enteros.\n")
        resultado_texto.insert(ctk.END, f"Detalles: {e}\n")

# Función para calcular la transpuesta de la matriz
def calcular_transpuesta():
    try:
        # Obtener la matriz ingresada desde los campos de entrada
        matriz = []
        for fila_entradas in entradas:
            fila = [int(entrada.get()) for entrada in fila_entradas]
            matriz.append(fila)
        
        # Calcular la transpuesta manualmente
        transpuesta = [[matriz[j][i] for j in range(len(matriz))] for i in range(len(matriz[0]))]
        
        # Mostrar los pasos detallados
        resultado_texto.delete("1.0", ctk.END)  # Limpiar el área de texto
        resultado_texto.insert(ctk.END, "Matriz Original:\n", "negrita")
        for fila in matriz:
            resultado_texto.insert(ctk.END, f"{fila}\n")
        
        resultado_texto.insert(ctk.END, "\nPaso 1: Intercambiar las filas por columnas.\n")
        for i in range(len(matriz)):  # Itera sobre las filas
            for j in range(len(matriz[0])):  # Itera sobre las columnas
                resultado_texto.insert(
                    ctk.END, f"El elemento ({i+1}, {j+1}) de la matriz original pasa a ser "
                             f"el elemento ({j+1}, {i+1}) en la transpuesta.\n"
                )
        
        resultado_texto.insert(ctk.END, "\nMatriz Transpuesta:\n", "negrita")
        for fila in transpuesta:
            resultado_texto.insert(ctk.END, f"{fila}\n")
        
    except Exception as e:
        resultado_texto.delete("1.0", ctk.END)
        resultado_texto.insert(ctk.END, "Error al calcular la transpuesta. Asegúrate de que los valores sean números enteros.\n")
        resultado_texto.insert(ctk.END, f"Detalles: {e}\n")

# Configuración de la interfaz gráfica
app = ctk.CTk()
app.title("Transpuesta de una Matriz")
app.geometry("800x600")

# Frame para los controles de filas y columnas
control_frame = ctk.CTkFrame(app)
control_frame.pack(pady=10)

filas_label = ctk.CTkLabel(control_frame, text="Número de Filas:")
filas_label.grid(row=0, column=0, padx=5, pady=5)
filas_entry = ctk.CTkEntry(control_frame, width=50)
filas_entry.grid(row=0, column=1, padx=5, pady=5)

columnas_label = ctk.CTkLabel(control_frame, text="Número de Columnas:")
columnas_label.grid(row=0, column=2, padx=5, pady=5)
columnas_entry = ctk.CTkEntry(control_frame, width=50)
columnas_entry.grid(row=0, column=3, padx=5, pady=5)

# Botón para generar los campos de entrada de la matriz
generar_botton = ctk.CTkButton(control_frame, text="Generar Matriz", command=generar_campos)
generar_botton.grid(row=0, column=4, padx=5, pady=5)

# Frame para los campos de entrada de la matriz
matriz_frame = ctk.CTkFrame(app)
matriz_frame.pack(pady=10)

# Botón para calcular la transpuesta
calcular_button = ctk.CTkButton(app, text="Calcular Transpuesta", command=calcular_transpuesta)
calcular_button.pack(pady=10)

# Área de texto para mostrar los resultados
resultado_texto = ctk.CTkTextbox(app, height=300, font=("Arial", 16), wrap="word")
resultado_texto.pack(pady=10, padx=10, fill="both", expand=True)

# Estilo para negrita
resultado_texto.configure("negrita", font=("Arial", 16, "bold"))

# Iniciar la aplicación
app.mainloop()
