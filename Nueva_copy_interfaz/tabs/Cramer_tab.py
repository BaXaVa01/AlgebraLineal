import customtkinter as ctk
from tkinter import messagebox
import numpy as np
from fractions import Fraction

class MetodoCramer:
    def __init__(self, tabview):
        # Crear la pestaña para el Método de Cramer
        self.tab = tabview.add("Método de Cramer")

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

        # Botón para encontrar la solución
        self.solve_button = ctk.CTkButton(
            self.left_frame, text="Encontrar Solución", command=self.solve_system, state="disabled"
        )
        self.solve_button.pack(pady=10)

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
        self.matrix_frame = ctk.CTkScrollableFrame(self.main_frame)
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

        # Variables internas
        self.matrix_entries = []  # Entradas de la matriz
        self.num_variables = 0

    def generate_matrix(self):
        """Genera la matriz de entradas basada en la cantidad de variables."""
        try:
            self.num_variables = int(self.variables_entry.get())
            if self.num_variables <= 0:
                raise ValueError("La cantidad de variables debe ser mayor que 0.")

            # Limpiar cualquier contenido existente
            for widget in self.matrix_frame.winfo_children():
                widget.destroy()
            self.matrix_entries = []

            # Crear un frame para centrar la matriz
            center_frame = ctk.CTkFrame(self.matrix_frame)
            center_frame.grid(row=0, column=0, sticky="nsew")

            # Crear etiquetas para los índices de las columnas
            for j in range(self.num_variables + 1):  # Columnas = variables + 1 (términos independientes)
                index_label = ctk.CTkLabel(
                    center_frame,
                    text=f"x{j+1}" if j < self.num_variables else "b",
                    width=50,
                    anchor="center"
                )
                index_label.grid(row=0, column=j, padx=5, pady=5)

            # Crear la matriz de coeficientes y términos independientes
            for i in range(self.num_variables):
                row_entries = []
                for j in range(self.num_variables + 1):
                    entry = ctk.CTkEntry(center_frame, width=50, justify="center")
                    entry.grid(row=i + 1, column=j, padx=5, pady=5)
                    row_entries.append(entry)
                self.matrix_entries.append(row_entries)

            # Activar el botón de solución
            self.solve_button.configure(state="normal")
            self.copy_matrix_button.configure(state = "normal")
        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")

    def solve_system(self):
        """Calcula la solución utilizando el Método de Cramer y muestra el paso a paso."""
        try:
            # Leer la matriz de coeficientes y términos independientes
            coefficients, constants = self._read_matrix()

            # Validar que el sistema tenga una solución única
            det_main = np.linalg.det(coefficients)
            if np.isclose(det_main, 0):
                raise ValueError("El sistema no tiene solución única (determinante principal = 0).")

            # Calcular determinantes y soluciones usando el Método de Cramer
            steps = [f"Determinante principal (det): {det_main:.2f}"]
            solutions = []
            num_variables = len(coefficients)

            for i in range(num_variables):
                # Crear una copia de la matriz de coeficientes
                modified_matrix = coefficients.copy()

                # Reemplazar la columna i con el vector de términos independientes
                modified_matrix[:, i] = constants

                # Calcular el determinante de la matriz modificada
                det_i = np.linalg.det(modified_matrix)
                solution = det_i / det_main
                solutions.append(solution)

                # Registrar el paso a paso
                steps.append(f"\nPaso {i + 1}: Reemplazar columna {i + 1} con los términos independientes.")
                steps.append(f"Matriz modificada:\n{self._matrix_to_string(modified_matrix)}")
                steps.append(f"Determinante de la matriz modificada (det_{i + 1}): {det_i:.2f}")
                steps.append(f"x{i + 1} = det_{i + 1} / det = {det_i:.2f} / {det_main:.2f} = {solution:.2f}")

            # Mostrar los pasos y la solución final
            steps.append("\nSoluciones:")
            for i, solution in enumerate(solutions):
                steps.append(f"x{i + 1} = {solution:.2f}")

            self._display_output("\n".join(steps))
            messagebox.showinfo("Éxito", "Solución calculada correctamente. Revisa los pasos en la salida.")
        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida o sistema inconsistente: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"{e}")

    def _read_matrix(self):
        """Lee los valores de la matriz de entradas y los separa en A y B."""
        coefficients = []
        constants = []

        for row in self.matrix_entries:
            coeff_row = []
            for j in range(len(row) - 1):
                value = row[j].get().strip()
                if not value:
                    raise ValueError("Todas las entradas deben estar llenas.")
                coeff_row.append(float(Fraction(value)))
            coefficients.append(coeff_row)

            # Leer el término independiente
            constant_value = row[-1].get().strip()
            if not constant_value:
                raise ValueError("Todas las entradas deben estar llenas.")
            constants.append(float(Fraction(constant_value)))

        return np.array(coefficients), np.array(constants)

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

        output_label = ctk.CTkLabel(
            self.output_frame,
            text=content,
            justify="left",
            wraplength=680,
            font=("Arial", 14)
        )
        output_label.pack(padx=10, pady=10)

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
