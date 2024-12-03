import customtkinter as ctk
import numpy as np
from fractions import Fraction
from tkinter import messagebox


class ComprobanteResultados:
    def __init__(self, tabview):
        # Crear la pestaña de Comprobación
        self.tab = tabview.add("Comprobante de Resultados")

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

        # Botón para pegar la matriz
        self.paste_matrix_button = ctk.CTkButton(
            self.left_frame, text="Pegar Matriz", command=self.paste_matrix, state="disabled"
        )
        self.paste_matrix_button.pack(pady=10)

        # Botón para comprobar la solución
        self.check_button = ctk.CTkButton(
            self.left_frame, text="Comprobar Resultados", command=self.check_solution, state="disabled"
        )
        self.check_button.pack(pady=10)
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

        # Variables internas
        self.matrix_entries = []  # Entradas de la matriz
        self.results_entries = []  # Entradas de resultados esperados

    def generate_matrix(self):
        """Genera la matriz de entradas, las etiquetas de índices, y las casillas para los valores a comprobar."""
        try:
            num_variables = int(self.variables_entry.get())
            if num_variables <= 0:
                raise ValueError("La cantidad de variables debe ser mayor que 0.")

            # Limpiar cualquier contenido existente en el frame
            for widget in self.matrix_frame.winfo_children():
                widget.destroy()
            self.matrix_entries = []

            # Crear un frame para organizar las matrices y entradas adicionales
            center_frame = ctk.CTkFrame(self.matrix_frame)
            center_frame.grid(row=0, column=0, sticky="nsew")

            # Crear etiquetas para los índices de las columnas (x1, x2, ..., b)
            for j in range(num_variables + 1):  # Columnas = variables + 1 (término independiente)
                index_label = ctk.CTkLabel(
                    center_frame,
                    text=f"x{j + 1}" if j < num_variables else "b",
                    width=50,
                    anchor="center"
                )
                index_label.grid(row=0, column=j, padx=5, pady=5)

            # Crear la matriz de coeficientes y términos independientes
            for i in range(num_variables):
                row_entries = []
                for j in range(num_variables + 1):
                    entry = ctk.CTkEntry(center_frame, width=50, justify="center")
                    entry.grid(row=i + 1, column=j, padx=5, pady=5)  # +1 para dejar espacio para las etiquetas
                    row_entries.append(entry)
                self.matrix_entries.append(row_entries)

            # Crear casillas para los valores a comprobar
            verify_label = ctk.CTkLabel(center_frame, text="Comprobar:")
            verify_label.grid(row=num_variables + 1, column=0, columnspan=num_variables, pady=10)

            self.verify_entries = []
            verify_frame = ctk.CTkFrame(center_frame)
            verify_frame.grid(row=num_variables + 2, column=0, columnspan=num_variables + 1, sticky="nsew", pady=10)

            for i in range(num_variables):
                entry = ctk.CTkEntry(verify_frame, width=50, justify="center")
                entry.grid(row=0, column=i, padx=5)
                self.verify_entries.append(entry)

            # Activar botones
            self.copy_matrix_button.configure(state="normal")
            self.paste_matrix_button.configure(state="normal")
            self.check_button.configure(state="normal")
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

    def check_solution(self):
        """Compara los resultados calculados con los valores ingresados en las casillas de comprobación."""
        try:
            # Leer la matriz de coeficientes y términos independientes
            coefficients, constants = self._read_matrix()

            # Resolver el sistema de ecuaciones
            calculated_results = np.linalg.solve(coefficients, constants)

            # Leer los valores ingresados en las casillas de comprobación
            verify_results = []
            for entry in self.verify_entries:
                value = entry.get()
                if value.strip() == "":
                    raise ValueError("Todas las casillas de comprobación deben estar llenas.")
                verify_results.append(float(Fraction(value)))

            # Comparar resultados calculados con los valores ingresados
            mismatches = []
            for i, (calculated, provided) in enumerate(zip(calculated_results, verify_results)):
                if not np.isclose(calculated, provided):
                    mismatches.append(f"x{i + 1}: Calculado = {calculated:.2f}, Ingresado = {provided}")

            # Mostrar resultados de la comparación
            if mismatches:
                mismatch_message = "\n".join(mismatches)
                messagebox.showwarning("Comprobación Fallida",
                                       f"Los siguientes valores no coinciden:\n{mismatch_message}")
            else:
                messagebox.showinfo("Éxito", "Todos los resultados coinciden.")
        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
        except np.linalg.LinAlgError:
            messagebox.showerror("Error", "El sistema no tiene solución única.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

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
    def adjust_font_size(self, value):
        """Ajusta dinámicamente el tamaño de la fuente para la salida."""
        self.font_size = int(value)
        # Refrescar la salida si ya hay contenido
        if self.output_frame.winfo_children():
            for widget in self.output_frame.winfo_children():
                widget.configure(font=("Arial", self.font_size))


