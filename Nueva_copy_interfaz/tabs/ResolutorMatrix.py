import customtkinter as ctk
import numpy as np
from scipy.linalg import lu
from tkinter import messagebox


class EquationSolver:
    def __init__(self, tabview):
        # Crear la pestaña de ecuaciones
        self.tab = tabview.add("Factorización LU")

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

        # Botón para copiar la matriz
        self.copy_matrix_button = ctk.CTkButton(
            self.left_frame, text="Copiar Matriz", command=self.copy_matrix, state="disabled"
        )
        self.copy_matrix_button.pack(pady=10)


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

        # Tamaño de fuente para la salida
        self.font_size = 14  # Valor predeterminado

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

            # Activar los botones de solución
            self.solve_button.configure(state="normal")
            self.steps_button.configure(state="normal")
        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")

    def find_solution(self):
        """Resuelve el sistema de ecuaciones utilizando la matriz ingresada."""
        try:
            coefficients, constants = self._read_matrix()

            if self._check_equivalent_rows(coefficients):
                self._display_output("Equivalentes (Número infinito de soluciones)")
                return

            if self._check_parallel_rows(coefficients, constants):
                self._display_output("Rectas paralelas (Sistema sin solución)")
                return

            if np.linalg.det(coefficients) == 0:
                self._display_output("El sistema no tiene solución única (determinante = 0).")
                return

            solution = np.linalg.solve(coefficients, constants)

            # Mostrar la solución en el frame de salida
            self._display_output(f"Solución Encontrada:\n\n" +
                                 "\n".join([f"x{i+1} = {value:.2f}" for i, value in enumerate(solution)]))
        except ValueError as e:
            self._display_output(f"Error: {e}")
        except Exception as e:
            self._display_output(f"Error inesperado: {e}")

    def _check_parallel_rows(self, coefficients, constants):
        """Verifica si las filas representan rectas paralelas."""
        num_rows = coefficients.shape[0]
        for i in range(num_rows):
            for j in range(i + 1, num_rows):
                if np.allclose(coefficients[i] / coefficients[j],
                               coefficients[i][0] / coefficients[j][0]) and not np.isclose(constants[i] / constants[j],
                                                                                           constants[i]):
                    return True
        return False

    def show_steps(self):
        """Muestra el paso a paso del cálculo utilizando factorización LU."""
        try:
            coefficients, constants = self._read_matrix()

            # Paso 1: Mostrar matrices iniciales
            steps = ["Paso 1: Matriz de coeficientes A y vector de términos independientes B:"]
            steps.append(f"Matriz A:\n{coefficients}")
            steps.append(f"Vector B:\n{constants}")

            # Paso 2: Factorización LU
            P, L, U = lu(coefficients)
            steps.append("\nPaso 2: Factorización LU (A = L * U):")
            steps.append(f"Matriz de permutación P:\n{P}")
            steps.append(f"Matriz triangular inferior L:\n{L}")
            steps.append(f"Matriz triangular superior U:\n{U}")

            # Paso 3: Sustitución hacia adelante (L * y = P * B)
            Pb = np.dot(P, constants)
            y = np.linalg.solve(L, Pb)
            steps.append("\nPaso 3: Resolver L * y = P * B (sustitución hacia adelante):")
            steps.append(f"Vector P * B:\n{Pb}")
            steps.append(f"Vector y (resultado intermedio):\n{y}")

            # Paso 4: Sustitución hacia atrás (U * x = y)
            x = np.linalg.solve(U, y)
            steps.append("\nPaso 4: Resolver U * x = y (sustitución hacia atrás):")
            steps.append(f"Vector solución x:\n{x}")

            # Mostrar los pasos en el frame de salida
            self._display_output("\n".join(steps))
        except ValueError as e:
            self._display_output(f"Error: {e}")
        except Exception as e:
            self._display_output(f"Error inesperado: {e}")

    def _check_equivalent_rows(self, matrix):
        """Verifica si hay filas equivalentes en la matriz."""
        num_rows = matrix.shape[0]
        for i in range(num_rows):
            for j in range(i + 1, num_rows):
                if np.allclose(matrix[i] / matrix[j], matrix[i][0] / matrix[j][0]):
                    return True
        return False

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

    def _read_matrix(self):
        """Lee los valores de la matriz de entradas y los separa en A y B."""
        coefficients = []
        constants = []

        for row in self.matrix_entries:
            coeff_row = []
            for j in range(len(row) - 1):
                coeff_row.append(float(row[j].get()))
            coefficients.append(coeff_row)
            constants.append(float(row[-1].get()))

        return np.array(coefficients), np.array(constants)

    def _display_output(self, content):
        """Muestra el contenido en el frame de salida desplazable."""
        for widget in self.output_frame.winfo_children():
            widget.destroy()  # Limpiar cualquier salida anterior

        output_label = ctk.CTkLabel(self.output_frame, text=content, justify="left", wraplength=680, font=("Arial", self.font_size))
        output_label.pack(padx=10, pady=10)

    def adjust_font_size(self, value):
        """Ajusta dinámicamente el tamaño de la fuente para la salida."""
        self.font_size = int(value)
        # Refrescar la salida si ya hay contenido
        if self.output_frame.winfo_children():
            for widget in self.output_frame.winfo_children():
                widget.configure(font=("Arial", self.font_size))
