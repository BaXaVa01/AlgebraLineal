import customtkinter as ctk
from tkinter import messagebox
from components.Math_renderer_widget import MathRendererWidget, procesar_formula
from components.table_widget import CTkTable
from components.graph_widget import GraphWidget
import numpy as np

class CustomTab:
    def __init__(self, tabview, tab_name, input_fields, table_columns, 
                 execute_callback=None, plot_step_callback=None):
        """
        Constructor para inicializar una pestaña dentro de un CTkTabview o CTkFrame.
        :param tabview: Puede ser un CTkTabview o un CTkFrame.
        :param tab_name: Nombre de la pestaña (solo aplica para CTkTabview).
        """
        self.inputs = {}
        self.current_step = 0
        self.previous_artists = []
        self.execute_callback = execute_callback  # Callback para ejecutar cálculos
        self.plot_step_callback = plot_step_callback  # Callback para graficar pasos

        # Determinar si `tabview` es un CTkTabview o un CTkFrame
        if hasattr(tabview, "add"):  # CTkTabview
            self.tab = tabview.add(tab_name)
        else:  # CTkFrame
            self.tab = tabview

        # Guardar campos de entrada y columnas de tabla
        self.input_fields = input_fields
        self.table_columns = table_columns

        # Configurar layout adaptable
        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)
        self.tab.grid_columnconfigure(1, weight=4)
        # Inicializar la interfaz de usuario
        self.init_ui()

    def init_ui(self):
        # Contenedor izquierdo (Inputs y Tabla) con scrollable frame
        self.left_frame = ctk.CTkScrollableFrame(self.tab)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.left_frame.grid_columnconfigure(0, weight=1)

        # Contenedor derecho (Gráfica y navegación)
        self.right_frame = ctk.CTkFrame(self.tab)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid_rowconfigure(0, weight=2)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_rowconfigure(2, weight=2)  # Fila para la tabla
        self.right_frame.grid_rowconfigure(1, weight=0, minsize=50)  # Fila para los botones con tamaño fijo
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Crear campos de entrada dinámicos
        current_row = 0  # Mantener el control de las filas
        for idx, field in enumerate(self.input_fields):
            label = ctk.CTkLabel(self.left_frame, text=f"{field}:", font=("Arial", 12), anchor="center")
            label.grid(row=current_row, column=0, pady=5, padx=5, sticky="ew")
            current_row += 1

            if idx == 0:
                # Campo de función con MathRendererWidget debajo
                entry = ctk.CTkTextbox(self.left_frame, height=30, font=("Arial", 10), width=250)
                entry.grid(row=current_row, column=0, pady=5, padx=5, sticky="ew")
                entry.bind("<KeyRelease>", self.update_math_renderer)

                # MathRendererWidget debajo del primer campo
                current_row += 1
                self.math_renderer_widget = MathRendererWidget(self.left_frame, width=250, height=120)
                self.math_renderer_widget.grid(row=current_row, column=0, pady=10, columnspan=1, sticky="ew")
            else:
                # Campos de entrada normales
                entry = ctk.CTkEntry(self.left_frame, font=("Arial", 10), width=250)
                entry.grid(row=current_row, column=0, pady=5, padx=5, sticky="ew")

            current_row += 1
            self.inputs[field] = entry

        # Botón para ejecutar
        btn_execute = ctk.CTkButton(self.left_frame, text="Ejecutar", command=self.execute_function, height=30, width=250)
        btn_execute.grid(row=current_row, column=0, pady=10, padx=5, sticky="ew")
        current_row += 1

        # Graficador
        self.graph_widget = GraphWidget(self.right_frame)
        self.graph_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        # Contenedor de botones de navegación (scrollable)
        self.button_frame = ctk.CTkFrame(self.right_frame, fg_color="gray15", corner_radius=8)
        self.button_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        # Botón para pasos previos
        self.btn_prev = ctk.CTkButton(self.button_frame, text="<--", command=self.plot_previous_step)
        self.btn_prev.pack(side="left", padx=5, pady=5)

        # Botón para pasos siguientes
        self.btn_next = ctk.CTkButton(self.button_frame, text="-->", command=self.plot_next_step)
        self.btn_next.pack(side="right", padx=5, pady=5)

        # Tabla
        self.table = CTkTable(self.right_frame, columns=self.table_columns, height=150)
        self.table.grid(row=2, column=0, pady=10, padx=5, sticky="nsew")

        # Vincular la selección de filas en la tabla con la gráfica
        self.table.tree.bind("<<TreeviewSelect>>", self.on_row_select)


    def on_row_select(self, event):
        """Maneja la selección de una fila en la tabla."""
        selected_item = self.table.tree.selection()  # Obtiene el ID de la fila seleccionada
        if selected_item:
            # Obtener el índice de la fila seleccionada
            index = self.table.tree.index(selected_item[0])
            self.current_step = index  # Actualizar el índice actual
            self.plot_step(self.current_step)  # Graficar el paso correspondiente

    def update_math_renderer(self, event):
        """Actualiza el MathRendererWidget con la fórmula procesada."""
        funcion = self.inputs[self.input_fields[0]].get("1.0", "end-1c").strip()
        try:
            funcion_procesada = procesar_formula(funcion)
            self.math_renderer_widget.update_text(funcion_procesada)
        except Exception as e:
            self.math_renderer_widget.update_text(f"Error: {e}")

    def execute_function(self):
        """Ejecuta la función personalizada."""
        if self.execute_callback:
            try:
                inputs = {field: self.get_input_value(field) for field in self.input_fields}
                self.execute_callback(inputs, self)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showinfo("Info", "No se ha definido una función personalizada para ejecutar.")

    def plot_previous_step(self):
        """Grafica el paso anterior y selecciona la fila en la tabla."""
        if self.current_step > 0:
            self.current_step -= 1
            self.table.tree.selection_set(self.table.tree.get_children()[self.current_step])  # Seleccionar fila
            self.plot_step(self.current_step)

    def plot_next_step(self):
        """Grafica el siguiente paso y selecciona la fila en la tabla."""
        if self.current_step < len(self.table.tree.get_children()) - 1:
            self.current_step += 1
            self.table.tree.selection_set(self.table.tree.get_children()[self.current_step])  # Seleccionar fila
            self.plot_step(self.current_step)

    def plot_step(self, step_index):
        """Grafica un paso específico, usando una función personalizada si está definida."""
        if self.plot_step_callback:
            try:
                self.plot_step_callback(step_index, self)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showinfo("Info", "No se ha definido una función personalizada para graficar un paso.")

    def get_input_value(self, field):
        """Obtiene el valor de un campo de entrada dado."""
        widget = self.inputs[field]
        if isinstance(widget, ctk.CTkTextbox):
            return widget.get("1.0", "end-1c").strip()
        else:
            return widget.get().strip()

