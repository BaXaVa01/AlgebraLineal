import tkinter as tk
from tkinter import messagebox

class Vector:
    def __init__(self, components):
        self.components = components

    def __mul__(self, scalar):
        return Vector([scalar * x for x in self.components])

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __add__(self, other):
        return Vector([x + y for x, y in zip(self.components, other.components)])

    def __eq__(self, other):
        return all([x == y for x, y in zip(self.components, other.components)])

    def __str__(self):
        return f"[{', '.join(map(str, self.components))}]"

class Matrix:
    def __init__(self, rows):
        self.rows = rows

    def multiply_vector(self, vector):
        result = []
        for i in range(len(self.rows)):
            value = sum(self.rows[i][j] * vector.components[j] for j in range(len(vector.components)))
            result.append(value)
        return Vector(result)

    def __str__(self):
        return f"[{', '.join(str(row) for row in self.rows)}]"

def generate_entries():
    try:
        dim = int(dim_entry.get())
        if dim <= 0 or dim > 10:
            raise ValueError("La dimensión debe estar entre 1 y 10.")
        
        for widget in input_frame.winfo_children():
            widget.destroy()

        global matrix_entries, vector_u_entries, vector_v_entries
        matrix_entries = []
        vector_u_entries = []
        vector_v_entries = []

        # Matriz A
        tk.Label(input_frame, text="Matriz A:", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=dim, sticky="w")
        for i in range(dim):
            row_entries = []
            for j in range(dim):
                entry = tk.Entry(input_frame, width=5, font=("Arial", 20))
                entry.grid(row=i+1, column=j, padx=1, pady=5)
                row_entries.append(entry)
            matrix_entries.append(row_entries)

        # Vector u
        tk.Label(input_frame, text="Vector u:", font=("Arial", 20, "bold")).grid(row=dim+1, column=0, sticky="w")
        for i in range(dim):
            entry = tk.Entry(input_frame, width=5, font=("Arial", 20))
            entry.grid(row=dim+2, column=i, padx=1, pady=5)
            vector_u_entries.append(entry)

        # Vector v
        tk.Label(input_frame, text="Vector v:", font=("Arial", 20, "bold")).grid(row=dim+3, column=0, sticky="w")
        for i in range(dim):
            entry = tk.Entry(input_frame, width=5, font=("Arial", 20))
            entry.grid(row=dim+4, column=i, padx=1, pady=5)
            vector_v_entries.append(entry)

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def show_steps_window(steps_text):
    # Crear una nueva ventana para mostrar los pasos del cálculo
    steps_window = tk.Toplevel(app)
    steps_window.title("Pasos del Cálculo")
    steps_window.geometry("600x400")
    
    steps_label = tk.Label(steps_window, text="Pasos del cálculo:", font=("Arial", 14, "bold"))
    steps_label.pack(pady=10)

    steps_text_widget = tk.Text(steps_window, wrap="word", font=("Arial", 20), padx=10, pady=10)
    steps_text_widget.insert(tk.END, steps_text)
    steps_text_widget.config(state=tk.DISABLED)  # Hacer que el widget sea solo de lectura
    steps_text_widget.pack(expand=True, fill=tk.BOTH)

def show_result_window(solution_text, steps_text):
    # Crear una nueva ventana para mostrar la solución
    result_window = tk.Toplevel(app)
    result_window.title("Resultado")
    result_window.geometry("600x300")

    # Mostrar solo la solución inicial
    result_label = tk.Label(result_window, text="Solución:", font=("Arial", 14, "bold"))
    result_label.pack(pady=10)

    solution_label = tk.Label(result_window, text=solution_text, font=("Arial", 20))
    solution_label.pack(pady=10)

    # Botón para mostrar los pasos detallados
    show_steps_button = tk.Button(result_window, text="Mostrar Pasos", command=lambda: show_steps_window(steps_text), font=("Arial", 20, "bold"))
    show_steps_button.pack(pady=10)

def calculate():
    try:
        dim = int(dim_entry.get())

        # Leer la matriz A
        A = Matrix([[float(matrix_entries[i][j].get()) for j in range(dim)] for i in range(dim)])

        # Leer los vectores u y v
        u = Vector([float(vector_u_entries[i].get()) for i in range(dim)])
        v = Vector([float(vector_v_entries[i].get()) for i in range(dim)])

        # Cálculos: A(u + v) y Au + Av
        u_plus_v = u + v
        A_u_plus_v = A.multiply_vector(u_plus_v)
        
        A_u = A.multiply_vector(u)
        A_v = A.multiply_vector(v)
        A_u_plus_A_v = A_u + A_v

        # Solución principal
        solution_text = f"A(u + v) = {A_u_plus_v}\nAu + Av = {A_u_plus_A_v}"

        # Mostrar los pasos de forma ordenada
        steps = []
        steps.append(f"1. Suma de los vectores u y v:")
        steps.append(f"   u = {u}")
        steps.append(f"   v = {v}")
        steps.append(f"   u + v = {u} + {v} = {u_plus_v}")
        steps.append("\n2. Multiplicación de la matriz A por el vector (u + v):")
        steps.append(f"   A = {A}")
        steps.append(f"   A(u + v) = {A} * {u_plus_v} = {A_u_plus_v}")
        steps.append("\n3. Multiplicación de A por u y A por v por separado:")
        steps.append(f"   Au = {A} * {u} = {A_u}")
        steps.append(f"   Av = {A} * {v} = {A_v}")
        steps.append("\n4. Suma de Au y Av:")
        steps.append(f"   Au + Av = {A_u} + {A_v} = {A_u_plus_A_v}")

        # Verificar la propiedad distributiva
        if A_u_plus_v == A_u_plus_A_v:
            steps.append(f"\nPropiedad distributiva verificada: A(u + v) = Au + Av")
            steps.append("\n**Explicación:**")
            steps.append("   Se cumple la propiedad distributiva porque:")
            steps.append("   A(u + v) es igual a la suma de los productos A por u y A por v por separado.")
            steps.append("   Esto significa que el resultado de multiplicar la matriz A por la suma de los vectores")
            steps.append("   es igual a sumar los resultados de multiplicar la matriz A por cada vector.")
        else:
            steps.append(f"\nLa propiedad distributiva NO se cumple")

        # Unir los pasos para mostrar en la nueva ventana
        steps_text = "\n".join(steps)
        show_result_window(solution_text, steps_text)

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

app = tk.Tk()
app.title("Calculadora de Matrices y Vectores")

# Configurar para pantalla completa
app.attributes('-fullscreen', True)  # Esta línea activa el modo de pantalla completa

frame = tk.Frame(app, padx=10, pady=10)
frame.pack(expand=True)

# Entrada para la dimensión de la matriz y los vectores
tk.Label(frame, text="Dimensión de la matriz y los vectores:", font=("Arial", 20, "bold")).grid(row=0, column=0, sticky="w")
dim_entry = tk.Entry(frame, font=("Arial", 20))
dim_entry.grid(row=0, column=1, pady=5)

tk.Button(frame, text="Generar", command=generate_entries, font=("Arial", 20, "bold")).grid(row=0, column=2, padx=10)

# Frame donde se ingresan los valores de la matriz y los vectores
input_frame = tk.Frame(frame)
input_frame.grid(row=1, column=0, columnspan=10, pady=10)

# Botón para realizar el cálculo
tk.Button(frame, text="Calcular", command=calculate, font=("Arial", 20, "bold")).grid(row=2, column=0, columnspan=3, pady=10)

app.mainloop()