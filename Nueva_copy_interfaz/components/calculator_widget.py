# components/calculator_widget.py
import customtkinter as ctk
from tkinter import messagebox
from math import sin, cos, tan, log, sqrt, pi, e
import re

class CalculatorWidget(ctk.CTkFrame):
    def __init__(self, master, width=300, **kwargs):
        super().__init__(master, width=width, **kwargs)
        
        # Configuración de la entrada de texto para la expresión
        self.entry = ctk.CTkEntry(self, width=width - 20, font=("Arial", 14))
        self.entry.pack(pady=5)

        # Botón para evaluar la expresión
        self.evaluate_button = ctk.CTkButton(self, text="Evaluar", command=self.evaluate_expression)
        self.evaluate_button.pack(pady=5)

    def evaluate_expression(self):
        """Evalúa la expresión matemática ingresada."""
        try:
            expression = self.entry.get()
            # Reemplazar el símbolo de potencia (^) por el operador de potencia (**)
            expression = expression.replace("^", "**")

            # Insertar multiplicación implícita, por ejemplo, 2x -> 2*x
            expression = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expression)

            # Evaluar la expresión en un entorno seguro
            result = eval(expression, {"__builtins__": None}, {
                "sin": sin, "cos": cos, "tan": tan, "log": log, "sqrt": sqrt, "pi": pi, "e": e
            })

            # Mostrar el resultado en la entrada
            self.entry.delete(0, "end")
            self.entry.insert(0, str(result))

        except Exception as e:
            messagebox.showerror("Error", f"Error en la expresión: {e}")
            self.entry.delete(0, "end")
