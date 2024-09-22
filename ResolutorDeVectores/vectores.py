import tkinter as tk
from tkinter import ttk, messagebox
import math

# Estilos personalizados para hacer la interfaz profesional
def setup_styles():
    style = ttk.Style()
    
    # Fondo y colores elegantes para el marco principal
    style.configure("TFrame", background="#f7f7f9")  # Fondo blanco suave
    style.configure("TLabel", background="#f7f7f9", font=("Helvetica Neue", 12))
    style.configure("TEntry", padding=10, font=("Helvetica Neue", 14))
    
    # Botones elegantes con bordes redondeados y efecto hover
    style.configure("TButton", font=("Helvetica Neue", 12, "bold"), foreground="#000000", background="#69a2ff", padding=10, relief="flat")
    
    # Ajustar el color del texto según el estado del botón
    style.map("TButton", 
              foreground=[('active', '#ffffff'), ('pressed', '#ffffff'), ('!active', '#000000')],
              background=[('active', '#4187f6'), ('pressed', '#4187f6'), ('!active', '#69a2ff')])

# Configuración de la app
def setup_app():
    global app
    app = tk.Tk()
    app.title("Calculadora de Vectores")
    app.geometry("950x700")
    app.resizable(False, False)
    app.configure(bg="#e3e4e6")  # Fondo suave gris claro
    return app

# Crear el frame principal con espaciado y diseño limpio
def setup_frame(app):
    frame = ttk.Frame(app, padding="30 30 30 30", style="TFrame")
    frame.pack(expand=True)
    return frame

# Configurar etiquetas y entradas con espaciado y diseño centrado
def setup_labels_and_entries(frame):
    ttk.Label(frame, text="Número de vectores:", font=("Helvetica Neue", 14, "bold"), background="#f7f7f9").grid(row=0, column=0, sticky="w")
    num_vectors_entry = ttk.Entry(frame, font=("Helvetica Neue", 14), style="TEntry")
    num_vectors_entry.grid(row=0, column=1, pady=10, padx=10)

    ttk.Label(frame, text="Dimensión de los vectores:", font=("Helvetica Neue", 14, "bold"), background="#f7f7f9").grid(row=1, column=0, sticky="w")
    dim_entry = ttk.Entry(frame, font=("Helvetica Neue", 14), style="TEntry")
    dim_entry.grid(row=1, column=1, pady=10, padx=10)

    return num_vectors_entry, dim_entry

# Configurar botones con bordes suaves y efectos visuales
def setup_buttons(frame, generate_entries, calculate):
    ttk.Button(frame, text="Generar", command=generate_entries, style="TButton").grid(row=2, column=2, padx=20, pady=15)
    ttk.Button(frame, text="Calcular", command=calculate, style="TButton").grid(row=4, column=0, columnspan=3, pady=20)

# Caja de vectores con bordes sutiles y diseño atractivo
def setup_scrollable_vectors_frame(frame):
    canvas = tk.Canvas(frame, bg="#f7f7f9", bd=0, highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas, style="TFrame")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=3, column=0, columnspan=10, sticky="nsew", padx=10, pady=10)
    scrollbar.grid(row=3, column=11, sticky="ns")

    return scrollable_frame

# Etiqueta de resultados con diseño profesional
def setup_result_label(frame):
    result_text = tk.StringVar()
    result_label = ttk.Label(frame, textvariable=result_text, justify="left", anchor="w", font=("Helvetica Neue", 14, "bold"), background="#f7f7f9")
    result_label.grid(row=5, column=0, columnspan=10, sticky="w")
    return result_text, result_label

