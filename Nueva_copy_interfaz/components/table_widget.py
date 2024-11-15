# components/table_widget.py
import customtkinter as ctk
from tkinter import ttk
from tkinter import END

class CTkTable(ctk.CTkFrame):
    def __init__(self, master, columns, advanced_features=False, **kwargs):
        super().__init__(master, **kwargs)

        # Configuración de Treeview para la tabla básica
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Configuración de las columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        # Estilos adicionales de ttk para adaptar a CustomTkinter
        style = ttk.Style()
        style.configure("Treeview", background="#333333", foreground="white", rowheight=25, fieldbackground="#333333")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        # Opciones avanzadas (configurables con argumentos)
        self.advanced_features = advanced_features
        if advanced_features:
            # Atributos adicionales solo si `advanced_features` está habilitado
            self.row_count = kwargs.get('row', 5)
            self.column_count = kwargs.get('column', len(columns))
            self.corner_radius = kwargs.get('corner_radius', 0)
            self.text_color = kwargs.get('text_color', "white")
            self.fg_color = kwargs.get('fg_color', "#333333")
            self.wraplength = kwargs.get('wraplength', 500)
            # Aquí puedes inicializar más funcionalidades avanzadas según tus necesidades

    def insert_data(self, data):
        """Inserta datos en la tabla."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in data:
            self.tree.insert("", END, values=item)

    def clear_data(self):
        """Limpia todos los datos de la tabla."""
        for row in self.tree.get_children():
            self.tree.delete(row)

    def add_row(self, values, index=None):
        """Añade una nueva fila en la tabla"""
        if index is None:
            index = "end"
        self.tree.insert("", index, values=values)

    def get_row(self, index):
        """Obtiene los datos de una fila específica por su índice"""
        item = self.tree.get_children()[index]
        return self.tree.item(item, 'values')

    def configure_table(self, **kwargs):
        """Configura el aspecto y las propiedades de la tabla"""
        if 'bg_color' in kwargs:
            self.fg_color = kwargs.pop('bg_color')
            style = ttk.Style()
            style.configure("Treeview", fieldbackground=self.fg_color)
        
        if 'text_color' in kwargs:
            self.text_color = kwargs.pop('text_color')
            style.configure("Treeview.Heading", foreground=self.text_color)

        if self.advanced_features:
            # Ajustes adicionales si `advanced_features` está activado
            self.wraplength = kwargs.get("wraplength", self.wraplength)
            self.corner_radius = kwargs.get("corner_radius", self.corner_radius)

    def delete_row(self, index=None):
        """Elimina una fila específica de la tabla"""
        if index is None:
            index = self.tree.get_children()[-1]
        self.tree.delete(index)

    def select_row(self, index):
        """Selecciona una fila específica"""
        self.tree.selection_set(self.tree.get_children()[index])

    def deselect_row(self, index):
        """Deselecciona una fila específica"""
        self.tree.selection_remove(self.tree.get_children()[index])

    def add_column(self, column_name):
        """Añade una nueva columna a la tabla"""
        self.tree["columns"] += (column_name,)
        self.tree.heading(column_name, text=column_name)
        self.tree.column(column_name, anchor="center")

