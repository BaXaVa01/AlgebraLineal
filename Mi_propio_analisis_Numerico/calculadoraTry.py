# Interfaz de calculadora estilo GeoGebra
import customtkinter as ctk
from math import sin, cos, tan, log, sqrt, pi, e
import re

# Variables
entry_text = ""

# Función para insertar texto en la entrada
def insert_text(text):
    global entry_text
    entry_text += text
    entry.delete(0, ctk.END)
    entry.insert(0, entry_text)

# Función para evaluar la expresión en la entrada
def evaluate_expression():
    global entry_text
    try:
        # Evaluar usando funciones matemáticas seguras
        entry_text = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', entry_text)  # Agregar * entre número y función
        result = eval(entry_text, {"__builtins__": None}, {"sin": sin, "cos": cos, "tan": tan, "log": log, "sqrt": sqrt, "pi": pi, "e": e})
        entry.delete(0, ctk.END)
        entry.insert(0, str(result))
        entry_text = str(result)
    except Exception as e:
        entry.delete(0, ctk.END)
        entry.insert(0, "Error")
        entry_text = ""

# Función para borrar la entrada
def clear_entry():
    global entry_text
    entry_text = ""
    entry.delete(0, ctk.END)

# Crear la ventana principal
root = ctk.CTk()
root.title("Calculadora estilo GeoGebra")
root.geometry("400x500")

# Campo de entrada
entry = ctk.CTkEntry(root, width=300, font=("Arial", 20))
entry.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

# Botones numéricos, operaciones y funciones
buttons = [
    ('7', '8', '9', '/'),
    ('4', '5', '6', '*'),
    ('1', '2', '3', '-'),
    ('0', '.', '(', ')'),
    ('+', 'sin', 'cos', 'tan'),
    ('pi', 'e', '^', 'sqrt'),
    ('C', '=', 'log', 'clear')
]

# Crear botones en la interfaz
for i, row in enumerate(buttons):
    for j, btn_text in enumerate(row):
        if btn_text == 'C':
            button = ctk.CTkButton(root, text=btn_text, width=60, command=clear_entry)
        elif btn_text == '=':
            button = ctk.CTkButton(root, text=btn_text, width=60, command=evaluate_expression)
        elif btn_text == 'clear':
            button = ctk.CTkButton(root, text="Clear", width=60, command=clear_entry)
        else:
            button = ctk.CTkButton(root, text=btn_text, width=60, command=lambda t=btn_text: insert_text(t))
        button.grid(row=i+1, column=j, padx=5, pady=5)

root.mainloop()
