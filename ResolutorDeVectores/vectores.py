import tkinter as tk
from tkinter import ttk, messagebox
import math

def setup_app():
    global app
    app = tk.Tk()
    app.title("Calculadora de Vectores")
    app.geometry("800x600")
    app.resizable(False, False)
    return app

def setup_frame(app):
    frame = ttk.Frame(app, padding="10 10 10 10")
    frame.pack(expand=True)
    return frame

def setup_labels_and_entries(frame):
    ttk.Label(frame, text="Número de vectores:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w")
    num_vectors_entry = ttk.Entry(frame, font=("Helvetica", 12))
    num_vectors_entry.grid(row=0, column=1, pady=5)

    ttk.Label(frame, text="Dimensión de los vectores:", font=("Helvetica", 12, "bold")).grid(row=1, column=0, sticky="w")
    dim_entry = ttk.Entry(frame, font=("Helvetica", 12))
    dim_entry.grid(row=1, column=1, pady=5)

    return num_vectors_entry, dim_entry

def setup_buttons(frame, generate_entries, calculate):
    ttk.Button(frame, text="Generar", command=generate_entries, style="TButton").grid(row=2, column=2, padx=10)
    ttk.Button(frame, text="Calcular", command=calculate, style="TButton").grid(row=4, column=0, columnspan=3, pady=10)

def setup_vectors_frame(frame):
    vectors_frame = ttk.Frame(frame)
    vectors_frame.grid(row=3, column=0, columnspan=10, pady=10)
    return vectors_frame

def setup_result_label(frame):
    result_text = tk.StringVar()
    result_label = ttk.Label(frame, textvariable=result_text, justify="left", anchor="w", font=("Helvetica", 14, "bold"))
    result_label.grid(row=5, column=0, columnspan=10, sticky="w")
    return result_text, result_label

def is_valid_number(value):
    try:
        if value.startswith('sqrt(') and value.endswith(')'):
            inner_value = value[5:-1]
            float(inner_value)
        else:
            float(value)
        return True
    except ValueError:
        return False

def parse_number(value):
    if value.startswith('sqrt(') and value.endswith(')'):
        inner_value = float(value[5:-1])
        return math.sqrt(inner_value)
    else:
        return float(value)

def generate_entries():
    try:
        num_vectors = int(num_vectors_entry.get())
        dim = int(dim_entry.get())
        if dim <= 0 or dim > 10:
            raise ValueError("La dimensión debe estar entre 1 y 10.")
        if num_vectors <= 0 or num_vectors > 10:
            raise ValueError("El número de vectores debe estar entre 1 y 10.")
        
        for widget in vectors_frame.winfo_children():
            widget.destroy()

        global vector_entries, scalar_entries
        vector_entries = []
        scalar_entries = []

        for i in range(num_vectors):
            scalar_label = ttk.Label(vectors_frame, text=f"Escalar para el vector {i+1}:", font=("Helvetica", 12, "bold"))
            scalar_label.grid(row=i*2, column=0, sticky="w", pady=(10, 0))
            scalar_entry = ttk.Entry(vectors_frame, font=("Helvetica", 12))
            scalar_entry.grid(row=i*2, column=1, pady=(10, 0), padx=5)
            scalar_entries.append(scalar_entry)

            vector_label = ttk.Label(vectors_frame, text=f"Componentes del vector {i+1}:", font=("Helvetica", 12, "bold"))
            vector_label.grid(row=i*2+1, column=0, sticky="w", pady=(5, 10))
            entries = []
            for j in range(dim):
                entry = ttk.Entry(vectors_frame, width=5, font=("Helvetica", 12))
                entry.grid(row=i*2+1, column=j+1, padx=5, pady=(5, 10))
                entries.append(entry)
            vector_entries.append(entries)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def calculate():
    try:
        num_vectors = int(num_vectors_entry.get())
        dim = int(dim_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
        return

    vectors = []
    procedure = ""
    for i in range(num_vectors):
        try:
            scalar_value = scalar_entries[i].get()
            if not is_valid_number(scalar_value):
                raise ValueError(f"Por favor, ingrese un valor numérico válido para el escalar del vector {i+1}.")
            scalar = parse_number(scalar_value)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        vector = []
        procedure += f"v{i+1} → con escalar {scalar}:\n"
        for j in range(dim):
            try:
                value = vector_entries[i][j].get()
                if not is_valid_number(value):
                    raise ValueError(f"Por favor, ingrese un valor numérico válido en el vector {i+1}, posición {j+1}.")
                parsed_value = parse_number(value)
                vector.append(scalar * parsed_value)
                procedure += f"  {scalar} * {parsed_value} = {scalar * parsed_value}\n"
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return
        vectors.append(vector)
        procedure += f"  Resultado de v{i+1} →: {vector}\n\n"

    result_vector = [sum(x) for x in zip(*vectors)]
    procedure += f"Suma de todos los vectores: {result_vector}\n"
    show_results(vectors, result_vector, procedure)

def show_results(vectors, result_vector, procedure):
    for widget in app.winfo_children():
        widget.destroy()

    result_frame = ttk.Frame(app, padding="10 10 10 10")
    result_frame.pack(expand=True)

    ttk.Label(result_frame, text="Resultados", font=("Helvetica", 16, "bold")).pack(pady=10)

    for i, vector in enumerate(vectors):
        ttk.Label(result_frame, text=f"v{i+1} → {vector}", font=("Helvetica", 12)).pack(anchor="w")

    ttk.Label(result_frame, text=f"Resultado final: {result_vector}", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=10)
    ttk.Label(result_frame, text="Procedimiento:", font=("Helvetica", 12, "bold")).pack(anchor="w")

    procedure_text = tk.Text(result_frame, font=("Helvetica", 12), wrap="word", height=15, width=80)
    procedure_text.pack(pady=10)
    procedure_text.insert("1.0", procedure)
    procedure_text.config(state="disabled")

    ttk.Button(result_frame, text="Calcular de nuevo", command=reset_app, style="TButton").pack(pady=10)

def reset_app():
    for widget in app.winfo_children():
        widget.destroy()
    initialize_interface()

def initialize_interface():
    frame = setup_frame(app)
    global num_vectors_entry, dim_entry, vectors_frame, result_text, scalar_entries, vector_entries
    num_vectors_entry, dim_entry = setup_labels_and_entries(frame)
    setup_buttons(frame, generate_entries, calculate)
    vectors_frame = setup_vectors_frame(frame)
    result_text, result_label = setup_result_label(frame)

def vectorfinal():
    global app
    app = setup_app()
    initialize_interface()
    app.mainloop()

# Llamada inicial a vectorfinal
vectorfinal()