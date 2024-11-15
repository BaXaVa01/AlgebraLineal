import customtkinter as ctk
from tkinter import messagebox
from utils.json_utils import guardar_input_operacion
from logic.biseccion_logic import *
import math
from components.table_widget import CTkTable  # Asegúrate de importar el widget CTkTable
from components.tooltip_widget import CTkToolTip  # Importa tu widget de tooltip

class BisectionTab:
    def __init__(self, tabview):
        self.tab = tabview.add("Bisección")
        
        # Inicializar la interfaz de usuario
        self.init_ui()

    def init_ui(self):
        # Etiqueta y campo de entrada para la función
        label_funcion = ctk.CTkLabel(self.tab, text="Función f(x):", font=("Arial", 14, "bold"))
        label_funcion.grid(row=0, column=0, pady=5, padx=20, sticky="w")
        self.funcion_input = ctk.CTkTextbox(self.tab, height=50, font=("Arial", 12))
        self.funcion_input.grid(row=1, column=0, pady=5, padx=20, sticky="w")
        # Botón y tooltip para Función f(x)
        btn_tooltip_funcion = ctk.CTkButton(self.tab, text="?", width=30, command=None)
        btn_tooltip_funcion.grid(row=1, column=1, pady=5, padx=(2, 0), sticky="w")  # Ajuste de padx
        CTkToolTip(btn_tooltip_funcion, message="Introduce la función matemática para f(x).")

        # Límite inferior (a)
        label_a = ctk.CTkLabel(self.tab, text="Límite inferior a:", font=("Arial", 14, "bold"))
        label_a.grid(row=2, column=0, pady=5, padx=20, sticky="w")
        self.a_entry = ctk.CTkEntry(self.tab, font=("Arial", 12))
        self.a_entry.grid(row=3, column=0, pady=5, padx=20, sticky="w")
                # Botón y tooltip para Límite inferior a
        btn_tooltip_a = ctk.CTkButton(self.tab, text="?", width=30, command=None)
        btn_tooltip_a.grid(row=3, column=1, pady=5, padx=(2, 0), sticky="w")  # Ajuste de padx
        CTkToolTip(btn_tooltip_a, message="Introduce el límite inferior del intervalo (a).")

        # Límite superior (b)
        label_b = ctk.CTkLabel(self.tab, text="Límite superior b:", font=("Arial", 14, "bold"))
        label_b.grid(row=4, column=0, pady=5, padx=20, sticky="w")
        self.b_entry = ctk.CTkEntry(self.tab, font=("Arial", 12))
        self.b_entry.grid(row=5, column=0, pady=5, padx=20, sticky="w")
                # Botón y tooltip para Límite superior b
        btn_tooltip_b = ctk.CTkButton(self.tab, text="?", width=30, command=None)
        btn_tooltip_b.grid(row=5, column=1, pady=5, padx=(2, 0), sticky="w")  # Ajuste de padx
        CTkToolTip(btn_tooltip_b, message="Introduce el límite superior del intervalo (b).")
        # Tolerancia (tol)
        label_tol = ctk.CTkLabel(self.tab, text="Tolerancia:", font=("Arial", 14, "bold"))
        label_tol.grid(row=6, column=0, pady=5, padx=20, sticky="w")
        self.tol_entry = ctk.CTkEntry(self.tab, font=("Arial", 12))
        self.tol_entry.grid(row=7, column=0, pady=5, padx=20, sticky="w")
                # Botón y tooltip para Tolerancia
        btn_tooltip_tol = ctk.CTkButton(self.tab, text="?", width=30, command=None)
        btn_tooltip_tol.grid(row=7, column=1, pady=5, padx=(2, 0), sticky="w")  # Ajuste de padx
        CTkToolTip(btn_tooltip_tol, message="Introduce la tolerancia aceptable para el error.")

        # Número máximo de iteraciones
        label_max_iter = ctk.CTkLabel(self.tab, text="Número máximo de iteraciones:", font=("Arial", 14, "bold"))
        label_max_iter.grid(row=8, column=0, pady=5, padx=20, sticky="w")
        self.max_iter_entry = ctk.CTkEntry(self.tab, font=("Arial", 12))
        self.max_iter_entry.grid(row=9, column=0, pady=5, padx=20, sticky="w")
        # Botón y tooltip para Número máximo de iteraciones
        btn_tooltip_max_iter = ctk.CTkButton(self.tab, text="?", width=30, command=None)
        btn_tooltip_max_iter.grid(row=9, column=1, pady=5, padx=(2, 0), sticky="w")  # Ajuste de padx
        CTkToolTip(btn_tooltip_max_iter, message="Introduce el número máximo de iteraciones permitidas.")


        # Botón para ejecutar el método de Bisección
        btn_ejecutar_biseccion = ctk.CTkButton(self.tab, text="Ejecutar Bisección", command=self.ejecutar_biseccion, font=("Arial", 12, "bold"))
        btn_ejecutar_biseccion.grid(row=10, column=0, pady=10)

        # Crear la tabla para mostrar los resultados de la bisección
        self.table = CTkTable(self.tab, columns=["Iteración", "a", "b", "c", "Error", "f(a)", "f(b)", "f(c)"])
        self.table.grid(row=13, column=1, pady=10, padx=20, sticky="nsew")

    def ejecutar_biseccion(self):
        try:
            # Obtener valores de entrada
            funcion = self.funcion_input.get("1.0", "end-1c").strip()
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            tol = float(self.tol_entry.get())
            max_iter = int(self.max_iter_entry.get())

            # Procesar la función y ejecutar el método de Bisección
            funcion_procesada = procesar_funcion(funcion)
            f = lambda x: eval(funcion_procesada, {"x": x, "math": math})
            raiz, error, pasos, iteraciones = biseccion(f, a, b, tol, max_iter)

            # Mostrar resultado en la tabla
            data = []
            for paso in pasos:
                iteracion, xi, xu, xr, Ea, yi, yu, yr = paso.split(", ")
                data.append([iteracion, xi, xu, xr, Ea, yi, yu, yr])

            self.table.insert_data(data)  # Insertamos los pasos en la tabla

            # Guardar la operación en el archivo JSON
            variables = {"a": a, "b": b, "tol": tol, "max_iter": max_iter}
            guardar_input_operacion("biseccion", funcion, variables, raiz)

        except ValueError as ve:
            self.table.clear_data()
            messagebox.showerror("Error", str(ve))
            
        except Exception as e:
            self.table.clear_data()
            messagebox.showerror("Error", str(ve))
