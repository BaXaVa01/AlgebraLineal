import customtkinter as ctk
import numpy as np
from fractions import Fraction
from tkinter import messagebox


class GaussJordanSolver:
    def __init__(self, tabview):
        # Crear la pestaña de Gauss-Jordan
        self.tab = tabview.add("Gauss-Jordan")

        # Configurar el sistema de grid para la pestaña principal
        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_columnconfigure((0, 1), weight=1)

        # Frame principal para organizar los elementos
        self.main_frame = ctk.CTkFrame(self.tab)
        self.main_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)

        # Frame izquierdo para botones y entrada
        self.left_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Entrada para cantidad de variables
        self.variables_label = ctk.CTkLabel(self.left_frame, text="Cantidad de Variables:")
        self.variables_label.pack(pady=5)
        self.variables_entry = ctk.CTkEntry(self.left_frame, width=100, placeholder_text="2")
        self.variables_entry.pack(pady=5)

        # Botón para generar la matriz de entradas
        self.generate_matrix_button = ctk.CTkButton(
            self.left_frame, text="Generar Matriz", command=self.generate_matrix
        )
        self.generate_matrix_button.pack(pady=10)

        # Botón para encontrar solución
        self.solve_button = ctk.CTkButton(
            self.left_frame, text="Encontrar Solución", command=self.find_solution, state="disabled"
        )
        self.solve_button.pack(pady=10)

        # Botón para mostrar el paso a paso
        self.steps_button = ctk.CTkButton(
            self.left_frame, text="Mostrar Paso a Paso", command=self.show_steps, state="disabled"
        )
        self.steps_button.pack(pady=10)
        # Botón para copiar la matriz
        self.copy_matrix_button = ctk.CTkButton(
            self.left_frame, text="Copiar Matriz", command=self.copy_matrix, state="disabled"
        )
        self.copy_matrix_button.pack(pady=10)
        # Botón para pegar la matriz
        self.paste_matrix_button = ctk.CTkButton(
            self.left_frame, text="Pegar Matriz", command=self.paste_matrix
        )
        self.paste_matrix_button.pack(pady=10)
        # Deslizador para ajustar el tamaño de la fuente

        self.font_slider_label = ctk.CTkLabel(self.left_frame, text="Tamaño de Fuente:")
        self.font_slider_label.pack(pady=5)
        self.font_slider = ctk.CTkSlider(
            self.left_frame, from_=10, to=30, command=self.adjust_font_size
        )
        self.font_slider.set(14)  # Valor predeterminado
        self.font_slider.pack(pady=5)

        # Frame derecho para la matriz
        self.matrix_frame = ctk.CTkFrame(self.main_frame)
        self.matrix_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Configurar el centrado de la matriz
        self.matrix_frame.grid_rowconfigure(0, weight=1)
        self.matrix_frame.grid_columnconfigure(0, weight=1)

        # Configurar el frame de salida desplazable
        self.output_frame = ctk.CTkScrollableFrame(self.tab, width=700, height=300)
        self.output_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)

        # Configurar pesos para ajustar el contenido automáticamente
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)
        self.tab.grid_rowconfigure(1, weight=1)

    def generate_matrix(self):
        """Genera la matriz de entradas basada en la cantidad de variables."""
        try:
            num_variables = int(self.variables_entry.get())
            if num_variables <= 0:
                raise ValueError("La cantidad de variables debe ser mayor que 0.")

            # Limpiar cualquier matriz existente
            for widget in self.matrix_frame.winfo_children():
                widget.destroy()
            self.matrix_entries = []

            # Crear un frame para centrar la matriz
            center_frame = ctk.CTkFrame(self.matrix_frame)
            center_frame.grid(row=0, column=0, sticky="nsew")

            for i in range(num_variables):
                row_entries = []
                for j in range(num_variables + 1):  # Columnas = variables + 1 (términos independientes)
                    entry = ctk.CTkEntry(center_frame, width=50, justify="center")
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    row_entries.append(entry)
                self.matrix_entries.append(row_entries)

            # Activar los botones de solución y copia
            self.solve_button.configure(state="normal")
            self.steps_button.configure(state="normal")
            self.copy_matrix_button.configure(state="normal")
        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")

    def copy_matrix(self):
        """Copia la matriz generada al portapapeles en formato tabular."""
        try:
            # Leer la matriz
            matrix_str = ""
            for row in self.matrix_entries:
                row_str = "\t".join(entry.get() or "0" for entry in row)
                matrix_str += row_str + "\n"

            # Copiar al portapapeles
            self.tab.clipboard_clear()
            self.tab.clipboard_append(matrix_str.strip())
            self.tab.update()  # Actualizar el portapapeles
            messagebox.showinfo("Copiado", "Matriz copiada al portapapeles.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar la matriz: {e}")

    def find_solution(self):
        """Resuelve el sistema de ecuaciones utilizando el método de Gauss-Jordan."""
        try:
            # Leer la matriz aumentada (coeficientes y términos independientes)
            coefficients, constants = self._read_matrix()
            augmented_matrix = np.hstack([coefficients, constants.reshape(-1, 1)])
            augmented_matrix = augmented_matrix.astype(float)  # Asegurarse de que los valores sean float

            num_rows, num_cols = augmented_matrix.shape

            # Gauss-Jordan Elimination
            for i in range(num_rows):
                # Verificar si el pivote es 0, buscar otra fila para intercambiar
                if augmented_matrix[i, i] == 0:
                    for j in range(i + 1, num_rows):
                        if augmented_matrix[j, i] != 0:
                            augmented_matrix[[i, j]] = augmented_matrix[[j, i]]
                            break
                    else:
                        self._display_output("El sistema no tiene solución (fila con todos ceros en los coeficientes).")
                        return

                # Normalizar la fila actual para que el pivote sea 1
                augmented_matrix[i] /= augmented_matrix[i, i]

                # Hacer 0 todos los demás valores en la columna del pivote
                for j in range(num_rows):
                    if i != j:
                        factor = augmented_matrix[j, i]
                        augmented_matrix[j] -= factor * augmented_matrix[i]

            # Verificar consistencia de la matriz
            for i in range(num_rows):
                if np.allclose(augmented_matrix[i, :-1], 0) and not np.isclose(augmented_matrix[i, -1], 0):
                    self._display_output(
                        "El sistema no tiene solución (inconsistencia en los términos independientes).")
                    return

            # Extraer la solución de la última columna
            solution = augmented_matrix[:, -1]

            # Mostrar la solución
            solution_str = "\n".join(
                [f"x{i + 1} = {Fraction(value).limit_denominator()}" for i, value in enumerate(solution)])
            self._display_output(f"Solución Encontrada:\n\n{solution_str}")
        except ValueError as e:
            self._display_output(f"Error: {e}")
        except Exception as e:
            self._display_output(f"Error inesperado: {e}")

    def show_steps(self):
        """Muestra el paso a paso del cálculo utilizando el método de Gauss-Jordan."""
        try:
            # Leer la matriz aumentada (coeficientes y términos independientes)
            coefficients, constants = self._read_matrix()
            augmented_matrix = np.hstack([coefficients, constants.reshape(-1, 1)])
            augmented_matrix = augmented_matrix.astype(float)  # Asegurarse de que los valores sean float

            num_rows, num_cols = augmented_matrix.shape
            steps = []  # Lista para registrar los pasos

            # Gauss-Jordan Elimination con registro de pasos
            for i in range(num_rows):
                steps.append(f"Paso {len(steps) + 1}: Matriz actual:\n{self._matrix_to_string(augmented_matrix)}")

                # Verificar si el pivote es 0, buscar otra fila para intercambiar
                if augmented_matrix[i, i] == 0:
                    for j in range(i + 1, num_rows):
                        if augmented_matrix[j, i] != 0:
                            augmented_matrix[[i, j]] = augmented_matrix[[j, i]]
                            steps.append(
                                f"Intercambio de fila {i + 1} con fila {j + 1}:\n{self._matrix_to_string(augmented_matrix)}")
                            break
                    else:
                        steps.append(
                            f"El sistema no tiene solución (fila {i + 1} tiene todos ceros en los coeficientes).")
                        self._display_output("\n".join(steps))
                        return

                # Normalizar la fila actual para que el pivote sea 1
                pivot = augmented_matrix[i, i]
                augmented_matrix[i] /= pivot
                steps.append(
                    f"Normalización de fila {i + 1} (pivote = {pivot}):\n{self._matrix_to_string(augmented_matrix)}")

                # Hacer 0 todos los demás valores en la columna del pivote
                for j in range(num_rows):
                    if i != j:
                        factor = augmented_matrix[j, i]
                        augmented_matrix[j] -= factor * augmented_matrix[i]
                        steps.append(
                            f"Eliminación en fila {j + 1} usando fila {i + 1} (factor = {factor}):\n{self._matrix_to_string(augmented_matrix)}")

            # Verificar consistencia de la matriz
            for i in range(num_rows):
                if np.allclose(augmented_matrix[i, :-1], 0) and not np.isclose(augmented_matrix[i, -1], 0):
                    steps.append(f"El sistema no tiene solución (fila {i + 1} inconsistente).")
                    self._display_output("\n".join(steps))
                    return

            # Mostrar los pasos y la solución final
            solution = augmented_matrix[:, -1]
            steps.append("Matriz final (forma escalonada reducida):\n" + self._matrix_to_string(augmented_matrix))
            solution_str = "\n".join(
                [f"x{i + 1} = {Fraction(value).limit_denominator()}" for i, value in enumerate(solution)])
            steps.append(f"Solución Final:\n{solution_str}")

            # Mostrar todos los pasos en el output_frame
            self._display_output("\n".join(steps))
        except ValueError as e:
            self._display_output(f"Error: {e}")
        except Exception as e:
            self._display_output(f"Error inesperado: {e}")

    def _read_matrix(self):
        """Lee los valores de la matriz de entradas y los separa en A y B."""
        coefficients = []
        constants = []

        for row in self.matrix_entries:
            coeff_row = []
            for j in range(len(row) - 1):
                coeff_row.append(Fraction(row[j].get()))
            coefficients.append(coeff_row)
            constants.append(Fraction(row[-1].get()))

        return np.array(coefficients), np.array(constants)

    def _matrix_to_string(self, matrix):
        """Convierte una matriz en un formato de texto para su visualización."""
        rows = []
        for row in matrix:
            formatted_row = "\t".join(f"{Fraction(value).limit_denominator()}" for value in row)
            rows.append(formatted_row)
        return "\n".join(rows)

    def _display_output(self, content):
        """Muestra el contenido en el frame de salida desplazable."""
        for widget in self.output_frame.winfo_children():
            widget.destroy()  # Limpiar cualquier salida anterior

        output_label = ctk.CTkLabel(self.output_frame, text=content, justify="left", wraplength=680, font=("Arial", 14))
        output_label.pack(padx=10, pady=10)
    def adjust_font_size(self, value):
        """Ajusta dinámicamente el tamaño de la fuente para la salida."""
        self.font_size = int(value)
        # Refrescar la salida si ya hay contenido
        if self.output_frame.winfo_children():
            for widget in self.output_frame.winfo_children():
                widget.configure(font=("Arial", self.font_size))


    def paste_matrix(self):
        """Pega la matriz copiada desde el portapapeles en las casillas correspondientes."""
        try:
            # Leer el contenido del portapapeles
            clipboard_content = self.tab.clipboard_get()

            # Dividir las filas y columnas
            rows = clipboard_content.strip().split("\n")
            matrix_values = [row.split("\t") for row in rows]

            # Validar si la matriz pegada coincide con las dimensiones generadas
            if len(matrix_values) != len(self.matrix_entries) or any(
                    len(row) != len(self.matrix_entries[0]) for row in matrix_values
            ):
                raise ValueError("La matriz pegada no coincide con las dimensiones actuales.")

            # Rellenar las entradas de la matriz
            for i, row in enumerate(matrix_values):
                for j, value in enumerate(row):
                    self.matrix_entries[i][j].delete(0, "end")
                    self.matrix_entries[i][j].insert(0, value)

            messagebox.showinfo("Éxito", "Matriz pegada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo pegar la matriz: {e}")