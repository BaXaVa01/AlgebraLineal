import customtkinter as ctk
from tkinter import messagebox
from utils.json_utils import guardar_input_operacion
from logic.biseccion_logic import *
import math
from components.table_widget import CTkTable  # Asegúrate de importar el widget CTkTable
from components.tooltip_widget import CTkToolTip  # Importa el widget para tooltips
from components.sidebar import FloatingSidebar
from utils.git_utils import generar_gif_desde_json
from utils.json_utils import obtener_ultimo_indice
from components.graph_widget import GraphWidget  # Importar el widget para graficar
from components.Math_renderer_widget import MathRendererWidget,procesar_formula # Importar el widget actualizado
import os
from sympy import sympify, symbols, lambdify

# Definir rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "files", "operaciones.json")


class BisectionTab:
    def __init__(self, tabview):
        self.tab = tabview.add("Bisección")

        # Configurar el layout adaptable
        self.tab.grid_rowconfigure(0, weight=1)  # Expandir widgets verticalmente
        self.tab.grid_columnconfigure(0, weight=1)  # Panel izquierdo ocupa más espacio
        self.tab.grid_columnconfigure(1, weight=4)  # Panel derecho para consolas y graficador

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

        # Botón y tooltip para Función f(x)
        btn_tooltip_funcion = ctk.CTkButton(self.left_frame, text="?", width=30, command=None)
        btn_tooltip_funcion.grid(row=1, column=1, pady=5, padx=(2, 0), sticky="w")
        CTkToolTip(btn_tooltip_funcion, message="Introduce la función matemática para f(x).")

        # Widget MathRendererWidget debajo de la consola de entrada de función
        self.math_renderer_widget = MathRendererWidget(self.left_frame, width=300, height=150)
        self.math_renderer_widget.grid(row=2, column=0, pady=10, columnspan=2, sticky="ew")

        # Límite inferior (a)
        label_a = ctk.CTkLabel(self.left_frame, text="Límite inferior (a):", font=("Arial", 14, "bold"), anchor="center")
        label_a.grid(row=3, column=0, columnspan=2, pady=5, padx=5)
        self.a_entry = ctk.CTkEntry(self.left_frame, font=("Arial", 12), width=300)
        self.a_entry.grid(row=4, column=0, pady=5, padx=(325,300), sticky="ew")

        # Botón y tooltip para Límite inferior (a)
        btn_tooltip_a = ctk.CTkButton(self.left_frame, text="?", width=30, command=None)
        btn_tooltip_a.grid(row=4, column=1, pady=5, padx=(2, 0), sticky="w")
        CTkToolTip(btn_tooltip_a, message="Introduce el límite inferior del intervalo (a).")

        # Límite superior (b)
        label_b = ctk.CTkLabel(self.left_frame, text="Límite superior (b):", font=("Arial", 14, "bold"), anchor="center")
        label_b.grid(row=5, column=0, columnspan=2, pady=5, padx=5)
        self.b_entry = ctk.CTkEntry(self.left_frame, font=("Arial", 12), width=300)
        self.b_entry.grid(row=6, column=0, pady=5, padx=(325,300), sticky="ew")

        # Botón y tooltip para Límite superior (b)
        btn_tooltip_b = ctk.CTkButton(self.left_frame, text="?", width=30, command=None)
        btn_tooltip_b.grid(row=6, column=1, pady=5, padx=(2, 0), sticky="w")
        CTkToolTip(btn_tooltip_b, message="Introduce el límite superior del intervalo (b).")

        # Tolerancia
        label_tol = ctk.CTkLabel(self.left_frame, text="Tolerancia:", font=("Arial", 14, "bold"), anchor="center")
        label_tol.grid(row=7, column=0, columnspan=2, pady=5, padx=5)
        self.tol_entry = ctk.CTkEntry(self.left_frame, font=("Arial", 12), width=300)
        self.tol_entry.grid(row=8, column=0, pady=5, padx=(325,300), sticky="ew")

        # Botón y tooltip para Tolerancia
        btn_tooltip_tol = ctk.CTkButton(self.left_frame, text="?", width=30, command=None)
        btn_tooltip_tol.grid(row=8, column=1, pady=5, padx=(2, 0), sticky="w")
        CTkToolTip(btn_tooltip_tol, message="Introduce la tolerancia aceptable para el error.")

        # Número máximo de iteraciones
        label_max_iter = ctk.CTkLabel(self.left_frame, text="Número máximo de iteraciones:", font=("Arial", 14, "bold"), anchor="center")
        label_max_iter.grid(row=9, column=0, columnspan=2, pady=5, padx=5)
        self.max_iter_entry = ctk.CTkEntry(self.left_frame, font=("Arial", 12), width=300)
        self.max_iter_entry.grid(row=10, column=0, pady=5, padx=(325,300), sticky="ew")

        # Botón y tooltip para Número máximo de iteraciones
        btn_tooltip_max_iter = ctk.CTkButton(self.left_frame, text="?", width=30, command=None)
        btn_tooltip_max_iter.grid(row=10, column=1, pady=5, padx=(2, 0), sticky="w")
        CTkToolTip(btn_tooltip_max_iter, message="Introduce el número máximo de iteraciones permitidas.")

        # Botón para ejecutar el método de Bisección
        btn_ejecutar_biseccion = ctk.CTkButton(self.left_frame, text="Ejecutar Bisección", command=self.ejecutar_biseccion)
        btn_ejecutar_biseccion.grid(row=11, column=0, pady=10, padx=5, sticky="ew")

        # Tabla de resultados
        self.table = CTkTable(self.left_frame, columns=["Iteración", "a", "b", "c", "Error", "f(a)", "f(b)", "f(c)"])
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
        self.sidebar = FloatingSidebar(self.tab, title="Gifs Bisección", from_right=True, width=250, height=500)
        self.sidebar.place(x=self.left_frame.winfo_width() - 40, y=0)
    def update_math_renderer(self, event):
        """
        Actualiza el MathRendererWidget con la fórmula procesada.
        """
        funcion = self.funcion_input.get("1.0", "end-1c").strip()
        try:
            # Procesar la fórmula antes de renderizar
            funcion_procesada = procesar_formula(funcion)
            self.math_renderer_widget.update_text(funcion_procesada)
        except Exception as e:
            self.math_renderer_widget.update_text(f"Error: {e}")





    def ejecutar_biseccion(self, boolean=False):
        try:
            self.sidebar.toggle_sidebar()

            # Obtener valores de entrada
            funcion = self.funcion_input.get("1.0", "end-1c").strip()
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            tol = float(self.tol_entry.get())
            max_iter = int(self.max_iter_entry.get())

            x = symbols("x")
            expr = sympify(funcion)
            f = lambdify(x, expr, "numpy")

            raiz, error, pasos, iteraciones = biseccion(f, a, b, tol, max_iter)

            self.graph_widget.plot_function(f, x_range=(a, b))

            data = []
            for paso in pasos:
                iteracion, xi, xu, xr, Ea, yi, yu, yr = paso.split(", ")
                data.append([iteracion, xi, xu, xr, Ea, yi, yu, yr])
            self.table.insert_data(data)

            variables = {"a": a, "b": b, "tol": tol, "max_iter": max_iter}
            guardar_input_operacion("biseccion", funcion, variables, raiz)

            indice = obtener_ultimo_indice(JSON_PATH, "biseccion")

            def mostrar_gif_en_sidebar(gif_path):
                if gif_path:
                    self.sidebar.show_single_gif(gif_path)
                else:
                    messagebox.showerror("Error", "No se pudo generar el GIF.")

            # Pasar el content_frame de la sidebar como target para la barra de progreso
            generar_gif_desde_json("biseccion", indice, gif_frame=self.sidebar.scrollable_gif_frame, callback=mostrar_gif_en_sidebar)

        except ValueError as ve:
            self.table.clear_data()
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            self.table.clear_data()
            messagebox.showerror("Error", str(e))


