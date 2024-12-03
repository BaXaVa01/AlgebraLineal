import customtkinter as ctk
from tkinter import messagebox
from fractions import Fraction
import numpy as np
import tkinter as tk
import string


class MatricesTab:
    def __init__(self, tabview):
        # Crear la pestaña de matrices
        self.tab = tabview.add("Matrices")

        # Configuración del grid principal
        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_rowconfigure(1, weight=0)  # Barra inferior
        self.tab.grid_columnconfigure((0, 1), weight=1)

        # Contenedor para las matrices (lado izquierdo)
        self.scrollable_frame = ctk.CTkScrollableFrame(self.tab, width=700, height=400)
        self.scrollable_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        # Frame para mostrar los resultados (lado derecho)
        self.results_frame = ctk.CTkFrame(self.tab, width=300)
        self.results_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        # Etiqueta para resultados
        self.results_label = ctk.CTkLabel(
            self.results_frame,
            text="Resultados:\n",
            justify="left",
            wraplength=280,
            font=("Arial", 14),
        )
        self.results_label.pack(pady=10)

        # Barra inferior para controles
        self.bottom_frame = ctk.CTkFrame(self.tab, height=50)
        self.bottom_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # Botón para añadir matrices
        self.add_matrix_button = ctk.CTkButton(
            self.bottom_frame, text="Añadir Matriz", command=self.add_new_matrix
        )
        self.add_matrix_button.pack(side="left", padx=5, pady=10)

        # Entrada para la operación
        self.operation_entry = ctk.CTkEntry(
            self.bottom_frame, width=200, placeholder_text="Ej: 3*A"
        )
        self.operation_entry.pack(side="left", padx=5, pady=10)

        # Botón para operar matrices
        self.operate_button = ctk.CTkButton(
            self.bottom_frame, text="Operar Matrices", command=self.process_general_operation
        )
        self.operate_button.pack(side="left", padx=5, pady=10)

        # Botón para copiar el resultado al portapapeles
        self.copy_result_button = ctk.CTkButton(
            self.bottom_frame, text="Copiar Resultado", command=self.copy_result_to_clipboard
        )

        self.copy_result_button.pack(side="right", padx=5, pady=10)

        # Variables internas
        self.matrices = []
        self.matrix_count = 0  # Contador de matrices

    def add_new_matrix(self):
        """Añade una nueva matriz editable."""
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.pack(side="left", padx=10, pady=10)

        # Identificador de la matriz
        identifier = chr(65 + self.matrix_count)  # A, B, C, ...
        self.matrix_count += 1
        frame.identifier = identifier

        # Etiqueta del identificador
        label = ctk.CTkLabel(frame, text=f"Matriz {identifier}", font=("Arial", 14))
        label.pack(pady=5)

        # Sub-frame para las entradas de la matriz
        matrix_entries_frame = ctk.CTkFrame(frame)
        matrix_entries_frame.pack(pady=5)
        frame.matrix_entries_frame = matrix_entries_frame  # Guardamos la referencia al sub-frame

        # Botón para modificar dimensiones
        modify_button = ctk.CTkButton(
            frame, text="Modificar Dimensiones", command=lambda: self.modify_dimensions(frame)
        )
        modify_button.pack(pady=5)

        # Botón para calcular el determinante
        det_button = ctk.CTkButton(
            frame, text="Determinante", command=lambda: self.calculate_determinant(frame)
        )
        det_button.pack(pady=5)

        # Botón para calcular la inversa
        inverse_button = ctk.CTkButton(
            frame, text="Inversa", command=lambda: self.calculate_inverse(frame)
        )
        inverse_button.pack(pady=5)

        # Botón para calcular la transpuesta
        transpose_button = ctk.CTkButton(
            frame, text="Transponer", command=lambda: self.calculate_transpose(frame)
        )
        transpose_button.pack(pady=5)

        # Botón para calcular el rango
        rank_button = ctk.CTkButton(
            frame, text="Rango", command=lambda: self.calculate_rank(frame)
        )
        rank_button.pack(pady=5)
        # Botón para copiar
        rank_button = ctk.CTkButton(
            frame, text="Copy", command=lambda: self.copy_matrix(identifier)
        )
        rank_button.pack(pady=5)

        # Botón para pegar
        rank_button = ctk.CTkButton(
            frame, text="Paste", command=lambda: self.paste_matrix(identifier)
        )
        rank_button.pack(pady=5)

        # Crear entradas para la matriz (dimensiones predeterminadas: 3x3)
        entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                entry = ctk.CTkEntry(matrix_entries_frame, width=50, justify="center")
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            entries.append(row_entries)

        frame.entries = entries
        self.matrices.append(frame)

    def perform_operation(self):
        """Procesa la operación ingresada y realiza la operación en las matrices."""
        try:
            # Leer la operación ingresada
            operation = self.operation_entry.get().strip()
            if not operation:
                raise ValueError("Debe ingresar una operación válida.")

            # Analizar la operación
            if "*" in operation:
                scalar, matrix_id = operation.split("*")
                scalar = float(Fraction(scalar.strip()))
                matrix_id = matrix_id.strip()
            else:
                raise ValueError("Formato de operación inválido. Ejemplo válido: 3*A")

            # Validar que la matriz exista
            matrix_frame = next((frame for frame in self.matrices if frame.identifier == matrix_id), None)
            if not matrix_frame:
                raise ValueError(f"No existe una matriz con el identificador '{matrix_id}'.")

            # Obtener los valores de la matriz
            matrix_values = self.get_matrix_values(matrix_frame)
            matrix_array = np.array(matrix_values, dtype=float)

            # Realizar la operación
            result = scalar * matrix_array

            # Mostrar el resultado
            self._display_result(matrix_id, scalar, result)
        except Exception as e:
            messagebox.showerror("Error", f"Error en la operación: {e}")

    def _display_result(self, matrix_id, scalar, result):
        """Muestra el resultado de la operación."""
        result_text = f"Operación: {scalar} * {matrix_id}\n\nResultado:\n{self._matrix_to_string(result)}"
        print(result_text)  # Puede mostrarse en consola o en otro lugar según lo necesites

    def _matrix_to_string(self, matrix):
        """Convierte una matriz en un formato de texto para su visualización."""
        rows = []
        for row in matrix:
            formatted_row = "\t".join(f"{value:.2f}" for value in row)
            rows.append(formatted_row)
        return "\n".join(rows)

    def get_matrix_values(self, frame):
        """Obtiene los valores de una matriz desde su frame."""
        values = []
        for row in frame.entries:
            values.append([float(Fraction(entry.get().strip()) or 0) for entry in row])
        return values

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

    def add_matrix_operations(self, frame, matrix_identifier):
        """Añade botones de operaciones debajo de cada matriz."""
        operations_frame = ctk.CTkFrame(frame)
        operations_frame.pack(pady=(7, 14))

        # Botones de operaciones individuales
        ctk.CTkButton(operations_frame, text="Copy", command=lambda: self.copy_matrix(matrix_identifier)).pack(pady=2)
        ctk.CTkButton(operations_frame, text="Paste", command=lambda: self.paste_matrix(matrix_identifier)).pack(pady=2)
        ctk.CTkButton(operations_frame, text="Determinante", command=lambda: self.calculate_determinant(frame)).pack(pady=2)
        ctk.CTkButton(operations_frame, text="Inversa", command=lambda: self.calculate_inverse(frame)).pack(pady=2)
        ctk.CTkButton(operations_frame, text="Transponer", command=lambda: self.calculate_transpose(frame)).pack(pady=2)
        ctk.CTkButton(operations_frame, text="Rango", command=lambda: self.calculate_rank(frame)).pack(pady=2)

    def add_global_operations(self):
        """Añade botones para operaciones entre matrices."""
        global_operations_frame = ctk.CTkFrame(self.tab)
        global_operations_frame.pack(pady=20)

        # Botones de operaciones entre matrices
        ctk.CTkButton(global_operations_frame, text="A + B", command=self.add_matrices).pack(side="left", padx=10)
        ctk.CTkButton(global_operations_frame, text="A - B", command=self.subtract_matrices).pack(side="left", padx=10)
        ctk.CTkButton(global_operations_frame, text="A x B", command=self.multiply_matrices).pack(side="left", padx=10)

    def _display_result(self, matrix_id, scalar, result):
        """Muestra el resultado de la operación en el frame de resultados."""
        result_text = f"Operación: {scalar} * {matrix_id}\n\nResultado:\n{self._matrix_to_string(result)}"
        self.results_label.configure(text=result_text)

    def calculate_inverse(self, matrix_frame):
        """Calcula la inversa de la matriz seleccionada."""
        try:
            # Obtener los valores de la matriz
            matrix_values = self.get_matrix_values(matrix_frame)
            matrix_array = np.array(matrix_values, dtype=float)

            # Verificar si la matriz es cuadrada
            if matrix_array.shape[0] != matrix_array.shape[1]:
                raise ValueError("La inversa solo se puede calcular para matrices cuadradas.")

            # Calcular el determinante para verificar que no sea cero
            determinant = np.linalg.det(matrix_array)
            if np.isclose(determinant, 0):
                raise ValueError("La matriz no tiene inversa porque su determinante es cero.")

            # Calcular la inversa
            inverse_matrix = np.linalg.inv(matrix_array)

            # Mostrar el resultado en el frame de resultados
            result_text = f"Inversa de la matriz:\n\n{self._matrix_to_string(inverse_matrix)}"
            self.results_label.configure(text=result_text)
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la inversa: {e}")

    def calculate_transpose(self, matrix_frame):
        """Calcula la transpuesta de la matriz seleccionada."""
        try:
            # Obtener los valores de la matriz
            matrix_values = self.get_matrix_values(matrix_frame)
            matrix_array = np.array(matrix_values, dtype=float)

            # Calcular la transpuesta
            transpose_matrix = matrix_array.T

            # Mostrar el resultado en el frame de resultados
            result_text = f"Transpuesta de la matriz:\n\n{self._matrix_to_string(transpose_matrix)}"
            self.results_label.configure(text=result_text)
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular la transpuesta: {e}")

    def calculate_rank(self, matrix_frame):
        """Calcula el rango de la matriz seleccionada."""
        try:
            # Obtener los valores de la matriz
            matrix_values = self.get_matrix_values(matrix_frame)
            matrix_array = np.array(matrix_values, dtype=float)

            # Calcular el rango
            rank = np.linalg.matrix_rank(matrix_array)

            # Mostrar el resultado en el frame de resultados
            result_text = f"Rango de la matriz:\n\n{rank}"
            self.results_label.configure(text=result_text)
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular el rango: {e}")



    def calculate_determinant(self, matrix_frame):
        """Calcula el determinante de la matriz seleccionada."""
        try:
            # Obtener los valores de la matriz
            matrix_values = self.get_matrix_values(matrix_frame)
            matrix_array = np.array(matrix_values, dtype=float)

            # Verificar si la matriz es cuadrada
            if matrix_array.shape[0] != matrix_array.shape[1]:
                raise ValueError("El determinante solo se puede calcular para matrices cuadradas.")

            # Calcular el determinante
            determinant = np.linalg.det(matrix_array)

            # Mostrar el resultado en el frame de resultados
            result_text = f"Determinante de la matriz:\n\n{determinant:.2f}"
            self.results_label.configure(text=result_text)
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular el determinante: {e}")

    def modify_dimensions(self, matrix_frame):
        """Abre un popup para modificar las dimensiones de la matriz."""
        popup = ctk.CTkToplevel(self.tab)
        popup.title(f"Modificar Dimensiones - {matrix_frame.identifier}")
        popup.geometry("300x200")

        # Etiquetas y entradas para filas y columnas
        rows_label = ctk.CTkLabel(popup, text="Filas:")
        rows_label.pack(pady=5)
        rows_entry = ctk.CTkEntry(popup, placeholder_text="Número de filas")
        rows_entry.pack(pady=5)

        cols_label = ctk.CTkLabel(popup, text="Columnas:")
        cols_label.pack(pady=5)
        cols_entry = ctk.CTkEntry(popup, placeholder_text="Número de columnas")
        cols_entry.pack(pady=5)

        # Botón para confirmar
        confirm_button = ctk.CTkButton(
            popup, text="Confirmar",
            command=lambda: self._apply_new_dimensions(matrix_frame, rows_entry, cols_entry, popup)
        )
        confirm_button.pack(pady=10)

    def _apply_new_dimensions(self, matrix_frame, rows_entry, cols_entry, popup):
        """Aplica las nuevas dimensiones a la matriz."""
        try:
            # Obtener las nuevas dimensiones
            rows = int(rows_entry.get().strip())
            cols = int(cols_entry.get().strip())

            if rows <= 0 or cols <= 0:
                raise ValueError("Las dimensiones deben ser mayores que 0.")

            # Limpiar las entradas actuales en el sub-frame
            for widget in matrix_frame.matrix_entries_frame.winfo_children():
                widget.destroy()

            # Crear nuevas entradas basadas en las dimensiones especificadas
            entries = []
            for i in range(rows):
                row_entries = []
                for j in range(cols):
                    entry = ctk.CTkEntry(matrix_frame.matrix_entries_frame, width=50, justify="center")
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    row_entries.append(entry)
                entries.append(row_entries)

            # Actualizar las entradas en el frame
            matrix_frame.entries = entries

            # Cerrar el popup
            popup.destroy()

        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")

    def paste_matrix(self, matrix_identifier):
        """Pega la matriz copiada desde el portapapeles en las casillas correspondientes."""
        try:
            # Obtener el frame de la matriz basado en el identificador
            matrix_frame = next((frame for frame in self.matrices if frame.identifier == matrix_identifier), None)
            if not matrix_frame:
                raise ValueError(f"No se encontró la matriz con identificador '{matrix_identifier}'.")

            # Leer el contenido del portapapeles
            clipboard_content = self.tab.clipboard_get()

            # Dividir las filas y columnas
            rows = clipboard_content.strip().split("\n")
            matrix_values = [row.split("\t") for row in rows]

            # Validar si la matriz pegada coincide con las dimensiones generadas
            if len(matrix_values) != len(matrix_frame.entries) or any(
                    len(row) != len(matrix_frame.entries[0]) for row in matrix_values
            ):
                raise ValueError("La matriz pegada no coincide con las dimensiones actuales.")

            # Rellenar las entradas de la matriz
            for i, row in enumerate(matrix_values):
                for j, value in enumerate(row):
                    matrix_frame.entries[i][j].delete(0, "end")
                    matrix_frame.entries[i][j].insert(0, value)

            messagebox.showinfo("Éxito", f"Matriz '{matrix_identifier}' pegada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo pegar la matriz: {e}")

    def copy_matrix(self, matrix_identifier):
        """Copia la matriz seleccionada al portapapeles en formato tabular."""
        try:
            # Obtener el frame de la matriz basado en el identificador
            matrix_frame = next((frame for frame in self.matrices if frame.identifier == matrix_identifier), None)
            if not matrix_frame:
                raise ValueError(f"No se encontró la matriz con identificador '{matrix_identifier}'.")

            # Leer los valores de la matriz
            matrix_str = ""
            for row in matrix_frame.entries:
                row_str = "\t".join(entry.get() or "0" for entry in row)
                matrix_str += row_str + "\n"

            # Copiar al portapapeles
            self.tab.clipboard_clear()
            self.tab.clipboard_append(matrix_str.strip())
            self.tab.update()  # Actualizar el portapapeles
            messagebox.showinfo("Copiado", f"Matriz '{matrix_identifier}' copiada al portapapeles.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar la matriz: {e}")

    def copy_result_to_clipboard(self):
        """Copia solo la matriz mostrada al portapapeles."""
        try:
            # Obtener el texto del label de resultados
            result_text = self.results_label.cget("text")
            if not result_text.strip():
                raise ValueError("No hay resultados para copiar.")

            # Extraer únicamente la matriz (asumiendo que comienza después de un salto de línea doble)
            matrix_start = result_text.find("\n\n") + 2
            if matrix_start <= 1:  # Si no encuentra el formato esperado
                raise ValueError("No se pudo encontrar una matriz válida en el resultado.")

            matrix_text = result_text[matrix_start:].strip()

            # Copiar la matriz al portapapeles
            self.tab.clipboard_clear()
            self.tab.clipboard_append(matrix_text)
            self.tab.update()  # Actualizar el portapapeles
            messagebox.showinfo("Copiado", "La matriz ha sido copiada al portapapeles.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar la matriz: {e}")

    def process_general_operation(self):
        """Procesa una operación general entre matrices."""
        try:
            # Leer la operación ingresada
            operation = self.operation_entry.get().strip()
            if not operation:
                raise ValueError("Debe ingresar una operación válida.")

            # Diccionario para almacenar las matrices con sus identificadores
            matrices_dict = {frame.identifier: np.array(self.get_matrix_values(frame), dtype=float)
                             for frame in self.matrices}

            # Validar que las matrices mencionadas en la operación existen
            for identifier in matrices_dict:
                operation = operation.replace(identifier, f"matrices_dict['{identifier}']")

            # Evaluar la operación
            result = eval(operation)

            # Validar el resultado (debe ser una matriz NumPy)
            if not isinstance(result, np.ndarray):
                raise ValueError("La operación no produjo una matriz válida.")

            # Mostrar el resultado
            self._display_result_general(result)

        except Exception as e:
            messagebox.showerror("Error", f"Error en la operación: {e}")

    def _display_result_general(self, result):
        """Muestra el resultado de una operación general entre matrices."""
        result_text = f"Resultado de la operación:\n\n{self._matrix_to_string(result)}"
        self.results_label.configure(text=result_text)