# Generar entradas para vectores con estilo más limpio
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
            scalar_label = ttk.Label(vectors_frame, text=f"Escalar para el v^{i+1}:", font=("Helvetica Neue", 12, "bold"), background="#f7f7f9")
            scalar_label.grid(row=i*2, column=0, sticky="w", pady=(10, 0))
            scalar_entry = ttk.Entry(vectors_frame, width=10, font=("Helvetica Neue", 12))
            scalar_entry.grid(row=i*2, column=1, pady=(10, 0), padx=5)
            scalar_entries.append(scalar_entry)

            vector_label = ttk.Label(vectors_frame, text=f"Componentes del v^{i+1}:", font=("Helvetica Neue", 12, "bold"), background="#f7f7f9")
            vector_label.grid(row=i*2+1, column=0, sticky="w", pady=(5, 10))
            entries = []
            for j in range(dim):
                entry = ttk.Entry(vectors_frame, width=5, font=("Helvetica Neue", 12))
                entry.grid(row=i*2+1, column=j+1, padx=5, pady=(5, 10))
                entries.append(entry)
            vector_entries.append(entries)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Cálculo de los vectores
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
            if not scalar_value.isnumeric():
                raise ValueError(f"Por favor, ingrese un valor numérico válido para el escalar del vector {i+1}.")
            scalar = float(scalar_value)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        vector = []
        procedure += f"v{i+1} → con escalar {scalar}:\n"
        for j in range(dim):
            try:
                value = vector_entries[i][j].get()
                if not value.isnumeric():
                    raise ValueError(f"Por favor, ingrese un valor numérico válido en el vector {i+1}, posición {j+1}.")
                vector.append(scalar * float(value))
                procedure += f"  {scalar} * {float(value)} = {scalar * float(value)}\n"
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return
        vectors.append(vector)
        procedure += f"  Resultado de v{i+1} →: {vector}\n\n"

    result_vector = [sum(x) for x in zip(*vectors)]
    procedure += f"Suma de todos los vectores: {result_vector}\n"
    show_results(vectors, result_vector, procedure)

# Mostrar los resultados en un formato profesional
def show_results(vectors, result_vector, procedure):
    for widget in app.winfo_children():
        widget.destroy()

    result_frame = ttk.Frame(app, padding="30 30 30 30", style="TFrame")
    result_frame.pack(expand=True)

    ttk.Label(result_frame, text="Resultados", font=("Helvetica Neue", 16, "bold"), background="#f7f7f9").pack(pady=20)

    for i, vector in enumerate(vectors):
        ttk.Label(result_frame, text=f"v{i+1} → {vector}", font=("Helvetica Neue", 12), background="#f7f7f9").pack(anchor="w")

    ttk.Label(result_frame, text=f"Resultado final: {result_vector}", font=("Helvetica Neue", 12, "bold"), background="#f7f7f9").pack(anchor="w", pady=20)
    ttk.Label(result_frame, text="Procedimiento:", font=("Helvetica Neue", 12, "bold"), background="#f7f7f9").pack(anchor="w")

    procedure_text = tk.Text(result_frame, font=("Helvetica Neue", 12), wrap="word", height=15, width=80, bg="#f7f7f9")
    procedure_text.pack(pady=10)
    procedure_text.insert("1.0", procedure)
    procedure_text.config(state="disabled")

    ttk.Button(result_frame, text="Calcular de nuevo", command=reset_app, style="TButton").pack(pady=20)

# Resetear la aplicación
def reset_app():
    for widget in app.winfo_children():
        widget.destroy()
    initialize_interface()

# Inicializar la interfaz con el estilo configurado
def initialize_interface():
    frame = setup_frame(app)
    global num_vectors_entry, dim_entry, vectors_frame, vector_entries, scalar_entries
    num_vectors_entry, dim_entry = setup_labels_and_entries(frame)
    setup_buttons(frame, generate_entries, calculate)
    vectors_frame = setup_scrollable_vectors_frame(frame)

# Crear la ventana principal
def vectorfinal():
    global app
    app = setup_app()
    setup_styles()  # Configurar los estilos
    initialize_interface()
    app.mainloop()

# Ejecutar el programa
vectorfinal()
