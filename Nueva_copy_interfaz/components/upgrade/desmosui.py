from components.table_widget import CTkTable
from sympy import symbols, sympify, lambdify,latex
import customtkinter as ctk
from tkinter.colorchooser import askcolor
from tkinter import Menu
from components.Math_renderer_widget import MathRendererWidget  # Importar tu widget para renderizar matemáticas
import tkinter as tk


class FunctionManager(CTkTable):
    def __init__(self, master, graph_widget, **kwargs):
        columns = ["Label", "Function", "Color"]
        super().__init__(master, columns, **kwargs)
        self.graph_widget = graph_widget
        self.color_palette = ["blue", "green", "red", "orange", "purple"]
        self.color_index = 0

        # Asegurar que haya una fila vacía al inicio
        self.ensure_empty_row()

                # Crear menú contextual para borrar filas
        self.popup_menu = Menu(self.tree, tearoff=0)
        self.popup_menu.add_command(label="Eliminar fila", command=self.remove_selected_row)

        # Vincular el clic derecho al menú contextual
        self.tree.bind("<Button-3>", self.show_popup)
        # Eventos interactivos
        self.tree.bind("<Double-1>", self.start_editing)
        self.tree.bind("<Return>", self.confirm_editing)

    def ensure_empty_row(self):
        """Garantiza que siempre haya una fila vacía al final."""
        if not self.has_empty_row():
            self.add_empty_row()

    def has_empty_row(self):
        """Verifica si hay una fila vacía en la tabla."""
        for row in self.tree.get_children():
            _, func_str, _ = self.tree.item(row, "values")
            if not func_str.strip():  # Si la función está vacía
                return True
        return False

    def add_empty_row(self):
        """Agrega una fila vacía con valores predeterminados."""
        label = f"f{len(self.tree.get_children()) + 1}(x)"
        self.add_row((label, "", self.get_next_color()))

    def add_function(self):
        """Agrega una nueva función si no hay filas vacías."""
        label = f"f{len(self.tree.get_children()) + 1}(x)"
        color = self.get_next_color()
        if not self.has_empty_row():
            self.add_row((label, "", color))
        self.ensure_empty_row()  # Asegura siempre una fila vacía
        self.update_graph()

    def remove_selected(self):
        """Elimina la fila seleccionada y garantiza una fila vacía."""
        selected = self.tree.selection()
        for item in selected:
            self.tree.delete(item)

        # Asegurar una fila vacía después de eliminar
        self.ensure_empty_row()
        self.update_graph()

    def update_graph(self):
        """Actualiza el gráfico con las funciones actuales."""
        functions = []
        for row in self.tree.get_children():
            label, func_str, color = self.tree.item(row, "values")
            if func_str.strip():  # Solo procesar filas con funciones no vacías
                try:
                    func = self.safe_eval_function(func_str)
                    functions.append({"func": func, "label": label, "color": color})
                except ValueError:
                    print(f"Función no válida: {func_str}")  # Ignorar errores en funciones específicas
        self.graph_widget.plot_multiple_functions(functions)

    def get_next_color(self):
        """Devuelve un color cíclico de la paleta."""
        color = self.color_palette[self.color_index]
        self.color_index = (self.color_index + 1) % len(self.color_palette)
        return color

    def start_editing(self, event):
        """Inicia la edición de una celda con vista previa matemática."""
        row_id = self.tree.identify_row(event.y)
        column_id = self.tree.identify_column(event.x)

        if column_id == "#3":  # Si es la columna de color
            self.edit_color(row_id)
            return

        selected_item = self.tree.item(row_id)
        current_value = selected_item["values"][int(column_id[1]) - 1]

        # Crear un Frame contenedor para el editor y la vista previa
        self.edit_container = ctk.CTkFrame(self.tree)
        self.edit_container.place(x=event.x, y=event.y)

        # Editor de texto para ingresar la fórmula
        self.edit_widget = ctk.CTkEntry(self.edit_container, width=100)
        self.edit_widget.insert(0, current_value)
        self.edit_widget.pack(fill="x")
        self.edit_widget.focus_set()  # Seleccionar automáticamente
        self.edit_widget.icursor(tk.END)  # Mueve el cursor al final
        self.edit_widget.select_range(0, tk.END)  # Seleccionar todo el texto

        # MathRendererWidget para mostrar la fórmula renderizada
        self.math_renderer = MathRendererWidget(self.edit_container, width=300, height=100)
        self.math_renderer.pack(fill="x", pady=5)

        # Actualizar la vista previa en tiempo real
        self.edit_widget.bind("<KeyRelease>", lambda e: self.update_math_preview())

        # Confirmar edición al presionar Enter
        self.edit_widget.bind("<Return>", lambda e: self.confirm_editing(row_id, column_id))
        self.edit_widget.bind("<FocusOut>", lambda e: self.cancel_editing())

    def confirm_editing(self, row_id, column_id):
        """Confirma los cambios en una celda."""
        new_value = self.edit_widget.get()
        self.tree.set(row_id, column=column_id, value=new_value)
        if hasattr(self, "edit_container"):
            self.edit_container.destroy()  # Elimina el contenedor completo
        self.update_graph()
        self.ensure_empty_row()  # Asegura que haya una fila vacía

    def cancel_editing(self):
        """Cancela la edición de una celda."""
        if hasattr(self, "edit_container"):
            self.edit_container.destroy()

    def edit_color(self, row_id):
        """Abre un selector de color para cambiar el color de la función."""
        color = askcolor(title="Seleccionar color")[1]
        if color:
            self.tree.item(row_id, values=(self.tree.item(row_id)["values"][0],
                                           self.tree.item(row_id)["values"][1],
                                           color))
            self.update_graph()

    def safe_eval_function(self, func_str):
        """Convierte una cadena de texto en una función evaluable usando sympy y numpy."""
        x = symbols("x")
        try:
            expr = sympify(func_str)
            return lambdify(x, expr, "numpy")
        except Exception as e:
            print(f"Error al procesar la función '{func_str}': {e}")
            raise ValueError(f"Función inválida: {func_str}")
        
    def show_popup(self, event):
        """Muestra el menú contextual al hacer clic derecho en una fila."""
        # Identificar la fila bajo el cursor
        row_id = self.tree.identify_row(event.y)
        if row_id:  # Si hay una fila bajo el cursor
            self.tree.selection_set(row_id)  # Seleccionar la fila
            self.popup_menu.post(event.x_root, event.y_root)  # Mostrar el menú

    def remove_selected_row(self):
        """Elimina la fila seleccionada al hacer clic derecho."""
        selected = self.tree.selection()
        for item in selected:
            self.tree.delete(item)

        # Asegurar que siempre quede una fila vacía
        self.ensure_empty_row()
        self.update_graph()
        
    def update_math_preview(self):
        """Actualiza la vista previa matemática en tiempo real."""
        func_str = self.edit_widget.get()
        try:
            latex_formula = self.procesar_formula(func_str)
            if(latex_formula==None):
                return
            self.math_renderer.update_text(latex_formula)
        except Exception as e:
            self.math_renderer.update_text("Error")

    def procesar_formula(self, funcion_str):
        """Convierte una fórmula en formato string a LaTeX."""
        x = symbols("x")
        try:
            expr = sympify(funcion_str)
            return latex(expr)
        except Exception:
            return
