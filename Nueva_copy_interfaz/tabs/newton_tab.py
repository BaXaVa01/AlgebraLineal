import customtkinter as ctk
from utils.json_utils import guardar_input_operacion
from logic.newton_raphson_logic import *
from tkinter import messagebox
from components.table_widget import CTkTable

class NewtonRaphsonTab:
    def __init__(self, tabview):
        self.tab = tabview.add("Newton")
        
        # Inicializar la interfaz de usuario
        self.init_ui()

    def init_ui(self):
        # Etiqueta y campo de entrada para la función
        label_funcion = ctk.CTkLabel(self.tab, text="Función f(x):", font=("Arial", 14, "bold"))
        label_funcion.grid(row=0, column=0, pady=5, padx=20, sticky="w")
        self.funcion_input = ctk.CTkTextbox(self.tab, height=50, font=("Arial", 12))
        self.funcion_input.grid(row=1, column=0, pady=5, padx=20, sticky="w")

        # Valor inicial x0
        label_x0 = ctk.CTkLabel(self.tab, text="Valor inicial x0:", font=("Arial", 14, "bold"))
        label_x0.grid(row=2, column=0, pady=5, padx=20, sticky="w")
        self.x0_entry = ctk.CTkEntry(self.tab, font=("Arial", 12))
        self.x0_entry.grid(row=3, column=0, pady=5, padx=20, sticky="w")

        # Tolerancia (tol)
        label_tol = ctk.CTkLabel(self.tab, text="Tolerancia:", font=("Arial", 14, "bold"))
        label_tol.grid(row=4, column=0, pady=5, padx=20, sticky="w")
        self.tol_entry = ctk.CTkEntry(self.tab, font=("Arial", 12))
        self.tol_entry.grid(row=5, column=0, pady=5, padx=20, sticky="w")

        # Número máximo de iteraciones
        label_max_iter = ctk.CTkLabel(self.tab, text="Número máximo de iteraciones:", font=("Arial", 14, "bold"))
        label_max_iter.grid(row=6, column=0, pady=5, padx=20, sticky="w")
        self.max_iter_entry = ctk.CTkEntry(self.tab, font=("Arial", 12))
        self.max_iter_entry.grid(row=7, column=0, pady=5, padx=20, sticky="w")

        # Botón para ejecutar el método de Newton-Raphson
        btn_ejecutar_newton_raphson = ctk.CTkButton(self.tab, text="Calcular Raíz", command=self.ejecutar_newton_raphson, font=("Arial", 12, "bold"))
        btn_ejecutar_newton_raphson.grid(row=8, column=0, pady=10)

        # Crear la tabla para los resultados de las iteraciones
        self.table = CTkTable(self.tab, columns=["Iteración", "x", "f(x)", "f'(x)", "Error"])
        self.table.grid(row=9, column=0, pady=10, padx=20, sticky="nsew")

    def ejecutar_newton_raphson(self):
        try:
            # Obtener valores de entrada
            funcion = self.funcion_input.get("1.0", "end-1c").strip()
            x0 = float(self.x0_entry.get())
            tol = float(self.tol_entry.get())
            max_iter = int(self.max_iter_entry.get())

            # Ejecutar el método de Newton-Raphson
            resultado = newton_raphson(funcion, x0, tol, max_iter)
            raiz = resultado["raiz"]
            iteraciones = resultado["iteraciones"]

            # Mostrar resultados en la tabla
            data = []
            for i, iteracion in enumerate(iteraciones):
                # Verifica si las claves correctas existen en el diccionario de la iteración
                x = iteracion.get("x", "No disponible")
                f_x = iteracion.get("f(x)", "No disponible")
                f_prime_x = iteracion.get("f'(x)", "No disponible")
                error = iteracion.get("error", "No disponible")

                data.append([i+1, x, f_x, f_prime_x, error])

            # Insertar los datos en la tabla
            self.table.insert_data(data)

            # Guardar la operación en el archivo JSON
            variables = {"x0": x0, "tol": tol, "max_iter": max_iter}
            guardar_input_operacion("newton_raphson", funcion, variables, raiz)

        except ValueError as ve:
            messagebox.showerror("Error", f"Error de valor: {ve}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

