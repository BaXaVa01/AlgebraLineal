import customtkinter as ctk  # Librería para la interfaz gráfica
from sympy import symbols, Eq, solve, sin, cos, tan, log, deg, simplify, latex  # sympy para manipulación simbólica de ecuaciones
from tkinter import messagebox  # Para mostrar mensajes de error
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Para renderizar gráficos en Tkinter
import matplotlib.pyplot as plt  # Para crear gráficos y renderizar LaTeX


class EcuacionesTab:
    def __init__(self, tabview):
        """Inicializa la pestaña única para resolver ecuaciones."""
        self.tab = tabview.add("Resolver Ecuaciones")  # Agrega una nueva pestaña llamada "Resolver Ecuaciones"
        self.history = []  # Lista para guardar el historial de ecuaciones resueltas
        self.setup_ui()  # Llama al método para configurar la interfaz gráfica

    def setup_ui(self):
        """Configura la interfaz gráfica de usuario."""
        # Configuración de diseño general de la pestaña
        self.tab.grid_rowconfigure(2, weight=1)  # Dos filas: una para entrada/resultados, otra para historial
        self.tab.grid_columnconfigure(0, weight=2)  # Columna izquierda más amplia para los resultados
        self.tab.grid_columnconfigure(1, weight=1)  # Columna derecha más estrecha para el historial

        # Frame superior para la entrada de ecuaciones
        self.input_frame = ctk.CTkFrame(self.tab, fg_color="gray80", corner_radius=10)
        self.input_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.input_frame.grid_columnconfigure(0, weight=1)

        # Campo de entrada para la ecuación
        self.equation_entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Ingresa tu ecuación aquí (ej: 2*cos(x)*tan(x) - 1 = 0)", 
            height=50
        )
        self.equation_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Botón para resolver la ecuación
        self.solve_button = ctk.CTkButton(
            self.input_frame, 
            text="Resolver", 
            command=self.solve_equation, 
            corner_radius=10
        )
        self.solve_button.grid(row=0, column=1, padx=10, pady=10)

        # Frame para mostrar los resultados en formato LaTeX
        self.results_frame = ctk.CTkFrame(self.tab, fg_color="white", corner_radius=10)
        self.results_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)

        # Canvas para renderizar los resultados
        self.canvas_frame = ctk.CTkFrame(self.results_frame, fg_color="white")
        self.canvas_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Frame para el historial de ecuaciones
        self.history_frame = ctk.CTkFrame(self.tab, fg_color="white", corner_radius=10)
        self.history_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)
        self.history_frame.grid_rowconfigure(0, weight=1)
        self.history_frame.grid_columnconfigure(0, weight=1)

        # Etiqueta para mostrar el historial
        self.history_label = ctk.CTkLabel(
            self.history_frame, 
            text="Historial (Últimas 3)", 
            justify="left", 
            anchor="nw", 
            font=("Arial", 14), 
            wraplength=300
        )
        self.history_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    def solve_equation(self):
        """Resuelve la ecuación ingresada y muestra los pasos y resultados en formato LaTeX."""
        # Obtener la entrada del usuario desde el campo de texto
        equation_input = self.equation_entry.get()

        if not equation_input:  # Validar que el campo no esté vacío
            messagebox.showerror("Error", "Por favor, ingresa una ecuación.")
            return

        try:
            # Definir la variable simbólica
            x = symbols('x')

            # Separar la ecuación en lado izquierdo y derecho si incluye un "="
            if "=" in equation_input:
                left, right = equation_input.split("=")
                equation = Eq(simplify(left), simplify(right))
            else:  # Si no tiene "=", se asume que se iguala a 0
                equation = Eq(simplify(equation_input), 0)

            # Resolver la ecuación
            solutions = solve(equation, x)

            # Determinar si contiene funciones trigonométricas
            is_trigonometric = any(func in equation_input for func in ["sin", "cos", "tan"])

            # Convertir las soluciones a valores numéricos
            numerical_solutions = [sol.evalf() for sol in solutions]

            # Crear la representación LaTeX de la ecuación
            equation_latex = f"${latex(equation)}$"
            solutions_latex = ""
            if is_trigonometric:  # Si la ecuación es trigonométrica, convertir soluciones a grados
                solutions_in_degrees = [round(float(deg(sol.evalf())) % 360, 5) for sol in numerical_solutions]
                solutions_latex = "Soluciones (en grados): " + ", ".join([f"{sol}°" for sol in solutions_in_degrees])
            else:  # Para ecuaciones algebraicas o logarítmicas
                solutions_latex = "Soluciones: " + ", ".join([f"{round(sol, 5)}" for sol in numerical_solutions])

            # Renderizar los resultados en LaTeX
            self.render_latex(equation_latex, solutions_latex)

            # Guardar en el historial
            self.add_to_history(equation_input, solutions_latex)

        except Exception as e:
            # Mostrar un mensaje de error si no se puede resolver la ecuación
            messagebox.showerror("Error", f"No se pudo resolver la ecuación: {e}")

    def render_latex(self, equation_latex, solutions_latex):
        """Renderiza la ecuación y las soluciones en formato LaTeX."""
        # Limpiar el canvas previo
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        # Crear una figura con matplotlib
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.axis("off")  # Ocultar los ejes
        ax.text(0.5, 0.7, equation_latex, fontsize=16, ha="center", va="center")
        ax.text(0.5, 0.3, solutions_latex, fontsize=14, ha="center", va="center")

        # Integrar el canvas en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)
        canvas.draw()

    def add_to_history(self, equation_input, solutions_latex):
        """Añade la ecuación y su solución al historial."""
        # Formatear una entrada para el historial
        history_entry = f"Ecuación: {equation_input}\nSolución: {solutions_latex}"

        # Mantener solo las últimas 3 entradas
        self.history.insert(0, history_entry)
        if len(self.history) > 3:
            self.history.pop()

        # Actualizar la etiqueta del historial
        self.update_history()

    def update_history(self):
        """Actualiza el contenido del historial en la interfaz."""
        history_text = "\n\n".join(self.history)  # Unir las entradas con doble salto de línea
        self.history_label.configure(text=f"Historial (Últimas 3):\n\n{history_text}")
