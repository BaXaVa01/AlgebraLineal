import customtkinter as ctk

class MatrizEditable:
    def __init__(self, parent_frame, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.entries = []

        # Crear frame para la matriz dentro del parent_frame
        self.frame = ctk.CTkFrame(parent_frame)
        self.frame.pack(pady=10, padx=10)

        # Crear matriz de entradas (CTkEntry)
        for i in range(self.filas):
            fila_entries = []
            for j in range(self.columnas):
                entry = ctk.CTkEntry(self.frame, width=50)
                entry.grid(row=i, column=j, padx=5, pady=5)
                fila_entries.append(entry)
            self.entries.append(fila_entries)

    def obtener_matriz(self):
        # Extraer los valores de las entradas
        matriz = []
        for fila_entries in self.entries:
            fila = []
            for entry in fila_entries:
                try:
                    valor = float(entry.get())
                except ValueError:
                    valor = 0.0  # Valor por defecto si el campo está vacío o no es numérico
                fila.append(valor)
            matriz.append(fila)
        return matriz


