import customtkinter as ctk

import tkinter as tk
import string


class MatricesTab:
    def __init__(self, tabview):
        # Crear la pestaña de matrices
        self.tab = tabview.add("Matrices")

        # Contenedor principal desplazable
        self.scrollable_frame = ctk.CTkScrollableFrame(self.tab, width=700, height=200)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Lista para almacenar matrices
        self.matrices = []
        self.matrix_count = 0  # Contador de matrices

        # Botón para añadir matrices
        self.add_matrix_button = ctk.CTkButton(
            self.tab, text="Añadir Matriz", command=self.add_new_matrix
        )
        self.add_matrix_button.pack(pady=10)

        # Botón para operar matrices
        self.operate_button = ctk.CTkButton(
            self.tab, text="Sumar Matrices", command=self.sum_matrices
        )
        self.operate_button.pack(pady=10)


    def add_new_matrix(self):
        """Añade una nueva matriz editable."""
        new_matrix = self._create_matrix_frame()
        new_matrix.pack(side="left", padx=10, pady=10)  # Cambiado de grid a pack para mejor compatibilidad
        self.matrices.append(new_matrix)
        self.matrix_count += 1

        # Actualizar el scrollable_frame
        self.scrollable_frame.update_idletasks()
        # self.scrollable_frame._canvas.configure(scrollregion=self.scrollable_frame._canvas.bbox("all"))


    def _create_matrix_frame(self):
        """Crea un frame con una matriz editable, un botón para eliminarla, y un identificador."""
        frame = ctk.CTkFrame(self.scrollable_frame)
        entries = []

        # Generar el identificador de la matriz usando letras del abecedario
        identifier_index = len(self.matrices)
        if identifier_index < 26:
            identifier = chr(65 + identifier_index)  # Asignar letra A-Z
        else:
            identifier = f"M{identifier_index + 1}"  # Si excede A-Z, usar "M1", "M2", etc.

        # Etiqueta con el identificador de la matriz
        identifier_label = ctk.CTkLabel(frame, text=f"Matriz {identifier}", font=("Arial", 14, "bold"))
        identifier_label.pack(pady=(5, 5))

        # Botón para eliminar la matriz
        delete_button = ctk.CTkButton(
            frame,
            text="Eliminar",
            width=80,
            command=lambda: self._remove_matrix(frame)
        )
        delete_button.pack(pady=(5, 10))

        # Crear entradas de la matriz
        for i in range(3):  # Filas
            row_frame = ctk.CTkFrame(frame)  # Frame para organizar la fila
            row_frame.pack()
            row_entries = []
            for j in range(3):  # Columnas
                entry = ctk.CTkEntry(row_frame, width=50, justify="center")
                entry.pack(side="left", padx=5, pady=5)
                row_entries.append(entry)
            entries.append(row_entries)

        # Agregar botones de operaciones individuales
        self.add_matrix_operations(frame, identifier)

        frame.entries = entries
        frame.identifier = identifier

        # Añadir al contenedor desplazable
        frame.pack(pady=10, padx=10)

        return frame


    def _remove_matrix(self, frame):
        """Elimina una matriz del contenedor y de la lista."""
        if frame in self.matrices:
            self.matrices.remove(frame)
            frame.destroy()
            self.matrix_count -= 1


    def get_matrix_values(self, frame):
        """Obtiene los valores de una matriz desde su frame."""
        values = []
        for row in frame.entries:
            values.append([entry.get() for entry in row])
        return values

    def sum_matrices(self):
        """Suma las dos primeras matrices y muestra el resultado."""
        if len(self.matrices) < 2:
            print("Se necesitan al menos dos matrices para sumar.")
            return

        # Obtener valores de las primeras dos matrices
        matrix1 = self.get_matrix_values(self.matrices[0])
        matrix2 = self.get_matrix_values(self.matrices[1])

        # Operar las matrices
        try:
            result = MatrixFunction.add_matrices(matrix1, matrix2)
        except ValueError:
            print("Error: Las matrices deben tener valores numéricos.")
            return

        # Mostrar resultado
        self.show_result_matrix(result)

    def add_matrix_operations(self, frame, matrix_identifier):
        """Añade botones de operaciones debajo de cada matriz."""
        operations_frame = ctk.CTkFrame(frame)
        operations_frame.pack(pady=(5, 10))

        # Botones de operaciones individuales
        ctk.CTkButton(operations_frame, text="Determinante", command=lambda: self.calculate_determinant(matrix_identifier)).pack(pady=2)
        ctk.CTkButton(operations_frame, text="Inversa", command=lambda: self.calculate_inverse(matrix_identifier)).pack(pady=2)
        ctk.CTkButton(operations_frame, text="Transponer", command=lambda: self.transpose_matrix(matrix_identifier)).pack(pady=2)
        ctk.CTkButton(operations_frame, text="Rango", command=lambda: self.calculate_rank(matrix_identifier)).pack(pady=2)

    def add_global_operations(self):
        """Añade botones para operaciones entre matrices."""
        global_operations_frame = ctk.CTkFrame(self.tab)
        global_operations_frame.pack(pady=20)

        # Botones de operaciones entre matrices
        ctk.CTkButton(global_operations_frame, text="A + B", command=self.add_matrices).pack(side="left", padx=10)
        ctk.CTkButton(global_operations_frame, text="A - B", command=self.subtract_matrices).pack(side="left", padx=10)
        ctk.CTkButton(global_operations_frame, text="A x B", command=self.multiply_matrices).pack(side="left", padx=10)


    def calculate_determinant(self, matrix_identifier):
        print(f"Calculando determinante de la matriz {matrix_identifier}")

    def calculate_inverse(self, matrix_identifier):
        print(f"Calculando inversa de la matriz {matrix_identifier}")

    def transpose_matrix(self, matrix_identifier):
        print(f"Transponiendo la matriz {matrix_identifier}")

    def calculate_rank(self, matrix_identifier):
        print(f"Calculando rango de la matriz {matrix_identifier}")

    def add_matrices(self):
        print("Sumando matrices A + B")

    def subtract_matrices(self):
        print("Restando matrices A - B")

    def multiply_matrices(self):
        print("Multiplicando matrices A x B")
