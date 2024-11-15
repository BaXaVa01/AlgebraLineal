# components/popup_keyboard.py
import customtkinter as ctk
from tkinter import Toplevel
import sys

class PopupKeyboard(Toplevel):
    def __init__(self, attach_widget, **kwargs):
        super().__init__(**kwargs)
        self.attach_widget = attach_widget
        self.overrideredirect(True)
        self.withdraw()  # Ocultar hasta que se necesite

        # Configurar apariencia en función del sistema operativo
        if sys.platform.startswith("win"):
            self.transparent_color = self._apply_appearance_mode("#333333")
            self.attributes("-transparentcolor", self.transparent_color)
        elif sys.platform.startswith("darwin"):
            self.attributes("-transparent", True)
            self.transparent_color = 'systemTransparent'
        else:
            self.transparent_color = "#333333"

        # Configuración de diseño y estilo
        self.bg_frame = ctk.CTkFrame(self, corner_radius=10)
        self.bg_frame.pack(fill="both", expand=True)

        # Definición de teclas para funciones matemáticas
        self.keys = [
            ['7', '8', '9', '/', '(', ')', 'π'],
            ['4', '5', '6', '*', 'sin', 'cos', 'tan'],
            ['1', '2', '3', '-', 'log', 'ln', 'sqrt'],
            ['0', '.', '^', '+', 'e', ',', '='],
            ['Space', 'Clear', '←', 'Enter']
        ]

        # Crear botones para cada tecla
        for row_index, row in enumerate(self.keys):
            for col_index, key in enumerate(row):
                button = ctk.CTkButton(self.bg_frame, text=key, width=60, command=lambda k=key: self.on_key_press(k))
                button.grid(row=row_index, column=col_index, padx=2, pady=2)

        # Vincular el evento de doble clic al widget de entrada para alternar el teclado
        self.attach_widget.bind("<Double-Button-1>", self.toggle)

    def on_key_press(self, key):
        """Define las acciones para cada tecla del teclado."""
        if key == '←':  # Borrar
            self.attach_widget.delete(len(self.attach_widget.get()) - 1)
        elif key == 'Clear':  # Limpiar entrada
            self.attach_widget.delete(0, "end")
        elif key == 'Space':  # Espacio
            self.attach_widget.insert("insert", ' ')
        elif key == 'Enter':  # Ocultar teclado
            self.withdraw()
        elif key == 'π':  # Insertar pi
            self.attach_widget.insert("insert", 'pi')
        elif key == 'e':  # Insertar e
            self.attach_widget.insert("insert", 'e')
        elif key in {'sin', 'cos', 'tan', 'log', 'ln', 'sqrt'}:  # Funciones trigonométricas y logarítmicas
            self.attach_widget.insert("insert", f"{key}(")
        elif key == '^':  # Potencia
            self.attach_widget.insert("insert", '**')
        else:
            self.attach_widget.insert("insert", key)

    def toggle(self, event=None):
        """Alterna la visibilidad del teclado."""
        if self.state() == "withdrawn":
            self.deiconify()
            self.geometry(f"+{self.attach_widget.winfo_rootx()}+{self.attach_widget.winfo_rooty() + 30}")
        else:
            self.withdraw()
