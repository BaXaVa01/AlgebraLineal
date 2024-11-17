import customtkinter as ctk
from utils.json_utils import guardar_input_operacion, obtener_ultimo_indice
from utils.git_utils import generar_gif_desde_json
from logic.newton_raphson_logic import newton_raphson
from tkinter import messagebox
from components.table_widget import CTkTable
from components.sidebar import FloatingSidebar
from components.graph_widget import GraphWidget
from components.Math_renderer_widget import MathRendererWidget, procesar_formula
from sympy import symbols, sympify, lambdify
import os

# Definir rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "files", "operaciones.json")

class NewtonRaphsonTab:
    def __init__(self, tabview):
        self.tab = tabview.add("Newton")

        # Configurar el layout adaptable
        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)
        self.tab.grid_columnconfigure(1, weight=4)  # Más peso al graficador (panel derecho)

        # Inicializar la interfaz de usuario
        self.init_ui()

    def init_ui(self):
        # Contenedor principal izquierdo (Inputs y Tabla)
        self.left_frame = ctk.CTkFrame(self.tab)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.left_frame.grid_rowconfigure(12, weight=1)  # Expandir tabla verticalmente
        self.left_frame.grid_columnconfigure(0, weight=1)

        # Contenedor principal derecho (Consolas y Graficador)
        self.right_frame = ctk.CTkFrame(self.tab)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid_rowconfigure(0, weight=2)  # Graficador
        self.right_frame.grid_rowconfigure(1, weight=1)  # Consolas
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Función f(x)
        label_funcion = ctk.CTkLabel(self.left_frame, text="Función f(x):", font=("Arial", 14, "bold"), anchor="center")
        label_funcion.grid(row=0, column=0, columnspan=2, pady=5, padx=5)
        self.funcion_input = ctk.CTkTextbox(self.left_frame, height=40, font=("Arial", 12), width=300)
        self.funcion_input.grid(row=1, column=0, pady=5, padx=5, sticky="ew")

        # Evento KeyRelease para actualizar el MathRendererWidget
        self.funcion_input.bind("<KeyRelease>", self.update_math_renderer)

        # Widget MathRendererWidget
        self.math_renderer_widget = MathRendererWidget(self.left_frame, width=300, height=150)
        self.math_renderer_widget.grid(row=2, column=0, pady=10, columnspan=2, sticky="ew")

        # Valor inicial (x0)
        label_x0 = ctk.CTkLabel(self.left_frame, text="Valor inicial (x0):", font=("Arial", 14, "bold"), anchor="center")
        label_x0.grid(row=3, column=0, columnspan=2, pady=5, padx=5)
        self.x0_entry = ctk.CTkEntry(self.left_frame, font=("Arial", 12), width=300)
        self.x0_entry.grid(row=4, column=0, pady=5, padx=5, sticky="ew")

        # Tolerancia
        label_tol = ctk.CTkLabel(self.left_frame, text="Tolerancia:", font=("Arial", 14, "bold"), anchor="center")
        label_tol.grid(row=5, column=0, columnspan=2, pady=5, padx=5)
        self.tol_entry = ctk.CTkEntry(self.left_frame, font=("Arial", 12), width=300)
        self.tol_entry.grid(row=6, column=0, pady=5, padx=5, sticky="ew")

        # Número máximo de iteraciones
        label_max_iter = ctk.CTkLabel(self.left_frame, text="Máx. Iteraciones:", font=("Arial", 14, "bold"), anchor="center")
        label_max_iter.grid(row=7, column=0, columnspan=2, pady=5, padx=5)
        self.max_iter_entry = ctk.CTkEntry(self.left_frame, font=("Arial", 12), width=300)
        self.max_iter_entry.grid(row=8, column=0, pady=5, padx=5, sticky="ew")

        # Botón para ejecutar
        btn_calcular = ctk.CTkButton(self.left_frame, text="Calcular", command=self.ejecutar_newton_raphson)
        btn_calcular.grid(row=9, column=0, pady=10, padx=5, sticky="ew")

        # Tabla de resultados
        self.table = CTkTable(self.left_frame, columns=["Iteración", "x", "f(x)", "f'(x)", "Error"])
        self.table.grid(row=12, column=0, pady=10, sticky="nsew", columnspan=2)

        # Configurar graficador en el panel derecho
        self.graph_widget = GraphWidget(self.right_frame)
        self.graph_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        # Configurar consolas en el panel derecho
        self.console_frame = ctk.CTkFrame(self.right_frame, fg_color="gray15", corner_radius=8)
        self.console_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.console_label = ctk.CTkLabel(self.console_frame, text="Consolas", font=("Arial", 14, "bold"))
        self.console_label.pack(pady=5)

        # Sidebar para mostrar GIFs
        self.sidebar = FloatingSidebar(self.tab, title="Gifs Newton-Raphson", from_right=True, width=250, height=500)
        self.sidebar.place(x=self.left_frame.winfo_width() - 40, y=0)

    def update_math_renderer(self, event):
        """
        Actualiza el MathRendererWidget con la fórmula procesada.
        """
        funcion = self.funcion_input.get("1.0", "end-1c").strip()
        try:
            funcion_procesada = procesar_formula(funcion)
            self.math_renderer_widget.update_text(funcion_procesada)
        except Exception as e:
            self.math_renderer_widget.update_text(f"Error: {e}")

    def ejecutar_newton_raphson(self):
        try:
            # Mostrar la sidebar
            self.sidebar.toggle_sidebar()

            # Obtener valores de entrada
            funcion = self.funcion_input.get("1.0", "end-1c").strip()
            x0 = float(self.x0_entry.get())
            tol = float(self.tol_entry.get())
            max_iter = int(self.max_iter_entry.get())

            # Crear función evaluable utilizando sympy y numpy
            x = symbols("x")
            try:
                expr = sympify(funcion)
                f = lambdify(x, expr, "numpy")
                f_prime = lambdify(x, expr.diff(x), "numpy")
            except Exception as e:
                raise ValueError(f"Error al procesar la función: {e}")

            # Llamar al método de Newton-Raphson
            raiz, pasos = newton_raphson(f, f_prime, x0, tol, max_iter)

            # Graficar la función en el widget
            self.graph_widget.plot_function(f, x_range=(x0 - 5, x0 + 5))

            # Mostrar resultados en la tabla
            data = []
            for paso in pasos:
                iteracion, xi, fi, f_prime_i, error = paso
                data.append([iteracion, xi, fi, f_prime_i, error])
            self.table.insert_data(data)

            # Guardar la operación en el archivo JSON
            variables = {"x0": x0, "tol": tol, "max_iter": max_iter}
            guardar_input_operacion("newton_raphson", funcion, variables, raiz)

            # Generar el GIF y mostrarlo en la sidebar
            indice = obtener_ultimo_indice(JSON_PATH, "newton_raphson")

            def mostrar_gif_en_sidebar(gif_path):
                if gif_path:
                    self.sidebar.show_single_gif(gif_path)
                else:
                    messagebox.showerror("Error", "No se pudo generar el GIF.")

            generar_gif_desde_json("newton_raphson", indice, callback=mostrar_gif_en_sidebar)

        except ValueError as ve:
            self.table.clear_data()
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            self.table.clear_data()
            messagebox.showerror("Error", str(e))



